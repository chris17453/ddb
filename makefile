# If the first argument is "run"...
# WIP...
ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif


THIS_FILE := $(lastword $(MAKEFILE_LIST))

git_username="Charles Watkins"
git_email="chris17453@gmail.com"
conf_dir="source/conf"
 
.DEFAULT: help

help:
	@echo "make build          | build bython files and make pypi package(runs unittest and standalone)"
	@echo "make bump           | bump the package version"
	@echo "make clean          | delete pypi packages and cython files"
	@echo "make init           | init git, create base directories"
	@echo "make install        | install the latest ddb from pypi in your user directory"
	@echo "make pipfile        | recreate the pipfile"
	@echo "make standalone     | compile into a linux single file executable"
	@echo "make unittest       | run unittest "
	@echo "make upload         | upload any build packages to pypi"
	@echo "make uninstall      | uninstall ddb from your user directory"
	

clean:
	@find . -type f -name "*.c" -exec rm -f {} \;
	@find . -type f -name "*.so" -exec rm -f {} \;


init:
	@echo dependencies for building...  dnf install python-devel libyaml-devel gcc make
	@if [[ ! -d 'dist' ]]; then  mkdir dist ; fi
	@if [[ ! -d '.git' ]]; then  git init; fi
	@git config --global user.email $(git_email)
	@git config --global user.name $(git_username)
	# bumpversion
	# twine
	# and other deps should be in the pipfile
	@pipenv install 
	
	#echo [bumpversion]>.bumpversion.cfg
	#echo current_version = $(shell cat setup.py | grep version | grep -Po "['].*[']" | tr -d "'")>>.bumpversion.cfg
	##echo files = setup.py>S>.bumpversion.cfg
	##echo commit = False>>.bumpversion.cfg
	#e#cho tag = False>>.bumpversion.cfg

pipfile:
	pipenv install twine --dev
	pipenv install ctyhon --dev
	# for binary executable
	pipenv install pyinstaller --dev
	pipenv install flextable
	
bump:
	@git add -A 
	@git commit -m 'Bump Version $(shell cat source/conf/version)'
	@./$(conf_dir)/bump.sh

unittest:
	@cd source; python -m test.test
	
build: bump 
	@find . -type f -name "*.tar.gz" -exec rm -f {} \;
    # makes ansible single script
	@python $(conf_dir)/build.py
	@cd source; python setup.py build_ext --inplace sdist  --dist-dir ../builds/pypi/ 
  # --use-cython
	#
	# @$(MAKE) -f $(THIS_FILE) standalone
	@$(MAKE) -f $(THIS_FILE) unittest

buildc: clean bump 
	@find . -type f -name "*.tar.gz" -exec rm -f {} \;
    # makes ansible single script
	@python $(conf_dir)/build.py
	@cd source; python setup.py build_ext --inplace sdist  --dist-dir ../builds/pypi/  --use-cython
	#
	# @$(MAKE) -f $(THIS_FILE) standalone
	@$(MAKE) -f $(THIS_FILE) unittest


standalone:
	@pyinstaller ddb.spec

upload:
	@pipenv run twine upload  builds/pypi/*.gz

install:
	pip install ddb --user

uninstall:
	pip uninstall ddb

 