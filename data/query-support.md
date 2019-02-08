# ddb query support

- Query support is limited to standard operations
- As needed I'll improve the system.


### DATABASE commands
- [USE](#USE)
### Data commands
- [SELECT](#SELECT)
- [INSERT](#INSERT)
- [UPDATE ](#UPDATE)
- [DELETE](#DELETE-FROM)
### Table commands
- [DESCRIBE TABLE ](#DESCRIBE-TABLE)
- [CREATE TABLE](#CREATE-TABLE)
- [DROP TABLE](#DROP-TABLE)
- [UPDATE TABLE](#UPDATE-TABLE)
### INFO Commands
- [SHOW TABLES](#SHOW-TABLES)
- [SHOW COLUMNS](#SHOW-COLUMNS-FROM)

- [Supported functions](#Supported-functions)
- [TODO](#TODO)





### USE
change the curent context the database is operating on. The active database.
```sql
 USE database
```

### SELECT
read data from a table
- select_expr = { {column | function () } [AS display_name]}
- order_expression = { ASC | DESC }
```sql
SELECT [DISTINCT] select_expr [,select_expr ... ]
[FROM table
[WHERE condition 
    [
        [AND condition] 
        [OR condition]
    ]
]
[ORDER BY {column_name} order_expression [,{column_name} order_expression ...]] 
]
[LIMIT [{offset, }] row_count]
```         

### INSERT
insert a row into the table
```sql
INSERT INTO table ({column [,column ...]}) VALUES ({values [,value ...]})
```

### DELETE
delete a row from the table
```sql
DELETE FROM table 
[WHERE condition 
    [
        [AND condition] 
        [OR condition]
    ] 
]
```

### UPDATE 
change a row in the table
```sql
UPDATE table 
SET column=value [, column=value ...] 
[WHERE condition 
    [
        [AND condition] 
        [OR condition]
    ] 
]
```

### DESCRIBE TABLE 
display information about a table
```sql
DESCRIBE TABLE table
```

### CREATE TABLE
create a new table
```sql
CREATE TABLE table 
    ({columns}) 
    FILE=data_file_path 
    [DELIMITER=field_delimiter(default=',')] 
    [WHITESPACE=bool] 
    [ERRORS=bool] 
    [COMMENTS=bool] 
    [DATA_ON=data_begins_on_line(default=1)]
```

### DROP TABLE
remove a table configuration from the database. data files are not affected.
```sql
DROP TABLE table
```

### UPDATE TABLE
update a table configuration in the database. data files are not affected.
```sql
 UPDATE TABLE table 
    ({columns}) 
    FILE=data_file_path 
    [DELIMITER=field_delimiter(default=',')] 
    [WHITESPACE=bool] 
    [ERRORS=bool] 
    [COMMENTS=bool] 
    [DATA_ON=data_begins_on_line(default=1)]
```

### SHOW TABLES
show all active tables in the database
```sql
 SHOW TABLES
```

### SHOW COLUMNS FROM
display the columns in a given table
 ```sql
SHOW COLUMNS FROM table
 ```


### Supported functions
these functions can be use as a select expression
- database(), returns curent db context
- version(), returns ddb version
- datetime(), returns datetime
- date(), returns date
- time(), returns time



### TODO
- aggregate function support 
- functions: COUNT, JOIN, SUM, DISTINCT, GROUP BY are all high on the list in that order