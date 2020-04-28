import os
import sys
#import sysconfig
import re
import subprocess
from pprint import pprint 
from distutils.core import setup, Command
from setuptools import setup, find_packages
#from distutils.extension import Extension
from setuptools.extension import Extension
from setuptools.command.build_py import build_py as _build_py



import multiprocessing

EXCLUDE_FILES = [
    'ddb/cli.py'
]

cmdclass = {}
ddb_name=None
USE_CYTHON=None    
no_extensions=None

# #noinspection PyPep8Naming
#class new_build_py(_build_py):
#
#    def find_package_modules(self, package, package_dir):
#        ext_suffix = sysconfig.get_config_var('EXT_SUFFIX')
#        modules = _build_py.find_package_modules(self,package, package_dir)
#        filtered_modules = []
#        for (pkg, mod, filepath) in modules:
#            file2=filepath.replace(str('.py'), str(ext_suffix))
#            if os.path.exists(file2):
#                continue
#            filtered_modules.append((pkg, mod, filepath, ))
#        return filtered_modules


try:
    for arg in sys.argv:
        tokens=arg.split("=")
        if tokens[0].strip()=="--name":
            ddb_name=tokens[1]
            sys.argv.pop(sys.argv.index(arg))  
            break

except:
    pass
if ddb_name==None:
    ddb_name="ddb"

print ("** BUILDING: "+ddb_name)


if '--build-python' in sys.argv:
    index = sys.argv.index('--build-python')
    sys.argv.pop(index)  # Removes the '--foo'
    no_extensions=True
    ext='.py'
    ext2='.py'
    prefix=ddb_name
elif '--build-cython' in sys.argv:
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
    prefix=ddb_name
    print("Using Cython")
    USE_CYTHON=True
else:
    # this is for pip installs... if its an realy old env use the py files
    if sys.version_info[0]==2 and sys.version_info[1]<7:
        no_extensions=True
    else:
    # if its > =2.7 compile it as an executable lib
        # if this is a package install, use the c files and build/register modules
        ext = '.c'
        ext2 = '.c'
        prefix=ddb_name
# cython: linetrace=True
# cython: binding=True
# distutils: define_macros=CYTHON_TRACE_NOGIL=1

#cmdclass.update({'build_py': new_build_py})

