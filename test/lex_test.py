import timeit

### ----                                     ----
### ddb BYTECODE LANGUAGE DEFINITIONS
### ----                                     ----
### Automagically generated, dont mess with this.
### ----  or you will be eaten by unicorns   ----
### ----                                     ----

# each word is given an integer value based on section, sections increment based on SECTION BLOCK_VALUE

# T=text
# R=Reserved word
# K=Key word
# B=Block    such as comment, text or code
# O=Operator

# comparisons are ordered to be done in greatest length order, to prevent uneven length but similar values
# this also doubles as a speed enhancement






#
# Integer Values
#


# BLOCK

DOUBLE_QUOTE=1000
SINGLE_QUOTE=1001
BACK_TIC=1002
LEFT_COMMENT=1003
RIGHT_COMMENT=1004
COMMENT_SINGLE=1005
LEFT_PAREN=1006
RIGHT_PAREN=1007

# RESERVED WORD

AND=2000
ASC=2001
AS=2002
BEFORE=2003
BETWEEN=2004
BY=2005
CREATE=2006
DATABASE=2007
DATABASES=2008
DESC=2009
DISTINCT=2010
DROP=2011
EXISTS=2012
FALSE=2013
FROM=2014
GROUP=2015
GROUPS=2016
HAVING=2017
IN=2018
INSERT=2019
INTO=2020
IS=2021
JOIN=2022
LEFT=2023
LIKE=2024
LIMIT=2025
MOD=2026
NOT=2027
NULL=2028
ON=2029
ORDER=2030
OR=2031
RIGHT=2032
SELECT=2033
SET=2034
SHOW=2035
TABLE=2036
TRUE=2037
UNION=2038
UNIQUE=2039
UPDATE=2040
VALUES=2041
WHERE=2042
XOR=2043

# KEYWORD

DATE=3000
DATETIME=3001
FULL=3002

# OPERATOR

NULL_SAFE_EQUALS=4000
PLUS_EQUALS=4001
MINUS_EQUALS=4002
MULTIPLY_EQUALS=4003
DIVIDE_EQUALS=4004
MODULUS_EQUALS=4005
GREATER_THAN_EQUALS=4006
LESS_THAN_EQUALS=4007
EQUALS=4008
NOT_EQUALS=4009
NOT_EQUALS=4010
OR_EQUALS=4011
AND_EQUALS=4012
XOR_EQUALS=4013
SET=4014
SHORT_CIRCUIT_OR=4015
SHORT_CIRCUIT_AND=4016
BITWISE_LEFT=4017
BITWISE_RIGHT=4018
BITWISE_INVERSION=4019
PLUS=4020
MINUS=4021
MULTIPLY=4022
DIVIDE=4023
MODULUS=4024
GREATER_THAN=4025
LESS_THAN=4026
ASIGN=4027
NEGATE=4028
OR=4029
AND=4030
XOR=4031

# Numeric

ZERO=5000
ONE=5001
TWO=5002
THREE=5003
FOUR=5004
FIVE=5005
SIX=5006
SEVEN=5007
EIGHT=5008
NINE=5009

# Alpha

a=6000
b=6001
c=6002
d=6003
e=6004
f=6005
g=6006
h=6007
i=6008
j=6009
k=6010
l=6011
m=6012
n=6013
o=6014
p=6015
q=6016
r=6017
s=6018
t=6019
u=6020
v=6021
w=6022
x=6023
y=6024
z=6025
A=6026
B=6027
C=6028
D=6029
E=6030
F=6031
G=6032
H=6033
I=6034
J=6035
K=6036
L=6037
M=6038
N=6039
O=6040
P=6041
Q=6042
R=6043
S=6044
T=6045
U=6046
V=6047
W=6048
X=6049
Y=6050
Z=6051

# Delimiter

NEW_LINE=7000
TAB=7001
SPACE=7002
COMMA=7003
PERIOD=7004
DOLLAR=7005
UNDERSCORE=7006

#
# String Values
#


# BLOCK

DOUBLE_QUOTE_STR='"'
SINGLE_QUOTE_STR="'"
BACK_TIC_STR='`'
LEFT_COMMENT_STR='/*'
RIGHT_COMMENT_STR='*/'
COMMENT_SINGLE_STR='--'
LEFT_PAREN_STR='('
RIGHT_PAREN_STR=')'

# RESERVED WORD

