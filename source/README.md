# ddb (delimited database)

 A serviceless sql interface for flat files written in python

## What does it do?

- ddb sits on top of text files, giving them a database access layer
- you can read, write, update text files of any type via sql

## Human benifits

- a common interface for text files
- sql is easy to work with, no coding required
- painless side by side integration
- multiple integration vectors (python, shell, slack, ansible)
- ease of automation

## Technical benifits

- abstraction layer for data
- provides migration path for data
- change control
- logging
- permissions
- low memory foot print
- error handeling
- data is live, never cached
- optimized for speed using cython


## Python 2 / 3 Compliant
- changes sorting
- tons of byte vs str (encoding)
