import os
import sys
import sysconfig

#from distutils.core import setup, Command
from setuptools import setup, find_packages
#from distutils.extension import Extension
from setuptools.extension import Extension
from setuptools.command.build_py import build_py as _build_py



import multiprocessing

EXCLUDE_FILES = [
    'ddb/cli.py'
]

cmdclass = {}

# noinspection PyPep8Naming
class build_py(_build_py):

    def find_package_modules(self, package, package_dir):
        ext_suffix = sysconfig.get_config_var('EXT_SUFFIX')
        modules = super().find_package_modules(package, package_dir)
        filtered_modules = []
        for (pkg, mod, filepath) in modules:
            if os.path.exists(filepath.replace('.py', ext_suffix)):
                continue
            filtered_modules.append((pkg, mod, filepath, ))
        return filtered_modules



if '--build-cython' in sys.argv:
    try:
        from Cython.Build import cythonize
        from Cython.Distutils import build_ext
        from Cython.Build import cythonize
        #from Cython.Distutils.extension import Extension
    except Exception as ex:
        print("Cant build Cython packages. Not installed.")
        exit(1)        
        pass

    # if this is is the system building the package from source, use the py files (or pyx)
    index = sys.argv.index('--build-cython')
    sys.argv.pop(index)  # Removes the '--foo'
    ext = '.py'
    ext2= '.py' # X when needed
    prefix=''
    print("Using Cython")
    USE_CYTHON=True
    
else:
    # if this is a package install, use the c files and build/register modules
    ext = '.c'
    ext2 = '.c'
    prefix=''
    USE_CYTHON=None    
# cython: linetrace=True
# cython: binding=True
# distutils: define_macros=CYTHON_TRACE_NOGIL=1
cmdclass.update({'build_py': build_py})

print("Using extension {0},{1}".format(ext,ext2))

extensions = [
    Extension("ddb.functions.functions",                [prefix+"./ddb/functions/functions" + ext], define_macros=[('CYTHON_TRACE', '1')]),
    Extension("ddb.lexer.language",                     [prefix+"./ddb/lexer/language" + ext], define_macros=[('CYTHON_TRACE', '1')]),
    Extension("ddb.lexer.tokenize",                     [prefix+"./ddb/lexer/tokenize" + ext], define_macros=[('CYTHON_TRACE', '1')]),
    Extension("ddb.lexer.lexer",                        [prefix+"./ddb/lexer/lexer" + ext], define_macros=[('CYTHON_TRACE', '1')]),
    Extension("ddb.meta.meta",                          [prefix+"./ddb/meta/meta" + ext], define_macros=[('CYTHON_TRACE', '1')]),
    Extension("ddb.configuration.column",               [prefix+"./ddb/configuration/column" + ext], define_macros=[('CYTHON_TRACE', '1')]),
    Extension("ddb.configuration.table",                [prefix+"./ddb/configuration/table" + ext], define_macros=[('CYTHON_TRACE', '1')]),
    Extension("ddb.configuration.database",             [prefix+"./ddb/configuration/database" + ext], define_macros=[('CYTHON_TRACE', '1')]),
    Extension("ddb.output.factory",                     [prefix+"./ddb/output/factory" + ext], define_macros=[('CYTHON_TRACE', '1')] ),
    Extension("ddb.output.factory_yaml",                [prefix+"./ddb/output/factory_yaml" + ext], define_macros=[('CYTHON_TRACE', '1')] ),
    Extension("ddb.output.factory_xml",                 [prefix+"./ddb/output/factory_xml" + ext], define_macros=[('CYTHON_TRACE', '1')] ),
    Extension("ddb.output.factory_json",                [prefix+"./ddb/output/factory_json" + ext], define_macros=[('CYTHON_TRACE', '1')] ),
    Extension("ddb.output.factory_term",                [prefix+"./ddb/output/factory_term" + ext], define_macros=[('CYTHON_TRACE', '1')] ),
    Extension("ddb.file_io.locking",                    [prefix+"./ddb/file_io/locking" + ext], define_macros=[('CYTHON_TRACE', '1')] ),
    Extension("ddb.methods.database_show_errors",       [prefix+"./ddb/methods/database_show_errors" + ext], define_macros=[('CYTHON_TRACE', '1')] ),            
    Extension("ddb.methods.database_use",               [prefix+"./ddb/methods/database_use" + ext], define_macros=[('CYTHON_TRACE', '1')] ),    
    Extension("ddb.methods.record_core",                [prefix+"./ddb/methods/record_core" + ext2], define_macros=[('CYTHON_TRACE', '1')] ),   
    Extension("ddb.methods.record_delete",              [prefix+"./ddb/methods/record_delete" + ext], define_macros=[('CYTHON_TRACE', '1')] ),     
    Extension("ddb.methods.record_insert",              [prefix+"./ddb/methods/record_insert" + ext], define_macros=[('CYTHON_TRACE', '1')] ),     
    Extension("ddb.methods.record_select",              [prefix+"./ddb/methods/record_select" + ext], define_macros=[('CYTHON_TRACE', '1')] ),     
    Extension("ddb.methods.record_update",              [prefix+"./ddb/methods/record_update" + ext], define_macros=[('CYTHON_TRACE', '1')] ),     
    Extension("ddb.methods.record_upsert",              [prefix+"./ddb/methods/record_upsert" + ext], define_macros=[('CYTHON_TRACE', '1')] ),     
    Extension("ddb.methods.system_begin",               [prefix+"./ddb/methods/system_begin" + ext], define_macros=[('CYTHON_TRACE', '1')] ),    
    Extension("ddb.methods.system_commit",              [prefix+"./ddb/methods/system_commit" + ext], define_macros=[('CYTHON_TRACE', '1')] ),     
    Extension("ddb.methods.system_rollback",            [prefix+"./ddb/methods/system_rollback" + ext], define_macros=[('CYTHON_TRACE', '1')] ),       
    Extension("ddb.methods.system_set",                 [prefix+"./ddb/methods/system_set" + ext], define_macros=[('CYTHON_TRACE', '1')] ),  
    Extension("ddb.methods.system_show_columns",        [prefix+"./ddb/methods/system_show_columns" + ext], define_macros=[('CYTHON_TRACE', '1')] ),           
    Extension("ddb.methods.system_show_output_modules", [prefix+"./ddb/methods/system_show_output_modules" + ext], define_macros=[('CYTHON_TRACE', '1')] ),                  
    Extension("ddb.methods.system_show_tables",         [prefix+"./ddb/methods/system_show_tables" + ext], define_macros=[('CYTHON_TRACE', '1')] ),          
    Extension("ddb.methods.system_show_variables",      [prefix+"./ddb/methods/system_show_variables" + ext], define_macros=[('CYTHON_TRACE', '1')] ),             
    Extension("ddb.methods.table_create",               [prefix+"./ddb/methods/table_create" + ext], define_macros=[('CYTHON_TRACE', '1')] ),    
    Extension("ddb.methods.table_describe",             [prefix+"./ddb/methods/table_describe" + ext], define_macros=[('CYTHON_TRACE', '1')] ),      
    Extension("ddb.methods.table_drop",                 [prefix+"./ddb/methods/table_drop" + ext], define_macros=[('CYTHON_TRACE', '1')] ),  
    Extension("ddb.methods.table_update",               [prefix+"./ddb/methods/table_update" + ext], define_macros=[('CYTHON_TRACE', '1')] ),    
    Extension("ddb.version",                            [prefix+"./ddb/version" + ext], define_macros=[('CYTHON_TRACE', '1')] ),
    Extension("ddb.engine",                             [prefix+"./ddb/engine" + ext], define_macros=[('CYTHON_TRACE', '1')] ),
    Extension("ddb.interactive",                        [prefix+"./ddb/interactive" + ext], define_macros=[('CYTHON_TRACE', '1')] ),
    Extension("ddb.cli",                                [prefix+"./ddb/cli" + ext], define_macros=[('CYTHON_TRACE', '1')] ),
]



