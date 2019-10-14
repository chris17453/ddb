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
    TOKEN_TYPE_FIELD        = 10
    TOKEN_TYPE_BLOCK_STRING = 20
    TOKEN_TYPE_STRING       = 30
    TOKEN_TYPE_COMMENT      = 40
    TOKEN_TYPE_WHITESPACE   = 50
    TOKEN_TYPE_EXPRESSION   = 60
    TOKEN_TYPE_OTHER        = 70
    TOKEN_TYPE_KEYWORD      = 80
    TOKEN_TYPE_RESERVED     = 90
    TOKEN_TYPE_NUMERIC      = 100
    TOKEN_TYPE_OPERATOR     = 110
    TOKEN_TYPE_DELIMITER    = 120
    TOKEN_TYPE_FUNCTION     = 130

    ERROR_RESERVERD_WORD_REQUIRES_IDENTIFYER = 10
    ERROR_INVALID_IDENTIFYER_TYPE            = 20

    IGNORE_WHITESPACE       =True
    IGNORE_COMMENTS         =True

    BLOCK_START     =1000
    BLOCK_END       =1999
    RESERVED_START  =2000
    RESERVED_END    =2999
    KEYWORD_START   =3000
    KEYWORD_END     =3999
    FUNCTION_START  =4000
    FUNCTION_END    =4999
    NUMERIC_START   =5000
    NUMERIC_END     =5999
    ALPHA_START     =6000
    ALPHA_END       =6999
    DELIMITER_START =7000
    DELIMITER_END   =7999
    OPERATOR_START  =8000
    OPERATOR_END    =8999


    
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
    
    DATE=0x07D0
    DATETIME=0x07D1
    FULL=0x07D2
    UNTIL=0x07D3
    USER=0x07D4
    VALUE=0x07D5
    VIEW=0x07D6
    
    # KEYWORD
    
    AND=0x0BB8
    ASC=0x0BB9
    AS=0x0BBA
    BEFORE=0x0BBB
    BETWEEN=0x0BBC
    BY=0x0BBD
    CREATE=0x0BBE
    DATABASE=0x0BBF
    DATABASES=0x0BC0
    DESC=0x0BC1
    DISTINCT=0x0BC2
    DROP=0x0BC3
    EXISTS=0x0BC4
    FALSE=0x0BC5
    FROM=0x0BC6
    GROUP=0x0BC7
    GROUPS=0x0BC8
    HAVING=0x0BC9
    IN=0x0BCA
    INSERT=0x0BCB
    INTO=0x0BCC
    IS=0x0BCD
    JOIN=0x0BCE
    LEFT=0x0BCF
    LIKE=0x0BD0
    LIMIT=0x0BD1
    MOD=0x0BD2
    NOT=0x0BD3
    NULL=0x0BD4
    ON=0x0BD5
    ORDER=0x0BD6
    OR=0x0BD7
    RIGHT=0x0BD8
    SELECT=0x0BD9
    SET=0x0BDA
    SHOW=0x0BDB
    TABLE=0x0BDC
    TRUE=0x0BDD
    UNION=0x0BDE
    UNIQUE=0x0BDF
    UPDATE=0x0BE0
    VALUES=0x0BE1
    WHERE=0x0BE2
    XOR=0x0BE3
    
    # FUNCTIONS
    
    ABS=0x0FA0
    ACOS=0x0FA1
    AND=0x0FA2
    AND=0x0FA3
    ASCII=0x0FA4
    ASIN=0x0FA5
    EQUALS=0x0FA6
    ASSIGN=0x0FA7
    ATAN=0x0FA8
    ATAN2=0x0FA9
    ATAN=0x0FAA
    AVG=0x0FAB
    BINARY=0x0FAC
    BIT_AND=0x0FAD
    BIT_COUNT=0x0FAE
    BIT_LENGTH=0x0FAF
    BIT_OR=0x0FB0
    BIT_XOR=0x0FB1
    AND=0x0FB2
    INVERSION=0x0FB3
    OR=0x0FB4
    XOR=0x0FB5
    CEIL=0x0FB6
    CEILING=0x0FB7
    CHAR=0x0FB8
    CHAR_LENGTH=0x0FB9
    COS=0x0FBA
    COT=0x0FBB
    COUNT=0x0FBC
    COUNT=0x0FBD
    CURDATE=0x0FBE
    CURRENT_DATE=0x0FBF
    CURRENT_TIME=0x0FC0
    CURRENT_TIMESTAMP=0x0FC1
    CURRENT_USER=0x0FC2
    CURTIME=0x0FC3
    DATABASE=0x0FC4
    DATE=0x0FC5
    DAY=0x0FC6
    DIVIDE=0x0FC7
    EQUALS=0x0FC8
    NULL_EQ=0x0FC9
    EXP=0x0FCA
    FLOOR=0x0FCB
    GREATER=0x0FCC
    GREATER_EQ=0x0FCD
    HEX=0x0FCE
    IN=0x0FCF
    IS=0x0FD0
    NOT=0x0FD1
    NULL=0x0FD2
    NULL=0x0FD3
    IS_UUID=0x0FD4
    ISNULL=0x0FD5
    LCASE=0x0FD6
    LEAST=0x0FD7
    LEFT=0x0FD8
    LEFT_SHIFT=0x0FD9
    LENGTH=0x0FDA
    LESS=0x0FDB
    LESS_EQ=0x0FDC
    LIKE=0x0FDD
    LOWER=0x0FDE
    LPAD=0x0FDF
    MAX=0x0FE0
    MD5=0x0FE1
    MICROSECOND=0x0FE2
    MIN=0x0FE3
    MINUS=0x0FE4
    MINUTE=0x0FE5
    MOD=0x0FE6
    MOD=0x0FE7
    MONTH=0x0FE8
    MONTHNAME=0x0FE9
    NOT=0x0FEA
    NOT_EQ=0x0FEB
    NOT_EQ=0x0FEC
    NOT_IN=0x0FED
    NOT_LIKE=0x0FEE
    NOW=0x0FEF
    OR=0x0FF0
    OR=0x0FF1
    ORD=0x0FF2
    PI=0x0FF3
    PLUS=0x0FF4
    POW=0x0FF5
    REPLACE=0x0FF6
    REVERSE=0x0FF7
    RIGHT=0x0FF8
    SHIFT_RIGHT=0x0FF9
    ROUND=0x0FFA
    ROW_COUNT=0x0FFB
    ROW_NUMBER=0x0FFC
    RPAD=0x0FFD
    RTRIM=0x0FFE
    SCHEMA=0x0FFF
    SECOND=0x1000
    SHA1=0x1001
    SHA1=0x1002
    SHA2=0x1003
    SIN=0x1004
    SQRT=0x1005
    STRCMP=0x1006
    SUBSTR=0x1007
    SUM=0x1008
    TAN=0x1009
    TIME=0x100A
    PRODUCT=0x100B
    TO_BASE64=0x100C
    TO_DAYS=0x100D
    TO_SECONDS=0x100E
    TRIM=0x100F
    TRUNCATE=0x1010
    UCASE=0x1011
    MINUS=0x1012
    UPPER=0x1013
    USER=0x1014
    UUID=0x1015
    VALUES=0x1016
    VERSION=0x1017
    WEEK=0x1018
    WEEKDAY=0x1019
    XOR=0x101A
    YEAR=0x101B
    YEARWEEK=0x101C
    
    # NUMERIC
    
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
    
    # ALPHA
    
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
    
    # DELIMITER
    
    NEW_LINE=0x1B58
    TAB=0x1B59
    SPACE=0x1B5A
    COMMA=0x1B5B
    PERIOD=0x1B5C
    DOLLAR=0x1B5D
    SEMICOLON=0x1B5E
    UNDERSCORE=0x1B5F
    
    # OPERATOR
    
    
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
    
    DATE_STR='DATE'
    DATETIME_STR='DATETIME'
    FULL_STR='FULL'
    UNTIL_STR='UNTIL'
    USER_STR='USER'
    VALUE_STR='VALUE'
    VIEW_STR='VIEW'
    
    # KEYWORD
    
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
    
    # FUNCTIONS
    
    ABS_STR='ABS'
    ACOS_STR='ACOS'
    AND_STR='AND'
    AND_STR='&&'
    ASCII_STR='ASCII'
    ASIN_STR='ASIN'
    EQUALS_STR='='
    ASSIGN_STR=':='
    ATAN_STR='ATAN'
    ATAN2_STR='ATAN2'
    ATAN_STR='ATAN'
    AVG_STR='AVG'
    BINARY_STR='BINARY'
    BIT_AND_STR='BIT_AND'
    BIT_COUNT_STR='BIT_COUNT'
    BIT_LENGTH_STR='BIT_LENGTH'
    BIT_OR_STR='BIT_OR'
    BIT_XOR_STR='BIT_XOR'
    AND_STR='&'
    INVERSION_STR='~'
    OR_STR='|'
    XOR_STR='^'
    CEIL_STR='CEIL'
    CEILING_STR='CEILING'
    CHAR_STR='CHAR'
    CHAR_LENGTH_STR='CHAR_LENGTH'
    COS_STR='COS'
    COT_STR='COT'
    COUNT_STR='COUNT'
    COUNT_STR='COUNT(DISTINCT)'
    CURDATE_STR='CURDATE'
    CURRENT_DATE_STR='CURRENT_DATE'
    CURRENT_TIME_STR='CURRENT_TIME'
    CURRENT_TIMESTAMP_STR='CURRENT_TIMESTAMP'
    CURRENT_USER_STR='CURRENT_USER'
    CURTIME_STR='CURTIME'
    DATABASE_STR='DATABASE'
    DATE_STR='DATE'
    DAY_STR='DAY'
    DIVIDE_STR='/'
    EQUALS_STR='='
    NULL_EQ_STR='<=>'
    EXP_STR='EXP'
    FLOOR_STR='FLOOR'
    GREATER_STR='>'
    GREATER_EQ_STR='>='
    HEX_STR='HEX'
    IN_STR='IN'
    IS_STR='IS'
    NOT_STR='IS NOT'
    NULL_STR='IS NOT NULL NOT NULL'
    NULL_STR='IS NULL NULL'
    IS_UUID_STR='IS_UUID'
    ISNULL_STR='ISNULL'
    LCASE_STR='LCASE'
    LEAST_STR='LEAST'
    LEFT_STR='LEFT'
    LEFT_SHIFT_STR='<<'
    LENGTH_STR='LENGTH'
    LESS_STR='<'
    LESS_EQ_STR='<='
    LIKE_STR='LIKE'
    LOWER_STR='LOWER'
    LPAD_STR='LPAD'
    MAX_STR='MAX'
    MD5_STR='MD5'
    MICROSECOND_STR='MICROSECOND'
    MIN_STR='MIN'
    MINUS_STR='-'
    MINUTE_STR='MINUTE'
    MOD_STR='MOD'
    MOD_STR='%'
    MONTH_STR='MONTH'
    MONTHNAME_STR='MONTHNAME'
    NOT_STR='NOT'
    NOT_EQ_STR='!='
    NOT_EQ_STR='<>'
    NOT_IN_STR='NOT IN'
    NOT_LIKE_STR='NOT LIKE'
    NOW_STR='NOW'
    OR_STR='OR'
    OR_STR='||'
    ORD_STR='ORD'
    PI_STR='PI'
    PLUS_STR='+'
    POW_STR='POW'
    REPLACE_STR='REPLACE'
    REVERSE_STR='REVERSE'
    RIGHT_STR='RIGHT'
    SHIFT_RIGHT_STR='>>'
    ROUND_STR='ROUND'
    ROW_COUNT_STR='ROW_COUNT'
    ROW_NUMBER_STR='ROW_NUMBER'
    RPAD_STR='RPAD'
    RTRIM_STR='RTRIM'
    SCHEMA_STR='SCHEMA'
    SECOND_STR='SECOND'
    SHA1_STR='SHA1'
    SHA1_STR='SHA'
    SHA2_STR='SHA2'
    SIN_STR='SIN'
    SQRT_STR='SQRT'
    STRCMP_STR='STRCMP'
    SUBSTR_STR='SUBSTR'
    SUM_STR='SUM'
    TAN_STR='TAN'
    TIME_STR='TIME'
    PRODUCT_STR='*'
    TO_BASE64_STR='TO_BASE64'
    TO_DAYS_STR='TO_DAYS'
    TO_SECONDS_STR='TO_SECONDS'
    TRIM_STR='TRIM'
    TRUNCATE_STR='TRUNCATE'
    UCASE_STR='UCASE'
    MINUS_STR='-'
    UPPER_STR='UPPER'
    USER_STR='USER'
    UUID_STR='UUID'
    VALUES_STR='VALUES'
    VERSION_STR='VERSION'
    WEEK_STR='WEEK'
    WEEKDAY_STR='WEEKDAY'
    XOR_STR='XOR'
    YEAR_STR='YEAR'
    YEARWEEK_STR='YEARWEEK'
    
    # NUMERIC
    
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
    
    # ALPHA
    
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
    
    # DELIMITER
    
    NEW_LINE_STR='\n'
    TAB_STR='\t'
    SPACE_STR=' '
    COMMA_STR=','
    PERIOD_STR='.'
    DOLLAR_STR='$'
    SEMICOLON_STR=';'
    UNDERSCORE_STR='_'
    
    # OPERATOR
    


    @staticmethod
    def get_intermediate_code_2(text):
        if text==None: return 0
        text=text.upper()
        text_length=len(text)
        text_hash=hash(text)
        if   text=='': 
            return 0 
        if   text_length==20:
            if   text_hash==2685835141087165576: return 0x0FD2
        elif text_length==17:
            if   text_hash==-2465261383222976365: return 0x0FC1
        elif text_length==15:
            if   text_hash==4037658321872535467: return 0x0FBD
        elif text_length==12:
            if   text_hash==-7082576370618590702: return 0x0FBF
            elif text_hash==8917431629020408577: return 0x0FC0
            elif text_hash==-8529183443948141929: return 0x0FC2
            elif text_hash==5939371364431313562: return 0x0FD3
        elif text_length==11:
            if   text_hash==790085836123405040: return 0x0FB9
            elif text_hash==-4182170197775145037: return 0x0FE2
        elif text_length==10:
            if   text_hash==6719388265795548058: return 0x0FAF
            elif text_hash==4117279704767084702: return 0x0FFC
            elif text_hash==1177747611616432039: return 0x100E
        elif text_length==9:
            if   text_hash==2287436798404490839: return 0x0BC0
            elif text_hash==5555305875986438504: return 0x0FAE
            elif text_hash==7321103001091467254: return 0x0FE9
            elif text_hash==5814585390684215025: return 0x0FFB
            elif text_hash==5797096014363584214: return 0x100C
        elif text_length==8:
            if   text_hash==-3335509522698720921: return 0x0BBF
            elif text_hash==-4427568144388930392: return 0x0BC2
            elif text_hash==-6213914849266237361: return 0x07D1
            elif text_hash==-3335509522698720921: return 0x0FC4
            elif text_hash==8654848824925262984: return 0x0FEE
            elif text_hash==-5487008874824183162: return 0x1010
            elif text_hash==-468990378493888581: return 0x101C
        elif text_length==7:
            if   text_hash==8422106668497960279: return 0x0BBC
            elif text_hash==-7723880023475818168: return 0x0FAD
            elif text_hash==-7723905023636818532: return 0x0FB1
            elif text_hash==-1922999326063428638: return 0x0FB7
            elif text_hash==2628857955610438613: return 0x0FBE
            elif text_hash==5075594029694990870: return 0x0FC3
            elif text_hash==3942850535070517281: return 0x0FD4
            elif text_hash==-7123748551811924177: return 0x0FF6
            elif text_hash==2112034384346248325: return 0x0FF7
            elif text_hash==-8164545538318340188: return 0x100D
            elif text_hash==5571671084300109907: return 0x1017
            elif text_hash==1715784304840850581: return 0x1019
        elif text_length==6:
            if   text_hash==5788341079899903583: return 0x0BBB
            elif text_hash==-2860899356599532118: return 0x0BBE
            elif text_hash==-6797446220009517626: return 0x0BC4
            elif text_hash==-1438505323107606634: return 0x0BC8
            elif text_hash==7813825114794786301: return 0x0BC9
            elif text_hash==-2667667377094072927: return 0x0BCB
            elif text_hash==-3655737310966507362: return 0x0BD9
            elif text_hash==2935381317924681307: return 0x0BDF
            elif text_hash==821116054469991117: return 0x0BE0
            elif text_hash==-8657821113436651404: return 0x0BE1
            elif text_hash==-8186543119211299231: return 0x0FAC
            elif text_hash==-4633207193029851283: return 0x0FB0
            elif text_hash==5196764764269337125: return 0x0FD1
            elif text_hash==-570373869569906735: return 0x0FD5
            elif text_hash==5087571862206094962: return 0x0FDA
            elif text_hash==-3457152658025383842: return 0x0FE5
            elif text_hash==500981198316972262: return 0x0FED
            elif text_hash==-6770121575391199425: return 0x0FFF
            elif text_hash==-4655874311900508846: return 0x1000
            elif text_hash==-1924800092293748419: return 0x1006
            elif text_hash==-8355939711653235695: return 0x1007
            elif text_hash==-8657821113436651404: return 0x1016
        elif text_length==5:
            if   text_hash==-426319011301440668: return 0x0BC5
            elif text_hash==2788289350344119428: return 0x0BC7
            elif text_hash==-5509471285393800684: return 0x0BD1
            elif text_hash==5046430602683938333: return 0x0BD6
            elif text_hash==-145964486211609629: return 0x0BD8
            elif text_hash==-6358197886813880007: return 0x0BDC
            elif text_hash==-3143589525201319736: return 0x0BDE
            elif text_hash==3323618512992715868: return 0x0BE2
            elif text_hash==-3143608525295319843: return 0x07D3
            elif text_hash==-5696290798678005810: return 0x07D5
            elif text_hash==5978145477214376060: return 0x0FA4
            elif text_hash==-5468539596203175055: return 0x0FA9
            elif text_hash==-8234174923546894144: return 0x0FBC
            elif text_hash==-7872965084715991993: return 0x0FCB
            elif text_hash==6937342788763751469: return 0x0FD6
            elif text_hash==937288788757751886: return 0x0FD7
            elif text_hash==-7509471285455800958: return 0x0FDE
            elif text_hash==4705186076095758959: return 0x0FE8
            elif text_hash==-145964486211609629: return 0x0FF8
            elif text_hash==-6145996486239609699: return 0x0FFA
            elif text_hash==7747279660527492983: return 0x0FFE
            elif text_hash==7856375474157678948: return 0x1011
            elif text_hash==-5143598525321320095: return 0x1013
        elif text_length==4:
            if   text_hash==5809132768366327263: return 0x0BC1
            elif text_hash==5809153768506327339: return 0x0BC3
            elif text_hash==-4328498044256676892: return 0x0BC6
            elif text_hash==8135334348070144970: return 0x0BCC
            elif text_hash==-6156980596043134620: return 0x0BCE
            elif text_hash==2152157665154412863: return 0x0BCF
            elif text_hash==2152169665101412709: return 0x0BD0
            elif text_hash==-7985434147538591845: return 0x0BD4
            elif text_hash==-5659258567968774201: return 0x0BDB
            elif text_hash==-1504828438253501924: return 0x0BDD
            elif text_hash==5809136768421327256: return 0x07D0
            elif text_hash==-4328491044353677245: return 0x07D2
            elif text_hash==2649858692839772309: return 0x07D4
            elif text_hash==6804450823649046655: return 0x07D6
            elif text_hash==-6654431622353492294: return 0x0FA1
            elif text_hash==-6654415622263492191: return 0x0FA5
            elif text_hash==-6654408622231492026: return 0x0FA8
            elif text_hash==-6654408622231492026: return 0x0FAA
            elif text_hash==1654702638691054863: return 0x0FB6
            elif text_hash==1654691638743055120: return 0x0FB8
            elif text_hash==5809136768421327256: return 0x0FC5
            elif text_hash==2152157665154412863: return 0x0FD8
            elif text_hash==2152169665101412709: return 0x0FDD
            elif text_hash==2152176665267413015: return 0x0FDF
            elif text_hash==8632785374281502105: return 0x0FFD
            elif text_hash==-5659258567978774333: return 0x1001
            elif text_hash==-5659258567978774336: return 0x1003
            elif text_hash==-5659267568045774354: return 0x1005
            elif text_hash==-1504821438373502217: return 0x100A
            elif text_hash==-1504828438281501888: return 0x100F
            elif text_hash==2649858692839772309: return 0x1014
            elif text_hash==2649856692951772773: return 0x1015
            elif text_hash==-7487871120403232704: return 0x1018
            elif text_hash==821265140655314519: return 0x101B
        elif text_length==3:
            if   text_hash==593367982096446688: return 0x0BB8
            elif text_hash==593367982099446576: return 0x0BB9
            elif text_hash==5527445905738704127: return 0x0BD2
            elif text_hash==4401390393099845880: return 0x0BD3
            elif text_hash==-1228887169288443101: return 0x0BDA
            elif text_hash==-6859164731816732220: return 0x0BE3
            elif text_hash==593367982084446675: return 0x0FA0
            elif text_hash==593367982096446688: return 0x0FA2
            elif text_hash==593367982104446715: return 0x0FAB
            elif text_hash==-1658743042926269182: return 0x0FBA
            elif text_hash==-1658743042926269179: return 0x0FBB
            elif text_hash==-2784798555555127363: return 0x0FC6
            elif text_hash==6223645544503735526: return 0x0FC9
            elif text_hash==-3910854067924984810: return 0x0FCA
            elif text_hash==-7289020605570558644: return 0x0FCE
            elif text_hash==5527445905736704105: return 0x0FE0
            elif text_hash==5527445905733704031: return 0x0FE1
            elif text_hash==5527445905744704007: return 0x0FE3
            elif text_hash==5527445905738704127: return 0x0FE6
            elif text_hash==4401390393099845880: return 0x0FEA
            elif text_hash==4401390393099845883: return 0x0FEF
            elif text_hash==3275334880745988474: return 0x0FF2
            elif text_hash==2149279368110130089: return 0x0FF5
            elif text_hash==-1228887169299442991: return 0x1002
            elif text_hash==-1228887169300443107: return 0x1004
            elif text_hash==-1228887169304443126: return 0x1008
            elif text_hash==-2354942681923301318: return 0x1009
            elif text_hash==-6859164731816732220: return 0x101A
        elif text_length==2:
            if   text_hash==8320049985075154: return 0x0BBA
            elif text_hash==8448050754076189: return 0x0BBD
            elif text_hash==9344056137084375: return 0x0BCA
            elif text_hash==9344056137084362: return 0x0BCD
            elif text_hash==10112060751091297: return 0x0BD5
            elif text_hash==10112060751091325: return 0x0BD7
            elif text_hash==6016036143054309: return 0x03EB
            elif text_hash==5376032298048467: return 0x03EC
            elif text_hash==5760034605052008: return 0x03ED
            elif text_hash==4864029222043862: return 0x0FA3
            elif text_hash==7424044602066961: return 0x0FA7
            elif text_hash==7936047678071557: return 0x0FCD
            elif text_hash==9344056137084375: return 0x0FCF
            elif text_hash==9344056137084362: return 0x0FD0
            elif text_hash==7680046140069258: return 0x0FD9
            elif text_hash==7680046140069259: return 0x0FDC
            elif text_hash==4224025377038108: return 0x0FEB
            elif text_hash==7680046140069256: return 0x0FEC
            elif text_hash==10112060751091325: return 0x0FF0
            elif text_hash==15872095356143114: return 0x0FF1
            elif text_hash==10240061520092347: return 0x0FF3
            elif text_hash==7936047678071558: return 0x0FF9
        elif text_length==1:
            if   text_hash==1280003851: return 0x1B58
            elif text_hash==1152003464: return 0x1B59
            elif text_hash==4096012321: return 0x1B5A
            elif text_hash==5632016941: return 0x1B5B
            elif text_hash==5888017711: return 0x1B5C
            elif text_hash==4608013861: return 0x1B5D
            elif text_hash==7552022714: return 0x1B5E
            elif text_hash==12160036574: return 0x1B5F
            elif text_hash==4352013091: return 0x03E8
            elif text_hash==4992015014: return 0x03E9
            elif text_hash==12288036961: return 0x03EA
            elif text_hash==5120015401: return 0x03EE
            elif text_hash==5248015784: return 0x03EF
            elif text_hash==7808023484: return 0x0FA6
            elif text_hash==4864014631: return 0x0FB2
            elif text_hash==16128048511: return 0x0FB3
            elif text_hash==15872047741: return 0x0FB4
            elif text_hash==12032036191: return 0x0FB5
            elif text_hash==6016018094: return 0x0FC7
            elif text_hash==7808023484: return 0x0FC8
            elif text_hash==7936023871: return 0x0FCC
            elif text_hash==7680023101: return 0x0FDB
            elif text_hash==5760017324: return 0x0FE4
            elif text_hash==4736014244: return 0x0FE7
            elif text_hash==5504016554: return 0x0FF4
            elif text_hash==5376016171: return 0x100B
            elif text_hash==5760017324: return 0x1012

        return 0


    @staticmethod
    def get_intermediate_code_3(text):
        if text==None: return 0
        text=text.upper()
        text_length=len(text)
        text_hash=hash(text)
        if   text=='': 
            return 0 
        if   text_length==20:
            if   text=='IS NOT NULL NOT NULL': return 0x0FD2
        elif text_length==17:
            if   text=='CURRENT_TIMESTAMP': return 0x0FC1
        elif text_length==15:
            if   text=='COUNT(DISTINCT)': return 0x0FBD
        elif text_length==12:
            if   text=='CURRENT_DATE': return 0x0FBF
            elif text=='CURRENT_TIME': return 0x0FC0
            elif text=='CURRENT_USER': return 0x0FC2
            elif text=='IS NULL NULL': return 0x0FD3
        elif text_length==11:
            if   text=='CHAR_LENGTH': return 0x0FB9
            elif text=='MICROSECOND': return 0x0FE2
        elif text_length==10:
            if   text=='BIT_LENGTH': return 0x0FAF
            elif text=='ROW_NUMBER': return 0x0FFC
            elif text=='TO_SECONDS': return 0x100E
        elif text_length==9:
            if   text=='DATABASES': return 0x0BC0
            elif text=='BIT_COUNT': return 0x0FAE
            elif text=='MONTHNAME': return 0x0FE9
            elif text=='ROW_COUNT': return 0x0FFB
            elif text=='TO_BASE64': return 0x100C
        elif text_length==8:
            if   text=='DATABASE': return 0x0BBF
            elif text=='DISTINCT': return 0x0BC2
            elif text=='DATETIME': return 0x07D1
            elif text=='DATABASE': return 0x0FC4
            elif text=='NOT LIKE': return 0x0FEE
            elif text=='TRUNCATE': return 0x1010
            elif text=='YEARWEEK': return 0x101C
        elif text_length==7:
            if   text=='BETWEEN': return 0x0BBC
            elif text=='BIT_AND': return 0x0FAD
            elif text=='BIT_XOR': return 0x0FB1
            elif text=='CEILING': return 0x0FB7
            elif text=='CURDATE': return 0x0FBE
            elif text=='CURTIME': return 0x0FC3
            elif text=='IS_UUID': return 0x0FD4
            elif text=='REPLACE': return 0x0FF6
            elif text=='REVERSE': return 0x0FF7
            elif text=='TO_DAYS': return 0x100D
            elif text=='VERSION': return 0x1017
            elif text=='WEEKDAY': return 0x1019
        elif text_length==6:
            if   text=='BEFORE': return 0x0BBB
            elif text=='CREATE': return 0x0BBE
            elif text=='EXISTS': return 0x0BC4
            elif text=='GROUPS': return 0x0BC8
            elif text=='HAVING': return 0x0BC9
            elif text=='INSERT': return 0x0BCB
            elif text=='SELECT': return 0x0BD9
            elif text=='UNIQUE': return 0x0BDF
            elif text=='UPDATE': return 0x0BE0
            elif text=='VALUES': return 0x0BE1
            elif text=='BINARY': return 0x0FAC
            elif text=='BIT_OR': return 0x0FB0
            elif text=='IS NOT': return 0x0FD1
            elif text=='ISNULL': return 0x0FD5
            elif text=='LENGTH': return 0x0FDA
            elif text=='MINUTE': return 0x0FE5
            elif text=='NOT IN': return 0x0FED
            elif text=='SCHEMA': return 0x0FFF
            elif text=='SECOND': return 0x1000
            elif text=='STRCMP': return 0x1006
            elif text=='SUBSTR': return 0x1007
            elif text=='VALUES': return 0x1016
        elif text_length==5:
            if   text=='FALSE': return 0x0BC5
            elif text=='GROUP': return 0x0BC7
            elif text=='LIMIT': return 0x0BD1
            elif text=='ORDER': return 0x0BD6
            elif text=='RIGHT': return 0x0BD8
            elif text=='TABLE': return 0x0BDC
            elif text=='UNION': return 0x0BDE
            elif text=='WHERE': return 0x0BE2
            elif text=='UNTIL': return 0x07D3
            elif text=='VALUE': return 0x07D5
            elif text=='ASCII': return 0x0FA4
            elif text=='ATAN2': return 0x0FA9
            elif text=='COUNT': return 0x0FBC
            elif text=='FLOOR': return 0x0FCB
            elif text=='LCASE': return 0x0FD6
            elif text=='LEAST': return 0x0FD7
            elif text=='LOWER': return 0x0FDE
            elif text=='MONTH': return 0x0FE8
            elif text=='RIGHT': return 0x0FF8
            elif text=='ROUND': return 0x0FFA
            elif text=='RTRIM': return 0x0FFE
            elif text=='UCASE': return 0x1011
            elif text=='UPPER': return 0x1013
        elif text_length==4:
            if   text=='DESC': return 0x0BC1
            elif text=='DROP': return 0x0BC3
            elif text=='FROM': return 0x0BC6
            elif text=='INTO': return 0x0BCC
            elif text=='JOIN': return 0x0BCE
            elif text=='LEFT': return 0x0BCF
            elif text=='LIKE': return 0x0BD0
            elif text=='NULL': return 0x0BD4
            elif text=='SHOW': return 0x0BDB
            elif text=='TRUE': return 0x0BDD
            elif text=='DATE': return 0x07D0
            elif text=='FULL': return 0x07D2
            elif text=='USER': return 0x07D4
            elif text=='VIEW': return 0x07D6
            elif text=='ACOS': return 0x0FA1
            elif text=='ASIN': return 0x0FA5
            elif text=='ATAN': return 0x0FA8
            elif text=='ATAN': return 0x0FAA
            elif text=='CEIL': return 0x0FB6
            elif text=='CHAR': return 0x0FB8
            elif text=='DATE': return 0x0FC5
            elif text=='LEFT': return 0x0FD8
            elif text=='LIKE': return 0x0FDD
            elif text=='LPAD': return 0x0FDF
            elif text=='RPAD': return 0x0FFD
            elif text=='SHA1': return 0x1001
            elif text=='SHA2': return 0x1003
            elif text=='SQRT': return 0x1005
            elif text=='TIME': return 0x100A
            elif text=='TRIM': return 0x100F
            elif text=='USER': return 0x1014
            elif text=='UUID': return 0x1015
            elif text=='WEEK': return 0x1018
            elif text=='YEAR': return 0x101B
        elif text_length==3:
            if   text=='AND': return 0x0BB8
            elif text=='ASC': return 0x0BB9
            elif text=='MOD': return 0x0BD2
            elif text=='NOT': return 0x0BD3
            elif text=='SET': return 0x0BDA
            elif text=='XOR': return 0x0BE3
            elif text=='ABS': return 0x0FA0
            elif text=='AND': return 0x0FA2
            elif text=='AVG': return 0x0FAB
            elif text=='COS': return 0x0FBA
            elif text=='COT': return 0x0FBB
            elif text=='DAY': return 0x0FC6
            elif text=='<=>': return 0x0FC9
            elif text=='EXP': return 0x0FCA
            elif text=='HEX': return 0x0FCE
            elif text=='MAX': return 0x0FE0
            elif text=='MD5': return 0x0FE1
            elif text=='MIN': return 0x0FE3
            elif text=='MOD': return 0x0FE6
            elif text=='NOT': return 0x0FEA
            elif text=='NOW': return 0x0FEF
            elif text=='ORD': return 0x0FF2
            elif text=='POW': return 0x0FF5
            elif text=='SHA': return 0x1002
            elif text=='SIN': return 0x1004
            elif text=='SUM': return 0x1008
            elif text=='TAN': return 0x1009
            elif text=='XOR': return 0x101A
        elif text_length==2:
            if   text=='AS': return 0x0BBA
            elif text=='BY': return 0x0BBD
            elif text=='IN': return 0x0BCA
            elif text=='IS': return 0x0BCD
            elif text=='ON': return 0x0BD5
            elif text=='OR': return 0x0BD7
            elif text=='/*': return 0x03EB
            elif text=='*/': return 0x03EC
            elif text=='--': return 0x03ED
            elif text=='&&': return 0x0FA3
            elif text==':=': return 0x0FA7
            elif text=='>=': return 0x0FCD
            elif text=='IN': return 0x0FCF
            elif text=='IS': return 0x0FD0
            elif text=='<<': return 0x0FD9
            elif text=='<=': return 0x0FDC
            elif text=='!=': return 0x0FEB
            elif text=='<>': return 0x0FEC
            elif text=='OR': return 0x0FF0
            elif text=='||': return 0x0FF1
            elif text=='PI': return 0x0FF3
            elif text=='>>': return 0x0FF9
        elif text_length==1:
            if   text=='\n': return 0x1B58
            elif text=='\t': return 0x1B59
            elif text==' ': return 0x1B5A
            elif text==',': return 0x1B5B
            elif text=='.': return 0x1B5C
            elif text=='$': return 0x1B5D
            elif text==';': return 0x1B5E
            elif text=='_': return 0x1B5F
            elif text=='"': return 0x03E8
            elif text=="'": return 0x03E9
            elif text=='`': return 0x03EA
            elif text=='(': return 0x03EE
            elif text==')': return 0x03EF
            elif text=='=': return 0x0FA6
            elif text=='&': return 0x0FB2
            elif text=='~': return 0x0FB3
            elif text=='|': return 0x0FB4
            elif text=='^': return 0x0FB5
            elif text=='/': return 0x0FC7
            elif text=='=': return 0x0FC8
            elif text=='>': return 0x0FCC
            elif text=='<': return 0x0FDB
            elif text=='-': return 0x0FE4
            elif text=='%': return 0x0FE7
            elif text=='+': return 0x0FF4
            elif text=='*': return 0x100B
            elif text=='-': return 0x1012

        return 0



    @staticmethod
    def get_code_type(code):
        if code>=bytecode.BLOCK_START     and code<=bytecode.BLOCK_END:      return bytecode.TOKEN_TYPE_BLOCK_STRING
        if code>=bytecode.RESERVED_START  and code<=bytecode.RESERVED_END:   return bytecode.TOKEN_TYPE_RESERVED
        if code>=bytecode.KEYWORD_START   and code<=bytecode.KEYWORD_END:    return bytecode.TOKEN_TYPE_KEYWORD
        if code>=bytecode.OPERATOR_START  and code<=bytecode.OPERATOR_END:   return bytecode.TOKEN_TYPE_OPERATOR
        if code>=bytecode.NUMERIC_START   and code<=bytecode.NUMERIC_END:    return bytecode.TOKEN_TYPE_NUMERIC
        if code>=bytecode.ALPHA_START     and code<=bytecode.ALPHA_END:      return bytecode.TOKEN_TYPE_STRING
        if code>=bytecode.DELIMITER_START and code<=bytecode.DELIMITER_END:  return bytecode.TOKEN_TYPE_DELIMITER
        if code>=bytecode.FUNCTION_START  and code<=bytecode.FUNCTION_END:  return bytecode.TOKEN_TYPE_FUNCTION
        #print code
        #print  bytecode.ALPHA_START , bytecode.ALPHA_END, bytecode.TOKEN_TYPE_ALPHA
        return 0

    @staticmethod
    def add_fragment(fragment='',fragment_length=0,uid='',fragment_id=0,fragment_type=None,depth=0):
        #print ".",fragment 
        new_fragments=[]
        error=0
        # ignore whitespace if configured
        if fragment_type==bytecode.TOKEN_TYPE_WHITESPACE and bytecode.IGNORE_WHITESPACE:
            return new_fragments
        elif fragment_type==bytecode.TOKEN_TYPE_COMMENT and bytecode.IGNORE_COMMENTS:
             return new_fragments

        # add all identfyer blocks... must only contain reserved words or db target.. , 
        # words after a "." do not require identifier brackets....
        elif fragment_type==bytecode.TOKEN_TYPE_FIELD:
            code=bytecode.get_intermediate_code_2(fragment)
            computed_fragment_type=fragment_type
            if code!=0:
                computed_fragment_type=bytecode.get_code_type(code)
                if computed_fragment_type!=bytecode.TOKEN_TYPE_RESERVED:
                    error=bytecode.ERROR_INVALID_IDENTIFYER_TYPE


            new_fragments.append([fragment,code,depth,uid,fragment_id,computed_fragment_type,error])
            return new_fragments
            
        elif fragment_type==bytecode.TOKEN_TYPE_BLOCK_STRING or fragment_type==bytecode.TOKEN_TYPE_COMMENT or fragment_type==bytecode.TOKEN_TYPE_WHITESPACE:
            #print fragment,fragment_type
            if fragment!="":
                new_fragments.append([fragment,0,depth,uid,fragment_id,fragment_type,error])
                return new_fragments
        
        # Add all strings, test for system or reserved
        elif  fragment_type==bytecode.TOKEN_TYPE_STRING:
            code=bytecode.get_intermediate_code_2(fragment)
            
            if code!=0:
                computed_fragment_type=bytecode.get_code_type(code)
            else:
                computed_fragment_type=fragment_type

            #if computed_fragment_type==bytecode.TOKEN_TYPE_RESERVED:
            #    error=bytecode.ERROR_RESERVERD_WORD_REQUIRES_IDENTIFYER
            new_fragments.append([fragment,code,depth,uid,fragment_id,computed_fragment_type,error])
            return new_fragments

        # its a bunch of delimiters, break it up and match if possible
        else:
            if fragment!="":
                right_fragment=""
                right_fragment_length=0


                while fragment_length>0:
                    found=None
                    for length in xrange(fragment_length,0,-1):
                        code=bytecode.get_intermediate_code_2(fragment[:length])
                        if code!=0:
                            if right_fragment_length>0:
                                computed_fragment_type=code#bytecode.get_code_type(code)
                                new_fragments.append([right_fragment,0,depth,uid,fragment_id,computed_fragment_type,error])
                                right_fragment_length=0
                                right_fragment=""

                            found=True
                            computed_fragment_type=bytecode.get_code_type(code)
                            new_fragments.append([fragment[:length],code,depth,uid,fragment_id,computed_fragment_type,error])
                            fragment_length-=length
                            if fragment_length>0:
                                fragment=fragment[length:]
                            break;
                    
                    # if we looped through all length combiniations and found nothing, add the remainder and shrink the stack
                    if found==None:
                        right_fragment+=fragment[0]
                        right_fragment_length+=1
                        fragment_length-=1
                        if fragment_length>0:
                            fragment=fragment[1:]
                # catch all
                if right_fragment_length>0:

                    new_fragments.append([right_fragment,0,depth,uid,fragment_id,fragment_type,error])
                    right_fragment_length=0


        return new_fragments
   
    @staticmethod
    def get_BYTECODE(data,depth=0,uid="1",fragment_id=1):
        fragments=[]
        fragment=""
        fragment_length=0
        fragment_type=None
        in_block=None
        in_alpha=None
        block_depth=0
        # main loop for tokenizing
        for c in data:
            
            if in_block:
                in_alpha=None

                # is it the other side of the block
                if c==bytecode.LEFT_PAREN_STR and in_block==bytecode.RIGHT_PAREN_STR:      
                    block_depth+=1
                    fragment+=c
                    fragment_length+=1
                    continue

                
                temp_test=fragment+c
                in_block_len=len(in_block)
                test_index_length=len(temp_test)
                test_index=test_index_length-in_block_len
                temp_test[test_index:]
                
                
                
                #print '>'+temp_test[test_index:]+'<' 
                #print '>'+in_block+'<' 
                #print '>'+fragment[test_index:]+'.'+in_block
                if test_index_length>=in_block_len and temp_test[test_index:]==in_block:
                         
                    if in_block==bytecode.RIGHT_PAREN_STR:
                        #print 'HI'+fragment+str(block_depth)

                        block_depth-=1
                        if block_depth!=0:
                            fragment+=c
                            fragment_length+=1
                            continue


                        # last character hasnt been added, but maybe others have. pull off the stack
                        #if in_block_len>0:
                        #    #print len(in_block),fragment+"-EDGE"
                        #1    fragment=fragment[0:-1]
                        #print fragment +'---'
                           
                        sub_code=bytecode.get_BYTECODE(fragment,depth+1,"{0}.{1}".format(uid,fragment_id),fragment_id)
                        #fragment_id=sub_code[1]['fragment_id']+1
                        fragment_id=sub_code[1]
                        fragments+=sub_code[0]
                    else:
                        # last character hasnt been added, but maybe others have. pull off the stack
                        if in_block_len>1:
                            #print len(in_block),fragment+"-EDGE"
                            fragment=fragment[:-in_block_len+0]

                        fragment_id+=1
                        fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,depth=depth,fragment_type=fragment_type)
                        fragment_type=None
                    fragment=""
                    fragment_length=0
                    in_block=None
                # no, add the contents
                else:
                    fragment+=c
                    fragment_length+=1
            else:
                # self closing or single character match
                if   c==bytecode.DOUBLE_QUOTE_STR:    
                    in_block  =bytecode.DOUBLE_QUOTE_STR
                    frag_temp =bytecode.TOKEN_TYPE_BLOCK_STRING
                elif c==bytecode.SINGLE_QUOTE_STR:    
                    in_block  =bytecode.SINGLE_QUOTE_STR
                    frag_temp =bytecode.TOKEN_TYPE_BLOCK_STRING
                elif c==bytecode.BACK_TIC_STR:        
                    in_block  =bytecode.BACK_TIC_STR
                    frag_temp =bytecode.TOKEN_TYPE_FIELD
                elif c==bytecode.LEFT_PAREN_STR:      
                    in_block  =bytecode.RIGHT_PAREN_STR
                    frag_temp =bytecode.TOKEN_TYPE_EXPRESSION
                    block_depth   +=1
        
                # matched pair, multi character
                test_fragment=fragment+c
                if test_fragment==bytecode.LEFT_COMMENT_STR:    
                    in_block  =bytecode.RIGHT_COMMENT_STR
                    frag_temp =bytecode.TOKEN_TYPE_COMMENT
                    fragment=""
                    fragment_length=0
                    
                elif test_fragment==bytecode.COMMENT_SINGLE_STR:  
                    fragment=""
                    fragment_length=0
                    in_block  =bytecode.NEW_LINE_STR
                    frag_temp =bytecode.TOKEN_TYPE_COMMENT

                
                if c==bytecode.SPACE_STR or c==bytecode.TAB_STR or c==bytecode.NEW_LINE_STR:
                    fragment_id+=1
                    fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,depth=depth,fragment_type=fragment_type)
                    fragments+=bytecode.add_fragment(c,fragment_length,uid,fragment_id,depth=depth,fragment_type=bytecode.TOKEN_TYPE_WHITESPACE)
                    fragment_type=None
                    fragment=""
                    fragment_length=0
                    continue
                    
                if in_block:
                    fragment_id+=1
                    fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,depth=depth,fragment_type=fragment_type)
                    fragment_type=frag_temp
                    fragment=""
                    fragment_length=0
                    continue
                    
                #not a block, or anything else
                #if 1==1:
                else:
                    # is this the start of an "WORD"
                    u_alpha   =c>=bytecode.A_STR and c<=bytecode.Z_STR
                    l_alpha   =c>=bytecode.a_STR and c<=bytecode.z_STR 
                    numeric   =c>=bytecode.ZERO_STR and c<=bytecode.NINE_STR
                    underscore=c==bytecode.UNDERSCORE_STR 
                    dollar    =c==bytecode.DOLLAR_STR

                    if fragment_type!=bytecode.TOKEN_TYPE_STRING:
                        if u_alpha or l_alpha or numeric or underscore or dollar:
                            fragment_id+=1
                            fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,depth=depth,fragment_type=fragment_type)
                            fragment=c
                            fragment_length=1
                            fragment_type=bytecode.TOKEN_TYPE_STRING
                            continue    
    
                    
                    # Are we in a "WORD"
                    else:
                        # If we just LEFT ... add the existing word, and start a new one
                        if not u_alpha and not l_alpha and not numeric and not underscore and not dollar:
                            fragment_id+=1
                            fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,depth=depth,fragment_type=fragment_type)
                            fragment=c
                            fragment_length=1
                            fragment_type=bytecode.TOKEN_TYPE_OTHER
                            continue

                        
                    # fallthrough
                    fragment+=c
                    fragment_length+=1

        # END Loop                
        # if anything is still left in the pipeline, cleanup
        
        fragment_id+=1
        fragments+=bytecode.add_fragment(fragment,fragment_length,uid,fragment_id,depth=depth,fragment_type=fragment_type)
        fragment=""
        fragment_length=0
    
    
        # err if block mismatch
        #if in_block:
        #    err_msg="Missing {0}".format(in_block)
        #    raise Exception(err_msg)
        
        # reduce groups that are single elements
        #while len(fragments)==1:
        #    print fragments
        #    elif isinstance(fragments,dict):
        #        fragments=fragments['sub']
        #    print fragments
        #    return fragments
        
        #return [{"sub":fragments,'fragment_id':fragment_id}]
        return [fragments,fragment_id]

    

    @staticmethod
    def print_code(codes,root=True):
        if root: print("Token                | Code   | Depth | UID         | Fragment ID | Type                 | Error  | Level")
        if root: print("---------------------+--------+-------+-------------+-------------+----------------------+--------+------ ")
        if isinstance(codes,list):
            for code in codes:
                #if isinstance(code,dict):
                #    bytecode.print_code(code['sub'],None)
                #elif isinstance(code,list):
                    pad=""
                    for i in range(code[2]):
                        pad+=" " 
                    level=pad+code[0]
                    if len(level)>15:
                        level=level[:15]+'...'
                    level=level.replace('\n',' ')
                    word=code[0]
                    if len(word)>15:
                        word=level[:15]+'...'
                    word=word.replace('\n',' ')
                    fragment_type=code[5]
                    error=code[6]
                    if   code[5]==bytecode.TOKEN_TYPE_FIELD       : fragment_type="FIELD"
                    elif code[5]==bytecode.TOKEN_TYPE_BLOCK_STRING: fragment_type="BLOCK_STRING"
                    elif code[5]==bytecode.TOKEN_TYPE_STRING      : fragment_type="STRING"
                    elif code[5]==bytecode.TOKEN_TYPE_COMMENT     : fragment_type="COMMENT"
                    elif code[5]==bytecode.TOKEN_TYPE_WHITESPACE  : fragment_type="WHITESPACE"
                    elif code[5]==bytecode.TOKEN_TYPE_EXPRESSION  : fragment_type="EXPRESSION"
                    elif code[5]==bytecode.TOKEN_TYPE_OTHER       : fragment_type="OTHER"
                    elif code[5]==bytecode.TOKEN_TYPE_KEYWORD     : fragment_type="KEYWORD"
                    elif code[5]==bytecode.TOKEN_TYPE_RESERVED    : fragment_type="RESERVED"
                    elif code[5]==bytecode.TOKEN_TYPE_NUMERIC     : fragment_type="NUMERIC"
                    elif code[5]==bytecode.TOKEN_TYPE_OPERATOR    : fragment_type="OPERATOR"
                    elif code[5]==bytecode.TOKEN_TYPE_DELIMITER   : fragment_type="DELIMITER"
                    elif code[5]==bytecode.TOKEN_TYPE_FUNCTION    : fragment_type="FUNCTION"
                    
                    bc='0x{0:04x}'.format(code[1])
                    if code[1]==0:
                        bc='      '
                    
                    print("{0:20} | {1} | {2}     | {3:10}  | {4:4}        | {5:13}        | {6:3}   | {7}".format(word,bc,code[2],code[3],code[4],fragment_type,error,level))

