import PyInstaller.__main__
import os
import platform

# 确保字体文件存在
if not os.path.exists('SimHei.ttf'):
    raise FileNotFoundError("请确保 SimHei.ttf 字体文件在当前目录下")

# 根据操作系统选择路径分隔符
separator = ';' if platform.system() == 'Windows' else ':'

# 打包参数
PyInstaller.__main__.run([
    'wordcloud_tool.py',  # 主程序文件
    '--name=词云生成工具',  # 生成的exe名称
    '--windowed',  # 使用窗口模式（不显示控制台）
    '--onefile',  # 打包成单个exe文件
    '--icon=guardian_final.ico',  # 程序图标
    f'--add-data=SimHei.ttf{separator}.',  # 添加字体文件
    '--clean',  # 清理临时文件
    '--noconfirm',  # 不确认覆盖
]) 