import os
from distutils.core import setup
from distutils.extension import Extension
#from setuptools import setup




USE_CYTHON = os.path.exists('ddb//engine/sql_engine.py')
print("USE_CYTHON",USE_CYTHON)


ext = '.py' if USE_CYTHON else '.c'


extensions = [
   Extension("ddb.engine.parser.language",        [ "./ddb/engine/parser/language"+ext ]),
   Extension("ddb.engine.tokenizer.sql_tokenize", [ "./ddb/engine/tokenizer/sql_tokenize"+ext ]) ,
   Extension("ddb.engine.parser.sql_parser",      [ "./ddb/engine/parser/sql_parser"+ext ]),
   Extension("ddb.engine.evaluate.match",         [ "./ddb/engine/evaluate/match"+ext ] ),
   Extension("ddb.engine.structure.column",       [ "./ddb/engine/structure/column"+ext ] ),
   Extension("ddb.engine.structure.table",        [ "./ddb/engine/structure/table"+ext ]),
   Extension("ddb.engine.structure.database",     [ "./ddb/engine/structure/database"+ext ]),
   Extension("ddb.engine.sql_engine",             [ "./ddb/engine/sql_engine"+ext ]),
   Extension("ddb.engine.functions.functions",    [ "./ddb/engine/functions/functions"+ext ]) ,
   Extension("ddb.engine.interactive",            [ "./ddb/engine/interactive"+ext ]),
   Extension("ddb.cli",                           [ "./ddb/cli"+ext ]) ,
]     
  
if USE_CYTHON:
    try:
        from Cython.Build import cythonize
    except:
        print ("Cython not found")
    extensions =  cythonize(extensions)

setup(
    name='ddb',
    version='1.0.125',
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
        """    
    
)



