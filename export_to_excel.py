# -*- coding: utf-8 -*-
"""
MediaCrawler 小红书数据一键导出 Excel（增强版）
================================================
功能：自动把 data/xhs/jsonl/ 下的爬取结果转换成 Excel，并生成"评论+笔记合并"表
      以及"潜在客户线索"表（识别疑似商家账号 + 求购/合作意向用户）。

Excel 包含 4 张表：
  1. 笔记内容      - 笔记 + 作者信息（含用户ID/主页链接）
  2. 评论明细      - 评论 + 评论者信息（含用户ID/主页链接）
  3. 评论+笔记合并 - 按笔记ID关联
  4. 潜在客户线索  - 面向 B2B 开发：疑似商家/品牌的作者 + 有求购/合作意向的评论用户

用法：
    py export_to_excel.py              # 处理最新一天的数据
    py export_to_excel.py 2026-09-24   # 处理指定日期的数据

生成文件：data/xhs/小红书数据_<日期>.xlsx ，用 Excel 直接打开即可。
"""
import json
import os
import re
import shutil
import sys
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSONL_DIR = os.path.join(BASE_DIR, "data", "xhs", "jsonl")
OUT_DIR = os.path.join(BASE_DIR, "data", "xhs")

DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def read_config_keywords():
    """从 config/base_config.py 读取当前 KEYWORDS，返回关键词列表（兼容中英文逗号）。"""
    cfg_path = os.path.join(BASE_DIR, "config", "base_config.py")
    try:
        with open(cfg_path, "r", encoding="utf-8") as fh:
            text = fh.read()
        m = re.search(r'KEYWORDS\s*=\s*\(\s*(".*?"\s*)+\)', text, re.S)
        if not m:
            return []
        parts = re.findall(r'"([^"]*)"', m.group(0))
        raw = "".join(parts)
        raw = raw.replace("，", ",")
        return [k.strip() for k in raw.split(",") if k.strip()]
    except Exception:
        return []

# ---------- 女包行业客户识别（评分制） ----------
# +50分：明确是卖包的品牌/店铺
HIGH_VALUE_WORDS = [
    "新品", "上新", "品牌", "店铺", "官网", "淘宝", "天猫", "独立站",
    "招商", "包款", "包包系列", "自有品牌", "品牌发布", "collection",
    "shop", "store", "官网", "旗舰店", "微店", "有赞",
]
# +30分：有设计能力/工作室
DESIGN_WORDS = [
    "原创设计", "设计师品牌", "工作室", "designer", "原创包",
    "手作包", "手工包", "独立设计师",
]
# +20分：涉及材料/定制/工厂合作
MATERIAL_WORDS = [
    "材质", "皮料", "皮革", "面料", "定制", "工厂", "代工",
    "OEM", "ODM", "来料", "材料开发", "工厂合作", "货源",
]
# -30分：教程/DIY/穿搭（不是客户）
NEGATIVE_LIGHT = [
    "教程", "DIY", "教学", "怎么", "如何", "穿搭", "搭配", "ootd",
    "改造", "旧衣", "收纳",
]
# -50分：完全无关行业
NEGATIVE_HEAVY = [
    "美妆", "护肤", "口红", "化妆品", "减肥", "健身", "食谱", "饼干",
    "烘焙", "蛋糕", "探店", "美食", "旅游", "酒店", "婚礼", "月子",
    "怀孕", "备孕", "植发", "美甲", "发型", "汽车", "房产",
]

# 只识别作者主动写在公开笔记/评论中的联系方式。
# 不读取、不推断、不尝试破解平台账号绑定的手机号。
PUBLIC_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PUBLIC_WECHAT_RE = re.compile(
    r"(?:微信|wechat|vx|v信|薇信)\s*[:：]?\s*([A-Za-z][-_A-Za-z0-9]{5,19})",
    re.IGNORECASE,
)


def find_dates():
    dates = set()
    if not os.path.isdir(JSONL_DIR):
        return dates
    for f in os.listdir(JSONL_DIR):
        m = DATE_RE.search(f)
        if m:
            dates.add(m.group(1))
    return dates


def read_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def ts2str(ms):
    try:
        d = datetime.fromtimestamp(int(ms) / 1000)
        return d.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(ms)


def split_imgs(image_list):
    if not image_list:
        return 0
    return len([x for x in str(image_list).split(",") if x])


def match_words(text, words):
    if not text:
        return []
    t = str(text)
    return [w for w in words if w in t]


