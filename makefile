# If the first argument is "run"...
# WIP...
ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif


THIS_FILE := $(lastword $(MAKEFILE_LIST))

git_username="Charles Watkins" pip install build27
git_email="chris17453@gmail.com"
conf_dir="source/conf"

RELEASE_DIR=pypy
DDB_NAME=ddb
PYTHON=python


.DEFAULT: help


.PHONY: all test clean profile script build 24 26 27 34 36 build24 build26 build27 build34 build36

help:
	@echo "[Maintenence]"
	@echo " make bump                | bump the package version"
	@echo " make clean               | delete pypi packages and cython files"
	@echo " make set_git             | update the git author config"
	@echo " make upload              | upload any build packages to pypi"
	@echo " make init                | init git, create base directories"
	
	@echo "[Install]"
	@echo " make install             | install the latest ddb from pypi in your user directory"
	@echo " make uninstall           | uninstall ddb from your user directory"
	
	@echo "[SVN]"
	@echo " make svn_start           | start svn docker"
	@echo " make svn_stop            | stop svn docker"
	
	@echo "[Build]"
	@echo " make build               | build distribution package"
	@echo " make meta                | rebuild the meta classes from the language file"
	@echo " make script              | make standalone single file"
	@echo " make standalone          | compile into a linux single file executable"
	@echo " make profile             | callgraphs and profilling"

	@echo "[Test]"
	@echo " make test                | run unit test"
	@echo " make lock-test           | locking test"
	@echo " make watch-lock-test     | watch the locking test"


	@echo "[Docker]"
	@echo " make build24               | build python 2.4 (cent5) distribution package"
	@echo " make build26               | build python 2.6 (cent6) distribution package"
	@echo " make build27               | build cython 2.7 (cent7) distribution package"
	@echo " make build34               | build cython 3.4 (cent7) distribution package"
	@echo " make build36               | build cython 3.6 (cent7) distribution package"

	@echo " make dev24                 | run a container with the python 2.4 (cent5) build"
	@echo " make dev26                 | run a container with the python 2.6 (cent6) build"
	@echo " make dev27                 | run a container with the cython 2.7 (cent7) build"
	@echo " make dev34                 | run a container with the cython 3.4 (cent7) build"
	@echo " make dev36                 | run a container with the cython 3.6 (cent7) build"







clean:
	@find . -type f -name "*.c" -exec rm -f {} \;
	@find . -type f -name "*.so" -exec rm -f {} \;

set_git:
	@git config --global user.email $(git_email)
	@git config --global user.name $(git_username)
	@git commit --amend --reset-author


init: set_git
	@echo dependencies for building...  dnf install python-devel libyaml-devel gcc make
	@if [[ ! -d 'dist' ]]; then  mkdir dist ; fi
	@if [[ ! -d '.git' ]]; then  git init; fi
	@git config --global user.email $(git_email)
	@git config --global user.name $(git_username)
	# bumpversion
	# twine
	# and other deps should be in the pipfile
	@pipenv install 
	@ln -s source/ddb/lexer/language.py tools/language.py
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
	
bump:
	@./$(conf_dir)/bump.sh
	@git add -A 
	@git commit -m 'Bump Version $(shell cat source/conf/version)'


test:
	@echo "Resetting Database"
	@cp test/data/MOCK_DATA_MASTER.csv test/data//MOCK_DATA.csv -f
	@echo "Running test with $(DDB_PYTHON)" 
	@$(DDB_PYTHON) -m test.test
	@echo "Test done"


test-single:
	@echo "Resetting Database"
	@cp test/data/MOCK_DATA_MASTER.csv test/data//MOCK_DATA.csv -f
	@echo "Running test"
	@python test/test.py
	@echo "Test done"

lock-test:
	@cd test; python test-locking.py

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
	@python tools/generate_bytecode.py>source/ddb/lexer/bytecode.py

lexer:
	@python tools/generate_bytecode.py>source/ddb/lexer/bytecode.py
	@python source/ddb/lexer/lexer-2.py

# builds the docker iamges
setup-docker:
	docker-compose -f source/docker/docker-compose.yml build

build:
	@$(MAKE) -f $(THIS_FILE) build24
	@$(MAKE) -f $(THIS_FILE) build26
	@$(MAKE) -f $(THIS_FILE) build27
	#@$(MAKE) -f $(THIS_FILE) build34
	@$(MAKE) -f $(THIS_FILE) build36
	#@$(MAKE) -f $(THIS_FILE) pypi

pyc:
	@find . -type f -name "*.pyc" -exec rm -f {} \;

release:  meta script
	@echo "This should be ran inside of a the build containers"
	@echo "USING PYTHON " $(PYTHON)
	@echo "Building $(DDB_NAME)  in  $(RELEASE_DIR)"
	@find . -type f -name "*.tar.gz" -exec rm -f {} \;
	@cd source; $(PYTHON) setup.py build_ext sdist  --dist-dir ../builds/$(RELEASE_DIR)/  --build-python --name=$(DDB_NAME)
	
	# @$(MAKE) -f $(THIS_FILE) standalone
	@$(MAKE) -f $(THIS_FILE) test

