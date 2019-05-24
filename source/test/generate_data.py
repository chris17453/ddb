from random import randint, choice

lines=100000

def make_word(len1=0):
    if len1==0:
        len1=randint(3,20)
    return ''.join(choice('abcdefghijklmnopqrstuvwxyz') for i in range(len1))


def random_ip():
    octets = []
    for x in range(4):
        octets.append(str(randint(0,255)))
    return '.'.join(octets)

def random_sex():
    if choice('12')=='1':
        return 'Male'
    else:
        return 'Female'

column_names=['id','first_name','last_name','email','gender','ip_address']
print (",".join(column_names))
for index in range(0,lines):
    c1=str(index)
    c2=make_word()
    c3=random_sex()
    c4=make_word()+'@'+make_word()+".com"
    c5=random_ip()
    columns=[]
    columns.append(c1)
    columns.append(c2)
    columns.append(c3)
    columns.append(c4)
    columns.append(c5)
    
    line=",".join(columns)
    print(line)