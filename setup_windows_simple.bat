@echo off
echo ==========================================
echo    WordCloud Tool - Windows Setup
echo ==========================================
echo.

echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.7+
    pause
    exit /b 1
)

echo Python OK
echo.

echo Installing pip...
python -m pip install --upgrade pip

echo.
echo Installing requirements...
python -m pip install -r requirements.txt

echo.
echo Installing PyInstaller...
python -m pip install pyinstaller

echo.
echo Building...
python build_windows.py

echo.
echo ==========================================
if exist "dist\wordcloud_tool.exe" (
    echo SUCCESS!
    echo File: dist\wordcloud_tool.exe
) else (
    echo BUILD FAILED!
)
echo ==========================================
pause 