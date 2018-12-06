import os
from distutils.core import setup
from distutils.extension import Extension
from pathlib import Path
import shutil

#from setuptools import setup




USE_CYTHON = os.path.exists('ddb/engine/sql_engine.py')
print("USE_CYTHON",USE_CYTHON)


ext = '.py' if USE_CYTHON else '.c'



class MyBuildExt(build_ext):
    def run(self):
        build_ext.run(self)

        build_dir = Path(self.build_lib)
        root_dir = Path(__file__).parent

        target_dir = build_dir if not self.inplace else root_dir


        self.copy_file('ddb/__init__.py',                    root_dir, target_dir)
        self.copy_file('ddb/engine/__init__.py',             root_dir, target_dir)
        self.copy_file('ddb/engine/evaluate/__init__.py',    root_dir, target_dir)
        self.copy_file('ddb/engine/functions/__init__.py',   root_dir, target_dir)
        self.copy_file('ddb/engine/parser/__init__.py',      root_dir, target_dir)
        self.copy_file('ddb/engine/structure/__init__.py',   root_dir, target_dir)
        self.copy_file('ddb/engine/tokenizer/__init__.py',   root_dir, target_dir)

    def copy_file(self, path, source_dir, destination_dir):
        if not (source_dir / path).exists():
            return

        shutil.copyfile(str(source_dir / path), str(destination_dir / path))



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
    version='1.0.128',
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
    cmdclass=dict(
        build_ext=MyBuildExt
    ),        

    
)



