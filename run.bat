@echo off
cd /d "%~dp0"
echo ============================================
echo   XHS Keyword Crawler - One Click Start
echo ============================================
echo.

if not exist ".venv" (
    echo [1/3] Creating venv...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo [2/3] Installing dependencies...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo [3/3] Installing browser...
    playwright install chromium
    echo.
    echo Setup complete! Run again to start.
    pause
    exit /b
)

call .venv\Scripts\activate.bat
echo Starting crawler... Please scan QR code to login.
echo.
python main.py

echo.
echo ============================================
echo   Crawl finished! Exporting to Excel...
echo ============================================
python export_to_excel.py

echo.
echo Done! Check the "导出结果" folder.
pause