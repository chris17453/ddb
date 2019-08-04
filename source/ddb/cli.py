# cython: linetrace=True

import argparse
import os
import sys
import fileinput
from .engine import engine
from .interactive import ddbPrompt
from .output.factory import output_factory

from subprocess import Popen, PIPE

from os.path import expanduser
import sys


def cli_main():


    parser = argparse.ArgumentParser("ddb", usage='%(prog)s [options]', description="""flat file database access""", epilog="And that's how you ddb")

    parser.add_argument('query', help='query to return data', nargs= "*")

    args = parser.parse_args()
    
    
    # get the path set in the environment
    # else expand the user path and look in the .ddb folder
    # else start with NO config, and no place to save...

    if 'DDB_DATA' in os.environ:
        # expand user vars, then get the absolute
        config_dir=os.path.abspath(os.path.expanduser(os.environ['DDB_DATA']))
    else:
        home = expanduser("~")
        config_dir = os.path.join(os.path.join(home, '.ddb'))

    # ddb always trys to create the config dir if non existant
    if config_dir:
        if os.path.exists(config_dir)==False:
            os.mkdir(config_dir)
            
    
    
    
    if len(args.query)!=0 or not sys.stdin.isatty():
        #try:
            if not sys.stdin.isatty():
                new_stdin = os.fdopen(sys.stdin.fileno(), 'r', 1024)
                query=""
                for c in new_stdin:
                    query+=c
                #query=sys.stdin.read()
            else:
                query=" ".join(args.query)
            #print (query)
            e = engine( config_dir=config_dir, 
                            debug=False, 
                            mode="full",
                            output='term',
                            output_file=None)
            results = e.query(query)
            #results.debug()
            #print(results) 
            if results.success==True:
                output_factory(results,output=e.system['OUTPUT_MODULE'],output_style=e.system['OUTPUT_STYLE'],output_file=None)
            else:
                output_factory(results,output=e.system['OUTPUT_MODULE'],output_style=e.system['OUTPUT_STYLE'],output_file=None)
            
            if None==results:
                exit_code=1
            elif results.success==True:
                exit_code=0
            elif results.success==False:
                exit_code=1
            sys.exit(exit_code)
        #except Exception as ex:
        #    print("Error:",ex)

    # is there something in stdin.. a pipe?
    else:
        # interactive session
        prompt = ddbPrompt()
        prompt.set_vars(config_dir=config_dir,
                        debug=False)
        prompt.cmdloop_with_keyboard_interrupt()


if __name__ == "__main__":
    cli_main()
