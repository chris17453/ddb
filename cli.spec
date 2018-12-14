# -*- mode: python -*-

block_cipher = None


a = Analysis(['ddb/cli.py'],
             pathex=['ddb'],
             binaries=[('./ddb/engine/tokenizer/sql_tokenize.so', 'engine/tokenizer'), ('./ddb/engine/tokenizer/__init__.py', 'engine/tokenizer'), ('./ddb/engine/evaluate/match.so', 'engine/evaluate'), ('./ddb/engine/evaluate/__init__.py', 'engine/evaluate'), ('./ddb/engine/functions/functions.so', 'engine/functions'), ('./ddb/engine/functions/__init__.py', 'engine/functions'), ('./ddb/engine/sql_engine.so', 'engine'), ('./ddb/engine/__init__.py', 'engine'), ('./ddb/engine/structure/__init__.py', 'engine/structure'), ('./ddb/engine/structure/table.so', 'engine/structure'), ('./ddb/engine/structure/column.so', 'engine/structure'), ('./ddb/engine/structure/database.so', 'engine/structure'), ('./ddb/engine/parser/__init__.py', 'engine/parser'), ('./ddb/engine/parser/sql_parser.so', 'engine/parser'), ('./ddb/engine/parser/language.so', 'engine/parser'), ('./ddb/engine/interactive.so', 'engine')],
             datas=[],
             hiddenimports=['yaml', 'nt', 'os2', 'emx_link', 'ce', 'riscos', 'riscospath', 'riscosenviron', 'msvcrt', 'subprocess', 'org', 'org.python', 'flextable'],
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
