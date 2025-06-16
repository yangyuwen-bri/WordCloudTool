@echo off
chcp 65001 >nul
echo ==========================================
echo        词云生成工具 - Windows打包助手
echo ==========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python环境！
    echo 请先安装Python 3.7以上版本，并确保已添加到系统PATH
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python环境检查通过
echo.

echo 正在安装/升级pip...
python -m pip install --upgrade pip

echo.
echo 正在安装项目依赖...
python -m pip install -r requirements.txt

echo.
echo 正在安装PyInstaller...
python -m pip install pyinstaller

echo.
echo 开始执行打包...
python build_windows.py

echo.
echo ==========================================
if exist "dist\词云生成工具.exe" (
    echo ✅ 打包成功完成！
    echo 📁 可执行文件已生成：dist\词云生成工具.exe
    echo.
    echo 你可以将此exe文件发送给其他Windows用户使用
) else (
    echo ❌ 打包可能失败，请检查上方错误信息
)
echo ==========================================
echo.
pause 