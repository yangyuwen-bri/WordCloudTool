@echo off
cd /d "%~dp0"
echo ==========================================
echo    WordCloud Tool - Windows Setup
echo ==========================================
echo Current directory: %CD%
echo.

echo Checking required files...
if not exist "wordcloud_tool.py" (
    echo ERROR: wordcloud_tool.py not found!
    echo Please run this script in the project directory
    echo Make sure all project files are in the same folder
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found!
    echo Please run this script in the project directory
    pause
    exit /b 1
)

if not exist "build_windows.py" (
    echo ERROR: build_windows.py not found!
    echo Please run this script in the project directory
    pause
    exit /b 1
)

echo All required files found!
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
if errorlevel 1 (
    echo WARNING: Some packages may have failed to install.
    echo Attempting to install critical packages individually...
    echo.
)

echo Ensuring openpyxl is installed correctly...
python -m pip install openpyxl==3.1.5 --force-reinstall
if errorlevel 1 (
    echo ERROR: Failed to install openpyxl!
    echo This package is required for Excel file processing.
    pause
    exit /b 1
)

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
    echo File: %CD%\dist\wordcloud_tool.exe
    echo.
    echo You can now distribute this exe file!
) else (
    echo BUILD FAILED!
    echo Please check the error messages above
)
echo ==========================================
pause 