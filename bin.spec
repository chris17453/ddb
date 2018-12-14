# -*- mode: python -*-

block_cipher = None


a = Analysis(['build/bin'],
             pathex=['/home/nd/repos/chris17453/ddb'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          name='bin',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , resources=['ddb/engine/tokenizer/sql_tokenize.so', 'ddb/engine/evaluate/match.so', 'ddb/engine/functions/functions.so', 'ddb/engine/sql_engine.so', 'ddb/engine/structure/table.so', 'ddb/engine/structure/column.so', 'ddb/engine/structure/database.so', 'ddb/engine/parser/sql_parser.so', 'ddb/engine/parser/language.so', 'ddb/engine/interactive.so', 'ddb/cli.so'])
