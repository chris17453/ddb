#.PHONY: help clean init bump build upload


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
	@find . -type f -name "*.gz" -exec rm -f {} \;


init:
	@if [[ ! -d 'dist' ]]; then  mkdir dist ; fi
	@if [[ ! -d '.git' ]]; then  git init; fi
	@git config --global user.email $(git_email)
	@git config --global user.name $(git_username)


bump:
	@git add -A 
	@git commit -m 'Bump Version $(shell cat setup.py | grep version | grep -Po "['].*[']" | tr -d "'"))'
	@pipenv run bumpversion patch --allow-dirty
	
	
build: clean init bump
	@python setup.py build_ext --inplace sdist 

upload:
	if [[ ! -z "$pub" ]]; then \
		@twine upload  dist/* ; \
	fi

