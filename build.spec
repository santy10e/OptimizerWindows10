import os
from pathlib import Path
from PyInstaller.building.build_main import Analysis, EXE
from PyInstaller.building.api import PYZ, COLLECT

base_path = Path(os.getcwd())

a = Analysis(
    ['main.py'],
    pathex=[str(base_path)],
    binaries=[],
    datas=[
        ('icon.ico', '.'),
        ('core', 'core'),
        ('gui', 'gui'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'psutil',
        'winreg',
        'concurrent.futures',
        'queue',
        'webbrowser',
        'threading',
        'subprocess',
        'ctypes',
        'time',
        'os'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OptimizadorWindowsPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # ❗️IMPORTANTE: desactivar UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='OptimizadorWindowsPro'
)
