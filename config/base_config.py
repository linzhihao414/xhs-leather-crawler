# -*- coding: utf-8 -*-
# Copyright (c) 2025 relakkes@gmail.com
#
# This file is part of MediaCrawler project.
# Repository: https://github.com/NanmiCoder/MediaCrawler/blob/main/config/base_config.py
# GitHub: https://github.com/NanmiCoder
# Licensed under NON-COMMERCIAL LEARNING LICENSE 1.1
#

# 澹版槑锛氭湰浠ｇ爜浠呬緵瀛︿範鍜岀爺绌剁洰鐨勪娇鐢ㄣ€備娇鐢ㄨ€呭簲閬靛畧浠ヤ笅鍘熷垯锛?# 1. 涓嶅緱鐢ㄤ簬浠讳綍鍟嗕笟鐢ㄩ€斻€?# 2. 浣跨敤鏃跺簲閬靛畧鐩爣骞冲彴鐨勪娇鐢ㄦ潯娆惧拰robots.txt瑙勫垯銆?# 3. 涓嶅緱杩涜澶ц妯＄埇鍙栨垨瀵瑰钩鍙伴€犳垚杩愯惀骞叉壈銆?# 4. 搴斿悎鐞嗘帶鍒惰姹傞鐜囷紝閬垮厤缁欑洰鏍囧钩鍙板甫鏉ヤ笉蹇呰鐨勮礋鎷呫€?# 5. 涓嶅緱鐢ㄤ簬浠讳綍闈炴硶鎴栦笉褰撶殑鐢ㄩ€斻€?#
# 璇︾粏璁稿彲鏉℃璇峰弬闃呴」鐩牴鐩綍涓嬬殑LICENSE鏂囦欢銆?# 浣跨敤鏈唬鐮佸嵆琛ㄧず鎮ㄥ悓鎰忛伒瀹堜笂杩板師鍒欏拰LICENSE涓殑鎵€鏈夋潯娆俱€?
# Basic configuration
PLATFORM = "xhs"  # Platform, xhs | dy | ks | bili | wb | tieba | zhihu

# 鏄惁浣跨敤娴峰鐗堝皬绾功 (rednote.com)
# 寮€鍚悗 API 璧?webapi.rednote.com锛宑ookie 鍩熶娇鐢?.rednote.com
XHS_INTERNATIONAL = False

# 小红书搜索关键词，改 keywords.txt 文件即可
KEYWORDS = (
    "皮女包，皮具"
)
LOGIN_TYPE = "qrcode"  # qrcode or phone or cookie
COOKIES = ""
CRAWLER_TYPE = (
    "search"  # Crawling type, search (keyword search) | detail (post details) | creator (creator homepage data)
)
# Whether to enable IP proxy
ENABLE_IP_PROXY = False

# Number of proxy IP pools
IP_PROXY_POOL_COUNT = 2

# Proxy IP provider name
IP_PROXY_PROVIDER_NAME = "kuaidaili"  # kuaidaili | wandouhttp | static

# Static proxy configuration (used when IP_PROXY_PROVIDER_NAME is set to "static")
# Format: "http://your_home_domain:port" or "http://user:password@your_home_domain:port"
STATIC_PROXY_URL = ""

# Setting to True will not open the browser (headless browser)
# Setting False will open a browser
# If Xiaohongshu keeps scanning the code to log in but fails, open the browser and manually pass the sliding verification code.
# If Douyin keeps prompting failure, open the browser and see if mobile phone number verification appears after scanning the QR code to log in. If it does, manually go through it and try again.
HEADLESS = False

# Whether to save login status
SAVE_LOGIN_STATE = True