print("Using extension {0},{1}".format(ext,ext2))
lang_level=sys.version_info[0]
macro=[('CYTHON_TRACE','1')]
comp_directive={
    'embedsignature':True,
    'language_level':lang_level
}
extensions = [
    Extension(ddb_name+".functions.functions",                [prefix+"/functions/functions" + ext],                 define_macros=macro),
    Extension(ddb_name+".lexer.language",                     [prefix+"/lexer/language" + ext],                      define_macros=macro),
    Extension(ddb_name+".lexer.tokenize",                     [prefix+"/lexer/tokenize" + ext],                      define_macros=macro),
    Extension(ddb_name+".lexer.lexer",                        [prefix+"/lexer/lexer" + ext],                         define_macros=macro),
    Extension(ddb_name+".meta.meta",                          [prefix+"/meta/meta" + ext],                           define_macros=macro),
    Extension(ddb_name+".configuration.column",               [prefix+"/configuration/column" + ext],                define_macros=macro),
    Extension(ddb_name+".configuration.table",                [prefix+"/configuration/table" + ext],                 define_macros=macro),
    Extension(ddb_name+".configuration.database",             [prefix+"/configuration/database" + ext],              define_macros=macro),
    Extension(ddb_name+".output.factory",                     [prefix+"/output/factory" + ext],                      define_macros=macro),
    Extension(ddb_name+".output.factory_yaml",                [prefix+"/output/factory_yaml" + ext],                 define_macros=macro),
    Extension(ddb_name+".output.factory_xml",                 [prefix+"/output/factory_xml" + ext],                  define_macros=macro),
    Extension(ddb_name+".output.factory_json",                [prefix+"/output/factory_json" + ext],                 define_macros=macro),
    Extension(ddb_name+".output.factory_term",                [prefix+"/output/factory_term" + ext],                 define_macros=macro),
    Extension(ddb_name+".file_io.locking",                    [prefix+"/file_io/locking" + ext],                     define_macros=macro),
    Extension(ddb_name+".methods.database_show_errors",       [prefix+"/methods/database_show_errors" + ext],        define_macros=macro),
    Extension(ddb_name+".methods.database_use",               [prefix+"/methods/database_use" + ext],                define_macros=macro),
    Extension(ddb_name+".methods.record",                     [prefix+"/methods/record" + ext2],                     define_macros=macro),
    Extension(ddb_name+".methods.record_core",                [prefix+"/methods/record_core" + ext2],                define_macros=macro),
    Extension(ddb_name+".methods.record_delete",              [prefix+"/methods/record_delete" + ext],               define_macros=macro),
    Extension(ddb_name+".methods.record_insert",              [prefix+"/methods/record_insert" + ext],               define_macros=macro),
    Extension(ddb_name+".methods.record_select",              [prefix+"/methods/record_select" + ext],               define_macros=macro),
    Extension(ddb_name+".methods.record_update",              [prefix+"/methods/record_update" + ext],               define_macros=macro),
    Extension(ddb_name+".methods.record_upsert",              [prefix+"/methods/record_upsert" + ext],               define_macros=macro),
    Extension(ddb_name+".methods.system_begin",               [prefix+"/methods/system_begin" + ext],                define_macros=macro),
    Extension(ddb_name+".methods.system_commit",              [prefix+"/methods/system_commit" + ext],               define_macros=macro),
    Extension(ddb_name+".methods.system_rollback",            [prefix+"/methods/system_rollback" + ext],             define_macros=macro),
    Extension(ddb_name+".methods.system_set",                 [prefix+"/methods/system_set" + ext],                  define_macros=macro),
    Extension(ddb_name+".methods.system_show_columns",        [prefix+"/methods/system_show_columns" + ext],         define_macros=macro),
    Extension(ddb_name+".methods.system_show_output_modules", [prefix+"/methods/system_show_output_modules" + ext],  define_macros=macro),
    Extension(ddb_name+".methods.system_show_tables",         [prefix+"/methods/system_show_tables" + ext],          define_macros=macro),
    Extension(ddb_name+".methods.system_show_variables",      [prefix+"/methods/system_show_variables" + ext],       define_macros=macro),
    Extension(ddb_name+".methods.table_create",               [prefix+"/methods/table_create" + ext],                define_macros=macro),
    Extension(ddb_name+".methods.table_describe",             [prefix+"/methods/table_describe" + ext],              define_macros=macro),      
    Extension(ddb_name+".methods.table_drop",                 [prefix+"/methods/table_drop" + ext],                  define_macros=macro),  
    Extension(ddb_name+".methods.table_update",               [prefix+"/methods/table_update" + ext],                define_macros=macro),    
    Extension(ddb_name+".version",                            [prefix+"/version" + ext],                             define_macros=macro),
    Extension(ddb_name+".engine",                             [prefix+"/engine" + ext],                              define_macros=macro),
    Extension(ddb_name+".interactive",                        [prefix+"/interactive" + ext],                         define_macros=macro),
    Extension(ddb_name+".cli",                                [prefix+"/cli" + ext],                                 define_macros=macro),
]


if no_extensions==True:
    print("No extensions")
    extensions=[]

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
        extensions=cythonize(extensions, nthreads=NB_COMPILE_JOBS,compiler_directives=comp_directive)
    except BaseException as ex:
        print ("No Cython installed {0}".format(ex))
        print("Building")
        exit(1)
else:
    print("Not using CYTHON")


# manually updated
packages=   [ddb_name,
            ddb_name+'.configuration',
            ddb_name+'.output',
            ddb_name+'.functions',
            ddb_name+'.methods',
            ddb_name+'.meta',
            ddb_name+'.lexer',
            ddb_name+'.file_io']

#packages=find_packages(exclude=['examples'])
#for package in packages:
#    print("Package: {0}".format(package))

#install_requires=[],

exec(open(prefix+'/version.py').read())

entry_points="""
        [console_scripts]
        ddb_name = ddb_name.cli:cli_main
        ddb_name-pipes = ddb_name.pipes:cli_main
        ddb_name-server = ddb_name.server:cli_main
        ddb_name-service = ddb_name.service:cli_main
        """.replace("ddb_name",ddb_name)

classifiers=[
    'Programming Language :: Python :: 2.7',
    "Development Status :: 3 - Alpha",
]

readme=open('README.md').read()

setup(
    name                            = ddb_name,
    packages                        = packages,
    version                         = __version__,
    include_package_data            = True,
    url                             = 'https://github.com/chris17453/ddb/',
    license                         = 'Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description                = readme,
    long_description_content_type   = "text/markdown",
    author                          = 'Charles Watkins',
    author_email                    = 'chris17453@gmail.com',
    description                     = 'A serviceless sql interface for flat files written in cython',
    ext_modules                     = extensions,
    cmdclass                        = cmdclass,
    classifiers                     = classifiers,
    entry_points                    = entry_points
)

