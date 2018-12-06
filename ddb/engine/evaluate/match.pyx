



def evaluate_single_match(test,row,table):

    compare1=None
    compare2=None
    compare1_is_column=False
    compare2_is_column=False

    comparitor=test['c']


    #if None !=comparitor:
    #   comparitor=comparitor.lower()

    
     
    for column in table.columns:
        #print column.data.name
        if column.data.name==test['e1']:
            index=table.ordinals[column.data.name]
            #print "found1", column.data.name
            compare1=row[index]#table.ordinals[].get_data_from_column(column,row)
            #compare1=table.get_data_from_column(column,row)
            compare1_is_column=True
        if column.data.name==test['e2']:
            index=table.ordinals[column.data.name]            
            #print "found2", column.data.name
            compare2=row[index] #table.get_data_from_column(column,row)
            #compare2=table.get_data_from_column(column,row)
            compare2_is_column=True
        if None !=compare1 and None != compare2:
            break

    if None == compare1:
        compare1=test['e1']
    if None == compare2:
        compare2=test['e2']
    if None == compare1 and None == compare2:
        raise Exception("Where invalid {}".format(test))
        
    if comparitor=='=' or comparitor=='is' :
        if compare1==compare2:
            #print compare1,compare2
            return True
    if comparitor=='like':  #paritial match

        if True == compare1_is_column and  True == compare2_is_column:
            raise Exception("Where invalid {}, like cant be between 2 columns".format(test))

        if True == compare1_is_column:
            like=compare2
            data=compare1
        else:
            like=compare1
            data=compare2

        if None == like:
            return False
        #if len(like)==0:
        #    return False
        #print "--"
        #print compare1,compare2,like
        if like[0]=='%':
            like_left=True
        else:
            like_left=False

        if like[-1]=='%':
            like_right=True
        else:
            like_right=False

        # compare middle of search
        if True == like_right and True == like_left:
            if data.find(like[1:-1])>-1:
                return True
            else:
                return False
        
        #if not found at end bail
        if True == like_left:
            if data[-(len(like)-1):]==like[1:]:
                return True
            else:
                return False

        #if not found at start, bail
        if True == like_right:
            if data[0:(len(like)-1)]==like[0:-1]:
                return True
            else:
                return False
        
        
        return False
    if comparitor=='<' :
        if compare1<compare2:
            return True
    if comparitor=='>' :
        if compare1>compare2:
            return True
    if comparitor=='>=' :
        if compare1>=compare2:
            return True
    if comparitor=='<=' :
        if compare1<=compare2:
            return True
    if comparitor=='!=' or comparitor=='<>' or comparitor=='not':
        if compare1!=compare2:
            return True

    return False


def evaluate_match(where,row,table):
    #print where
    if None == row: 
        return False
        
    if 0 == len(where):
        #print "0 len"
        return True
    success=None
    skip_section=False
    operation=""
    for test in where:
        #print test
        # if a evaluation chain failed, continue until out of that section
        if 'and' in test and skip_section==True:
            continue
        else:
            skip_section=False
           
        operation=None
        if 'where' in test:
            operation='where'

        if 'or' in test:
            operation='or'
            if success==True:
                return True
        
        if 'and' in test:

            operation='and'
            if success==False:
                skip_section=True
                continue

        test_operation=test[operation]
        success=evaluate_single_match(test_operation,row,table)

    # never matched anytthing...
    if success==None:
        return False
    return success

