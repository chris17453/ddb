# ddb query support

- Query support is limited. As needed I'll improve the system.
- If you're doing vastly comlicated things, it shouldn't be with a flat file.
- This code is no t fast, but not slow either. It will be refactored, but not until more support is added.
- compiled with cython gives a 450%+ boost in execution time. 
- My test record set with 60k records, at first, came back in 1.6 seconds, now comes in at .35 seconds

### Supported Querys

- USE [DATABASE]
- SHOW TABLES
- SHOW COLUMNS FROM [TABLE]
- CREATE TABLE [TABLE] ([COLUMNS]) file=[DATA_FILE_PATH] delimiter=[FIELD_DELIMITER(default=',')] [WHITESPACE=bool] [ERRORS=bool] [COMMENTS=bool] data_on=[DATA_BEGINS_AT_LINE(default=1)] 
- DROP TABLE [TABLE]
- SELECT [[COLUMN [AS COLUMN]]|[FUNCTION(...) [AS COLUMN]]] FROM [TABLE] [WHERE] [AND] [OR] [ORDER BY] [LIMIT]
- INSERT INTO [TABLE] ([[COLUMNS]]) VALUES ([[VALUES])
- DELETE FROM [TABLE] [WHERE] [AND] [OR]
- UPDATE [TABLE] SET [[COLUMN=VALUE]] [WHERE]
- DESCRIBE TABLE [TABLE]
- UPDATE TABLE [TABLE] ([COLUMNS]) file=[DATA_FILE_PATH] delimiter=[FIELD_DELIMITER(default=',')] [WHITESPACE=bool] [ERRORS=bool] [COMMENTS=bool] data_on=[DATA_BEGINS_AT_LINE(default=1)] 

### Supported functions

- database(), returns curent db context
- version(), returns ddb version
- datetime(), returns datetime
- date(), returns date
- time(), returns time

### TODO

- curses browser for results (wil be built in flextable)
- output to yaml,json,raw, csv formatted string (should be simple)
- adding test cases for tokenizing
- aggregate function support 
- functions: COUNT, JOIN, SUM, DISTINCT, GROUP BY are all high on the list in that order