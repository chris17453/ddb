from .factory_term import flextable
from .factory_json import factory_json
from .factory_yaml import factory_yaml
from .factory_xml import factory_xml


class output_factory:

    def __init__(self,query_results,output='term',output_file=None):
            """display results in different formats
            if output_file==None then everything is directed to stdio

            output=(bash|term|yaml|json|xml)
            output_file= None or file to write to
            """        
            if None==query_results:
                return
            
            mode=output.lower()
            if 'bash'==mode:
                self.format_bash(query_results,output_file)
            
            elif 'term'==mode:
                self.format_term(query_results,output_file)
            
            elif 'raw'==mode:
                self.format_raw(query_results,output_file)
            
            elif 'yaml'==mode:
                self.format_yaml(query_results,output_file)
            
            elif 'json'==mode:
                self.format_json(query_results,output_file)
            
            elif 'xml'==mode:
                self.format_xml(query_results,output_file)
            #default
            else: 
                self.format_term(query_results,output_file)


    def format_term(self,query_results,output_file):
        """ouput results data in the term format"""
        try:
            if query_results.data and query_results.columns:
                flextable(data=query_results.data,columns=query_results.columns)
            print("executed in {0:.6f}, {1} rows returned".format(query_results.time,query_results.data_length))

        except Exception as ex:
            print(ex)
            #print(query_results.data)

    def format_bash(self,query_results,output_file):
        """ouput results data in the bash format"""
        data=query_results.data
        
        name="ddb"

        print ("{0}_row_length={1}".format(name,len(data)))
        print ("{0}_column_length={1}".format(name,len(query_results.columns)))
        print ("")

        column_index=0
        for column in query_results.columns:
            print("{0}_columns['{1}']='{2}'".format(name,column_index,column))
            column_index+=1


        row_index=0
        for row in data:
            for column_index in range(0,len(query_results.columns)):
                print('{0}_data[{1}][{2}]="{3}"'.format(name,row_index,column_index,row['data'][column_index]))
            row_index+=1
        

    def format_raw(self,query_results,output_file):
        """ouput results data in the yaml format"""
        print(query_results.data)
        if not output_file:
            for row in query_results.data:
                if 'raw' in row:
                    print(row['raw'].rstrip())
        else:
            with open(output_file, "w") as write_file:
                for row in query_results.data:
                    if 'raw' in row:
                        write_file.write(row['raw'])

    def format_yaml(self,query_results,output_file):
        """ouput results data in the yaml format"""
        results=query_results.data
        factory=factory_yaml()
        dump=factory.dump(results)
        if not output_file:
            print dump
        else:
            with open(output_file, "w") as write_file:
                write_file.write(dump)

    def format_json(self,query_results,output_file):
        """ouput results data in the json format"""
        results=query_results.data
        factory=factory_json()
        dump=factory.dumps(results)
        if not output_file:
            print dump
        else:
            with open(output_file, "w") as write_file:
                write_file.write(dump)
        
    def format_xml(self,query_results,output_file):
        """ouput results data in the xml format"""
        results=query_results.data
        factory=factory_xml()
        dump=factory.dumps({'data':results})
        if not output_file:
            print dump
        else:
            with open(output_file, "w") as write_file:
                write_file.write(dump)