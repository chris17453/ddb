



def evaluate_single_match(test,row,table):
    compare1=None
    compare2=None
    compare1_is_column=False
    compare2_is_column=False
    if None !=test['condition']:
        test['condition']=test['condition'].lower()
        
    for column in table.columns:
        #print column.data.name
        if column.data.name==test['expression1']:
            #print "found1", column.data.name
            compare1=table.get_data_from_column(column,row)
            compare1_is_column=True
        if column.data.name==test['expression2']:
            #print "found2", column.data.name
            compare2=table.get_data_from_column(column,row)
            compare2_is_column=True
        if None !=compare1 and None != compare2:
            break
    if None == compare1:
        compare1=test['expression1']
    if None == compare2:
        compare2=test['expression2']
    if None == compare1 and None == compare2:
        raise Exception("Where invalid {}".format(test))
        
    if test['condition']=='=' or test['condition']=='is' :
        if compare1==compare2:
            return True
    if test['condition']=='like':  #paritial match

        if True == compare1_is_column and  True == compare2_is_column:
            raise Exception("Where invalid {}, like cant be between 2 columns".format(test))

        if True == compare1_is_column:
            like=compare2
            data=compare1
        else:
            like=compare1
            data=compare2

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
    if test['condition']=='<' :
        if compare1<compare2:
            return True
    if test['condition']=='>' :
        if compare1>compare2:
            return True
    if test['condition']=='>=' :
        if compare1>=compare2:
            return True
    if test['condition']=='<=' :
        if compare1<=compare2:
            return True
    if test['condition']=='!=' or test['condition']=='<>' or test['condition']=='not':
        if compare1!=compare2:
            return True

    return False


def evaluate_match(where,row,table):
    #print where
    if None == row: 
        return False
    if 0 == len(where):
        return True
    success=None
    in_condition="and"
    skip_section=False
    for test in where:

        # if a evaluation chain failed, continue until out of that section
        if True == skip_section:
            if test['condition'] in {'or','and','not'}:
                skip_section=False
            else:
                continue

        if isinstance(test,list):
            print "in list"
            success=evaluate_match(test,row,table)
        else:
            if test['condition']=='or':
                if success==True:
                    return True
                in_condition="or"
                continue
            
            if test['condition']=='and':
                in_condition="and"
                if success==False:
                    skip_section=True
                continue
            
            if test['condition']=='not':
                in_condition='not'
                continue
            
            # evaluator
            success=evaluate_single_match(test,row,table)
                    

    # never matched anytthing...
    if success==None:
        return False
    return success

