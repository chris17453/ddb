# ddb code integration

```python
import ddb

engine=ddb.engine(mode='object')

# defining the table.
# not needed if you define out of code in the cli app with "create table"
# you could even create the table with a query in code, and not use the class function
engine.define_table(table_name='test_table',
                    database_name='test_db',
                    field_delimiter=',',
                    columns=['name','document','os','id','price','qty','value'],
                    data_file='/MOCK_DATA.csv')



# standard query
query="SELECT * FROM `test_table` WHERE id='{}'".format(id)

# an array of matched results
# None if an invalid query or error
# an empty array if nothing matches the query
results=self.engine.query(query)
```
