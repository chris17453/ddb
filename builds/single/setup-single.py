import os
import sys
import re
from pprint import pprint 
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py



ddb_name=None
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

packages=['ddb']
entry_points="""
[console_scripts]
ddb_name = ddb:cli_main
""".replace("ddb_name",ddb_name)

exec(open('ddb/version.py').read())
setup(
    name=ddb_name,
    version=__version__,
    packages=packages,
    #include_package_data=True,
    url='https://github.com/chris17453/ddb/',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Charles Watkins',
    author_email='chris17453@gmail.com',
    description='A serviceless sql interface for flat files written in cython',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
    ],
    entry_points=entry_points
)

