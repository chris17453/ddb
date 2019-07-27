# ddb (delimited database)

 A serviceless sql interface for flat files written in python


## What does it do?

- ddb sits on top of text files, giving them a database access layer
- you can read, write, update csv's or any type of delimited text file via sql


## What are the human benifits to using ddb?

- a common interface for all of your flat files
- change control
- access and modification logging
- multiple points of integration (python, shell, slack, ansible)
- sql is easy to work with, no coding required
- the text file stays the same
- wont break or affect anything that might use the file


## What are the technical benifits to using ddb?

- it does not run as a service, nothing to maintain
- it can run on any server with python 2.7>
- low memory foot print. it reads data 1 line at a time
- eases the effort of data migration using sql
- the text file does not change
- accessibility of the text file doesnt change
- ease of automation
- error handeling for bad data
- event logging
- no caching at all, all access is live
- optimized for speed using cython


## How do I use it?
- with python [python integration](docs/python-integration.md)
- from bash [cli](docs/cli.md)


## Where do I get it?
- the code -> [github](https://github.com/chris17453/ddb)
- the offical package -> [Pypi](https://pypi.org/project/ddb/)


## How do I install it?
The github repo is where I work. Stable releases should be downloaded from pypi.
```bash
pip install ddb --user

```
## If you dont want to quote everything in shell
- disable globing for ddb


### BASH
```bash
   echo "alias ddb='set -f;ddb';ddb(){ command ddb "$@";set +f;}" >~/.bashrc
```


## Getting started
- [cli](docs/cli.md)
- [bash examples](docs/examples.md)
- [code example](/source/examples/example.py)
- [unittest example](/source/test/test.py)
- [walkthrough](docs/walkthrough.md)


## dev stuff
- [query support](docs/query-support.md)
- [data output](docs/output.md)
- [python integration](docs/python-integration.md)
- [build](docs/build.md)
- [notes](docs/notes.md)
- [changelog](docs/changelog.md)

# ddb WorkFlow
![Workflow](https://raw.githubusercontent.com/chris17453/ddb/master/source/resources/ddb-internal-flow-diagram.png)

### BASH Demo
![Demo](https://raw.githubusercontent.com/chris17453/ddb/master/docs/ddb-bash-demo.gif)

### DDB Icon
![DDB](https://raw.githubusercontent.com/chris17453/ddb/master/source/resources/ddb-icon.png)

## Will you help me?
Sure, within reason and ability. Just contact [me](mailto:chris174543@gmail.com)
