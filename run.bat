@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   小红书关键词采集工具 - 一键启动
echo ============================================
echo.

REM 检测 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] 未检测到 Python，正在自动下载安装...
    echo.
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe' -OutFile '%TEMP%\python_install.exe'}"
    echo [*] 正在静默安装 Python，请耐心等待...
    %TEMP%\python_install.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    del %TEMP%\python_install.exe
    REM 刷新环境变量
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python310;%LOCALAPPDATA%\Programs\Python\Python310\Scripts;%PATH%"
    echo [OK] Python 安装完成
    echo.
)

if not exist ".venv" (
    echo [1/3] 首次运行，正在创建虚拟环境...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo [2/3] 正在安装依赖，请耐心等待（约2-3分钟）...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo [3/3] 正在安装浏览器组件...
    playwright install chromium
    echo.
    echo ============================================
    echo   ✅ 环境安装完成！以后双击 run.bat 直接启动
    echo ============================================
    echo.
) else (
    call .venv\Scripts\activate.bat
)

echo 启动采集中，请扫码登录小红书...
echo.
python main.py

pause
