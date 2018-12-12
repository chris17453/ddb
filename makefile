
dir=$(pwd)
git_username="Charles Watkins"
git_email="charles@titandws.com"

.DEFAULT: help

help:
	@echo "make init   | init git, create base directories"
	@echo "make clean  | delete pypi packages and cython files"
	@echo "make build  | build bython files and make pypi package"
	@echo "make bump   | bump the package version"
	@echo "make upload | upload to pypi"


clean:
	@find . -type f -name "*.c" -exec rm -f {} \;
	@find . -type f -name "*.so" -exec rm -f {} \;


init:
	@echo dependencies for building...  dnf install python-devel libyaml-devel gcc make
	@if [[ ! -d 'dist' ]]; then  mkdir dist ; fi
	@if [[ ! -d '.git' ]]; then  git init; fi
	@git config --global user.email $(git_email)
	@git config --global user.name $(git_username)
	pipenv install bumpversion --dev
	pipenv install twine --dev
	pipenv install cython --dev
	
	

	@echo [bumpversion]>.bumpversion.cfg
	@echo current_version = $(shell cat setup.py | grep version | grep -Po "['].*[']" | tr -d "'")>>.bumpversion.cfg
	@echo files = setup.py>>.bumpversion.cfg
	@echo commit = False>>.bumpversion.cfg
	@echo tag = False>>.bumpversion.cfg


bump:
	@git add -A 
	@git commit -m 'Bump Version $(shell cat setup.py | grep version | grep -Po "['].*[']" | tr -d "'"))'
	@pipenv run bumpversion patch --allow-dirty
	
	
build: bump
	@find .dist -type f -name "*.gz" -exec rm -f {} \;
	@python setup.py build_ext --inplace sdist 

upload:
	@twine upload  dist/*

install:
	pip install . --user
	

