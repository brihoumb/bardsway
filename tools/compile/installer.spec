# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
from PyInstaller.utils.hooks import collect_all

path = '.'
installer_datas = [(f'{path}/software_installer/front', 'front'),
                  (f'{path}/software_installer/style', 'style'),
                  (f'{path}/software_installer/script', 'script'),
                  (f'{path}/software_installer/resources', 'resources')]
checksumdir_datas, checksumdir_binaries, checksumdir_hiddenimports = collect_all('checksumdir')

a = Analysis(['__main_installer__.py'],
             pathex=[""],
             binaries=[] + checksumdir_binaries,
             datas=[] + installer_datas + checksumdir_datas,
             hiddenimports=[] + checksumdir_hiddenimports,
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
          [],
          exclude_binaries=True,
          name='installer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          uac_admin=True,
          icon='./logo.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='installer')
