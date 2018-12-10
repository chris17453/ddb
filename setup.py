import os
from distutils.core import setup
from distutils.extension import Extension

#from setuptools import setup




USE_CYTHON = os.path.exists('ddb/engine/sql_engine.py')
print("USE_CYTHON",USE_CYTHON)


ext = '.pyx' if USE_CYTHON else '.c'



extensions = [
   Extension("ddb.engine.parser.language",        [ "./ddb/engine/parser/language"+ext ]),
   Extension("ddb.engine.tokenizer.sql_tokenize", [ "./ddb/engine/tokenizer/sql_tokenize"+ext ]) ,
   Extension("ddb.engine.evaluate.match",         [ "./ddb/engine/evaluate/match"+ext ] ),
   Extension("ddb.engine.structure.column",       [ "./ddb/engine/structure/column"+ext ] ),
   Extension("ddb.engine.functions.functions",    [ "./ddb/engine/functions/functions"+ext ]) ,
  
   Extension("ddb.engine.parser.sql_parser",      [ "./ddb/engine/parser/sql_parser"+ext ],
    libraries = ['ddb.engine.tokenizer.sql_tokenize',
                'ddb.engine.structure.table',
                'ddb.engine.parser.language'],
   ),
   Extension("ddb.engine.structure.table",        [ "./ddb/engine/structure/table"+ext ],
    libraries = ['ddb.engine.structure.column',],
   ),
   Extension("ddb.engine.structure.database",     [ "./ddb/engine/structure/database"+ext ],
    libraries = ['ddb.engine.structure.table',],
   ),

   Extension("ddb.engine.sql_engine",             [ "./ddb/engine/sql_engine"+ext ],
    libraries = ['ddb.engine.parser.sql_parser',
                 'ddb.engine.structure.table',
                 'ddb.engine.structure.database',
                 'ddb.engine.structure.column',
                 'ddb.engine.evaluate.match',
                 'ddb.engine.functions',]
   ),
   Extension("ddb.engine.interactive",            [ "./ddb/engine/interactive"+ext ],
    libraries = ['ddb.engine.structure.table',
                'ddb.engine.structure.database',
                'ddb.engine.sql_engine',]


   ),
   #Extension("ddb.cli",                           [ "./ddb/cli"+ext ]) ,
]     
  
if USE_CYTHON:
    try:
        from Cython.Build import cythonize
    except:
        print ("Cython not found")
        exit(1)
    
    extensions =  cythonize(extensions)

setup(
    name='ddb',
    version='1.0.144',
    packages=['ddb',],
    include_package_data=True,
    url='https://github.com/chris17453/ddb/',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    author= 'Charles Watkins',
    author_email= 'charles@titandws.com',
    description= '',
    install_requires=['pyyaml','flextable'],
    ext_modules = extensions,
    
    #data_files=[
    #    ('share/icons/hicolor/scalable/apps', ['data/proxx.svg']),
    #    ('share/applications', ['data/proxx.desktop'])
    #],
    entry_points="""
        [console_scripts]
        ddb = ddb.cli:cli_main
        """ ,
       

    
)



#packages = ['cli.ddb',
#   'interactive.engine.ddb',
#   'functions.functions.engine.ddb',
#   'sql_engine.engine.ddb',
#   'database.structure.engine.ddb',
#   'table.structure.engine.ddb',
#   'column.structure.engine.ddb',
#   'match.evaluate.engine.ddb',
#   'sql_parser.parserengine.ddb',
#   'sql_tokenize.tokenizer.engine.ddb',
#   'language.parser.engine.ddb',],
#