cython-release:  meta
	@echo "This should be ran inside of a the build containers"
	@echo "USING PYTHON BINARY: " $(PYTHON)
	@echo "Removing old release packages"
	@find builds/$(RELEASE_DIR) -type f -name "*.tar.gz" -exec rm -f {} \;
	@echo "Building $(DDB_NAME)  in  $(RELEASE_DIR)"
	@$(PYTHON) $(conf_dir)/build.py
	@cd source; $(PYTHON) setup.py build_ext sdist  --dist-dir ../builds/$(RELEASE_DIR)/  --build-cython --name=$(DDB_NAME)
	# @$(MAKE) -f $(THIS_FILE) standalone
	@$(MAKE) -f $(THIS_FILE) test

single: export DDB_RELEASE_DIR=../builds/single
single: script
	@echo "START Single Buid"
	@echo "Making Project Directory"
	@mkdir -p  builds/single/ddb
	@echo "Making Release Directory"
	@mkdir -p  builds/$(RELEASE_DIR)
	@echo "Copying files"
	@cp source/setup-single.py builds/single/ -f
	@cp source/README.md builds/single/ -f
	@cp builds/standalone/ddb.py builds/single/ddb/ -f
	@cp source/ddb/version.py builds/single/ddb/ -f
	@touch builds/single/ddb/__init__.py
	@echo "Removing old release packages"
	@find builds/$(RELEASE_DIR) -type f -name "*.tar.gz" -exec rm -f {} \;
	@echo "Running Setup"
	@cd builds/single; $(PYTHON) setup-single.py build_ext sdist  --dist-dir ../$(RELEASE_DIR)/  --name=$(DDB_NAME)
	@echo "Done Building"
	@$(MAKE) -f $(THIS_FILE) test-single

#build: meta bump cython-release

#internal docker build commands
# build python 2.4 on cent 5
24: RELEASE_DIR = release/2.4
24: DDB_NAME = ddb24python
24: PYTHON = python
24: export DDB_PYTHON=python
24: export DDB_RELEASE=2.4
24: single

# build python 2.6 on cent 6
26: RELEASE_DIR = release/2.6
26: DDB_NAME = ddb26python
26: PYTHON = python
26: export DDB_PYTHON=python
26: export DDB_RELEASE=2.6
26: single

# build python 2.7 on cent 7
27: RELEASE_DIR = release/2.7
27: DDB_NAME = ddb27cython
27: PYTHON = python
27: export DDB_PYTHON=python
27: export DDB_RELEASE=2.7
27: cython-release

# build python 3.4 on cent 7
34: RELEASE_DIR = release/3.4
34: DDB_NAME = ddb34cython
34: PYTHON = python3.4
34: export DDB_PYTHON=python3.4
34: export DDB_RELEASE=3.4
34: cython-release

# build python 3.6 on cent 7
36: RELEASE_DIR = release/3.6
36: DDB_NAME = ddb3cython
36: PYTHON = python3.6
36: export DDB_PYTHON=python3.6
36: export DDB_RELEASE=3.6
36: cython-release


#Individual docker build commands ran from host

build24:
	@docker-compose -f source/docker/docker-compose.yml up ddb24

build26:
	@docker-compose -f source/docker/docker-compose.yml up ddb26

build27:
	@docker-compose -f source/docker/docker-compose.yml up ddb27

build34:
	@docker-compose -f source/docker/docker-compose.yml up ddb34

build36:
	@docker-compose -f source/docker/docker-compose.yml up ddb36


dev24:
	@docker run -v $(shell pwd):/ddb -it  watkinslabs/ddb24  bash

dev26:
	@docker run -v $(shell pwd):/ddb -it  watkinslabs/ddb26  bash

dev27:
	@docker run -v $(shell pwd):/ddb -it  watkinslabs/ddb27  bash

dev34:
	@docker run -v $(shell pwd):/ddb -it  watkinslabs/ddb34  bash

dev36:
	@docker run -v $(shell pwd):/ddb -it  watkinslabs/ddb36  bash




script:
	@python $(conf_dir)/build.py
	@sed -i "s/u'\([^']*\)*'.format(/stringer(u'\1',/g" builds/standalone/ddb.py
	@sed -i 's/u"\([^"]*\)*".format(/stringer(u"\1",/g' builds/standalone/ddb.py	

	@sed -i "s/'\([^']*\)*'.format(/stringer('\1',/g" builds/standalone/ddb.py
	@sed -i 's/"\([^"]*\)*".format(/stringer("\1",/g' builds/standalone/ddb.py	


test-script:
	@python builds/standalone/ddb.py

standalone:
	@pyinstaller ddb.spec

upload:
	#@pipenv run twine upload  builds/pypi/*.gz
	@pipenv run twine upload  builds/release/2.4/*.gz
	@pipenv run twine upload  builds/release/2.6/*.gz
	@pipenv run twine upload  builds/release/2.7/*.gz
	@pipenv run twine upload  builds/release/3.4/*.gz
	@pipenv run twine upload  builds/release/3.6/*.gz

install: uninstall
	pip install source/. --user
install-build:
	pip install builds/pypi/ddb*.gz  --user
uninstall:
	pip uninstall ddb -y

meta:
	@python -m tools.generate_meta_class >source/ddb/meta/meta.py
big_data:
	@python  tools/generate_data.py>test/data/MOCK_DATA_LARGE.csv
	

