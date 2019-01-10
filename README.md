# ddb (delimited database)

 A serviceless sql interface for flat files written in python


## What does it do?
- ddb sits on top of text files, giving them a database access layer
- you can read, write, update csv's or any type of delimited text file via sql


## What are the human benifits to using ddb?
- a common interface for all of your flat files
- multiple points of integration (progromatic and cli)
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


## How do I use it?
- with python [python integration](data/python-integration.md)
- from bash [cli](data/cli.md)


## Where do I get it?
- the code -> [github](https://github.com/chris17453/ddb)
- the offical package -> [Pypi](https://pypi.org/project/ddb/)


## How do I install it?
```bash
pip install ddb --user
```


## Getting started
- [cli](data/cli.md)
- [examples](data/examples.md)
- [walkthrough](data/walkthrough.md)


## dev stuff
- [query support](data/query-support.md)
- [data output](data/output.md)
- [python integration](data/python-integration.md)
- [build](data/build.md)
- [notes](data/notes.md)
- [changelog](data/changelog.md)



### Demo
![Demo](https://raw.githubusercontent.com/chris17453/ddb/master/data/ddb-demo.gif)

