import os
from distutils.core import setup
from distutils.extension import Extension


USE_CYTHON = os.path.exists('ddb/sql_engine.pyx')
# print("USE_CYTHON",USE_CYTHON)


ext = '.pyx' if USE_CYTHON else '.c'
prefix='' if USE_CYTHON else ''

extensions = [
    Extension("ddb.evaluate.match",                [prefix+"./ddb/evaluate/match" + ext]),
    Extension("ddb.functions.functions",           [prefix+"./ddb/functions/functions" + ext]),
    Extension("ddb.lexer.language",                [prefix+"./ddb/lexer/language" + ext]),
    Extension("ddb.lexer.tokenize",                [prefix+"./ddb/lexer/tokenize" + ext]),
    Extension("ddb.lexer.parser",                  [prefix+"./ddb/lexer/parser" + ext],
                                      include_dirs=[prefix+'./ddb/lexer/',
                                                    prefix+'./ddb/structure/'],
              ),
    Extension("ddb.structure.column",              [prefix+"./ddb/structure/column" + ext]),
    Extension("ddb.structure.table",               [prefix+"./ddb/structure/table" + ext]),
    Extension("ddb.structure.database",            [prefix+"./ddb/structure/database" + ext]),
    Extension("ddb.output.factory",                [prefix+"./ddb/output/factory" + ext], ),
    Extension("ddb.output.factory_yaml",           [prefix+"./ddb/output/factory_yaml" + ext], ),
    Extension("ddb.output.factory_xml",            [prefix+"./ddb/output/factory_xml" + ext], ),
    Extension("ddb.output.factory_json",           [prefix+"./ddb/output/factory_json" + ext], ),
    Extension("ddb.version",                       [prefix+"./ddb/version" + ext], ),
    Extension("ddb.engine",                        [prefix+"./ddb/engine" + ext], ),
    Extension("ddb.interactive",                   [prefix+"./ddb/interactive" + ext], ),
#    Extension("ddb.cli", ["./ddb/cli" + ext], ),
]


if USE_CYTHON:
    try:
        from Cython.Build import cythonize
    except BaseException:
        print ("No Cython installed")
        exit(1)

    extensions = cythonize(extensions)
exec(open('ddb/version.pyx').read())
setup(
    name='ddb',
    version=__version__,
    packages=['ddb',
              'ddb.lexer',
              'ddb.evaluate',
              'ddb.structure',
              'ddb.functions',
              'ddb.structure',
              'ddb.output',
              ],
    include_package_data=True,
    url='https://github.com/chris17453/ddb/',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",

    author='Charles Watkins',
    author_email='charles@titandws.com',
    description='A serviceless sql interface for flat files written in python',
    install_requires=['pyyaml','lazyxml', 'flextable'],
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


