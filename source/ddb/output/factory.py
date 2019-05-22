# cython: linetrace=True

from .factory_term import flextable
from .factory_json import factory_json
from .factory_yaml import factory_yaml
from .factory_xml import factory_xml


class output_factory:

    def __init__(self,query_results,output='term',output_style="flextable",output_file=None,output_stream='STDIO',color=True): # style single double rst
            """display results in different formats
            if output_file==None then everything is directed to stdio

            output=(bash|term|yaml|json|xml)
            output_file= None or file to write to
            """        
            if None==query_results:
                return
            self.output=None
            mode=output.lower()
            if 'bash'==mode:
                self.output=self.format_bash(query_results)
            
            elif 'term'==mode:
                self.output=self.format_term(query_results,output_style,output_stream=output_stream,color=color)
            
            elif 'raw'==mode:
                self.output=self.format_raw(query_results,output_stream)
            
            elif 'yaml'==mode:
                self.output=self.format_yaml(query_results)
            
            elif 'json'==mode:
                self.output=self.format_json(query_results)
            
            elif 'xml'==mode:
                self.output=self.format_xml(query_results)
            elif 'time'==mode:
                self.output ="User Time:Start:{0}, End:{1}, Elapsed:{2}".format(query_results.start_time,query_results.end_time,query_results.time)
                self.output+="Wall Time:Start:{0}, End:{1}, Elapsed:{2}".format(query_results.wall_start,query_results.wall_end,query_results.wall_time)            #default
            else: 
                self.output=self.format_term(query_results)


    def format_term(self,query_results,output_style=None,output_stream=None,color=True):
        """ouput results data in the term format"""
        #try:
        if query_results.columns:
            ft=flextable(data=query_results.data,columns=query_results.columns,display_style=output_style,output_stream=output_stream,render_color=color)
            res=ft.output_destination
        else:
            res=None
        if True == query_results.success:
            if res:
                res.append("executed in {0:.6f}, {1} rows returned".format(query_results.time,query_results.data_length))
            else:
                print("executed in {0:.6f}, {1} rows returned".format(query_results.time,query_results.data_length))
        else:
            # may never get here...
            if res:
                res.append("Query Failed")
            else:
                print("Query Failed")
        #print res
        return res
        #except Exception as ex:
        #    print("TERM Formatting: {0}".format(ex))
            #print(query_results.data)

    def format_bash(self,query_results):
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
        # TODO return output for this
        return ""
        

    def format_raw(self,query_results,output_stream):
        """ouput results data in the yaml format"""
        #print(query_results.data)
        delimiter=query_results.delimiter
        res=[]
        for row in query_results.data:
            if 'data' in row:
                raw=delimiter.join(row['data'])
                if output_stream=='STDIO':
                    print(raw)
                else:
                    res.append(raw)

        if output_stream=='STRING':
            return res

    def format_yaml(self,query_results):
        """ouput results data in the yaml format"""
        results=query_results.data
        factory=factory_yaml()
        dump=factory.dump(results)
        print(dump)
        # TODO return output for this
        return ""

    def format_json(self,query_results):
        """ouput results data in the json format"""
        results=query_results.data
        factory=factory_json()
        dump=factory.dumps(results)
        print(dump)
        # TODO return output for this
        return ""
        
    def format_xml(self,query_results):
        """ouput results data in the xml format"""
        results=query_results.data
        factory=factory_xml()
        dump=factory.dumps({'data':results})
        print(dump)
        # TODO return output for this
        return ""
