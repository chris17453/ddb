# ddb notes


## Notes to self

- cython builds the python code as a ".so"
- packages can see down, not up
- in code import using full package name
- cython packages must be marked as extensions
- all pure cython packages must be marked as packages in setup, otherwise "le fail"
- unless specified, all configurations apply to ~/.ddb/ddb.conf in your home directory
- this is a lookup file for the tables
- table configs are stored in a sub directory based on the db name
- ; is a command seperator. everything after this is a new command
- results are only returned for the last operation preformed
- all interactions are parsed directly from the data_files at time of execution
- 5 querys will consist of 5 file reads.
- anything inside of a block quote is treated as a single expression. '...' or "..." or [...]