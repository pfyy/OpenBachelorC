# -*- mode: python ; coding: utf-8 -*-


a_main = Analysis(
    ['src\\win_binary\\main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz_main = PYZ(a_main.pure)
exe_main = EXE(
    pyz_main,
    a_main.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

a_setup_pc = Analysis(
    ['src\\launcher\\openbachelorc\\setup_pc.py'],
    pathex=['src\\launcher\\openbachelorc\\'],
    binaries=[],
    datas=[],
    hiddenimports=['pc_const'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz_setup_pc = PYZ(a_setup_pc.pure)
exe_setup_pc = EXE(
    pyz_setup_pc,
    a_setup_pc.scripts,
    [],
    exclude_binaries=True,
    name='setup_pc',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

a_unset_pc = Analysis(
    ['src\\launcher\\openbachelorc\\unset_pc.py'],
    pathex=['src\\launcher\\openbachelorc\\'],
    binaries=[],
    datas=[],
    hiddenimports=['pc_const'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz_unset_pc = PYZ(a_unset_pc.pure)
exe_unset_pc = EXE(
    pyz_unset_pc,
    a_unset_pc.scripts,
    [],
    exclude_binaries=True,
    name='unset_pc',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe_main,
    a_main.binaries,
    a_main.datas,

    exe_setup_pc,
    a_setup_pc.binaries,
    a_setup_pc.datas,

    exe_unset_pc,
    a_unset_pc.binaries,
    a_unset_pc.datas,

    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
