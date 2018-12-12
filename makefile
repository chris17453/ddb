.PHONY: help clean init bump build upload


dir=$(pwd)
git_username="Charles Watkins"
git_email="charles@titandws.com"
version := $(shell cat setup.py | grep version | grep -Po "['].*[']" | tr -d "'") 

.DEFAULT: help

help:
	@echo "make init   | init git"
	@echo "make clean  | delete pypi packages and cython files"
	@echo "make build  | build bython files and make pypi package"
	@echo "make bump   | bump the package version"
	@echo "make upload | upload to pypi"


clean:
	@rm *.c -f
	@rm *.so -f 
	@if [[ ! -d 'dist' ]]; then  mkdir dist ; fi
	@cd dist
	@rm *.gz -f
	@cd ..


init:
	@if [[ ! -d '.git' ]]; then  git init; fi
	@git config --global user.email $git_email
	@git config --global user.name $git_username


bump:
	@git add -A 
	git commit -m 'Bump Version $(version)'

	@pipenv run bumpversion patch --allow-dirty; EXIT_CODE=$?; echo $EXIT_CODE

	@if [[  $($EXIT_CODE) -ne 0 ]]; then \
		@pipenv install bumpversion --dev ;\
		@touch .bumpversion.cfg ;\
		@echo $'[bumpversion]\n'>.bumpversion.cfg ;\
		@echo $'current_version = $version\n'>.bumpversion.cfg ;\
		@echo $'files = setup.py\n'>.bumpversion.cfg ;\
		@echo $'commit = False\n'>.bumpversion.cfg ;\
		@echo $'tag = False\n'>.bumpversion.cfg ;\
		@git commit -m 'BumpVersion Config - '$version ;\
	fi

build:
	remove-pypi-images
	init-git
	bump-verion
	@python setup.py build_ext --inplace sdist 

upload:
	if [[ ! -z "$pub" ]]; then \
		@twine upload  dist/* ; \
	fi

