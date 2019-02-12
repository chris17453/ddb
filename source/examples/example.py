import ddb
import json 

engine=ddb.engine(mode='object')

# defining the table.
# not needed if you define out of code in the cli app with "create table"
# you could even create the table with a query in code, and not use the class function
# define table is a temporary table definition
engine.define_table(table_name='test_table',
                    database_name='test_db',
                    field_delimiter=',',
                    columns=['id','first_name','last_name','email','gender','ip_address'],
                    data_file='/home/nd/repos/chris17453/ddb/ddb/test/MOCK_DATA.csv')



length=10
for page in range(1,3):
    print ("Page: {0}".format(page+1))
    # standard query
    query="use test_db; SELECT * FROM test_table ORDER BY email desc LIMIT {0},{1}".format(page*length,length)

    # an array of matched results
    # None if an invalid query or error
    # an empty array if nothing matches the query
    results=engine.query(query)
    #print (json.dumps(results,indent=4) )
    for r in results:
        print("ID: {0} Email: {1}".format(r['id'],r['email']))


    # The output should look like this
    '''
    [ddb]$ python examples/example.py 
    Page: 2
    ID: 118 Email: ybeste39@weibo.com
    ID: 328 Email: ybeelby93@sciencedaily.com
    ID: 232 Email: xwhitmarsh6f@zdnet.com
    ID: 578 Email: xroslingg1@skyrock.com
    ID: 151 Email: wyouel46@mlb.com
    ID: 939 Email: wwoolhouseq2@phoca.cz
    ID: 959 Email: wwinterburnqm@weather.com
    ID: 230 Email: wwilkenson6d@mediafire.com
    ID: 696 Email: wwaistelljb@hhs.gov
    ID: 991 Email: wpettipherri@hc360.com
    Page: 3
    ID: 666 Email: wmcgroryih@wufoo.com
    ID: 228 Email: wlomasney6b@weebly.com
    ID: 445 Email: wjeynesscc@vimeo.com
    ID: 414 Email: wguerrerobh@canalblog.com
    ID: 881 Email: weverog@columbia.edu
    ID: 461 Email: wderyebarrettcs@harvard.edu
    ID: 577 Email: wdaymontg0@quantcast.com
    ID: 487 Email: wcrippelldi@quantcast.com
    ID: 593 Email: wburnsellgg@eepurl.com
    ID: 161 Email: wburbridge4g@xing.com
    [ddb]$ 

    '''