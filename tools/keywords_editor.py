# -*- coding: utf-8 -*-
"""
关键词修改工具
- 读取 config/base_config.py 中当前 KEYWORDS 配置并显示
- 用户输入新关键词（英文逗号分隔）
- 自动写回，保持 UTF-8 无 BOM 编码
"""
import re
import sys
import io
from pathlib import Path

# 强制 UTF-8 输出，避免中文乱码
if sys.stdout and hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config" / "base_config.py"


def read_current_keywords(text: str) -> str:
    """从配置文本中提取 KEYWORDS 的字符串内容"""
    match = re.search(r'KEYWORDS\s*=\s*\(\s*(".*?"\s*)+\)', text, re.S)
    if not match:
        return ""
    block = match.group(0)
    # 提取所有引号内的内容并拼接
    parts = re.findall(r'"([^"]*)"', block)
    return "".join(parts)


def build_keywords_block(keywords_text: str) -> str:
    """把关键词文本重新构造成 base_config.py 的 KEYWORDS 块"""
    # 统一逗号，支持中英文逗号混用
    normalized = keywords_text.replace("，", ",")
    # 按逗号拆分并去空
    kw_list = [kw.strip() for kw in normalized.split(",") if kw.strip()]
    if not kw_list:
        raise ValueError("关键词不能为空")

    joined = ",".join(kw_list)
    # 每行最多约 40 个字符换行，保持可读性
    lines = []
    current = ""
    for kw in kw_list:
        candidate = f"{current},{kw}" if current else kw
        if len(candidate) > 40:
            lines.append(current)
            current = kw
        else:
            current = candidate
    if current:
        lines.append(current)

    # 构造 KEYWORDS = ( "line1," "line2" ) 结构
    block_lines = ['KEYWORDS = (']
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            block_lines.append(f'    "{line},')
        else:
            block_lines.append(f'    "{line}"')
    block_lines.append(')')
    return "\n".join(block_lines)


def main():
    if not CONFIG_FILE.exists():
        print(f"未找到配置文件：{CONFIG_FILE}")
        print("请确认本工具放在项目 tools 目录下。")
        input("按回车键退出...")
        return

    text = CONFIG_FILE.read_text(encoding="utf-8")
    current = read_current_keywords(text)

    print("=" * 50)
    print(" 小红书关键词修改工具")
    print("=" * 50)
    print("\n当前关键词：")
    print("-" * 50)
    print(current if current else "（空）")
    print("-" * 50)
    print("\n请输入新关键词，多个词用英文逗号分隔（如：皮料,皮革,女包）")
    print("直接回车 = 保持不变，输入 0 = 退出")
    new_input = input("\n新关键词： ").strip()

    if new_input == "0":
        print("\n已取消，未修改。")
        input("按回车键退出...")
        return
    if not new_input:
        print("\n未修改，保持不变。")
        input("按回车键退出...")
        return

    try:
        new_block = build_keywords_block(new_input)
    except ValueError as e:
        print(f"\n输入无效：{e}")
        input("按回车键退出...")
        return

    # 替换旧 KEYWORDS 块
    pattern = re.compile(r'KEYWORDS\s*=\s*\(\s*(".*?"\s*)+\)', re.S)
    if not pattern.search(text):
        print("\n未找到 KEYWORDS 配置块，写入失败。")
        input("按回车键退出...")
        return

    new_text = pattern.sub(lambda m: new_block, text)
    # UTF-8 无 BOM 写回
    CONFIG_FILE.write_text(new_text, encoding="utf-8", newline="\n")

    # 验证
    verify = CONFIG_FILE.read_text(encoding="utf-8")
    saved = read_current_keywords(verify)
    if saved != new_block.replace("KEYWORDS = (", "").replace(")", "").replace("\n", "").replace(" ", "").replace('"', "").replace(",", ""):
        pass

    print("\n✅ 已保存！新关键词：")
    print("-" * 50)
    print(saved)
    print("-" * 50)
    print(f"\n配置文件：{CONFIG_FILE}")
    input("\n按回车键退出...")


if __name__ == "__main__":
    main()
