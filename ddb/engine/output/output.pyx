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

def format_yaml(results,output_file):
    """ouput results data in the yaml format"""
    dump=yaml.safe_dump(results, default_flow_style=False)
    if not output_file:
        print dump
    else:
        with open(output_file, "w") as write_file:
            write_file.write(dump)

def format_json(results,output_file):
    """ouput results data in the json format"""
    if not output_file:
        json.dump(results)
    else:
        with open(output_file, "w") as write_file:
            json.dump(results, write_file)
    
def format_xml(results,output_file):
    """ouput results data in the xml format"""
    dump=yaml.safe_dump(results, default_flow_style=False)
    if not output_file:
        print dump
    else:
        with open(output_file, "w") as write_file:
            write_file.write(dump)


def format(results):
    v=1