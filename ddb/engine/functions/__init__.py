def show_columns(database,table):
    temp_table=database.temp_table(columns=['table','column'])
    
    for c in table.columns:
        columns=[table.data.name,c.data.name]
        temp_table.append_data(columns)
    return temp_table

def show_tables(database):
    temp_table=database.temp_table(columns=['table'])
    for t in database.tables:
        columns=[t.data.name]
        temp_table.append_data(columns)
    return temp_table


def show_errors(database,table):
    temp_table=database.temp_table(columns=['error'])
    for e in table.errors:
        columns=[e]
        temp_table.append_data(columns)
    return temp_table