AND_STR='AND'
ASC_STR='ASC'
AS_STR='AS'
BEFORE_STR='BEFORE'
BETWEEN_STR='BETWEEN'
BY_STR='BY'
CREATE_STR='CREATE'
DATABASE_STR='DATABASE'
DATABASES_STR='DATABASES'
DESC_STR='DESC'
DISTINCT_STR='DISTINCT'
DROP_STR='DROP'
EXISTS_STR='EXISTS'
FALSE_STR='FALSE'
FROM_STR='FROM'
GROUP_STR='GROUP'
GROUPS_STR='GROUPS'
HAVING_STR='HAVING'
IN_STR='IN'
INSERT_STR='INSERT'
INTO_STR='INTO'
IS_STR='IS'
JOIN_STR='JOIN'
LEFT_STR='LEFT'
LIKE_STR='LIKE'
LIMIT_STR='LIMIT'
MOD_STR='MOD'
NOT_STR='NOT'
NULL_STR='NULL'
ON_STR='ON'
ORDER_STR='ORDER'
OR_STR='OR'
RIGHT_STR='RIGHT'
SELECT_STR='SELECT'
SET_STR='SET'
SHOW_STR='SHOW'
TABLE_STR='TABLE'
TRUE_STR='TRUE'
UNION_STR='UNION'
UNIQUE_STR='UNIQUE'
UPDATE_STR='UPDATE'
VALUES_STR='VALUES'
WHERE_STR='WHERE'
XOR_STR='XOR'

# KEYWORD

DATE_STR='DATE'
DATETIME_STR='DATETIME'
FULL_STR='FULL'

# OPERATOR

NULL_SAFE_EQUALS_STR='<=>'
PLUS_EQUALS_STR='+='
MINUS_EQUALS_STR='-='
MULTIPLY_EQUALS_STR='*='
DIVIDE_EQUALS_STR='/='
MODULUS_EQUALS_STR='%='
GREATER_THAN_EQUALS_STR='>='
LESS_THAN_EQUALS_STR='<='
EQUALS_STR='=='
NOT_EQUALS_STR='!='
NOT_EQUALS_STR='<>'
OR_EQUALS_STR='|='
AND_EQUALS_STR='&='
XOR_EQUALS_STR='^='
SET_STR='=:'
SHORT_CIRCUIT_OR_STR='||'
SHORT_CIRCUIT_AND_STR='&&'
BITWISE_LEFT_STR='<<'
BITWISE_RIGHT_STR='>>'
BITWISE_INVERSION_STR='~'
PLUS_STR='+'
MINUS_STR='-'
MULTIPLY_STR='*'
DIVIDE_STR='/'
MODULUS_STR='%'
GREATER_THAN_STR='>'
LESS_THAN_STR='<'
ASIGN_STR='='
NEGATE_STR='!'
OR_STR='|'
AND_STR='&'
XOR_STR='^'

# Numeric

ZERO_STR='0'
ONE_STR='1'
TWO_STR='2'
THREE_STR='3'
FOUR_STR='4'
FIVE_STR='5'
SIX_STR='6'
SEVEN_STR='7'
EIGHT_STR='8'
NINE_STR='9'

# Alpha

a_STR='a'
b_STR='b'
c_STR='c'
d_STR='d'
e_STR='e'
f_STR='f'
g_STR='g'
h_STR='h'
i_STR='i'
j_STR='j'
k_STR='k'
l_STR='l'
m_STR='m'
n_STR='n'
o_STR='o'
p_STR='p'
q_STR='q'
r_STR='r'
s_STR='s'
t_STR='t'
u_STR='u'
v_STR='v'
w_STR='w'
x_STR='x'
y_STR='y'
z_STR='z'
A_STR='A'
B_STR='B'
C_STR='C'
D_STR='D'
E_STR='E'
F_STR='F'
G_STR='G'
H_STR='H'
I_STR='I'
J_STR='J'
K_STR='K'
L_STR='L'
M_STR='M'
N_STR='N'
O_STR='O'
P_STR='P'
Q_STR='Q'
R_STR='R'
S_STR='S'
T_STR='T'
U_STR='U'
V_STR='V'
W_STR='W'
X_STR='X'
Y_STR='Y'
Z_STR='Z'

# Delimiter

NEW_LINE_STR='\n'
TAB_STR='\t'
SPACE_STR=' '
COMMA_STR=','
PERIOD_STR='.'
DOLLAR_STR='$'
UNDERSCORE_STR='_'

#
# Code
#