import os
import re
import subprocess


def available_cpu_count():
    """ Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program"""

    # cpuset
    # cpuset may restrict the number of *available* processors
    try:
        m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$',
                      open('/proc/self/status').read())
        if m:
            res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
            if res > 0:
                return res
    except IOError:
        pass

    # Python 2.6+
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    # https://github.com/giampaolo/psutil
    try:
        import psutil
        return psutil.cpu_count()   # psutil.NUM_CPUS on old versions
    except (ImportError, AttributeError):
        pass

    # POSIX
    try:
        res = int(os.sysconf('SC_NPROCESSORS_ONLN'))

        if res > 0:
            return res
    except (AttributeError, ValueError):
        pass

    # Windows
    try:
        res = int(os.environ['NUMBER_OF_PROCESSORS'])

        if res > 0:
            return res
    except (KeyError, ValueError):
        pass

    # jython
    try:
        from java.lang import Runtime
        runtime = Runtime.getRuntime()
        res = runtime.availableProcessors()
        if res > 0:
            return res
    except ImportError:
        pass

    # BSD
    try:
        sysctl = subprocess.Popen(['sysctl', '-n', 'hw.ncpu'],
                                  stdout=subprocess.PIPE)
        scStdout = sysctl.communicate()[0]
        res = int(scStdout)

        if res > 0:
            return res
    except (OSError, ValueError):
        pass

    # Linux
    try:
        res = open('/proc/cpuinfo').read().count('processor\t:')

        if res > 0:
            return res
    except IOError:
        pass

    # Solaris
    try:
        pseudoDevices = os.listdir('/devices/pseudo/')
        res = 0
        for pd in pseudoDevices:
            if re.match(r'^cpuid@[0-9]+$', pd):
                res += 1

        if res > 0:
            return res
    except OSError:
        pass

    # Other UNIXes (heuristic)
    try:
        try:
            dmesg = open('/var/run/dmesg.boot').read()
        except IOError:
            dmesgProcess = subprocess.Popen(['dmesg'], stdout=subprocess.PIPE)
            dmesg = dmesgProcess.communicate()[0]

        res = 0
        while '\ncpu' + str(res) + ':' in dmesg:
            res += 1

        if res > 0:
            return res
    except OSError:
        pass

    raise Exception('Can not determine number of CPUs on this system')

NB_COMPILE_JOBS =  available_cpu_count()



if USE_CYTHON:
    try:
        print("Compiling using {0} cores:".format(NB_COMPILE_JOBS))
        extensions=cythonize(extensions, nthreads=NB_COMPILE_JOBS,compiler_directives={'language_level' : sys.version_info[0]})
        #extensions = cythonize(extensions)
    except BaseException as ex:
        print ("No Cython installed",ex)
        print("Building")
        exit(1)
else:
    print("Not using CYTHON")



    





packages=find_packages(exclude=['examples'])
for package in packages:
    print("Package: {0}".format(package))


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
    author_email='chris17453@gmail.com',
    description='A serviceless sql interface for flat files written in cython',
    ext_modules=extensions,
    cmdclass=cmdclass,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        ddb = ddb.cli:cli_main
        ddb-pipes = ddb.pipes:cli_main
        ddb-server = ddb.server:cli_main
        ddb-service = ddb.service:cli_main
        """
)

