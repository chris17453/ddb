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


    parser = argparse.ArgumentParser("ddb", usage='%(prog)s [options]', description="""flat file database access
                    """, epilog="And that's how you ddb")

    # actions
    #parser.add_argument('-v', '--debug', help='show debuging statistics', action='store_true')
    #parser.add_argument('-c', '--config', help='yaml configuration file')
    #parser.add_argument('-o', '--output', help='output type (raw,json,yaml,xml|bash,term) defaults to "term"', default='term')
    #parser.add_argument('-f', '--file', help='output file (if nothing, output is redirected to stdio)', default= None)
    parser.add_argument('query', help='query to return data', nargs= "*")

    args = parser.parse_args()
    
    # set the config q
    # file location
    # if args.config is not None:
    #    config_file = args.config
    # else:
    home = expanduser("~")
    config_file = os.path.join(os.path.join(home, '.ddb'), 'ddb.conf')

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
            e = engine( config_file=config_file, 
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
        prompt.set_vars(config_file=config_file,
                        debug=False)
        prompt.cmdloop_with_keyboard_interrupt()


if __name__ == "__main__":
    cli_main()