def public_contacts(text):
    """Extract only explicitly published email/WeChat IDs from visible text."""
    if not text:
        return []
    text = str(text)
    contacts = ["邮箱:" + x for x in PUBLIC_EMAIL_RE.findall(text)]
    contacts.extend("微信:" + x for x in PUBLIC_WECHAT_RE.findall(text))
    return sorted(set(contacts))


def style_sheet(ws, headers, widths):
    fill = PatternFill("solid", fgColor="4472C4")
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.freeze_panes = "A2"
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[1].height = 20


def write_sheet(ws, headers, rows):
    ws.append(headers)
    for r in rows:
        ws.append(r)
    return len(rows)


def sync_to_export_folder(out_path):
    """把生成的 Excel 自动同步复制到根目录的 导出结果 文件夹。

    - 保留带日期的原文件名
    - 同时另存一份固定名"小红书数据_最新.xlsx"，方便直接打开最新结果
    """
    export_dir = os.path.join(BASE_DIR, "导出结果")
    os.makedirs(export_dir, exist_ok=True)
    fname = os.path.basename(out_path)
    latest_name = "小红书数据_最新.xlsx"

    copied = []
    for name in (fname, latest_name):
        dest = os.path.join(export_dir, name)
        try:
            shutil.copy2(out_path, dest)
            copied.append(name)
        except OSError as e:
            print("  [警告] 复制到导出结果失败 %s: %s" % (name, e))

    if copied:
        print("已同步到导出结果文件夹：%s" % export_dir)
        print("  文件：%s" % "、".join(copied))


def read_sort_choice():
    """Read 排序选择.txt: 1=likes, 2=collected, 3=comments, 4=newest"""
    p = os.path.join(BASE_DIR, "排序选择.txt")
    if not os.path.exists(p):
        p = os.path.join(BASE_DIR, "sort.txt")
    try:
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("//"):
                    return int(line)
        return 1
    except Exception:
        return 1


SORT_NAMES = {1: "最多点赞", 2: "最多收藏", 3: "最多评论", 4: "最新发布"}
SORT_FIELDS = {1: "liked_count", 2: "collected_count", 3: "comment_count", 4: "time"}


