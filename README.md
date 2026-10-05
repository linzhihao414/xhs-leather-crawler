# 小红书关键词采集工具

基于 [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 定制的小红书笔记采集工具，**改关键词即可采集对应内容**，自动导出 Excel。

## 功能特性

- **改 txt 就行**：编辑 `关键词.txt`，不用改代码
- **自动导出 Excel**：采集完自动生成到"导出结果"文件夹
- **最新排序**：默认只采最新发布的笔记
- **评论采集**：每篇笔记自动抓取评论
- **手动过滑块**：遇到验证码自动暂停，手动过了继续

## 环境要求

- Python 3.10+（[下载 Python](https://www.python.org/downloads/)，安装时勾选 **Add to PATH**）
- Windows 系统
- Chrome 浏览器

## 快速开始（Windows 一键运行）

1. 下载 zip：点页面绿色 **Code** → **Download ZIP**
2. 解压到任意文件夹
3. **双击 `run.bat`**

首次运行会自动：
- 创建虚拟环境
- 安装依赖：`pip install -r requirements.txt`
- 安装浏览器：`playwright install chromium`

装完后再双击一次 `run.bat` 就开始采集。

## 改关键词

打开 `关键词.txt`，改成你要搜的词，逗号分隔，保存：

```
皮革,人造革,PU革,皮革面料
```

然后双击 `run.bat` 就行。

## 看结果

采集完自动导出 Excel，在 **导出结果** 文件夹里：
- `小红书数据_最新.xlsx` — 最新一次采集结果
- 笔记按点赞降序，评论按时间降序

## 手动运行（开发者）

```bash
git clone https://github.com/linzhihao414/xhs-leather-crawler.git
cd xhs-leather-crawler
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
python sync_keywords.py
python main.py
python export_to_excel.py
```

## 常见问题

**Q：双击 run.bat 闪退？**
> 在文件夹地址栏输入 `cmd` 回车，然后输入 `run.bat` 回车，就能看到错误信息。

**Q：提示 No module named xxx？**
> 删掉 `.venv` 文件夹，重新双击 `run.bat` 自动重装。

**Q：遇到滑块验证？**
> 正常现象，在浏览器里手动拖一下滑块，脚本会自动继续。

**Q：采集很慢？**
> 每条笔记有防封间隔，属正常现象。词越多、条数越大越慢。

## 免责声明

- 本项目仅供学习研究使用，请遵守小红书平台服务条款
- 请合理控制采集频率，勿对平台造成干扰
- 请勿用于任何非法或商业用途
- 基于 [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 开源项目定制
