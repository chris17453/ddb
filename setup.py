from distutils.core import setup
from Cython.Build import cythonize
from setuptools import setup
from setuptools.extension import Extension



extensions = [
  Extension(
     "ddb.engine.evaluate.match",
     [ "./ddb/engine/evaluate/match.py" ] ),
    Extension(
     "ddb.engine.structure.column",
     [ "./ddb/engine/structure/column.py" ] ),
    Extension(

     "ddb.engine.structure.table",
     [ "./ddb/engine/structure/table.py" ]),
    Extension(

     "ddb.engine.structure.database",
     [ "./ddb/engine/structure/database.py" ]),
    Extension(
     "ddb.engine.sql_engine",
     [ "./ddb/engine/sql_engine.py" ]),
    Extension(
        "ddb.engine.interactive",
         [ "./ddb/engine/interactive.py" ]),
    Extension(
        "ddb.engine.parser.language",
         [ "./ddb/engine/parser/language.py" ]),
    Extension(
        "ddb.engine.parser.sql_parser",
         [ "./ddb/engine/parser/sql_parser.py" ]),
    Extension(
        "ddb.engine.tokenizer.sql_tokenize",
         [ "./ddb/engine/tokenizer/sql_tokenize.py" ]) ,
    Extension(
        "ddb.engine.functions.functions",
         [ "./ddb/engine/functions/functions.py" ]) ,
]     
  


setup(
    name='ddb',
    version='1.0.98',
    packages=['ddb',],
    include_package_data=True,
    url='https://github.com/chris17453/ddb/',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    author= 'Charles Watkins',
    author_email= 'charles@titandws.com',
    description= '',
    install_requires=['pyyaml','flextable','Cython'
    ],
    ext_modules = cythonize(extensions),
    #data_files=[
    #    ('share/icons/hicolor/scalable/apps', ['data/proxx.svg']),
    #    ('share/applications', ['data/proxx.desktop'])
    #],
    entry_points="""
        [console_scripts]
        ddb = ddb.cli:cli_main
        """    
    
)



