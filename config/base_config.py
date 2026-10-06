# -*- coding: utf-8 -*-
# Basic configuration
PLATFORM = "xhs"

# Search keywords (edit keywords.txt instead)
KEYWORDS = (
    "皮女包，皮具"
)

# Login: qrcode / phone / cookie
LOGIN_TYPE = "qrcode"
COOKIES = ""

# Crawl type: search / detail / creator
CRAWLER_TYPE = (
    "search"
)

# Proxy settings
ENABLE_IP_PROXY = False
IP_PROXY_POOL_COUNT = 2
IP_PROXY_PROVIDER_NAME = "kuaidaili"
STATIC_PROXY_URL = ""

# Browser
HEADLESS = False
SAVE_LOGIN_STATE = True

# CDP mode
ENABLE_CDP_MODE = False
CDP_DEBUG_PORT = 9222
CUSTOM_BROWSER_PATH = ""
BROWSER_LAUNCH_TIMEOUT = 60
CDP_CONNECT_EXISTING = True
AUTO_CLOSE_BROWSER = True

# Data saving
SAVE_DATA_OPTION = "jsonl"
SAVE_DATA_PATH = ""
USER_DATA_DIR = "%s_user_data_dir"
START_PAGE = 1

# Max notes per keyword
CRAWLER_MAX_NOTES_COUNT = 300

# Search sort: general / popularity_descending / time_descending
SORT_TYPE = "popularity_descending"
SEARCH_SORTS = "general"

# Concurrency
MAX_CONCURRENCY_NUM = 2

# Media / comments
ENABLE_GET_MEDIA = False
ENABLE_GET_COMMENTS = True
CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 30
ENABLE_GET_SUB_COMMENTS = False

# Word cloud
ENABLE_GET_WORDCLOUD = False
CUSTOM_WORDS = {
    "test": "custom",
}
STOP_WORDS_FILE = "./docs/hit_stopwords.txt"
FONT_PATH = "./docs/STZHONGS.TTF"

# Timing
CRAWLER_MAX_SLEEP_SEC = 2

# SSL
DISABLE_SSL_VERIFY = False

from .bilibili_config import *
from .xhs_config import *
from .dy_config import *
from .ks_config import *
from .weibo_config import *
from .tieba_config import *
from .zhihu_config import *