def main():
    dates = find_dates()
    if not dates:
        print("未找到 jsonl 数据文件。请先运行爬虫再执行本脚本。")
        return

    target = sys.argv[1] if len(sys.argv) > 1 else max(dates)
    if target not in dates:
        print("没有 %s 的数据。可用日期: %s" % (target, ", ".join(sorted(dates))))
        return

    contents_path = os.path.join(JSONL_DIR, "search_contents_%s.jsonl" % target)
    comments_path = os.path.join(JSONL_DIR, "search_comments_%s.jsonl" % target)

    if not os.path.exists(contents_path):
        print("缺少文件: %s" % contents_path)
        return
    if not os.path.exists(comments_path):
        print("缺少文件: %s" % comments_path)
        return

    contents = read_jsonl(contents_path)
    comments = read_jsonl(comments_path)

    # ---- 只保留当前配置关键词对应的数据（避免同一天累积的旧词数据混入）----
    config_keywords = read_config_keywords()
    if config_keywords:
        kw_set = set(config_keywords)

        def _kw_match(source_keyword):
            """source_keyword 与当前配置关键词匹配：
            1) 整串（归一化后）命中配置词；2) 拆开后的任一子词命中配置词。"""
            sk = str(source_keyword or "").replace("，", ",").strip()
            if not sk:
                return False
            if sk in kw_set:
                return True
            return any(k in kw_set for k in [x.strip() for x in sk.split(",") if x.strip()])

        before_c = len(contents)
        contents = [n for n in contents if _kw_match(n.get("source_keyword"))]
        kept_ids = {n["note_id"] for n in contents}
        before_m = len(comments)
        comments = [c for c in comments if c.get("note_id") in kept_ids]
        if before_c != len(contents) or before_m != len(comments):
            print("已按当前配置关键词过滤（%s）：笔记 %d -> %d 条，评论 %d -> %d 条"
                  % ("、".join(config_keywords), before_c, len(contents), before_m, len(comments)))
    else:
        print("[提示] 未能读取配置关键词，导出全部数据。")

    if not contents:
        print("[提示] 当前关键词没有匹配到数据，改为导出全部数据。")
        # 重新读全部数据
        contents = read_jsonl(contents_path)
        comments = read_jsonl(comments_path)
        if not contents:
            print("[错误] 没有任何笔记数据，请先运行爬虫采集。")
            return

    # ---- 排序：按 sort.txt 选择 ----
    sort_choice = read_sort_choice()
    sort_field = SORT_FIELDS.get(sort_choice, "liked_count")
    print("排序方式：%s" % SORT_NAMES.get(sort_choice, "最多点赞"))

    def _to_num(v, default=0):
        try:
            return int(str(v).replace(",", "").strip())
        except Exception:
            return default

    if sort_field == "time":
        # 最新：按发布时间降序
        contents.sort(key=lambda n: _to_num(n.get("time")), reverse=True)
    else:
        contents.sort(key=lambda n: _to_num(n.get(sort_field)), reverse=True)
    comments.sort(key=lambda c: _to_num(c.get("create_time")), reverse=True)

    note_index = {n["note_id"]: n for n in contents}
    matched = 0
    for c in comments:
        if c.get("note_id") in note_index:
            matched += 1

    wb = Workbook()

    # ---- Sheet1 笔记内容（含作者用户ID/主页） ----
    ws1 = wb.active
    ws1.title = "笔记内容"
    headers1 = ["笔记ID", "标题", "描述", "作者昵称", "作者用户ID", "作者主页链接",
                "点赞数", "收藏数", "评论数", "分享数", "标签", "笔记链接",
                "来源关键词", "发布时间", "图片数"]
    rows1 = []
    for n in contents:
        rows1.append([
            str(n.get("note_id", "")), n.get("title", ""), n.get("desc", ""),
            n.get("nickname", ""), n.get("user_id", ""), n.get("user_url", ""),
            n.get("liked_count", ""), n.get("collected_count", ""),
            n.get("comment_count", ""), n.get("share_count", ""), n.get("tag_list", ""),
            n.get("note_url", ""), n.get("source_keyword", ""),
            ts2str(n.get("time")), split_imgs(n.get("image_list"))
        ])
    write_sheet(ws1, headers1, rows1)
    style_sheet(ws1, headers1, [20, 30, 50, 14, 18, 40, 10, 10, 10, 10, 20, 50, 25, 16, 8])

    # ---- Sheet2 评论明细（含评论者用户ID/主页） ----
    ws2 = wb.create_sheet("评论明细")
    headers2 = ["评论ID", "笔记ID", "评论内容", "评论者昵称", "评论者用户ID", "评论者主页链接",
                "点赞数", "回复数", "评论时间"]
    rows2 = []
    for c in comments:
        rows2.append([
            str(c.get("comment_id", "")), str(c.get("note_id", "")), c.get("content", ""),
            c.get("nickname", ""), c.get("user_id", ""), c.get("user_url", ""),
            c.get("like_count", ""), c.get("sub_comment_count", ""),
            ts2str(c.get("create_time"))
        ])
    write_sheet(ws2, headers2, rows2)
    style_sheet(ws2, headers2, [20, 20, 60, 14, 18, 40, 10, 10, 16])

    # ---- Sheet3 评论+笔记合并 ----
    ws3 = wb.create_sheet("评论+笔记合并")
    headers3 = ["笔记ID", "笔记标题", "笔记作者", "笔记作者主页", "笔记点赞数", "笔记链接",
                "评论内容", "评论者昵称", "评论者主页", "评论点赞数", "回复数", "评论时间"]
    rows3 = []
    for c in comments:
        n = note_index.get(c.get("note_id"))
        rows3.append([
            str(c.get("note_id", "")),
            n.get("title", "") if n else "",
            n.get("nickname", "") if n else "",
            n.get("user_url", "") if n else "",
            n.get("liked_count", "") if n else "",
            n.get("note_url", "") if n else "",
            c.get("content", ""), c.get("nickname", ""), c.get("user_url", ""),
            c.get("like_count", ""), c.get("sub_comment_count", ""),
            ts2str(c.get("create_time"))
        ])
    write_sheet(ws3, headers3, rows3)
    style_sheet(ws3, headers3, [20, 30, 14, 40, 10, 50, 60, 14, 40, 10, 10, 16])

    # ---- Sheet4 女包行业客户识别（只看笔记作者，评论用户不算客户） ----
    ws4 = wb.create_sheet("女包客户识别")
    headers4 = ["客户评分", "客户等级", "账号昵称", "用户ID", "用户主页链接",
                "符合特征", "扣分特征", "公开联系方式",
                "对应笔记标题", "笔记链接", "笔记点赞数", "来源关键词", "笔记内容摘要"]
    leads = {}  # key=(uid或昵称)

    def score_author(note):
        """Score a note author as potential customer. Returns (score, hits_pos, hits_neg)."""
        text = "%s %s %s %s" % (
            note.get("title", ""), note.get("desc", ""),
            note.get("tag_list", ""), note.get("nickname", "")
        )
        pos = []
        neg = []
        score = 0

        for w in HIGH_VALUE_WORDS:
            if w in text:
                score += 50
                pos.append(w)
        for w in DESIGN_WORDS:
            if w in text:
                score += 30
                pos.append(w)
        for w in MATERIAL_WORDS:
            if w in text:
                score += 20
                pos.append(w)
        for w in NEGATIVE_LIGHT:
            if w in text:
                score -= 30
                neg.append(w)
        for w in NEGATIVE_HEAVY:
            if w in text:
                score -= 50
                neg.append(w)

        return score, pos, neg

    def add_lead(note):
        key = note.get("user_id") or note.get("nickname") or "unknown"
        score, pos, neg = score_author(note)
        text = "%s %s %s" % (note.get("title", ""), note.get("desc", ""), note.get("tag_list", ""))
        contacts = public_contacts(text)

        if key not in leads:
            leads[key] = {
                "nickname": note.get("nickname", ""), "uid": note.get("user_id", ""),
                "url": note.get("user_url", ""),
                "score": score, "pos": set(pos), "neg": set(neg),
                "contacts": set(contacts), "titles": [], "urls": [],
                "liked": note.get("liked_count", ""), "keyword": note.get("source_keyword", ""),
                "summary": text[:200],
            }
        else:
            leads[key]["score"] = max(leads[key]["score"], score)
            leads[key]["pos"].update(pos)
            leads[key]["neg"].update(neg)
            leads[key]["contacts"].update(contacts)
        if note.get("title") and note["title"] not in leads[key]["titles"]:
            leads[key]["titles"].append(note["title"])
        if note.get("note_url") and note["note_url"] not in leads[key]["urls"]:
            leads[key]["urls"].append(note["note_url"])

    # 只从笔记作者中筛选，评论用户不再算客户
    for n in contents:
        add_lead(n)

    # 按评分排序，只保留有意义的（>=0分）
    def grade(score):
        if score >= 80:
            return "A-核心客户"
        elif score >= 40:
            return "B-潜在客户"
        elif score >= 10:
            return "C-观察"
        else:
            return "D-排除"

    rows4 = []
    for key in sorted(leads.keys(), key=lambda k: leads[k]["score"], reverse=True):
        d = leads[key]
        if d["score"] < 0:
            continue
        rows4.append([
            d["score"], grade(d["score"]), d["nickname"], d["uid"], d["url"],
            "、".join(sorted(d["pos"])), "、".join(sorted(d["neg"])),
            "、".join(sorted(d["contacts"])),
            " | ".join(d["titles"][:2]),
            " | ".join(d["urls"][:2]),
            d["liked"], d["keyword"], d["summary"]
        ])
    write_sheet(ws4, headers4, rows4)
    style_sheet(ws4, headers4, [10, 12, 14, 18, 40, 30, 20, 30, 40, 50, 10, 20, 50])

    out_path = os.path.join(OUT_DIR, "小红书数据_%s.xlsx" % target)
    try:
        wb.save(out_path)
    except PermissionError:
        # 原文件可能正被 Excel 打开占用，自动改用带时间戳的文件名
        stamp = datetime.now().strftime("%H%M%S")
        out_path = os.path.join(OUT_DIR, "小红书数据_%s_%s.xlsx" % (target, stamp))
        wb.save(out_path)

    # 自动同步到根目录"导出结果"文件夹
    sync_to_export_folder(out_path)

    a_count = len([r for r in rows4 if r[1].startswith("A")])
    b_count = len([r for r in rows4 if r[1].startswith("B")])
    c_count = len([r for r in rows4 if r[1].startswith("C")])
    print("完成！已生成: %s" % out_path)
    print("  笔记 %d 条 | 评论 %d 条 | 评论匹配到笔记 %d 条（匹配率 %d%%）"
          % (len(contents), len(comments), matched, matched * 100 // max(len(comments), 1)))
    print("  女包客户识别（仅笔记作者）：A类核心客户 %d 个 | B类潜在客户 %d 个 | C类观察 %d 个"
          % (a_count, b_count, c_count))
    print("  重点看A类，直接联系；B类可关注；C类先观察。")


if __name__ == "__main__":
    main()
