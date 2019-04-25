# src builds



## Standalone
- these two single file scripts are generated to give different deployment options

### core
- a computed build 
- just the stuff needed for python integration
- no output formats like bash/term/yaml etc...

### standalone
- a computed build
- all the regular dependencies
- everything in a single file
- includes cli access


## ansible
- the ansible ddb module using core build

## pypi
- ddb for python 2.7 using cython c files

## slack
- slack bot using core build