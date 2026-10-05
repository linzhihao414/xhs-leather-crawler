@echo off
cd /d "%~dp0"
echo ============================================
echo   XHS Keyword Crawler
echo ============================================
echo.
python --version >nul 2>&1
if errorlevel 1 goto NOPYTHON
goto GOTPY
:NOPYTHON
echo [ERROR] Python not found! Install Python 3.10+ first.
echo Download: https://www.python.org/downloads/
pause
exit /b
:GOTPY
if not exist ".venv" goto SETUP
goto RUN
:SETUP
echo Creating venv...
python -m venv .venv
call .venv\Scripts\activate.bat
echo Installing dependencies...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
echo Installing browser...
playwright install chromium
echo.
echo Setup done! Run run.bat again.
pause
exit /b
:RUN
call .venv\Scripts\activate.bat
python sync_keywords.py
echo.
echo Starting crawler... scan QR code.
python main.py
echo.
echo Exporting to Excel...
python export_to_excel.py
echo.
echo Done! Check output folder.
pause