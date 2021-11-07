# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import sys
import platform
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

path = '.'
tf_hidden_imports = collect_submodules('tensorflow')
sklearn_hidden_imports = collect_submodules('sklearn')
spleeter_hidden_imports = collect_submodules('spleeter')
tf_datas = collect_data_files('tensorflow', subdir=None, include_py_files=True)
librosa_datas = [(f'{sys.path[-1]}/librosa/util/example_data', 'librosa/util/example_data')]
software_datas = [(f'{path}/software/front', 'front'),
                  (f'{path}/software/style', 'style'),
                  (f'{path}/software/script', 'script'),
                  (f'{path}/software/resources', 'resources')]


a = Analysis(['__main__.py'],
             pathex=[""],
             binaries=[],
             datas=tf_datas + librosa_datas + software_datas,
             hiddenimports=tf_hidden_imports + sklearn_hidden_imports + spleeter_hidden_imports,
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
          name='bardsway',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          uac_admin=True,
          icon='./logo.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='bardsway')
