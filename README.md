# 小红书关键词采集工具

基于 [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 定制的小红书笔记采集工具，**改关键词即可采集对应内容**，支持抓取**最新发布 + 最热高赞**笔记，自动导出 Excel。

## 功能特性

- **关键词采集**：修改 `config/base_config.py` 中的 `KEYWORDS` 即可，中英文逗号兼容
- **双排序**：`popularity_descending`（最热高赞）+ `time_descending`（最新发布），按笔记 ID 自动去重合并
- **自动导出 Excel**：笔记按点赞降序、评论按时间降序
- **评论采集**：每篇笔记自动抓取评论
- **多平台**：除小红书外，还支持抖音、快手、B站、微博、知乎、贴吧

## 环境要求

- Python 3.11+
- Windows / macOS / Linux
- Chrome 浏览器

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/linzhihao414/xhs-leather-crawler.git
cd xhs-leather-crawler
```

### 2. 创建虚拟环境并安装依赖

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. 安装 Playwright 浏览器

```bash
playwright install chromium
```

### 4. 修改关键词

编辑 `config/base_config.py`：

```python
# 采集关键词（中英文逗号均可）
KEYWORDS = "皮革,人造革,PU革,皮革面料"

# 每个关键词、每种排序最多采集条数
CRAWLER_MAX_NOTES_COUNT = 300

# 搜索排序：最热=popularity_descending | 最新=time_descending | 综合=general
SEARCH_SORTS = "popularity_descending,time_descending"

# 是否抓评论
ENABLE_GET_COMMENTS = True
```

### 5. 运行采集

```bash
python main.py
```

首次运行会自动弹出浏览器，**用手机小红书 App 扫码登录**即可开始采集。

### 6. 导出 Excel

采集完成后运行：

```bash
python export_to_excel.py
```

导出的 Excel 位于 `data/` 目录下。

## 配置说明

| 配置项 | 说明 | 默认值 |
|---|---|---|
| `KEYWORDS` | 采集关键词，逗号分隔 | `皮革,人造革,PU革,皮革面料` |
| `CRAWLER_MAX_NOTES_COUNT` | 每个关键词每排序最大条数 | `300` |
| `SEARCH_SORTS` | 排序方式，逗号分隔 | `popularity_descending,time_descending` |
| `MAX_CONCURRENCY_NUM` | 并发数（调大易被风控） | `2` |
| `ENABLE_GET_COMMENTS` | 是否采集评论 | `True` |
| `ENABLE_GET_SUB_COMMENTS` | 是否采集子评论 | `False` |

## 导出结果

Excel 包含以下工作表：

| 工作表 | 内容 |
|---|---|
| 笔记内容 | 所有笔记，按点赞数降序 |
| 评论明细 | 每篇笔记的评论，按时间降序 |
| 评论+笔记合并 | 评论和笔记信息合并 |
| 潜在客户线索 | 按作者聚合 |

## 常见问题

**Q：为什么导出结果是旧数据？**
> 导出 Excel 只是把已采集的 jsonl 数据转成表格，需要先运行 `python main.py` 重新采集才会更新数据。

**Q：采集很慢？**
> 每条笔记有防封间隔，属正常现象。词越多、条数越大越慢。

**Q：扫码后登录失败？**
> 重新运行 `python main.py` 再次扫码；若多次失败，检查网络或稍后再试。

## 免责声明

- 本项目仅供学习研究使用，请遵守小红书平台服务条款
- 请合理控制采集频率，勿对平台造成干扰
- 请勿用于任何非法或商业用途
- 基于 [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 开源项目定制，遵循其许可协议