# ==================== CDP (Chrome DevTools Protocol) 閰嶇疆 ====================
# 鏄惁鍚敤 CDP 妯″紡 - 浣跨敤鐢ㄦ埛鏈湴鐨?Chrome/Edge 娴忚鍣ㄨ繘琛岀埇鍙栵紝鍏锋湁鏇村ソ鐨勫弽妫€娴嬭兘鍔?# 寮€鍚悗锛屼細鑷姩妫€娴嬪苟鍚姩鐢ㄦ埛鐨?Chrome/Edge 娴忚鍣紝閫氳繃 CDP 鍗忚杩涜鎺у埗
# 璇ユ柟寮忎娇鐢ㄧ湡瀹炴祻瑙堝櫒鐜锛屽寘鎷敤鎴风殑鎵╁睍銆丆ookie 鍜岃缃紝澶у箙闄嶄綆琚鎺ф娴嬬殑椋庨櫓
# 銆愭敞鎰忋€戝鏋滄湰鏈?Chrome 鏈紑璋冭瘯绔彛(9222)锛岃淇濇寔 False锛屼娇鐢ㄥ唴缃祻瑙堝櫒锛堟帹鑽愶紝宸茶濂斤級
ENABLE_CDP_MODE = False

# CDP 璋冭瘯绔彛锛岀敤浜庝笌娴忚鍣ㄩ€氫俊
# 濡傛灉绔彛琚崰鐢紝绯荤粺浼氳嚜鍔ㄥ皾璇曚笅涓€涓彲鐢ㄧ鍙?CDP_DEBUG_PORT = 9222

# 鑷畾涔夋祻瑙堝櫒璺緞锛堝彲閫夛級
# 濡傛灉涓虹┖锛岀郴缁熶細鑷姩妫€娴?Chrome/Edge 鐨勫畨瑁呰矾寰?# Windows 绀轰緥: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
# macOS 绀轰緥: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CUSTOM_BROWSER_PATH = ""

# 鏄惁鍦?CDP 妯″紡涓嬪惎鐢ㄦ棤澶存ā寮?# 娉ㄦ剰锛氬嵆浣胯缃负 True锛屾煇浜涘弽妫€娴嬪姛鑳藉湪鏃犲ご妯″紡涓嬪彲鑳芥棤娉曟甯稿伐浣?CDP_HEADLESS = False

# 娴忚鍣ㄥ惎鍔ㄨ秴鏃舵椂闂达紙绉掞級
BROWSER_LAUNCH_TIMEOUT = 60

# 鏄惁杩炴帴鐢ㄦ埛宸叉墦寮€鐨勬祻瑙堝櫒锛岃€屼笉鏄惎鍔ㄦ柊鐨勬祻瑙堝櫒
# 寮€鍚悗锛岀▼搴忎細杩炴帴涓€涓凡缁忓惎鐢ㄤ簡杩滅▼璋冭瘯鐨勬祻瑙堝櫒
# 鐢ㄦ埛闇€瑕佸湪 Chrome 涓紑鍚繙绋嬭皟璇曪細chrome://inspect/#remote-debugging
# 鎴栬€呬娇鐢ㄥ懡浠よ鍙傛暟鍚姩 Chrome锛?-remote-debugging-port=9222
# 杩欑鏂瑰紡鍙嶆娴嬫晥鏋滄渶濂斤紝鍥犱负鐩存帴浣跨敤鐢ㄦ埛鐪熷疄娴忚鍣ㄧ殑鎵€鏈?Cookie銆佹墿灞曞拰娴忚鍘嗗彶
CDP_CONNECT_EXISTING = True

# 绋嬪簭缁撴潫鏃舵槸鍚﹁嚜鍔ㄥ叧闂祻瑙堝櫒
# 璁剧疆涓?False 鍙互淇濇寔娴忚鍣ㄨ繍琛岋紝鏂逛究璋冭瘯
AUTO_CLOSE_BROWSER = True

# Data saving type option configuration, supports: csv, db, json, jsonl, sqlite, excel, postgres. It is best to save to DB, with deduplication function.
SAVE_DATA_OPTION = "jsonl"  # csv or db or json or jsonl or sqlite or excel or postgres

# Data saving path, if not specified by default, it will be saved to the data folder.
SAVE_DATA_PATH = ""

# Browser file configuration cached by the user's browser
USER_DATA_DIR = "%s_user_data_dir"  # %s will be replaced by platform name

# The number of pages to start crawling starts from the first page by default
START_PAGE = 1

