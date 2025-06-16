import PyInstaller.__main__
import os
import platform

print("Starting Windows build process...")

# Check if font file exists
if not os.path.exists('SimHei.ttf'):
    raise FileNotFoundError("Please ensure SimHei.ttf font file is in current directory")

# Check if icon file exists
if not os.path.exists('guardian_final.ico'):
    print("Warning: guardian_final.ico not found, building without icon")

# Windows build parameters
args = [
    'wordcloud_tool.py',  # Main program file
    '--name=wordcloud_tool',  # Generated exe name (use English to avoid encoding issues)
    '--windowed',  # Window mode (no console)
    '--onefile',  # Package to single exe file
    '--add-data=SimHei.ttf;.',  # Add font file (Windows uses semicolon)
    '--clean',  # Clean temporary files
    '--noconfirm',  # No confirmation for overwrite
    '--distpath=dist',  # Output directory
    '--workpath=build',  # Work directory
    # 添加所有必要的隐藏导入
    '--hidden-import=openpyxl',
    '--hidden-import=openpyxl.workbook',
    '--hidden-import=openpyxl.worksheet',
    '--hidden-import=openpyxl.cell',
    '--hidden-import=pandas',
    '--hidden-import=jieba',
    '--hidden-import=wordcloud',
    '--hidden-import=matplotlib',
    '--hidden-import=matplotlib.pyplot',
    '--hidden-import=matplotlib.backends.backend_tkagg',
    '--hidden-import=PIL',
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=tkinter',
    '--hidden-import=tkinter.ttk',
    '--hidden-import=tkinter.filedialog',
    '--hidden-import=tkinter.messagebox',
    # 添加数据收集器选项
    '--collect-data=jieba',
    '--collect-data=wordcloud',
]

# Add icon if available
if os.path.exists('guardian_final.ico'):
    args.append('--icon=guardian_final.ico')

# Add stopwords file if available
if os.path.exists('stopwords.txt'):
    args.append('--add-data=stopwords.txt;.')

print("Build parameters:", args)

# Execute build
try:
    PyInstaller.__main__.run(args)
    print("\n✅ Build completed successfully!")
    print("📁 Executable location: dist/wordcloud_tool.exe")
    print("\nUsage instructions:")
    print("1. Send dist/wordcloud_tool.exe to users")
    print("2. Users can double-click to run, no Python installation needed")
    print("3. First run may be blocked by Windows security, choose 'Run anyway'")
    print("4. Make sure target system has Visual C++ Redistributable installed")
except Exception as e:
    print(f"❌ Build failed: {e}")
    print("Please check if all dependencies are correctly installed") 