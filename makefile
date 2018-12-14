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
git_email="charles@titandws.com"

.DEFAULT: help

help:
	@echo "make build          | build bython files and make pypi package"
	@echo "make bump           | bump the package version"
	@echo "make clean          | delete pypi packages and cython files"
	@echo "make init           | init git, create base directories"
	@echo "make install        | install the latest ddb from pypi in your user directory"
	@echo "make make-pipfile   | recreate the pipfile"
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
	
	@echo [bumpversion]>.bumpversion.cfg
	@echo current_version = $(shell cat setup.py | grep version | grep -Po "['].*[']" | tr -d "'")>>.bumpversion.cfg
	@echo files = setup.py>S>.bumpversion.cfg
	@echo commit = False>>.bumpversion.cfg
	@echo tag = False>>.bumpversion.cfg

make-pipfile:
	pipenv install bumpversion --dev
	pipenv install twine --dev
	pipenv install ctyhon --dev
	pipenv install flake8 --dev
	pipenv install autopep8 --dev
	pipenv install pyyaml
	pipenv install flextable
	

bump:
	@git add -A 
	@git commit -m 'Bump Version $(shell cat setup.py | grep version | grep -Po "['].*[']" | tr -d "'"))'
	@pipenv run bumpversion patch --allow-dirty

unittest:
	@python ddb/test.py
	
build: bump 
	@find dist -type f -name "*.gz" -exec rm -f {} \;
	@pipenv run python setup.py build_ext 
	@$(MAKE) -f $(THIS_FILE) unittest

pyinstaller:
	@pyinstaller \
				--add-binary "./ddb/engine/tokenizer/sql_tokenize.so:engine/tokenizer" \
				--add-binary "./ddb/engine/tokenizer/__init__.py:engine/tokenizer" \
				--add-binary "./ddb/engine/evaluate/match.so:engine/evaluate" \
				--add-binary "./ddb/engine/evaluate/__init__.py:engine/evaluate" \
				--add-binary "./ddb/engine/functions/functions.so:engine/functions" \
				--add-binary "./ddb/engine/functions/__init__.py:engine/functions" \
				--add-binary "./ddb/engine/sql_engine.so:engine" \
				--add-binary "./ddb/engine/__init__.py:engine" \
				--add-binary "./ddb/engine/structure/__init__.py:engine/structure" \
				--add-binary "./ddb/engine/structure/table.so:engine/structure" \
				--add-binary "./ddb/engine/structure/column.so:engine/structure" \
				--add-binary "./ddb/engine/structure/database.so:engine/structure" \
				--add-binary "./ddb/engine/parser/__init__.py:engine/parser" \
				--add-binary "./ddb/engine/parser/sql_parser.so:engine/parser" \
				--add-binary "./ddb/engine/parser/language.so:engine/parser" \
				--add-binary "./ddb/engine/interactive.so:engine" \
				ddb/cli2.py 


upload:
	@pipenv run twine upload  dist/*

install:
	pip install ddb --user

uninstall:
	pip uninstall ddb

