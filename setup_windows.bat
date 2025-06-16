@echo off
chcp 65001 >nul
echo ==========================================
echo        WordCloud Tool - Windows Setup
echo ==========================================
echo.

echo Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.7+ and add to PATH
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python environment OK
echo.

echo Installing/upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing project dependencies...
python -m pip install -r requirements.txt

echo.
echo Installing PyInstaller...
python -m pip install pyinstaller

echo.
echo Starting build process...
python build_windows.py

echo.
echo ==========================================
if exist "dist\wordcloud_tool.exe" (
    echo SUCCESS: Build completed!
    echo Executable file: dist\wordcloud_tool.exe
    echo.
    echo You can distribute this exe file to other Windows users
) else (
    echo BUILD FAILED: Please check error messages above
)
echo ==========================================
echo.
pause 