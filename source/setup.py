import os
import sys
from distutils.core import setup, Command
from distutils.extension import Extension

ext = '.py'
if '--use-cython' in sys.argv:
    index = sys.argv.index('--use-cython')
    sys.argv.pop(index)  # Removes the '--foo'
    ext = '.c'
    prefix=''
    print("Using Cython")
    USE_CYTHON=True
else:
    prefix=''
    USE_CYTHON=None    

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
    Extension("ddb.methods.database_show_errors",       [prefix+"./ddb/methods/database_show_errors" + ext],),            
    Extension("ddb.methods.database_use",               [prefix+"./ddb/methods/database_use" + ext],),    
    Extension("ddb.methods.record_core",                [prefix+"./ddb/methods/record_core" + ext],),   
    Extension("ddb.methods.record_delete",              [prefix+"./ddb/methods/record_delete" + ext],),     
    Extension("ddb.methods.record_insert",              [prefix+"./ddb/methods/record_insert" + ext],),     
    Extension("ddb.methods.record_select",              [prefix+"./ddb/methods/record_select" + ext],),     
    Extension("ddb.methods.record_update",              [prefix+"./ddb/methods/record_update" + ext],),     
    Extension("ddb.methods.record_upsert",              [prefix+"./ddb/methods/record_upsert" + ext],),     
    Extension("ddb.methods.system_begin",               [prefix+"./ddb/methods/system_begin" + ext],),    
    Extension("ddb.methods.system_commit",              [prefix+"./ddb/methods/system_commit" + ext],),     
    Extension("ddb.methods.system_rollback",            [prefix+"./ddb/methods/system_rollback" + ext],),       
    Extension("ddb.methods.system_set",                 [prefix+"./ddb/methods/system_set" + ext],),  
    Extension("ddb.methods.system_show_columns",        [prefix+"./ddb/methods/system_show_columns" + ext],),           
    Extension("ddb.methods.system_show_output_modules", [prefix+"./ddb/methods/system_show_output_modules" + ext],),                  
    Extension("ddb.methods.system_show_tables",         [prefix+"./ddb/methods/system_show_tables" + ext],),          
    Extension("ddb.methods.system_show_variables",      [prefix+"./ddb/methods/system_show_variables" + ext],),             
    Extension("ddb.methods.table_create",               [prefix+"./ddb/methods/table_create" + ext],),    
    Extension("ddb.methods.table_describe",             [prefix+"./ddb/methods/table_describe" + ext],),      
    Extension("ddb.methods.table_drop",                 [prefix+"./ddb/methods/table_drop" + ext],),  
    Extension("ddb.methods.table_update",               [prefix+"./ddb/methods/table_update" + ext],),    
    Extension("ddb.version",                            [prefix+"./ddb/version" + ext], ),
    Extension("ddb.engine",                             [prefix+"./ddb/engine" + ext], ),
    Extension("ddb.interactive",                        [prefix+"./ddb/interactive" + ext], ),
#    Extension("ddb.cli", ["./ddb/cli" + ext], ),
]
if USE_CYTHON:
    try:
        from Cython.Build import cythonize
    except BaseException:
        print ("No Cython installed")
        print("Building")
        exit(1)
    extensions = cythonize(extensions)
    #packages=['ddb',
    #          'ddb.lexer',
    #          'ddb.evaluate',
    #          'ddb.file_io',
    #          'ddb.methods',
    #          'ddb.functions',
    #          'ddb.configuration',
    #          'ddb.output',
    #          ]
    
packages=['ddb']

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