def get_intermediate_code_2(text):
    if text==None: return 0
    text=text.upper()
    text_length=len(text)
    text_hash=hash(text)
    if   text=='': return 0 

    
    if   text_length==9:
        if   text_hash==2287436798404490839: return 2008
    elif text_length==8:
        if   text_hash==-3335509522698720921: return 2007
        elif text_hash==-4427568144388930392: return 2010
        elif text_hash==-6213914849266237361: return 3001
    elif text_length==7:
        if   text_hash==8422106668497960279: return 2004
    elif text_length==6:
        if   text_hash==5788341079899903583: return 2003
        elif text_hash==-2860899356599532118: return 2006
        elif text_hash==-6797446220009517626: return 2012
        elif text_hash==-1438505323107606634: return 2016
        elif text_hash==7813825114794786301: return 2017
        elif text_hash==-2667667377094072927: return 2019
        elif text_hash==-3655737310966507362: return 2033
        elif text_hash==2935381317924681307: return 2039
        elif text_hash==821116054469991117: return 2040
        elif text_hash==-8657821113436651404: return 2041
    elif text_length==5:
        if   text_hash==-426319011301440668: return 2013
        elif text_hash==2788289350344119428: return 2015
        elif text_hash==-5509471285393800684: return 2025
        elif text_hash==5046430602683938333: return 2030
        elif text_hash==-145964486211609629: return 2032
        elif text_hash==-6358197886813880007: return 2036
        elif text_hash==-3143589525201319736: return 2038
        elif text_hash==3323618512992715868: return 2042
    elif text_length==4:
        if   text_hash==5809132768366327263: return 2009
        elif text_hash==5809153768506327339: return 2011
        elif text_hash==-4328498044256676892: return 2014
        elif text_hash==8135334348070144970: return 2020
        elif text_hash==-6156980596043134620: return 2022
        elif text_hash==2152157665154412863: return 2023
        elif text_hash==2152169665101412709: return 2024
        elif text_hash==-7985434147538591845: return 2028
        elif text_hash==-5659258567968774201: return 2035
        elif text_hash==-1504828438253501924: return 2037
        elif text_hash==5809136768421327256: return 3000
        elif text_hash==-4328491044353677245: return 3002
    elif text_length==3:
        if   text_hash==593367982096446688: return 2000
        elif text_hash==593367982099446576: return 2001
        elif text_hash==5527445905738704127: return 2026
        elif text_hash==4401390393099845880: return 2027
        elif text_hash==-1228887169288443101: return 2034
        elif text_hash==-6859164731816732220: return 2043
        elif text_hash==6223645544503735526: return 4000
    elif text_length==2:
        if   text_hash==8320049985075154: return 2002
        elif text_hash==8448050754076189: return 2005
        elif text_hash==9344056137084375: return 2018
        elif text_hash==9344056137084362: return 2021
        elif text_hash==10112060751091297: return 2029
        elif text_hash==10112060751091325: return 2031
        elif text_hash==6016036143054309: return 1003
        elif text_hash==5376032298048467: return 1004
        elif text_hash==5760034605052008: return 1005
        elif text_hash==5504033067049726: return 4001
        elif text_hash==5760034605052024: return 4002
        elif text_hash==5376032298048449: return 4003
        elif text_hash==6016036143054322: return 4004
        elif text_hash==4736028453042704: return 4005
        elif text_hash==7936047678071557: return 4006
        elif text_hash==7680046140069259: return 4007
        elif text_hash==7808046909070408: return 4008
        elif text_hash==4224025377038108: return 4009
        elif text_hash==7680046140069256: return 4010
        elif text_hash==15872095356143179: return 4011
        elif text_hash==4864029222043853: return 4012
        elif text_hash==12032072286108581: return 4013
        elif text_hash==7808046909070415: return 4014
        elif text_hash==15872095356143114: return 4015
        elif text_hash==4864029222043862: return 4016
        elif text_hash==7680046140069258: return 4017
        elif text_hash==7936047678071558: return 4018
    elif text_length==1:
        if   text_hash==1280003851: return 7000
        elif text_hash==1152003464: return 7001
        elif text_hash==4096012321: return 7002
        elif text_hash==5632016941: return 7003
        elif text_hash==5888017711: return 7004
        elif text_hash==4608013861: return 7005
        elif text_hash==12160036574: return 7006
        elif text_hash==4352013091: return 1000
        elif text_hash==4992015014: return 1001
        elif text_hash==12288036961: return 1002
        elif text_hash==5120015401: return 1006
        elif text_hash==5248015784: return 1007
        elif text_hash==16128048511: return 4019
        elif text_hash==5504016554: return 4020
        elif text_hash==5760017324: return 4021
        elif text_hash==5376016171: return 4022
        elif text_hash==6016018094: return 4023
        elif text_hash==4736014244: return 4024
        elif text_hash==7936023871: return 4025
        elif text_hash==7680023101: return 4026
        elif text_hash==7808023484: return 4027
        elif text_hash==4224012704: return 4028
        elif text_hash==15872047741: return 4029
        elif text_hash==4864014631: return 4030
        elif text_hash==12032036191: return 4031
    return 0

