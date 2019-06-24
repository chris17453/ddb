import os
import sys
from .context import  ddb
from pprint import pprint



engine = ddb.engine(config_file=False)

create="""create temporary table 'etmeta'.'properties' 
            (environment,application,server,instance,node,property,value) 
            file='/etrade/etc/properties' 
            delimiter=':' 
            whitespace=False 
            errors=True 
            comments=False 
            strict=False 
            data_starts_on=2"""
engine.query(create)

res=engine.query("select * from 'etmeta'.'properties'")


for row in res['data']:
    print row['data']
