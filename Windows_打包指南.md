# Windows 系统打包指南

## 📋 预检查清单

### ✅ 必需文件检查
- [x] `wordcloud_tool.py` - 主程序文件
- [x] `requirements.txt` - Python依赖列表
- [x] `SimHei.ttf` - 中文字体文件
- [x] `guardian_final.ico` - 守护羊图标文件
- [x] `stopwords.txt` - 停用词文件（可选）
- [x] `build_windows.py` - Windows打包脚本
- [x] `setup_windows.bat` - 一键安装和打包脚本

### ✅ 更新完成的配置
- [x] Windows打包脚本已更新使用 `guardian_final.ico` 图标
- [x] 字体路径处理支持跨平台兼容
- [x] 依赖文件正确添加到打包中

## 🚀 Windows 打包步骤

### 方法一：使用一键脚本（推荐）

**重要：确保在正确的目录中运行！**

#### 选项A：直接双击运行（推荐）
1. 在文件管理器中找到项目文件夹
2. **右键点击 `setup_windows.bat`**
3. 选择 **"以管理员身份运行"**

#### 选项B：命令行运行
```cmd
# 1. 先切换到项目目录
cd /d "C:\你的项目文件夹路径"

# 2. 运行脚本
setup_windows.bat
```

### 方法二：手动执行
```cmd
# 1. 安装依赖
python -m pip install -r requirements.txt
python -m pip install pyinstaller

# 2. 执行打包
python build_windows.py
```

## 📁 文件传输清单

从macOS传输到Windows系统时，确保以下文件存在：

### 核心文件
```
项目根目录/
├── wordcloud_tool.py           # 主程序
├── requirements.txt            # Python依赖
├── SimHei.ttf                 # 中文字体
├── guardian_final.ico         # 守护羊图标
├── stopwords.txt              # 停用词库
├── build_windows.py           # Windows打包脚本
└── setup_windows.bat          # 一键安装脚本
```

### 可选文件
```
├── README.md                  # 说明文档
├── guardian_sheep_icon.svg    # 原始SVG图标
├── guardian_final.png         # PNG版本图标
└── Windows_打包指南.md        # 此指南文件
```

## ⚠️ Windows 特殊注意事项

### 1. 系统要求
- Windows 7/8/10/11 (64位推荐)
- Python 3.7+ (推荐 3.8-3.11)
- 管理员权限（首次安装时）

### 2. 防火墙和安全软件
- 首次运行可能被Windows Defender拦截
- 360、腾讯管家等可能报毒，需要添加信任
- 建议运行时选择"允许"或"添加到白名单"

### 3. 中文路径支持
- 确保Python安装路径不包含中文
- 项目文件夹路径避免使用中文
- 输出文件夹可以是中文

### 4. 字体问题
- 已包含 SimHei.ttf 字体文件
- 如果有字体问题，检查字体文件是否损坏
- Windows系统中文显示应该没有问题

## 🛠️ 故障排除

### 问题1：PyInstaller安装失败
```cmd
# 解决方案：升级pip并重新安装
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools
python -m pip install pyinstaller
```

### 问题2：打包过程中出现模块错误
```cmd
# 解决方案：确保所有依赖都已安装
python -m pip install -r requirements.txt --force-reinstall
```

### 问题3：生成的EXE无法运行
- 检查是否被安全软件拦截
- 尝试以管理员身份运行
- 检查Windows系统缺少的运行库

### 问题4：图标显示异常
- 确保 `guardian_final.ico` 文件存在
- 重新运行打包脚本
- 检查文件是否损坏

## 📊 预期结果

成功打包后，你将得到：

```
dist/
└── 词云生成工具.exe          # 约70-80MB的可执行文件
```

### 功能测试清单
- [x] 双击启动应用
- [x] 界面显示正常（守护羊图标）
- [x] 选择输入文件夹功能
- [x] 选择输出文件夹功能
- [x] 选择停用词文件功能
- [x] 生成词云功能
- [x] 中文字体显示正常
- [x] 进度显示正常

## 🎯 最终检查

### Windows用户体验
1. **首次运行**：可能需要1-2分钟启动（解压临时文件）
2. **后续运行**：启动速度正常
3. **文件大小**：单个EXE约70-80MB
4. **系统兼容**：支持Windows 7及以上版本
5. **无需安装**：用户双击即可运行

### 分发建议
- 将EXE文件压缩后分发
- 提供简单的使用说明
- 告知用户首次运行时的安全软件提示
- 建议用户在桌面创建快捷方式

## 🔧 开发者备注

- Windows版本使用与macOS相同的代码
- 图标已统一为守护工具羊设计
- 所有路径处理都支持跨平台
- 字体文件自动打包，无需用户额外安装 