import os

class tpl:
    variable={}
    padding={}

    def __init__(self,file):
        self.dir=os.path.dirname(os.path.realpath(__file__))
        self.open(os.path.join(self.dir,file))
        
        pass
    
    def add_var(self,var,padding=0):
        self.variable[var]=""
        self.padding[var]=padding
        
    def add(self,var,data):
        padding=""
        if var in self.padding:
            for i in range(self.padding[var]):
                padding+=' '
        
        
        self.variable[var]+=padding+data+"\n"
    
    def open(self,file):
        template=""
        with open(file) as content:
            template=content.read()
        self.template=template

    def build(self):
        self.output=self.template
        for var in self.variable:
            self.output=self.output.replace('{{{0}}}'.format(var),self.variable[var])

    def dump(self):
        print(self.output)
        pass
