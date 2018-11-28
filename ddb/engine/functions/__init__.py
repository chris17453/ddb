



def show_columns(database,table_name):
    temp_table=database.temp_table(columns=['table','column'])
    columns=[]
    
    source_table=database.get(table_name)
    for c in source_table.columns:
        columns.append([source_table.data.name,c.data.name])
    temp_table.append_data(columns)
    return temp_table

def show_tables(database):
    temp_table=database.temp_table(columns=['table'])
    columns=[]
    
    
    for t in database.tables:
        columns.append([t.data.name])
    temp_table.append_data(columns)
    return temp_table


def show_errors(database,table):
    temp_table=database.temp_table(columns=['error'])
    columns=[]
    
    for e in table.errors:
        columns.append([e])
    temp_table.append_data(columns)
    return temp_table
