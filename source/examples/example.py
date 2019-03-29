from .context import  ddb
import json 


def example1():
    engine=ddb.engine(mode='object')
    # defining the table.
    # not needed if you define out of code in the cli app with "create table"
    # you could even create the table with a query in code, and not use the class function
    # define table is a temporary table definition
    engine.define_table(table_name='test_table',
                        database_name='test_db',
                        field_delimiter=',',
                        data_starts_on=2,
                        columns=['id','first_name','last_name','email','gender','ip_address'],
                        data_file='~/repos/chris17453/ddb/source/test/MOCK_DATA.csv'
                        )



    length=20
    for page in range(1,3):
        print ("Page: {0}".format(page+1))
        # standard query
        query="use test_db; SELECT * FROM test_table ORDER BY email desc LIMIT {0},{1}".format(page*length,length)
        print(query)
        # an array of matched results
        # None if an invalid query or error
        # an empty array if nothing matches the query
        results=engine.query(query)
        print (results.success)
        #print (json.dumps(results,indent=4) )
        for r in results.data:
            print("ID: {0} Email: {1}".format(r['data']['id'],r['data']['email']))
        #print (results.columns)


        # The output should look like this
        '''
Page: 2
use test_db; SELECT * FROM test_table ORDER BY email desc LIMIT 20,20
True
ID: 991 Email: wpettipherri@hc360.com
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
ID: 729 Email: wbreinleink8@exblog.jp
ID: 711 Email: wbramhalljq@multiply.com
ID: 471 Email: wbidnalld2@mapquest.com
ID: 859 Email: wbalderstonenu@sfgate.com
ID: 636 Email: wapdellhn@fema.gov
ID: 322 Email: vvedekhov8x@irs.gov
ID: 239 Email: vtett6m@boston.com
ID: 575 Email: vservisfy@51.la
ID: 121 Email: vsebright3c@dailymail.co.uk
Page: 3
use test_db; SELECT * FROM test_table ORDER BY email desc LIMIT 40,20
True
ID: 29 Email: vsalsburys@icio.us
ID: 334 Email: vrosenthal99@arizona.edu
ID: 573 Email: vmeijerfw@paypal.com
ID: 90 Email: vmccluskey2h@ovh.net
ID: 667 Email: vmalacridaii@ucoz.com
ID: 957 Email: vlabuschagneqk@unicef.org
ID: 376 Email: vjordineaf@unblog.fr
ID: 235 Email: vjamieson6i@nifty.com
ID: 423 Email: vhebblewhitebq@wp.com
ID: 994 Email: vdentithrl@squarespace.com
ID: 914 Email: vdauneypd@github.io
ID: 643 Email: vdalessandrohu@fda.gov
ID: 522 Email: vcranhameh@mysql.com
ID: 355 Email: vclopton9u@simplemachines.org
ID: 912 Email: vchuterpb@youtu.be
ID: 173 Email: vbunyan4s@oaic.gov.au
ID: 540 Email: vbrewerez@sun.com
ID: 296 Email: vbamfield87@ovh.net
ID: 560 Email: utinanfj@go.com
ID: 539 Email: ulimmerey@spotify.com

        '''

if __name__ == '__main__':
    example1()

# on error data=None