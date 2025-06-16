# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['wordcloud_tool.py'],
    pathex=[],
    binaries=[],
    datas=[('SimHei.ttf', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='词云生成工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['guardian_final.ico'],
)
app = BUNDLE(
    exe,
    name='词云生成工具.app',
    icon='guardian_final.ico',
    bundle_identifier=None,
)
