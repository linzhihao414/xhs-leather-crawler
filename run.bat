@echo off
cd /d "%~dp0"
echo ============================================
echo   XHS Keyword Crawler - One Click Start
echo ============================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.10+ first.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b
)

if not exist ".venv" (
    echo [1/3] Creating venv...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create venv
        pause
        exit /b
    )
    call .venv\Scripts\activate.bat
    echo [2/3] Installing dependencies...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if %errorlevel% neq 0 (
        echo [ERROR] pip install failed
        pause
        exit /b
    )
    echo [3/3] Installing browser...
    playwright install chromium
    echo.
    echo Setup complete! Run again to start.
    pause
    exit /b
)

call .venv\Scripts\activate.bat

echo Loading keywords...
python sync_keywords.py
if %errorlevel% neq 0 (
    echo [WARN] sync_keywords failed, continuing...
)
echo.

echo Starting crawler... Please scan QR code.
echo.
python main.py

echo.
echo ============================================
echo   Exporting to Excel...
echo ============================================
python export_to_excel.py

echo.
echo Done! Check "导出结果" folder.
pause