##
## End bytecode class
##





# calls the bytecode class and converts the sql into a list of integers and strings
# which are pattern matched
class lexer:
    bytecode_index=0
    bytecode_length=0
    bytecode_id=0
    _offset=None
    _length=None
    _from  =None
    _joins =None
    
    def __init__(self,cmd_text,debug=True):
        print ("LEXER")
        self.bytecode,self.bytecode_id=bytecode.get_BYTECODE(cmd_text)
        print ("BYTECODE")
        self.bytecode_length=len(self.bytecode)
        if debug: bytecode.print_code(self.bytecode) 

        print ("LEX")
        self.process_bytecode(bytecode)

    

    def get_next_bytecode(self):
        if isinstance(codes,list):
            for code in codes:
                if isinstance(code,dict):
                    bytecode.print_code(code['sub'],None)
        
    def pin_index(self):
        self.bytecode_index_pin=self.bytecode_index

    def resetpin_index(self):
        self.bytecode_index=self.bytecode_index=pin

    def validate_match_set(self,results):
        for result in results:
            if result==None:
                return None
        return retults

    def match(self,pattern,optional=None):
        found=None
        bytecode_index=self.bytecode_index
        for sequence in  pattern:
            if bytecode_index>=self.bytecode_length:
                break
            pattern_match=None
            if isinstance(sequence,int):
                print sequence,self.bytecode[bytecode_index]
                if self.bytecode[bytecode_index][1]==sequence:
                    print ("match {0}".format(sequence))
                    pattern_match=True
                    found=[]

            if None==pattern_match:
                raise Exception("Pattern not found, PRE")        

            bytecode_index+=1
        
        if found!=None:
            self.bytecode_index=bytecode_index
            return found
        if optional:
            self.bytecode_index=bytecode_index
            return None
        raise Exception ("No Match")
    
    # atleast 1 thing must be matched, or it fails
    def match_or(self,patterns):
        for pattern in patterns:
            try:
                return self.match(pattern)
            except:
                pass
        raise Exception ("No or Match")

    def process_bytecode(self,bytecode):
        self.bytecode_index=0
        while self.bytecode_index<self.bytecode_length:
            old_bytecode_index=self.bytecode_index
            self.keyword_select()
            if self.bytecode_index==old_bytecode_index:
                raise Exception("Not found")
    
    def keyword_select(self):
        try:
            self.match([bytecode.SELECT])
        except Exception as ex:
            print ex
            return

        self.simple_expression()
        self.keyword_FROM()
        self.keyword_JOIN()
        self.keyword_LEFT_JOIN()
        self.keyword_RIGHT_JOIN()
        self.keyword_FULL_JOIN()
        self.keyword_OUTER_JOIN()
        self.keyword_INNER_JOIN()
        self.keyword_WHERE()
        self.keyword_ORDER_BY()
        self.keyword_GROUP_BY()
        self.keyword_LIMIT()

    def simple_expression(self):
        pass

    def keyword_FROM(self):
        try:
            self._from= self.match([bytecode.FROM,'F']) 
        except:
            pass

    def keyword_JOIN(self):
        try:
            self._joins.append(self.match([bytecode.JOIN,'F']) )
        except:
            pass

    def keyword_LEFT_JOIN(self):
        try:
            self.joins.append(match([bytecode.LEFT_JOIN,'F']) )
        except:
            pass
        pass

    def keyword_RIGHT_JOIN(self):
        self.joins.append(match([bytecode.RIGHT_JOIN,'F']) )
        pass

    def keyword_FULL_JOIN(self):
        self._joins.append(self.match([bytecode.FULL_JOIN,'F']) )
        pass

    def keyword_OUTER_JOIN(self):
        pass

    def keyword_INNER_JOIN(self):
        pass

    def keyword_WHERE(self):
        pass

    def keyword_ORDER_BY(self):
        pass

    def keyword_GROUP_BY(self):
        pass

    def keyword_LIMIT(self):
        try:
            self._offset,self._length= match([K_LIMIT,'I,I']) 
        except:
            try:
                self._length         = match([K_LIMIT,'I']) 
            except:
                pass




    def bit_expression(bytecode):
        try:
            self.bit_expr()
            self.match(bytecode.O_OR)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_AND)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_LEFT_SHIFT)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_RIGHT_SHIFT)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_PLUS)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_MINUS)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_MULTIPLY)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_DIVIDE)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.DIV)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.MOD)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_MODULUS)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.XOR)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_PLUS)
            self.interval_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.O_MINUS)
            self.interval_expr()
        except:
            pass

        try:
            self.simple_expr()
        except:
            pass
        raise Exception("No BIT_EXPR")
        # time intercal expression

    def interval_exp(self):
        try:
            self.match(bytecode.INTERVAL)
        except:
            raise exception("Not an interval")

        patterns=[
            [bytecode.INTERVAL,INT                                   , bytecode.MICROSECONDS],
            [bytecode.INTERVAL,INT                                   , bytecode.SECOND],
            [bytecode.INTERVAL,INT                                   , bytecode.MINUTE],
            [bytecode.INTERVAL,INT                                   , bytecode.HOUR],
            [bytecode.INTERVAL,INT                                   , bytecode.DAY],
            [bytecode.INTERVAL,INT                                   , bytecode.WEEK],
            [bytecode.INTERVAL,INT                                   , bytecode.MONTH],
            [bytecode.INTERVAL,INT                                   , bytecode.QUARTER],
            [bytecode.INTERVAL,INT                                   , bytecode.YEAR],
            [bytecode.INTERVAL,[INT,DOT,INT                        ] , bytecode.SECOND_MICROSECOND],
            [bytecode.INTERVAL,[INT,COLON,INT,DOT,INT              ] , bytecode.MINUTE_MICROSECOND],
            [bytecode.INTERVAL,[INT,COLON,INT                      ] , bytecode.MINUTE_SECOND],
            [bytecode.INTERVAL,[INT,COLON,INT,COLON,INT,DOT,INT    ] , bytecode.HOUR_MICROSECOND],
            [bytecode.INTERVAL,[INT,COLON,INT,COLON,INT            ] , bytecode.HOUR_SECOND],
            [bytecode.INTERVAL,[INT,COLON,INT                      ] , bytecode.HOUR_MINUTE],
            [bytecode.INTERVAL,[INT,INT,COLON,INT,COLON,INT,DOT,INT] , bytecode.DAY_MICROSECOND],
            [bytecode.INTERVAL,[INT,INT,COLON,INT,COLON,INT        ] , bytecode.DAY_SECOND],
            [bytecode.INTERVAL,[INT,INT,COLON,INT                  ] , bytecode.DAY_MINUTE],
            [bytecode.INTERVAL,[INT,INT                            ] , bytecode.DAY_HOUR],
            [bytecode.INTERVAL,[INT,DASH,INT                       ] , bytecode.YEAR_MONTH],
        ]

        for pattern in patterns:
            results=self.match(pattern)
            if results:
                return results
        raise Exception("Not a interval Expression")    # comparitors

    def comparison_operator(self): 
     # TOD  <> OR !=... fix
     return self.match_or([EQUALS,OR,GREATER_EQ,GREATER,LESS_EQ,LESS,NOT_EQ])

    def expression(self):
        try:
            self.expr()
            self.match(bytecode.OR)
            self.expr()
        except:
            pass

        try:
            self.expr()
            self.match(bytecode.SHORT_CIRCUIT_OR)
            self.expr()
        except:
            pass

        try:
            self.expr()
            self.match(bytecode.XOR)
            self.expr()
        except:
            pass


        try:
            self.expr()
            self.match(bytecode.AND)
            self.expr()
        except:
            pass

        try:
            self.expr()
            self.match(bytecode.SHORT_CIRCUIT_AND)
            self.expr()
        except:
            pass

        try:
            self.match(bytecode.NOT)
            self.expr()
        except:
            pass
        
        try:
            self.match(bytecode.NEGATE)
            self.expr()
        except:
            pass
        
        try:
            self.boolean_primary()
            self.match(bytecode.IS) 
            self.match(bytecode.NOT,optional=True)
            self.match_or([bytecode.TRUE,bytecode.FALSE,bytecode.UNKNOWN])
        except:
            pass

        try:
            self.boolean_primary()
        except:
            pass

        raise Exception ("No Expression")
   
    def boolean_primary(self):
        try:
            self.boolean_primary()
            self.match(bytecode.IS)
            self.match(bytecode.NOT,optional=True)
            self.match(bytecode.NULL)
        except: 
            pass
        
        try:
            self.boolean_primary()
            self.match(bytecode.NULL_EQ)
            self.predicate()
        except:
            pass
    
        try:
            self.boolean_primary()
            self.comparison_operator()
            self.predicate()
        except:
            pass

        try:
            self.boolean_primary()
            self.comparison_operator()
            self.predicate()
        except:
            pass
        try:
            self.boolean_primary()
            self.comparison_operator()
            # {ALL | ANY}
            self.match_or([bytecode.ALL,bytecode.ANY],optional) 
            self.subquery()
        except:
            pass
        try:
            self.predicate()
        except:
            pass
        raise Exception("No boolean primary")
 
    def predicate(self):
        try:
            self.bit_expr()
            self.match(bytecode.NOT,OPTIONAL)
            self.match(bytecode.IN)
            self.subquery()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.NOT,optional=True)
            self.match(bytecode.IN)
            self.expr_array()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.NOT,optional=True)
            self.match(bytecode.BETWEEN)
            self.bit_expr()
            self.match(bytecode.AND)
            self.predicate
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.SOUNDS,bytecode.LIKE)
            self.bit_expr()
        except:
            pass

        try:
            self.bit_expr()
            self.match(bytecode.NOT,optional=True)
            self.match(bytecode.LIKE)
            self.simple_expr()
            try:
                results=self.match(bytecode.ESCAPE,optional=True)
                if results:
                    self.simple_expr()
            except:
                raise Exception("Escape syntax")
        except:
            pass

        try:
            self.bit_expr()
            self.match(sbytecode.NOT,optional=True)
            self.match(bytecode.REGEXP)
            self.bit_expr()
        except:
            pass

        try:
            return self.bit_expr()
        except:
            pass
        raise Exception ("No predicate")

    def colation_name(self):
        return self.match_OR([bytecode.COLATION_DATABASE_DEFAULT,bytecode.COLATION_UTF8])

    # strig or numeric literal
    def literal(self):
        if is_instance(self.bytecode[self.bytecode_index],str):
            return True
        raise Exception("Not Literal")


    # TODO
    def identifier(self):
        return True

    def function_call(self):
        return True

    def param_marker(self):
        return True

    def variable(self):
        return True

    def expr_array(self):
        return True
    
    def subquery(self):
        return True        
    
    def match_expr(self):
        return True
    
    def case_expr(self):
        return True
    

    def simple_expr(self):
        # sets the restart pointer for the bytecode index
        self.pin_index()
        
        try:   
            self.resetpin_index()
            return { self.literal() }
        except: 
            pass
        
        try:    
            self.resetpin_index()
            return { self.identifier() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.function_call() }
        except: 
            pass
        
        try:    
            self.resetpin_index()
            return { self.simple_expr(),self.match(bytecode.COLLATE),self.colation_name() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.param_marker() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.variable() }
        except: 
            pass
        
        try:    
            self.resetpin_index()
            return { self.simple_expr() , self.match(bytecode.O_SHORTCIRCUIT_OR) , self.simple_expr() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.match(self.bytecode.O_PLUS)  , simple_expr() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.match(self.bytecode.O_MINUS) , simple_expr() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.match(self.bytecode.O_NOT)   , simple_expr() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.match(self.bytecode.O_NEGATE), simple_expr() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.match(self.bytecode.BINARY)  , simple_expr() }
        except: 
            pass
        
        try:    
            self.resetpin_index()
            return { self.expr_array() }
        except: 
            pass
        
        # I dont really know what the ROW(expr[,expr ...]) does
        #try:    
        #    self.resetpin_index()
        #    return { self.match(self.bytecode.ROW), (,self.expr_array()) }
        #except: 
        #    pass

        try:    
            self.resetpin_index()
            return { self.subquery() }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.match(bytecode.EXISTS) ,self.subquery() }
        except: 
            pass
        

        try:    
            self.resetpin_index()
            return { self.identifier(),self.expr() }  # {}? }
        except: 
            pass

        try:    
            self.resetpin_index()
            return { self.match_expr() }
        except: pass

        
        try:    
            self.resetpin_index()
            return { self.case_expr() }
        except: pass

        
        try:     
            self.resetpin_index()
            return { self.interval_expr() }
        except:  pass

        # nothing matched. 
        self.resetpin_index()
        

# PASS 1 TOKENIZE, and identify
# pass 2 pattern match
# pass 3 error handle
# identfiyers not required after "." on quoted identifyer or valid...thing like DB something (l;ook up again)

def test(debug=None):
    query="""
    select COUNT(*) AS number,*,(SELECT first_name FROM test.mock LIMIT 1) as first_name
    FROM test.mock 
    WHERE first_name='bob' 
    and last_name not 'sam' 
    and gender=F 
    and last_name in (SELECT last_name FROM test.mock LIMIT 10 WHERE last_name like '%sam%') as first_name
    
    -- this is a comment
    -- this is another comment /* */ fe
    -- this is also a comment 'quote'
    -- this is also a comment "double quote"
    ;
    b=:('rewrew')
    /*
        Block Comment #1
    */
        """
    lexer(query)
    #codes=bytecode.get_BYTECODE(query)
    #if debug: bytecode.print_code(codes) 


#print(timeit.timeit(test, number=10))

test(True)




# Rules....
# 
# 
# 
# RESERVED words do not use quotes or filed identifiers
# Keywords MUST use field identifiers -> ` <-

# 
# 
# 
# 
# 
# if the word is a keyword, congert to bytecode
# if the word isnt, store as string

