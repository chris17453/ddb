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
    print(results)

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