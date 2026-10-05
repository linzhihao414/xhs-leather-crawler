@echo off
cd /d "%~dp0"

echo ============================================
echo   XHS Keyword Crawler - One Click Start
echo ============================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.10+ first.
    pause
    exit /b
)

if not exist ".venv" (
    echo [1/3] Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo [2/3] Installing dependencies...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo [3/3] Installing browser...
    playwright install chromium
    echo.
    echo ============================================
    echo   Setup complete! Run again to start crawling.
    echo ============================================
    pause
    exit /b
)

call .venv\Scripts\activate.bat
echo Starting crawler... Please scan QR code to login.
echo.
python main.py
pause