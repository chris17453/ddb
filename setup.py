from distutils.core import setup
from Cython.Build import cythonize
from setuptools import setup
from setuptools.extension import Extension



extensions = [
  Extension(
     "ddb.engine.evaluate.match",
     [
         "./ddb/engine/evaluate/match.pyx"
              ]
     
  )]


setup(
    name='ddb',
    version='1.0.86',
    packages=['ddb',],
    include_package_data=True,
    url='https://github.com/chris17453/ddb/',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    author= 'Charles Watkins',
    author_email= 'charles@titandws.com',
    description= '',
    install_requires=['pyyaml','flextable'
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



