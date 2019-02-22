import os
import sys
from distutils.core import setup, Command
from distutils.extension import Extension


if '--use-cython' in sys.argv:
    index = sys.argv.index('--use-cython')
    sys.argv.pop(index)  # Removes the '--foo'
    ext = '.c'
    prefix=''
    print("Using Cython")
    USE_CYTHON=True
    extensions = [
        Extension("ddb.evaluate.match",                     [prefix+"./ddb/evaluate/match" + ext]),
        Extension("ddb.functions.functions",                [prefix+"./ddb/functions/functions" + ext]),
        Extension("ddb.lexer.language",                     [prefix+"./ddb/lexer/language" + ext]),
        Extension("ddb.lexer.tokenize",                     [prefix+"./ddb/lexer/tokenize" + ext]),
        Extension("ddb.lexer.lexer",                        [prefix+"./ddb/lexer/lexer" + ext], include_dirs=[prefix+'./ddb/structure/'],),
        Extension("ddb.structure.column",                   [prefix+"./ddb/structure/column" + ext]),
        Extension("ddb.structure.table",                    [prefix+"./ddb/structure/table" + ext]),
        Extension("ddb.structure.database",                 [prefix+"./ddb/structure/database" + ext]),
        Extension("ddb.output.factory",                     [prefix+"./ddb/output/factory" + ext], ),
        Extension("ddb.output.factory_yaml",                [prefix+"./ddb/output/factory_yaml" + ext], ),
        Extension("ddb.output.factory_xml",                 [prefix+"./ddb/output/factory_xml" + ext], ),
        Extension("ddb.output.factory_json",                [prefix+"./ddb/output/factory_json" + ext], ),
        Extension("ddb.methods.database.set",               [prefix+"./ddb/methods/database/set" + ext], ),
        Extension("ddb.methods.database.use",               [prefix+"./ddb/methods/database/use" + ext], ),
        Extension("ddb.methods.table.data.delete",          [prefix+"./ddb/methods/table/data/delete" + ext], ),
        Extension("ddb.methods.table.data.insert",          [prefix+"./ddb/methods/table/data/insert" + ext], ),
        Extension("ddb.methods.table.data.select",          [prefix+"./ddb/methods/table/data/select" + ext], ),
        Extension("ddb.methods.table.data.update",          [prefix+"./ddb/methods/table/data/update" + ext], ),
        Extension("ddb.methods.table.structure.create",     [prefix+"./ddb/methods/table/structure/create" + ext], ),
        Extension("ddb.methods.table.structure.drop",       [prefix+"./ddb/methods/table/structure/drop" + ext], ),
        Extension("ddb.methods.table.structure.describe",   [prefix+"./ddb/methods/table/structure/describe" + ext], ),
        Extension("ddb.methods.table.structure.update",     [prefix+"./ddb/methods/table/structure/update" + ext], ),
        Extension("ddb.version",                            [prefix+"./ddb/version" + ext], ),
        Extension("ddb.engine",                             [prefix+"./ddb/engine" + ext], ),
        Extension("ddb.interactive",                        [prefix+"./ddb/interactive" + ext], ),
    #    Extension("ddb.cli", ["./ddb/cli" + ext], ),
    ]
    try:
        from Cython.Build import cythonize
    except BaseException:
        print ("No Cython installed")
        exit(1)
    extensions = cythonize(extensions)
    packages=['ddb',
              'ddb.lexer',
              'ddb.evaluate',
              'ddb.structure',
              'ddb.functions',
              'ddb.structure',
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
              'ddb.structure',
              'ddb.functions',
              'ddb.structure',
              'ddb.output',
              'ddb.methods',
              'ddb.methods.database',
              'ddb.methods.table.data',
              'ddb.methods.table.structure',
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