# Control the number of crawled videos/posts (per keyword). Default 30 鈫?20/page*1page
# 姣忎釜鍏抽敭璇嶆渶澶氶噰闆嗙殑绗旇鏁帮細30=绾?椤?0鏉★紱100=绾?椤碉紱300=绾?5椤碉紱500=绾?5椤点€傛寜闇€璋冨ぇ銆?CRAWLER_MAX_NOTES_COUNT = 300

# 灏忕孩涔︽悳绱㈡帓搴忥細general=缁煎悎 | popularity_descending=鏈€鐑?鐐硅禐楂樹紭鍏? | time_descending=鏈€鏂?# 瑕?鐐硅禐鏁伴珮鐨勬枃绔?璇蜂繚鎸?popularity_descending
SORT_TYPE = "popularity_descending"

# 鎼滅储鎺掑簭鍒楄〃锛堝彲澶氶€夛紝鐢ㄩ€楀彿鍒嗛殧锛屾寜绗旇ID鑷姩鍘婚噸鍚堝苟锛夛細
#   popularity_descending = 鏈€鐑紙鐐硅禐楂樹紭鍏堬級
#   time_descending       = 鏈€鏂帮紙鍒氬彂甯冪殑浼樺厛锛?#   general               = 缁煎悎
# Search sort: general=comprehensive
SEARCH_SORTS = "general"

# Controlling the number of concurrent crawlers (1=鎱絾绋? 2-3=蹇竴浜?
MAX_CONCURRENCY_NUM = 2

# 鏄惁鍚敤濯掍綋涓嬭浇锛堝皝闈€佽棰戯紝浠ュ強鍥炬枃甯栫殑鍥剧墖锛夛紝榛樿鍏抽棴銆?# 寮€鍚悗濯掍綋鏂囦欢鎸?{SAVE_DATA_PATH 鎴?data}/{platform}/media/{鍐呭ID}/ 鐩綍鑱氬悎瀛樻斁銆?# 鏀寔鐨勫钩鍙帮細xhs / dy / ks / bili / wb锛坱ieba銆亃hihu 鐨勬暟鎹粨鏋勪腑娌℃湁濯掍綋瀛楁锛屼笉鏀寔锛夈€?# 鍛戒护琛屽紑鍏筹細--get_media
ENABLE_GET_MEDIA = False

# Whether to enable comment crawling mode. Comment crawling is enabled by default.
ENABLE_GET_COMMENTS = True

# Control the number of crawled first-level comments (single video/post)
CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 30

# Whether to enable the mode of crawling second-level comments. By default, crawling of second-level comments is not enabled.
# If the old version of the project uses db, you need to refer to schema/tables.sql line 287 to add table fields.
ENABLE_GET_SUB_COMMENTS = False

# word cloud related
# Whether to enable generating comment word clouds
ENABLE_GET_WORDCLOUD = False
# Custom words and their groups
# Add rule: xx:yy where xx is a custom-added phrase, and yy is the group name to which the phrase xx is assigned.
CUSTOM_WORDS = {
    "test": "custom",
}

# Deactivate (disabled) word file path
STOP_WORDS_FILE = "./docs/hit_stopwords.txt"

# Chinese font file path
FONT_PATH = "./docs/STZHONGS.TTF"

# Crawl interval
CRAWLER_MAX_SLEEP_SEC = 2

# 鏄惁绂佺敤 SSL 璇佷功楠岃瘉銆備粎鍦ㄤ娇鐢ㄤ紒涓氫唬鐞嗐€丅urp Suite銆乵itmproxy 绛変細娉ㄥ叆鑷鍚嶈瘉涔︾殑涓棿浜轰唬鐞嗘椂璁句负 True銆?# 璀﹀憡锛氱鐢?SSL 楠岃瘉灏嗕娇鎵€鏈夋祦閲忔毚闇蹭簬涓棿浜烘敾鍑婚闄╋紝璇峰嬁鍦ㄧ敓浜х幆澧冧腑寮€鍚€?DISABLE_SSL_VERIFY = False

from .bilibili_config import *
from .xhs_config import *
from .dy_config import *
from .ks_config import *
from .weibo_config import *
from .tieba_config import *
from .zhihu_config import *



