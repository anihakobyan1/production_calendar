# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\Hp\\Desktop\\Calendar\\image\\calendar_icon_main.png', 'image'), ('C:\\Users\\Hp\\Desktop\\Calendar\\image\\close_icon.png', 'image'), ('C:\\Users\\Hp\\Desktop\\Calendar\\image\\next_arrow.png', 'image'), ('C:\\Users\\Hp\\Desktop\\Calendar\\image\\open_icon.png', 'image'), ('C:\\Users\\Hp\\Desktop\\Calendar\\image\\prev_arrow.png', 'image')],
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
    name='Календарь',
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
    icon=['C:\\Users\\Hp\\Desktop\\Calendar\\image\\calendar_icon.ico'],
)
