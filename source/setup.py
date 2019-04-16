import os
import sys
from distutils.core import setup, Command
from distutils.extension import Extension


if '--use-cython' in sys.argv:
    index = sys.argv.index('--use-cython')
    sys.argv.pop(index)  # Removes the '--foo'
    ext = '.py'
    prefix=''
    print("Using Cython")
    USE_CYTHON=True
    extensions = [
        Extension("ddb.evaluate.match",                     [prefix+"./ddb/evaluate/match" + ext]),
        Extension("ddb.functions.functions",                [prefix+"./ddb/functions/functions" + ext]),
        Extension("ddb.lexer.language",                     [prefix+"./ddb/lexer/language" + ext]),
        Extension("ddb.lexer.tokenize",                     [prefix+"./ddb/lexer/tokenize" + ext]),
        Extension("ddb.lexer.lexer",                        [prefix+"./ddb/lexer/lexer" + ext]),
        Extension("ddb.configuration.column",               [prefix+"./ddb/configuration/column" + ext]),
        Extension("ddb.configuration.table",                [prefix+"./ddb/configuration/table" + ext]),
        Extension("ddb.configuration.database",             [prefix+"./ddb/configuration/database" + ext]),
        Extension("ddb.output.factory",                     [prefix+"./ddb/output/factory" + ext], ),
        Extension("ddb.output.factory_yaml",                [prefix+"./ddb/output/factory_yaml" + ext], ),
        Extension("ddb.output.factory_xml",                 [prefix+"./ddb/output/factory_xml" + ext], ),
        Extension("ddb.output.factory_json",                [prefix+"./ddb/output/factory_json" + ext], ),
        Extension("ddb.output.factory_term",                [prefix+"./ddb/output/factory_term" + ext], ),
        Extension("ddb.file_io.locking",                    [prefix+"./ddb/file_io/locking" + ext], ),
        #Extension("ddb.methods",                            [prefix+"./ddb/methods/" + ext], ),
        #Extension("ddb.methods",                            [prefix+"./ddb/methods/table/core" + ext], ),
        Extension("ddb.version",                            [prefix+"./ddb/version" + ext], ),
        Extension("ddb.engine",                             [prefix+"./ddb/engine" + ext], ),
        Extension("ddb.interactive",                        [prefix+"./ddb/interactive" + ext], ),
    #    Extension("ddb.cli", ["./ddb/cli" + ext], ),
    ]
    try:
        from Cython.Build import cythonize
    except BaseException:
        print ("No Cython installed")
        print("Building")
        exit(1)
    extensions = cythonize(extensions)
    packages=['ddb',
              'ddb.lexer',
              'ddb.evaluate',
              'ddb.file_io',
              'ddb.methods',
              'ddb.methods',
              'ddb.functions',
              'ddb.configuration',
              'ddb.output',
              ]
else:
    ext = '.py'
    prefix='' 
    USE_CYTHON=None
    extensions=None
    packages=['ddb',
              'ddb.lexer',
              'ddb.evaluate',
              'ddb.configuration',
              'ddb.functions',
              'ddb.output',
              'ddb.methods',
              ]




exec(open('ddb/version.py').read())
setup(
    name='ddb',
    version=__version__,
    packages=packages,
    include_package_data=True,
    url='https://github.com/chris17453/ddb/',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Charles Watkins',
    author_email='charles@titandws.com',
    description='A serviceless sql interface for flat files written in python',
    ext_modules=extensions,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        ddb = ddb.cli:cli_main
        """,
    compiler_directives={"language_level": "2"},
    

 
)


