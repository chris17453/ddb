import argparse
import os
from engine.sql_engine import sql_engine
from engine.interactive import ddbPrompt
from engine.output import format_output


from os.path import expanduser


def cli_main():


    parser = argparse.ArgumentParser("ddb", usage='%(prog)s [options]', description="""flat file database access
                    """, epilog="And that's how you ddb")

    # actions
    parser.add_argument('-v', '--debug', help='show debuging statistics', action='store_true')
    parser.add_argument('-c', '--config', help='yaml configuration file')
    parser.add_argument('-o', '--output', help='output type (raw,json,yaml,xml|bash,term) defaults to "term"', default= 'term')
    parser.add_argument('-f', '--file', help='output file (if nothing, output is redirected to stdio)', default= None)
    parser.add_argument('query', help='query to return data', nargs= "?")

    args = parser.parse_args()
    
    # set the config q
    # file location
    if args.config is not None:
        config_file = args.config
    else:
        home = expanduser("~")
        config_file = os.path.join(os.path.join(home, '.ddb'), 'ddb.conf')
    
    if args.query is not None:
        e = sql_engine( config_file=config_file, 
                        debug=args.debug, 
                        mode="full",
                        output=args.output,
                        output_file=args.file)
        results = e.query(args.query)
        output=format_output(results,output=args.output,output_file=args.file)

    else:
        # interactive session
        prompt = ddbPrompt()
        prompt.set_vars(config_file=config_file,
                        debug=args.debug)
        prompt.cmdloop_with_keyboard_interrupt()


if __name__ == "__main__":
    cli_main()