def get_intermediate_code_3(text):
    if text==None: return 0
    text=text.upper()
    text_length=len(text)
    text_hash=hash(text)
    if   text=='': return 0 

    
    if   text_length==9:
        if   text=='DATABASES': return 2008
    elif text_length==8:
        if   text=='DATABASE': return 2007
        elif text=='DISTINCT': return 2010
        elif text=='DATETIME': return 3001
    elif text_length==7:
        if   text=='BETWEEN': return 2004
    elif text_length==6:
        if   text=='BEFORE': return 2003
        elif text=='CREATE': return 2006
        elif text=='EXISTS': return 2012
        elif text=='GROUPS': return 2016
        elif text=='HAVING': return 2017
        elif text=='INSERT': return 2019
        elif text=='SELECT': return 2033
        elif text=='UNIQUE': return 2039
        elif text=='UPDATE': return 2040
        elif text=='VALUES': return 2041
    elif text_length==5:
        if   text=='FALSE': return 2013
        elif text=='GROUP': return 2015
        elif text=='LIMIT': return 2025
        elif text=='ORDER': return 2030
        elif text=='RIGHT': return 2032
        elif text=='TABLE': return 2036
        elif text=='UNION': return 2038
        elif text=='WHERE': return 2042
    elif text_length==4:
        if   text=='DESC': return 2009
        elif text=='DROP': return 2011
        elif text=='FROM': return 2014
        elif text=='INTO': return 2020
        elif text=='JOIN': return 2022
        elif text=='LEFT': return 2023
        elif text=='LIKE': return 2024
        elif text=='NULL': return 2028
        elif text=='SHOW': return 2035
        elif text=='TRUE': return 2037
        elif text=='DATE': return 3000
        elif text=='FULL': return 3002
    elif text_length==3:
        if   text=='AND': return 2000
        elif text=='ASC': return 2001
        elif text=='MOD': return 2026
        elif text=='NOT': return 2027
        elif text=='SET': return 2034
        elif text=='XOR': return 2043
        elif text=='<=>': return 4000
    elif text_length==2:
        if   text=='AS': return 2002
        elif text=='BY': return 2005
        elif text=='IN': return 2018
        elif text=='IS': return 2021
        elif text=='ON': return 2029
        elif text=='OR': return 2031
        elif text=='/*': return 1003
        elif text=='*/': return 1004
        elif text=='--': return 1005
        elif text=='+=': return 4001
        elif text=='-=': return 4002
        elif text=='*=': return 4003
        elif text=='/=': return 4004
        elif text=='%=': return 4005
        elif text=='>=': return 4006
        elif text=='<=': return 4007
        elif text=='==': return 4008
        elif text=='!=': return 4009
        elif text=='<>': return 4010
        elif text=='|=': return 4011
        elif text=='&=': return 4012
        elif text=='^=': return 4013
        elif text=='=:': return 4014
        elif text=='||': return 4015
        elif text=='&&': return 4016
        elif text=='<<': return 4017
        elif text=='>>': return 4018
    elif text_length==1:
        if   text=='\n': return 7000
        elif text=='\t': return 7001
        elif text==' ': return 7002
        elif text==',': return 7003
        elif text=='.': return 7004
        elif text=='$': return 7005
        elif text=='_': return 7006
        elif text=='"': return 1000
        elif text=="'": return 1001
        elif text=='`': return 1002
        elif text=='(': return 1006
        elif text==')': return 1007
        elif text=='~': return 4019
        elif text=='+': return 4020
        elif text=='-': return 4021
        elif text=='*': return 4022
        elif text=='/': return 4023
        elif text=='%': return 4024
        elif text=='>': return 4025
        elif text=='<': return 4026
        elif text=='=': return 4027
        elif text=='!': return 4028
        elif text=='|': return 4029
        elif text=='&': return 4030
        elif text=='^': return 4031
    return 0

def add_fragment(fragment,fragment_length,bulk=None,depth=0):
    new_fragments=[]
    if bulk:
        if fragment!="":
            new_fragments.append([fragment,0,depth])
    else:
        if fragment!="":
            right_fragment=""
            right_fragment_length=0
    
            while fragment_length>0:
                found=0
                for length in range(fragment_length,0,-1):
                    code=get_intermediate_code_2(fragment[:length])
                    if code!=0:
                        found=True
                        if code==SPACE or code==TAB or code==NEW_LINE:
                            pass
                        else:
                            new_fragments.append([fragment[:length],code,depth])
                        fragment_length-=length
                        if fragment_length>0:
                            fragment=fragment[length:]
                        break;
                
                # if we looped through all length combiniations and found nothing, add the remainder and shrink the stack
                if found==0:
                    new_fragments.append([fragment[0],0,depth])
                    fragment_length-=1
                    if fragment_length>0:
                        fragment=fragment[1:]
    return new_fragments
   

