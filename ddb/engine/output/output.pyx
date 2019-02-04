from .factory_json import factory_json
from .factory_yaml import factory_yaml
from .factory_xml import factory_xml
import flextable


class output_factory:

    def __init__(self,results,output='term',output_file=None):
            """display results in different formats
            if output_file==None then everything is directed to stdio

            output=(bash|term|yaml|json|xml)
            output_file= None or file to write to
            """        
            if None==results:
                return
            
            mode=output.lower()
            if 'bash'==mode:
                self.format_bash(results,output_file)
            
            elif 'term'==mode:
                self.format_term(results,output_file)
            
            elif 'raw'==mode:
                self.format_raw(results,output_file)
            
            elif 'yaml'==mode:
                self.format_yaml(results,output_file)
            
            elif 'json'==mode:
                self.format_json(results,output_file)
            
            elif 'xml'==mode:
                self.format_xml(results,output_file)
            #default
            else: 
                self.format_term(results,output_file)


    def format_term(self,results,output_file):
        """ouput results data in the term format"""
        try:
            config = flextable.table_config()
            config.columns = results.get_columns_display()
            flextable.table(data=results.results, args=config)
        except:
            print(results.results)

    def format_bash(self,temp_table,output_file):
        """ouput results data in the bash format"""
        data=temp_table.get_results()
        
        name="ddb"
        print ("# bash variable assignment for ddb output")
        print ("declare {0}_data -A".format(name))
        print ("declare {0}_info -A".format(name))
        print ("declare {0}_columns -A".format(name))
        print ("")

        column_index=0
        for column in data['columns']:
            print("{0}_columns[{1}]='{2}'".format(name,column_index,column))
            column_index+=1


        row_index=0
        for row in data['results']:
            column_index=0
            if not row['error']:
                row_error=''
            else:
                row_error=row['error']
            print("{0}_info[{1},error]='{2}'".format(name,row_index,row_error))
            if not row['type']:
                row_type=''
            else:
                row_type=row['type']
            print("{0}_info[{1},type]='{2}'".format(name,row_index,row_type))
            if not row['raw']:
                row_raw=''
            else:
                row_raw=row['raw']
            print("{0}_info[{1},raw]='{2}'".format(name,row_index,row_raw))
            for column in row['data']:
                print("{0}_data[{1},{2}]='{3}'".format(name,row_index,column_index,column))
                column_index+=1
            row_index+=1
        print ("# end ddb output ")
                
        

    def format_raw(self,results,output_file):
        """ouput results data in the yaml format"""
        print(results.results)
        if not output_file:
            for row in results.results:
                if 'raw' in row:
                    print(row['raw'].rstrip())
        else:
            with open(output_file, "w") as write_file:
                for row in results.results:
                    write_file.write(row['raw'])

    def format_yaml(self,temp_table,output_file):
        """ouput results data in the yaml format"""
        results=temp_table.get_results()
        factory=factory_yaml()
        dump=factory.dumps(results)
        if not output_file:
            print dump
        else:
            with open(output_file, "w") as write_file:
                write_file.write(dump)

    def format_json(self,temp_table,output_file):
        """ouput results data in the json format"""
        results=temp_table.get_results()
        factory=factory_json()
        dump=factory.dumps(results)
        if not output_file:
            print dump
        else:
            with open(output_file, "w") as write_file:
                write_file.write(dump)
        
    def format_xml(self,temp_table,output_file):
        """ouput results data in the xml format"""
        results=temp_table.get_results()
        factory=factory_xml()
        dump=factory.dumps({'data':results})
        if not output_file:
            print dump
        else:
            with open(output_file, "w") as write_file:
                write_file.write(dump)