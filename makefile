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

.PHONY: all test clean profile script

help:
	@echo "make build          | build python files and make pypi package(runs unittest and standalone)"
	@echo "make bump           | bump the package version"
	@echo "make clean          | delete pypi packages and cython files"
	@echo "make init           | init git, create base directories"
	@echo "make install        | install the latest ddb from pypi in your user directory"
	@echo "make pipfile        | recreate the pipfile"
	@echo "make standalone     | compile into a linux single file executable"
	@echo "make unittest       | run unittest "
	@echo "make upload         | upload any build packages to pypi"
	@echo "make uninstall      | uninstall ddb from your user directory"
	@echo "make uninstall      | uninstall ddb from your user directory"
	@echo "make svn_start      | start svn docker"
	@echo "make svn_stop       | stop svn docker"
	@echo "make test           | run unit test"
	@echo "make profile        | callgraphs and profilling"
	@echo "make meta           | rebuild the meta classes from the language file"


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
	@./$(conf_dir)/bump.sh
	@git add -A 
	@git commit -m 'Bump Version $(shell cat source/conf/version)'


test:
	@cp test/data//MOCK_DATA_MASTER.csv test/data//MOCK_DATA.csv -f
	@python -m test.test


lock-test:
	@python -m test.test-locking

watch-lock-test:
	@test/watch_locks.sh

profile:
	@python -m test.profile

svn_stop:
	@test/svn_stop.sh

svn_start:
	@test/svn_start.sh

#build: bump svn_start meta
#	@find . -type f -name "*.tar.gz" -exec rm -f {} \;
## makes ansible single script
#	#@python $(conf_dir)/build.py
#	@cd source; python setup.py build_ext --inplace sdist  --dist-dir ../builds/pypi/ 
#	# --use-cython
#	# @$(MAKE) -f $(THIS_FILE) standalone
#	@$(MAKE) -f $(THIS_FILE) test

bytecode:
	@python source/ddb/lexer/reserved_words.py>test/lex_test.py
	@python test/lex_test.py

build: svn_start meta bump
	@find . -type f -name "*.tar.gz" -exec rm -f {} \;
# makes ansible single script

	@python $(conf_dir)/build.py
	@cd source; python setup.py build_ext --inplace sdist  --dist-dir ../builds/pypi/  --build-cython
	
	# @$(MAKE) -f $(THIS_FILE) standalone
	@$(MAKE) -f $(THIS_FILE) test

script:
	@python $(conf_dir)/build.py


standalone:
	@pyinstaller ddb.spec

upload:
	@pipenv run twine upload  builds/pypi/*.gz

install: uninstall
	pip install source/. --user
install-build:
	pip install builds/pypi/ddb*.gz  --user
uninstall:
	pip uninstall ddb -y

meta:
	@cp source/ddb/lexer/language.py tools/language.py
	@python -m tools.generate_meta_class >source/ddb/meta/meta.py
big_data:
	@python  tools/generate_data.py>test/data/MOCK_DATA_LARGE.csv
	

