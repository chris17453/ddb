import os
from distutils.core import setup
from distutils.extension import Extension


USE_CYTHON = os.path.exists('ddb/engine/sql_engine.pyx')
# print("USE_CYTHON",USE_CYTHON)


ext = '.pyx' if USE_CYTHON else '.c'
prefix='' if USE_CYTHON else ''

extensions = [
    Extension("ddb.engine.parser.language",
              [prefix+"./ddb/engine/parser/language" + ext]),
    Extension("ddb.engine.tokenizer.sql_tokenize",
              [prefix+"./ddb/engine/tokenizer/sql_tokenize" + ext]),
    Extension("ddb.engine.evaluate.match",
              [prefix+"./ddb/engine/evaluate/match" + ext]),
    Extension("ddb.engine.structure.column",
              [prefix+"./ddb/engine/structure/column" + ext]),
    Extension("ddb.engine.functions.functions",
              [prefix+"./ddb/engine/functions/functions" + ext]),
    Extension("ddb.engine.parser.sql_parser", [prefix+"./ddb/engine/parser/sql_parser" + ext],
              include_dirs=[prefix+'./ddb/engine/tokenizer/',
                            prefix+'./ddb/engine/language/',
                            prefix+'./ddb/engine/structure/'],
              ),
    Extension("ddb.engine.structure.table",
              [prefix+"./ddb/engine/structure/table" + ext]),
    Extension("ddb.engine.structure.database",
              [prefix+"./ddb/engine/structure/database" + ext]),
    Extension("ddb.engine.sql_engine", [prefix+"./ddb/engine/sql_engine" + ext], ),
    Extension("ddb.engine.interactive", [prefix+"./ddb/engine/interactive" + ext], ),
#    Extension("ddb.cli", ["./ddb/cli" + ext], ),
]


if USE_CYTHON:
    try:
        from Cython.Build import cythonize
    except BaseException:
        exit(1)

    extensions = cythonize(extensions)

setup(
    name='ddb',
    version='1.0.479',
    packages=['ddb',
              'ddb.engine.parser',
              'ddb.engine.tokenizer',
              'ddb.engine.evaluate',
              'ddb.engine.structure',
              'ddb.engine.functions',
              'ddb.engine.structure',
              'ddb.engine'
              ],
    include_package_data=True,
    url='https://github.com/chris17453/ddb/',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",

    author='Charles Watkins',
    author_email='charles@titandws.com',
    description='A serviceless sql interface for flat files written in python',
    install_requires=['pyyaml', 'flextable'],
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



)
