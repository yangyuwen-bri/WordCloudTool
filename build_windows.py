import PyInstaller.__main__
import os
import platform

print("开始Windows版本打包...")

# 确保字体文件存在
if not os.path.exists('SimHei.ttf'):
    raise FileNotFoundError("请确保 SimHei.ttf 字体文件在当前目录下")

# 确保图标文件存在
if not os.path.exists('guardian_final.ico'):
    print("警告：未找到 guardian_final.ico 文件，将不使用图标")

# Windows打包参数
args = [
    'wordcloud_tool.py',  # 主程序文件
    '--name=词云生成工具',  # 生成的exe名称
    '--windowed',  # 使用窗口模式（不显示控制台）
    '--onefile',  # 打包成单个exe文件
    '--add-data=SimHei.ttf;.',  # 添加字体文件（Windows使用分号）
    '--clean',  # 清理临时文件
    '--noconfirm',  # 不确认覆盖
    '--distpath=dist',  # 指定输出目录
    '--workpath=build',  # 指定工作目录
]

# 如果图标文件存在，添加图标参数
if os.path.exists('guardian_final.ico'):
    args.append('--icon=guardian_final.ico')

# 如果停用词文件存在，添加到数据文件
if os.path.exists('stopwords.txt'):
    args.append('--add-data=stopwords.txt;.')

print("打包参数:", args)

# 执行打包
try:
    PyInstaller.__main__.run(args)
    print("\n✅ 打包完成！")
    print("📁 可执行文件位置: dist/词云生成工具.exe")
    print("\n使用说明:")
    print("1. 将 dist/词云生成工具.exe 文件发送给用户")
    print("2. 用户双击即可运行，无需安装Python环境")
    print("3. 第一次运行可能会被Windows安全软件拦截，选择允许运行即可")
except Exception as e:
    print(f"❌ 打包失败: {e}")
    print("请检查所有依赖是否正确安装") 