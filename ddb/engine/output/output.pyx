import json
import yaml
import flextable


def format_term(results,output_file):
    """ouput results data in the term format"""
    config = flextable.table_config()
    config.columns = results.get_columns_display()
    flextable.table(data=results.results, args=config)

def format_bash(results,output_file):
    """ouput results data in the bash format"""
    data=temp_table.get_results()
    
    for c in data.columns:
    """ouput results data in the bash format"""
    row_index=0
    
    column_index=0
    for column in data['columns']:
        print("{0}_columns[{1}]='{2}'".format(name,column_index,column)
        column_index+=1


    for row in data['results']:
        column_index=0
        print("{0}_info[{1},error]='{3}'".format(name,row_index,row['error'])
        print("{0}_info[{1},type]='{3}'".format(name,row_index,row['type'])
        print("{0}_info[{1},raw]='{3}'".format(name,row_index,row['raw'])
        for column in row['data']:
            print("{0}_data[{1},{2}]='{3}'".format(name,row_index,column_index,column)
            column_index+=1
        row_index+=1
    

def format_raw(results,output_file):
    """ouput results data in the yaml format"""
    dump="S"
    if not output_file:
        print dump
    else:
        with open(output_file, "w") as write_file:
            write_file.write(dump)

def format_yaml(temp_table,output_file):
    """ouput results data in the yaml format"""
    results=temp_table.get_results()
    dump=yaml.safe_dump(results, default_flow_style=False)
    if not output_file:
        print dump
    else:
        with open(output_file, "w") as write_file:
            write_file.write(dump)

def format_json(temp_table,output_file):
    """ouput results data in the json format"""
    results=temp_table.get_results()
    if not output_file:
        dump=json.dumps(results)
        print dump
    else:
        with open(output_file, "w") as write_file:
            json.dump(results, write_file)
    
def format_xml(temp_table,output_file):
    """ouput results data in the xml format"""
    results=temp_table.get_results()
    dump=yaml.safe_dump(results, default_flow_style=False)
    if not output_file:
        print dump
    else:
        with open(output_file, "w") as write_file:
            write_file.write(dump)


def format(results,output_file):
    v=1