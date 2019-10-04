import timeit

### ----                                     ----
### ddb BYTECODE LANGUAGE DEFINITIONS
### ----                                     ----
### Automagically generated, dont mess with this.
### ----  or you will be eaten by unicorns   ----
### ----                                     ----

# each word is given an integer value based on section, sections increment based on SECTION BLOCK_VALUE

# R=Reserved word
# K=Key word
# B=Block    such as comment, text or code
# O=Operator
# D=Delimiter
# A=Alpha
# N=Numeric
# comparisons are ordered to be done in greatest length order, to prevent uneven length but similar values
# this also doubles as a speed enhancement



class bytecode:

    
    ##
    ## Integer Values
    ##
    
    
    # BLOCK
    
    DOUBLE_QUOTE=0x03E8
    SINGLE_QUOTE=0x03E9
    BACK_TIC=0x03EA
    LEFT_COMMENT=0x03EB
    RIGHT_COMMENT=0x03EC
    COMMENT_SINGLE=0x03ED
    LEFT_PAREN=0x03EE
    RIGHT_PAREN=0x03EF
    
    # RESERVED WORD
    
    AND=0x07D0
    ASC=0x07D1
    AS=0x07D2
    BEFORE=0x07D3
    BETWEEN=0x07D4
    BY=0x07D5
    CREATE=0x07D6
    DATABASE=0x07D7
    DATABASES=0x07D8
    DESC=0x07D9
    DISTINCT=0x07DA
    DROP=0x07DB
    EXISTS=0x07DC
    FALSE=0x07DD
    FROM=0x07DE
    GROUP=0x07DF
    GROUPS=0x07E0
    HAVING=0x07E1
    IN=0x07E2
    INSERT=0x07E3
    INTO=0x07E4
    IS=0x07E5
    JOIN=0x07E6
    LEFT=0x07E7
    LIKE=0x07E8
    LIMIT=0x07E9
    MOD=0x07EA
    NOT=0x07EB
    NULL=0x07EC
    ON=0x07ED
    ORDER=0x07EE
    OR=0x07EF
    RIGHT=0x07F0
    SELECT=0x07F1
    SET=0x07F2
    SHOW=0x07F3
    TABLE=0x07F4
    TRUE=0x07F5
    UNION=0x07F6
    UNIQUE=0x07F7
    UPDATE=0x07F8
    VALUES=0x07F9
    WHERE=0x07FA
    XOR=0x07FB
    
    # KEYWORD
    
    DATE=0x0BB8
    DATETIME=0x0BB9
    FULL=0x0BBA
    
    # OPERATOR
    
    NULL_SAFE_EQUALS=0x0FA0
    PLUS_EQUALS=0x0FA1
    MINUS_EQUALS=0x0FA2
    MULTIPLY_EQUALS=0x0FA3
    DIVIDE_EQUALS=0x0FA4
    MODULUS_EQUALS=0x0FA5
    GREATER_THAN_EQUALS=0x0FA6
    LESS_THAN_EQUALS=0x0FA7
    EQUALS=0x0FA8
    NOT_EQUALS=0x0FA9
    NOT_EQUALS=0x0FAA
    OR_EQUALS=0x0FAB
    AND_EQUALS=0x0FAC
    XOR_EQUALS=0x0FAD
    SET=0x0FAE
    SHORT_CIRCUIT_OR=0x0FAF
    SHORT_CIRCUIT_AND=0x0FB0
    BITWISE_LEFT=0x0FB1
    BITWISE_RIGHT=0x0FB2
    BITWISE_INVERSION=0x0FB3
    PLUS=0x0FB4
    MINUS=0x0FB5
    MULTIPLY=0x0FB6
    DIVIDE=0x0FB7
    MODULUS=0x0FB8
    GREATER_THAN=0x0FB9
    LESS_THAN=0x0FBA
    ASIGN=0x0FBB
    NEGATE=0x0FBC
    OR=0x0FBD
    AND=0x0FBE
    XOR=0x0FBF
    
    # Numeric
    
    ZERO=0x1388
    ONE=0x1389
    TWO=0x138A
    THREE=0x138B
    FOUR=0x138C
    FIVE=0x138D
    SIX=0x138E
    SEVEN=0x138F
    EIGHT=0x1390
    NINE=0x1391
    
    # Alpha
    
    a=0x1770
    b=0x1771
    c=0x1772
    d=0x1773
    e=0x1774
    f=0x1775
    g=0x1776
    h=0x1777
    i=0x1778
    j=0x1779
    k=0x177A
    l=0x177B
    m=0x177C
    n=0x177D
    o=0x177E
    p=0x177F
    q=0x1780
    r=0x1781
    s=0x1782
    t=0x1783
    u=0x1784
    v=0x1785
    w=0x1786
    x=0x1787
    y=0x1788
    z=0x1789
    A=0x178A
    B=0x178B
    C=0x178C
    D=0x178D
    E=0x178E
    F=0x178F
    G=0x1790
    H=0x1791
    I=0x1792
    J=0x1793
    K=0x1794
    L=0x1795
    M=0x1796
    N=0x1797
    O=0x1798
    P=0x1799
    Q=0x179A
    R=0x179B
    S=0x179C
    T=0x179D
    U=0x179E
    V=0x179F
    W=0x17A0
    X=0x17A1
    Y=0x17A2
    Z=0x17A3
    
    # Delimiter
    
    NEW_LINE=0x1B58
    TAB=0x1B59
    SPACE=0x1B5A
    COMMA=0x1B5B
    PERIOD=0x1B5C
    DOLLAR=0x1B5D
    UNDERSCORE=0x1B5E
    
    ##
    ## String Values
    ##
    
    
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


    @staticmethod
    def get_intermediate_code_2(text):
        if text==None: return 0
        text=text.upper()
        text_length=len(text)
        text_hash=hash(text)
        if   text=='': 
            return 0 
        if   text_length==9:
            if   text_hash==2287436798404490839: return 0x07D8
        elif text_length==8:
            if   text_hash==-3335509522698720921: return 0x07D7
            elif text_hash==-4427568144388930392: return 0x07DA
            elif text_hash==-6213914849266237361: return 0x0BB9
        elif text_length==7:
            if   text_hash==8422106668497960279: return 0x07D4
        elif text_length==6:
            if   text_hash==5788341079899903583: return 0x07D3
            elif text_hash==-2860899356599532118: return 0x07D6
            elif text_hash==-6797446220009517626: return 0x07DC
            elif text_hash==-1438505323107606634: return 0x07E0
            elif text_hash==7813825114794786301: return 0x07E1
            elif text_hash==-2667667377094072927: return 0x07E3
            elif text_hash==-3655737310966507362: return 0x07F1
            elif text_hash==2935381317924681307: return 0x07F7
            elif text_hash==821116054469991117: return 0x07F8
            elif text_hash==-8657821113436651404: return 0x07F9
        elif text_length==5:
            if   text_hash==-426319011301440668: return 0x07DD
            elif text_hash==2788289350344119428: return 0x07DF
            elif text_hash==-5509471285393800684: return 0x07E9
            elif text_hash==5046430602683938333: return 0x07EE
            elif text_hash==-145964486211609629: return 0x07F0
            elif text_hash==-6358197886813880007: return 0x07F4
            elif text_hash==-3143589525201319736: return 0x07F6
            elif text_hash==3323618512992715868: return 0x07FA
        elif text_length==4:
            if   text_hash==5809132768366327263: return 0x07D9
            elif text_hash==5809153768506327339: return 0x07DB
            elif text_hash==-4328498044256676892: return 0x07DE
            elif text_hash==8135334348070144970: return 0x07E4
            elif text_hash==-6156980596043134620: return 0x07E6
            elif text_hash==2152157665154412863: return 0x07E7
            elif text_hash==2152169665101412709: return 0x07E8
            elif text_hash==-7985434147538591845: return 0x07EC
            elif text_hash==-5659258567968774201: return 0x07F3
            elif text_hash==-1504828438253501924: return 0x07F5
            elif text_hash==5809136768421327256: return 0x0BB8
            elif text_hash==-4328491044353677245: return 0x0BBA
        elif text_length==3:
            if   text_hash==593367982096446688: return 0x07D0
            elif text_hash==593367982099446576: return 0x07D1
            elif text_hash==5527445905738704127: return 0x07EA
            elif text_hash==4401390393099845880: return 0x07EB
            elif text_hash==-1228887169288443101: return 0x07F2
            elif text_hash==-6859164731816732220: return 0x07FB
            elif text_hash==6223645544503735526: return 0x0FA0
        elif text_length==2:
            if   text_hash==8320049985075154: return 0x07D2
            elif text_hash==8448050754076189: return 0x07D5
            elif text_hash==9344056137084375: return 0x07E2
            elif text_hash==9344056137084362: return 0x07E5
            elif text_hash==10112060751091297: return 0x07ED
            elif text_hash==10112060751091325: return 0x07EF
            elif text_hash==6016036143054309: return 0x03EB
            elif text_hash==5376032298048467: return 0x03EC
            elif text_hash==5760034605052008: return 0x03ED
            elif text_hash==5504033067049726: return 0x0FA1
            elif text_hash==5760034605052024: return 0x0FA2
            elif text_hash==5376032298048449: return 0x0FA3
            elif text_hash==6016036143054322: return 0x0FA4
            elif text_hash==4736028453042704: return 0x0FA5
            elif text_hash==7936047678071557: return 0x0FA6
            elif text_hash==7680046140069259: return 0x0FA7
            elif text_hash==7808046909070408: return 0x0FA8
            elif text_hash==4224025377038108: return 0x0FA9
            elif text_hash==7680046140069256: return 0x0FAA
            elif text_hash==15872095356143179: return 0x0FAB
            elif text_hash==4864029222043853: return 0x0FAC
            elif text_hash==12032072286108581: return 0x0FAD
            elif text_hash==7808046909070415: return 0x0FAE
            elif text_hash==15872095356143114: return 0x0FAF
            elif text_hash==4864029222043862: return 0x0FB0
            elif text_hash==7680046140069258: return 0x0FB1
            elif text_hash==7936047678071558: return 0x0FB2
        elif text_length==1:
            if   text_hash==1280003851: return 0x1B58
            elif text_hash==1152003464: return 0x1B59
            elif text_hash==4096012321: return 0x1B5A
            elif text_hash==5632016941: return 0x1B5B
            elif text_hash==5888017711: return 0x1B5C
            elif text_hash==4608013861: return 0x1B5D
            elif text_hash==12160036574: return 0x1B5E
            elif text_hash==4352013091: return 0x03E8
            elif text_hash==4992015014: return 0x03E9
            elif text_hash==12288036961: return 0x03EA
            elif text_hash==5120015401: return 0x03EE
            elif text_hash==5248015784: return 0x03EF
            elif text_hash==16128048511: return 0x0FB3
            elif text_hash==5504016554: return 0x0FB4
            elif text_hash==5760017324: return 0x0FB5
            elif text_hash==5376016171: return 0x0FB6
            elif text_hash==6016018094: return 0x0FB7
            elif text_hash==4736014244: return 0x0FB8
            elif text_hash==7936023871: return 0x0FB9
            elif text_hash==7680023101: return 0x0FBA
            elif text_hash==7808023484: return 0x0FBB
            elif text_hash==4224012704: return 0x0FBC
            elif text_hash==15872047741: return 0x0FBD
            elif text_hash==4864014631: return 0x0FBE
            elif text_hash==12032036191: return 0x0FBF

        return 0


    @staticmethod
    def get_intermediate_code_3(text):
        if text==None: return 0
        text=text.upper()
        text_length=len(text)
        text_hash=hash(text)
        if   text=='': 
            return 0 
        if   text_length==9:
            if   text=='DATABASES': return 0x07D8
        elif text_length==8:
            if   text=='DATABASE': return 0x07D7
            elif text=='DISTINCT': return 0x07DA
            elif text=='DATETIME': return 0x0BB9
        elif text_length==7:
            if   text=='BETWEEN': return 0x07D4
        elif text_length==6:
            if   text=='BEFORE': return 0x07D3
            elif text=='CREATE': return 0x07D6
            elif text=='EXISTS': return 0x07DC
            elif text=='GROUPS': return 0x07E0
            elif text=='HAVING': return 0x07E1
            elif text=='INSERT': return 0x07E3
            elif text=='SELECT': return 0x07F1
            elif text=='UNIQUE': return 0x07F7
            elif text=='UPDATE': return 0x07F8
            elif text=='VALUES': return 0x07F9
        elif text_length==5:
            if   text=='FALSE': return 0x07DD
            elif text=='GROUP': return 0x07DF
            elif text=='LIMIT': return 0x07E9
            elif text=='ORDER': return 0x07EE
            elif text=='RIGHT': return 0x07F0
            elif text=='TABLE': return 0x07F4
            elif text=='UNION': return 0x07F6
            elif text=='WHERE': return 0x07FA
        elif text_length==4:
            if   text=='DESC': return 0x07D9
            elif text=='DROP': return 0x07DB
            elif text=='FROM': return 0x07DE
            elif text=='INTO': return 0x07E4
            elif text=='JOIN': return 0x07E6
            elif text=='LEFT': return 0x07E7
            elif text=='LIKE': return 0x07E8
            elif text=='NULL': return 0x07EC
            elif text=='SHOW': return 0x07F3
            elif text=='TRUE': return 0x07F5
            elif text=='DATE': return 0x0BB8
            elif text=='FULL': return 0x0BBA
        elif text_length==3:
            if   text=='AND': return 0x07D0
            elif text=='ASC': return 0x07D1
            elif text=='MOD': return 0x07EA
            elif text=='NOT': return 0x07EB
            elif text=='SET': return 0x07F2
            elif text=='XOR': return 0x07FB
            elif text=='<=>': return 0x0FA0
        elif text_length==2:
            if   text=='AS': return 0x07D2
            elif text=='BY': return 0x07D5
            elif text=='IN': return 0x07E2
            elif text=='IS': return 0x07E5
            elif text=='ON': return 0x07ED
            elif text=='OR': return 0x07EF
            elif text=='/*': return 0x03EB
            elif text=='*/': return 0x03EC
            elif text=='--': return 0x03ED
            elif text=='+=': return 0x0FA1
            elif text=='-=': return 0x0FA2
            elif text=='*=': return 0x0FA3
            elif text=='/=': return 0x0FA4
            elif text=='%=': return 0x0FA5
            elif text=='>=': return 0x0FA6
            elif text=='<=': return 0x0FA7
            elif text=='==': return 0x0FA8
            elif text=='!=': return 0x0FA9
            elif text=='<>': return 0x0FAA
            elif text=='|=': return 0x0FAB
            elif text=='&=': return 0x0FAC
            elif text=='^=': return 0x0FAD
            elif text=='=:': return 0x0FAE
            elif text=='||': return 0x0FAF
            elif text=='&&': return 0x0FB0
            elif text=='<<': return 0x0FB1
            elif text=='>>': return 0x0FB2
        elif text_length==1:
            if   text=='\n': return 0x1B58
            elif text=='\t': return 0x1B59
            elif text==' ': return 0x1B5A
            elif text==',': return 0x1B5B
            elif text=='.': return 0x1B5C
            elif text=='$': return 0x1B5D
            elif text=='_': return 0x1B5E
            elif text=='"': return 0x03E8
            elif text=="'": return 0x03E9
            elif text=='`': return 0x03EA
            elif text=='(': return 0x03EE
            elif text==')': return 0x03EF
            elif text=='~': return 0x0FB3
            elif text=='+': return 0x0FB4
            elif text=='-': return 0x0FB5
            elif text=='*': return 0x0FB6
            elif text=='/': return 0x0FB7
            elif text=='%': return 0x0FB8
            elif text=='>': return 0x0FB9
            elif text=='<': return 0x0FBA
            elif text=='=': return 0x0FBB
            elif text=='!': return 0x0FBC
            elif text=='|': return 0x0FBD
            elif text=='&': return 0x0FBE
            elif text=='^': return 0x0FBF

        return 0



    @staticmethod
    def add_fragment(fragment,fragment_length,uid,fragment_id,bulk=None,depth=0):
        new_fragments=[]
        if bulk:
            if fragment!="":
                new_fragments.append([fragment,0,depth,uid,fragment_id])
        else:
            if fragment!="":
                right_fragment=""
                right_fragment_length=0
        
                while fragment_length>0:
                    found=None
                    for length in xrange(fragment_length,0,-1):
                        code=bytecode.get_intermediate_code_2(fragment[:length])
                        if code!=0:
                            found=True
                            if code==bytecode.SPACE or code==bytecode.TAB or code==bytecode.NEW_LINE or code==bytecode.COMMA:
                                pass
                            else:
                                new_fragments.append([fragment[:length],code,depth,uid,fragment_id])
                            fragment_length-=length
                            if fragment_length>0:
                                fragment=fragment[length:]
                            break;
                    
                    # if we looped through all length combiniations and found nothing, add the remainder and shrink the stack
                    if found==None:
                        new_fragments.append([fragment[0],0,depth,uid,fragment_id])
                        fragment_length-=1
                        if fragment_length>0:
                            fragment=fragment[1:]
        
        return new_fragments
   
    @staticmethod
    def get_BYTECODE(data,depth=0,uid="1"):
        fragments=[]
        fragment=""
        fragment_length=0
        in_block=None
        in_alpha=None
        block_depth=0
        fragment_id=1
        # main loop for tokenizing
        for c in data:
            
            if in_block:
                in_alpha=None
                # is it the other side of the block
                if c==bytecode.LEFT_PAREN_STR:      
                    block_depth+=1
                    fragment+=c
                    fragment_length+=1
                    continue
    
                if c==in_block:
                    
                    if in_block==bytecode.RIGHT_PAREN_STR:
                        block_depth-=1
                        if block_depth!=0:
                            fragment+=c
                            fragment_length+=1
                            continue

                        sub_code=bytecode.get_BYTECODE(fragment,depth+1,"{0}.{1}".format(uid,fragment_id))
                        fragments+=sub_code
                    else:
                        fragment_id+=1
                        fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,True,depth)
                    fragment=""
                    fragment_length=0
                    in_block=None
                # no, add the contents
                else:
                    fragment+=c
                    fragment_length+=1
            else:
                # self closing
                if   c==bytecode.DOUBLE_QUOTE_STR:    in_block=bytecode.DOUBLE_QUOTE_STR
                elif c==bytecode.SINGLE_QUOTE_STR:    in_block=bytecode.SINGLE_QUOTE_STR
                elif c==bytecode.BACK_TIC_STR:        in_block=bytecode.BACK_TIC_STR
                
                # matched pair
                elif c==bytecode.LEFT_COMMENT_STR:    in_block=bytecode.RIGHT_COMMENT_STR
                elif c==bytecode.COMMENT_SINGLE_STR:  in_block=bytecode.NEW_LINE_STR
                elif c==bytecode.LEFT_PAREN_STR:      
                    in_block=bytecode.RIGHT_PAREN_STR
                    block_depth+=1
        
                if in_block:
                    fragment_id+=1
                    fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,None,depth)
                    fragment=""
                    fragment_length=0
                    continue
                    
                #not a block, or anything else
                else:
                    # is this the start of an "WORD"
                    u_alpha   =c>=bytecode.A_STR and c<=bytecode.Z_STR
                    l_alpha   =c>=bytecode.a_STR and c<=bytecode.z_STR 
                    numeric   =c>=bytecode.ZERO_STR and c<=bytecode.NINE_STR
                    underscore=c==bytecode.UNDERSCORE_STR 
                    dollar    =c==bytecode.DOLLAR_STR

                    if in_alpha==None:
                        if u_alpha or l_alpha or numeric or underscore or dollar:
                            fragment_id+=1
                            fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,in_alpha,depth)
                            fragment=c
                            fragment_length=1
                            in_alpha=True
                            continue    
    
                    # Are we in a "WORD"
                    else:
                        # If we just LEFT ... add the existing word, and start a new one
                        if not u_alpha and not l_alpha and not numeric and not underscore and not dollar:
                            fragment_id+=1
                            fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,True,depth)
                            fragment=c
                            fragment_length=1
                            in_alpha=None
                            continue    

                    # fallthrough
                    fragment+=c
                    fragment_length+=1

        # END Loop                
        # if anything is still left in the pipeline, cleanup
        
        fragment_id+=1
        fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,in_alpha,depth)
        fragment=""
        fragment_length=0
    
    
        # err if block mismatch
        if in_block:
            err_msg="Missing {0}".format(in_block)
            raise Exception(err_msg)
        
        # reduce groups that are single elements
        #while len(fragments)==1:
        #    print fragments
        #    elif isinstance(fragments,dict):
        #        fragments=fragments['sub']
        #    print fragments
        #    return fragments
        
        return [{"sub":fragments}]

    @staticmethod
    def print_code(codes,root=True):
        if root: print("Token                | Code   | Depth | UID         | Fragment ID ")
        if root: print("---------------------+--------+-------+-------------+-------------")
        if isinstance(codes,list):
            for code in codes:
                if isinstance(code,dict):
                    bytecode.print_code(code['sub'],None)
                elif isinstance(code,list):
                    #for i in range(code[2]):
                    #    print " " , 
                    print("{0:20} | 0x{1:04X} | {2}     | {3:10}  | {4}".format(code[0],code[1],code[2],code[3],code[4]))

    
##
## End bytecode class
##

def test(debug=None):
    query="""SELECT * FROM test.mock WHERE first_name='bob' and last_name not 'sam' and gender=F and last_name in (sam,bob,pizza,chicken) 
        """
    codes=bytecode.get_BYTECODE(query)
    if debug: bytecode.print_code(codes) 


#print(timeit.timeit(test, number=10))

test(True)
