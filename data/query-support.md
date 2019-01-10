# ddb query support

- Query support is limited to standard operations
- As needed I'll improve the system.



## DATABASE Commands

### USE
```sql
 USE database
```

## DATA Commands

### SELECT
- select_expr = { {column | function () } [AS display_name]}
- order_expression = { ASC | DESC }
```sql
SELECT select_expr [,select_expr ... ]
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
```sql
INSERT INTO table ({column [,column ...]}) VALUES ({values [,value ...]})
```

### DELETE FROM
```sql
DELETE FROM table 
[WHERE condition 
    [
        [AND condition] 
        [OR condition]
    ] 
]
```

###  UPDATE 
```sql
table SET column=value [WHERE]
```

## TABLE Commands

### DESCRIBE TABLE 
```sql
DESCRIBE TABLE table
```

### CREATE TABLE
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

### DROP TABLE table
```sql
DROP TABLE table
```

### UPDATE TABLE
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
```sql
 SHOW TABLES
```

### SHOW COLUMNS FROM
 ```sql
SHOW COLUMNS FROM table
 ```


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