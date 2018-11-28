import sys
import time
from cmd import Cmd
from .structure.table import table
from .structure.database import database
from sql_engine  import sql_engine
from .formatting.colors import bcolors


class ddbPrompt(Cmd):
    prompt = 'ddb> '
    intro = "Welcome! Type ? to list commands"

    def cmdloop_with_keyboard_interrupt(self):
        doQuit = False
        while doQuit != True:
            try:
                self.cmdloop()
                doQuit = True
            except KeyboardInterrupt:
                self.help_exit("")

    def set_vars(self,
                 database,
                 debug,
                 no_clip,
                 width ,
                 format):
        if debug==None:
            debug=False
        self.debug=debug
        self.no_clip=no_clip
        self.width=width
        self.format=format
        self.engine=sql_engine(database,debug=self.debug)

    def msg(self,type,name,message=''):
        if type=='info':
            color=bcolors.OKGREEN
        if type=='warn':
            color=bcolors.WARNING
        if type=='error':
            color=bcolors.FAIL

        print("{2}>>>{3} {4}{0}{3} {1}".format(name,message,bcolors.OKBLUE,bcolors.ENDC,color))

    ##
    def do_exit(self,inp):
        self.msg("info","Bye")
        return True

    def help_exit(self,inp):
        self.msg("info",'exit the application. Shorthand: x q Ctrl-D.')

    ##
    def do_debug(self,inp):
        if self.debug==False:
            self.debug=True
            self.msg("info","Debugging ON")
        else:
            self.debug=False
            self.msg("info","Debugging Off")

    def help_debug(self,inp):
        self.msg("info",'Toggle debugging on or off')


    ##
    def do_config_dir(self, inp):
        try:
            self.msg("info","configuration_dir set to'{}'".format(inp))
            self.engine=self.engine(database=inp,debug=self.debug)
        except Exception as ex:
            self.msg("error","config_dir",ex)

    def help_config_dir(self):
        self.msg("info","Set configuration Directory. Files end in ddb.yaml.")

    ##
    #def do_show_errors(self, inp):
    #    self.engine.print_errors()
        

    #def help_show_errors(self):
    #   self.msg("info","Show last error(s) generated")
    ##


    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit("")
        
        try:
            if None == self.engine:
                print ("sql engin gone")
                return
            start = time.time()
            self.engine.query(sql_query=inp)
            end = time.time()
            self.engine.format_data(no_clip=self.no_clip,width='auto',format='term')
            self.msg("info","executed in {} seconds".format(end - start))
        except Exception as ex:
            self.msg("error",ex)

    def default_exit(self):
        self.msg("info",'exit the application. Shorthand: x q Ctrl-D.')

    do_EOF = help_exit
    help_EOF = help_exit
    
 






