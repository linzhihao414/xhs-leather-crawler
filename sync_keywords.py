"""从 关键词.txt 读取关键词，自动写入 config/base_config.py"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
keywords_file = ROOT / "关键词.txt"
config_file = ROOT / "config" / "base_config.py"

keywords = keywords_file.read_text(encoding="utf-8").strip()
# 去掉多余空行和注释
keywords = re.sub(r'#.*', '', keywords).strip()

config_text = config_file.read_text(encoding="utf-8")

# 替换 KEYWORDS = (...) 块
new_keywords_block = f'KEYWORDS = (\n    "{keywords}",\n)'
config_text = re.sub(
    r'KEYWORDS\s*=\s*\([^)]*\)',
    new_keywords_block,
    config_text,
    count=1,
    flags=re.S
)

config_file.write_text(config_text, encoding="utf-8")
print(f"[OK] Keywords loaded: {keywords}")
