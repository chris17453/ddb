import time
from cmd import Cmd
from .engine import engine
from .version import __version__
from .output.factory import output_factory


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ddbPrompt(Cmd):
    prompt = 'ddb> '
    intro = "Welcome! Type ? to list commands. Version: {0}".format(__version__)

    def cmdloop_with_keyboard_interrupt(self):
        doQuit = False
        while doQuit != True:
            try:
                self.cmdloop()
                doQuit = True
            except KeyboardInterrupt:
                self.help_exit("")

    def set_vars(self,
                 config_file=None,
                 debug=False,
                 no_clip=False,
                 width='auto'):
        if debug is None:
            debug = False
        self.debug = debug
        self.no_clip = no_clip
        self.width = width
        self.engine = sql_engine(config_file=config_file, debug=self.debug, mode="full",output='term',output_file=None)

    def msg(self, type, name, message=''):
        if type == 'info':
            color = bcolors.OKGREEN
        if type == 'warn':
            color = bcolors.WARNING
        if type == 'error':
            color = bcolors.FAIL

        print("{2}>>>{3} {4}{0}{3} {1}".format(name, message, bcolors.OKBLUE, bcolors.ENDC, color))

    ##
    def do_exit(self, inp):
        self.msg("info", "Bye")
        return True

    def help_exit(self, inp):
        self.msg("info", 'exit the application. Shorthand: x q Ctrl-D.')

    ##
    def do_debug(self, inp):
        if not self.debug:
            self.debug = True
            self.msg("info", "Debugging ON")
        else:
            self.debug = False
            self.msg("info", "Debugging Off")
        self.engine.debugging(debug=self.debug)

    def help_debug(self, inp):
        self.msg("info", 'Toggle debugging on or off')

    ##

    def do_config(self, inp):
        try:
            self.msg("info", "configuration_file set to'{}'".format(inp))
            self.engine = sql_engine(config_file=inp, debug=self.debug)
        except Exception as ex:
            self.msg("error", "config", ex)

    def help_config(self):
        self.msg("info", "Set configuration file.")

    ##
    # def do_show_errors(self, inp):
    #    self.engine.print_errors()

    # def help_show_errors(self):
    #   self.msg("info","Show last error(s) generated")
    ##

    def default(self, inp):
        #print inp
        if inp == 'x' or inp == 'q':
            return self.do_exit("")

        try:
            if None == self.engine:
                print ("sql engin gone")
                return
            start = time.time()
            results = self.engine.query(sql_query=inp)
            end = time.time()
            o=output_factory(results)

            self.msg("info", "executed in {} seconds".format(end - start))
            inp = None
        except Exception as ex:
            self.msg("error", ex)

    def default_exit(self):
        self.msg("info", 'exit the application. Shorthand: x q Ctrl-D.')

    do_EOF = help_exit
    help_EOF = help_exit
