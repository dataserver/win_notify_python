
# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("src/appicon.png", "./"),
        ("src/appicon.ico", "./"),
        ("src/config.json", "./")
        ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # excludes=["tkinter", "email", "xml", "unittest", "pdb","sqlite3", "idlelib", "pytz", "crypt", "ssl", "zlib"],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='notify-listener',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/appicon.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
