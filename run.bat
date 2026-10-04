@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   小红书关键词采集工具 - 一键启动
echo ============================================
echo.

if not exist ".venv (
    echo [1/3] 首次运行，正在创建虚拟环境...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo [2/3] 正在安装依赖，请耐心等待...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo [3/3] 正在安装浏览器组件...
    playwright install chromium
    echo.
    echo ✅ 环境安装完成！
) else (
    call .venv\Scripts\activate.bat
)

echo.
echo 启动采集中，请扫码登录小红书...
echo.
python main.py

pause
