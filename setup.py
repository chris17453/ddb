from distutils.core import setup
from Cython.Build import cythonize
#from setuptools import setup
from setuptools.extension import Extension

try:
     from Cython.distutils import build_ext
except ImportError:
     from distutils.command import build_ext




USE_CYTHON = os.path.exists('ddb/sql_engine.py')


ext = '.pyx' if USE_CYTHON else '.c'


extensions = [
  Extension(
     "ddb.engine.evaluate.match",
     [ "./ddb/engine/evaluate/match"+ext ] ),
    Extension(
     "ddb.engine.structure.column",
     [ "./ddb/engine/structure/column"+ext ] ),
    Extension(

     "ddb.engine.structure.table",
     [ "./ddb/engine/structure/table"+ext ]),
    Extension(

     "ddb.engine.structure.database",
     [ "./ddb/engine/structure/database"+ext ]),
    Extension(
     "ddb.engine.sql_engine",
     [ "./ddb/engine/sql_engine"+ext ]),
    Extension(
        "ddb.engine.interactive",
         [ "./ddb/engine/interactive"+ext ]),
    Extension(
        "ddb.engine.parser.language",
         [ "./ddb/engine/parser/language"+ext ]),
    Extension(
        "ddb.engine.parser.sql_parser",
         [ "./ddb/engine/parser/sql_parser"+ext ]),
    Extension(
        "ddb.engine.tokenizer.sql_tokenize",
         [ "./ddb/engine/tokenizer/sql_tokenize"+ext ]) ,
    Extension(
        "ddb.engine.functions.functions",
         [ "./ddb/engine/functions/functions"+ext ]) ,
]     
  


setup(
    name='ddb',
    version='1.0.99',
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



