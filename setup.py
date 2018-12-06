from distutils.core import setup
from Cython.Build import cythonize
from setuptools import setup
from setuptools.extension import Extension



extensions = [
  Extension(
     "ddb.engine.evaluate.match",
     [ "./ddb/engine/evaluate/match.pyx" ] ),
    Extension(
     "ddb.engine.structure.column",
     [ "./ddb/engine/structure/column.pyx" ] ),
    Extension(

     "ddb.engine.structure.table",
     [ "./ddb/engine/structure/table.pyx" ]),
    Extension(

     "ddb.engine.structure.database",
     [ "./ddb/engine/structure/database.pyx" ]),
    Extension(
     "ddb.engine.sql_engine",
     [ "./ddb/engine/sql_engine.pyx" ]),
    Extension(
        "ddb.engine.interactive",
         [ "./ddb/engine/interactive.pyx" ]),
    Extension(
        "ddb.engine.parser.language",
         [ "./ddb/engine/parser/language.pyx" ]),
    Extension(
        "ddb.engine.parser.sql_parser",
         [ "./ddb/engine/parser/sql_parser.pyx" ]),
    Extension(
        "ddb.engine.tokenizer.sql_tokenize",
         [ "./ddb/engine/tokenizer/sql_tokenize.pyx" ]) ,
]     
  


setup(
    name='ddb',
    version='1.0.90',
    packages=['ddb',],
    include_package_data=True,
    url='https://github.com/chris17453/ddb/',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    author= 'Charles Watkins',
    author_email= 'charles@titandws.com',
    description= '',
    install_requires=['pyyaml','flextable'
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