def get_BYTECODE(data,depth=0):
    #print data
    fragments=[]
    fragment=""
    fragment_length=0
 
    in_block=None
    in_alpha=None
    block_depth=0

    # main loop for tokenizing
    for c in data:
        if in_block:
            in_alpha=None
            # is it the other side of the block
            if c==LEFT_PAREN_STR:      
                block_depth+=1
                fragment+=c
                fragment_length+=1
                continue

            if c==in_block:
                
                if in_block==RIGHT_PAREN_STR:
                    #print block_depth
                    block_depth-=1
                    if block_depth!=0:
                        fragment+=c
                        fragment_length+=1
                        continue
                    pass
                    sub_code=get_BYTECODE(fragment,depth+1)
                    fragments+=sub_code
                else:
                    fragments+=add_fragment(fragment,fragment_length,True,depth)
                fragment=""
                fragment_length=0
                in_block=None
                #block_depth=0
            # no, add the contents
            else:
                fragment+=c
                fragment_length+=1
        else:
            # self closing
            if   c==DOUBLE_QUOTE_STR:    in_block=DOUBLE_QUOTE_STR
            elif c==SINGLE_QUOTE_STR:    in_block=SINGLE_QUOTE_STR
            elif c==BACK_TIC_STR:        in_block=BACK_TIC_STR
            
            # matched pair
            elif c==LEFT_COMMENT_STR:    in_block=RIGHT_COMMENT_STR
            elif c==COMMENT_SINGLE_STR:  in_block=NEW_LINE_STR
            elif c==LEFT_PAREN_STR:      
                in_block=RIGHT_PAREN_STR
                
                block_depth+=1
                
                
    
            if in_block:
                fragments+=add_fragment(fragment,fragment_length,None,depth)
                fragment=""
                fragment_length=0
                continue
            
    
            #not a block, or anything else
            else:
                # is this the start of an "WORD"
                if in_alpha==None:
                    if ( c>=A_STR and c<=Z_STR ) or ( c>=a_STR and c<=z_STR ) or ( c>=ZERO_STR and c<=NINE_STR ) or c== UNDERSCORE_STR or c==DOLLAR_STR:
                        fragments+=add_fragment(fragment,fragment_length,None,depth)
                        fragment=c
                        fragment_length=1
                        in_alpha=True

                    # not in a word, none word zone stuff..
                    else:
                        fragment+=c
                        fragment_length+=1

                # Are we in a "WORD"
                else:
                    # If we just LEFT ... add the existing word, and start a new one
                    if not ( c>=A_STR and c<=Z_STR ) and  not ( c>=a_STR and c<=z_STR ) and not ( c>=ZERO_STR and c<=NINE_STR ) and c!=UNDERSCORE_STR and  c!=DOLLAR_STR:
                        fragments+=add_fragment(fragment,fragment_length,True,depth)
                        fragment=c
                        fragment_length=1
                        in_alpha=None

                    # IF SO append
                    else:
                        fragment+=c
                        fragment_length+=1

    # END Loop                
    
    # if anything is still left in the pipeline, cleanup
    
    fragments+=add_fragment(fragment,fragment_length,in_alpha,depth)
    fragment=""
    fragment_length=0


    # err if block mismatch
    if in_block:
        err_msg="Missing {0}".format(in_block)
        raise Exception(err_msg)
    
    # reduce groups that are single elements
    
    
    #while len(fragments)==1:
        #print fragments
        #eif isinstance(fragments,dict):
        #    fragments=fragments['sub']
    #    print fragments
    #    return fragments
    
    return [{"sub":fragments}]
   

def print_code(codes,root=True):
    
    if isinstance(codes,list):
        for code in codes:
            if isinstance(code,dict):
                print_code(code['sub'],None)
            elif isinstance(code,list):
                for i in range(code[2]):
                    print " " , 
                print(code)
    

def test(debug=None):
    codes=get_BYTECODE("SELECT * FROM (PIZ (((o ber )) && == ZAZ) )(hh.'hh')  (f) 'db blah 432%^$#@'.\"rfdsf table\" where  && || | >= == &&& === this=that and that not 5")
    if debug: print_code(codes) 


#print(timeit.timeit(test, number=10))

test(True)


