# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files=[('resource/sinomine_logo.ico','resource'),
             ('resource/master_splash.png','resource'),
             ('resource','resource'),
             ('widget/*.py','widget'),
             ('util/*.py','util'),
             ('sclScript/*.py','sclScript'),
             ('sclScript/*.tbc','sclScript'),
             ('sclScript/*.tcl','sclScript'),
             ('*.yml','.')]

a = Analysis(['py_platform.py'],
             pathex=['D:\\Workspace\\py_platform_20200409'],
             binaries=[],
             datas=added_files,
             hiddenimports=['win32timezone'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Master',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          icon='resource/sinomine_logo.ico')
