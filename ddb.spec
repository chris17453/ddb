# -*- mode: python -*-

block_cipher = None


a = Analysis(['src_build/python/standalone/ddb_standalone.py'],
             pathex=['.'],
             binaries=[ ],
             datas=[],
             hiddenimports=['nt', 'os2', 'ce', 'riscos', 'riscospath', 'riscosenviron', 'msvcrt', 'subprocess',  'flextable'],
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
          name='ddb',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
