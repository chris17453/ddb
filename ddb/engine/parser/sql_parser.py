from ..tokenizer.sql_tokenize import *
from ..structure.table import *
import copy 

class sql_parser:
    

    def __init__(self,configs,query,debug=False):
        # select * from table where x=y and y=2 order by x,y limit 10,2
        # select c1,c2,c3,c4 as x,* from table where x=y and y=2 order by x,y limit 10,2
        # select top 10 * from table where x=y and y=2 order by x,y 
        # insert into table () values ()
        # delete from table where x=y and y=2
        self.mode=None
        self.limit_start=None
        self.limit_length=None
        self.where=[]
        self.target=None
        self.source=None
        self.columns=[]
        self.order=[]
        self.show=None

        argument_number=0
        section=None
        tokens=tokenize(query)
        processed_query=""
        #print (tokens)
        for token in tokens:
            #print(token)
            #print(section)
            processed_query+=token['data']

            if 'delimiter' == token['type']:
                if token['data']==',':
                    argument_number=0
                continue


            data=token['data']
            lower_case_token=data.lower()
            
            if token['type']=='keyword':
                if lower_case_token=="select":
                    section='columns'
                    self.mode='select'
                    continue
                if lower_case_token=="show":
                    section='show'
                    self.mode='show'
                    argument_number=0
                    continue
                if lower_case_token=="insert":
                    section='action'
                    self.mode='insert'
                    continue
                if lower_case_token=="delete":
                    section='action'
                    self.mode='delete'
                    continue
                if lower_case_token=="update":
                    section='action'
                    self.mode='update'
                    continue
                if lower_case_token=="top":
                    section='top'
                    continue
                if lower_case_token=="limit":
                    section='limit'
                    continue
                if lower_case_token=="from":
                    section='source'
                    continue
                if lower_case_token=="into":
                    section='target'
                    continue
                if lower_case_token=="where":
                    section='where'
                    argument_number=0
                    continue
                if lower_case_token=="and" and section=='where':
                    test={'condition':'and','expression1':None,'expression2':None}
                    self.where.append(test)
                    argument_number=0
                    continue
                
                if lower_case_token=="or" and section=='where':
                    test={'condition':'or','expression1':None,'expression2':None}
                    self.where.append(test)
                    argument_number=0
                    continue

                if lower_case_token=="not" and section=='where':
                    test={'condition':'not','expression1':None,'expression2':None}
                    self.where.append(test)
                    argument_number=0
                    continue
                                    
                if lower_case_token=="order":
                    section='order'
                    argument_number=0
                    continue
                if lower_case_token=="by" and section=='order':
                    section='order_by'
                    argument_number=0
                    continue
                if lower_case_token=="as":
                    section='column_as'
                    continue
            
            # data selection for section
            if section=='show':
                if argument_number==0:
                
                    if lower_case_token=="columns":
                        self.show=data
                    if lower_case_token=="errors":
                        self.show=data
                    if lower_case_token=="tables":
                        self.show=data

                argument_number+=1
                    
                

            if section=='top' and self.mode=='select':
                self.limit_length=int(data)
                self.limit_start=0
                section='columns'
                continue

            if section=='limit' and self.mode=='select':
                if None == self.limit_length:
                    self.limit_length=int(data)
                    continue
                else:
                    self.limit_start=self.limit_length
                    self.limit_length=int(data)
                    section='None'
                    continue

            if section=='source':
                self.source=data

            if section=='target':
                self.target=data

            if section=='columns':
                self.columns.append({'name':data,'display':None})

            if section=='column_as':
                col=self.columns.pop()
                col['display']=data
                self.columns.append(col)
                section="columns"

            if section=='where':
                #print argument_number
                if argument_number==0:
                    if token['type']=='data':
                        test={'condition':None,'expression1':data,'expression2':None}
                        
                        self.where.append(test)
                    else:
                        raise Exception("Error near: {}, Invalid keyword in 'WHERE': {}".format(processed_query,data))
                else:
                    if token['type']=='data':
                        t_where=self.where.pop()
                        if t_where['expression2']==None:
                            t_where['expression2']=data
                            self.where.append(test)
                        else:
                            raise Exception("Error near: {}, Invalid data in 'WHERE': {} expression #2 ".format(processed_query,data))
                    if token['type']=='operator':
                        t_where=self.where.pop()

                        if t_where['condition']==None:
                            t_where['condition']=data
                            self.where.append(test)
                        else:
                            raise Exception("Error near: {}, Invalid data in 'WHERE': {} condition ".format(processed_query,data))
                argument_number+=1


            if section=='order_by':
                if argument_number==0:
                    argument_number+=1
                    if token['type']=='data':
                        self.order.append({'column':data,'direction':'ASC'})
                        continue
                    else:
                        print(token)
                        raise Exception("Error near: {}, Invalid data in 'ORDER BY': {}".format(processed_query,data))
                if argument_number==1:
                    argument_number+=1
                    if token['type']=='keyword':
                        if lower_case_token=='asc' or lower_case_token=='desc':
                            t_order=self.order.pop()
                            t_order['direction']=data.upper()
                            self.order.append(t_order)
                            continue
                        else:
                            raise Exception("Error Near: {}, Error invalid keyword for 'ORDER BY': {}".format(processed_query,data))
                    else:
                        raise Exception("Error Near: {}, Error invalid keyword for 'ORDER BY': {}".format(processed_query,data))
                if argument_number==2:
                        raise Exception("Error Near: {}, Error invalid syntax for 'ORDER BY' to many arguments: {}".format(processed_query,data))



        if None == self.mode:
            raise Exception("Invalid Query")

        if self.mode=='select':
            cf=configs.get(self.source)
            columns2=[]
            if None!=cf:
                for c in self.columns:
                    if c['name']=='*':
                        for c in cf.columns:
                            columns2.append({'name':c.data.name,'display':None})
                        continue

                    if False == cf.has_column(c['name']):
                        raise Exception("No column {}".format(c['name']))
                    columns2.append(copy.deepcopy(c))
                self.columns=columns2


        if True == debug:
            print("")
            print("--Query Stats-------------------")

            print("Mode     : {}".format(self.mode))
            print("Range    : {},{}".format(self.limit_start,self.limit_length))
            print("Where    : {}".format(self.where))
            print("Target   : {}".format(self.target))
            print("Source   : {}".format(self.source))
            print("Columns  : {}".format(self.columns))
            print("Show     : {}".format(self.show))

            print("Order    : {}".format(self.order))

                    


        
        # err handeling
        if None == self.mode:
            raise Exception("No mode slected. Select, Insert, Update, Delete")
            
                



