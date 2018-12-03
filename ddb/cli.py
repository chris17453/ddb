import argparse
from engine.sql_engine  import sql_engine
from engine.interactive import ddbPrompt
import tempfile
import flextable


def cli_main():
    parser = argparse.ArgumentParser("ddb", usage='%(prog)s [options]'
                    ,description=
                    """flat file database access
                    """, epilog="And that's how you ddb")

    # actions
    parser.add_argument('-v'      ,'--debug'            , help='show debuging statistics',action='store_true')
    parser.add_argument('-s'      ,'--show-config'      , help='yaml configuration file' ,action='store_true')
    parser.add_argument('-c'      ,'--config'           , help='yaml configuration file')
    parser.add_argument('-d'      ,'--config-dir'       , help='yaml configuration directory (all files ending with .ddb.yml')
    parser.add_argument('-q'      ,'--query'            , help='query to return data')
    parser.add_argument('-f'      ,'--format'           , help='How to output the data, CSV,ARRAY,YAML,JSONI,TERM. Default TERM')
    parser.add_argument('-e'      ,'--show-errors'      , help='display errors encourtered in system processing',action='store_true')
    parser.add_argument('-tw'     ,'--term-width'       , help='Terminal output, width per column, auto')
    parser.add_argument('-cl'     ,'--term-no-clip'     , help='Terminal output, dont clip fields'              ,action='store_true')
    args = parser.parse_args()
    
        
    
    if None != args.query:
        if None == args.config_dir:
            config_dir="."
        else:
            config_dir=args.config_dir

            #temp = tempfile.TemporaryFile() #2

            e=sql_engine(database_dir=config_dir,debug=args.debug)
            results=e.query(args.query)
            #print results.results
            #if True == args.show_errors:
            config=flextable.table_config()
            config.columns=results.get_columns()
            flextable.table(data=results.results,args=config)

    else:
        # interactive session
        prompt=ddbPrompt()
        prompt.set_vars(database = args.config_dir,
                        debug   = args.debug,
                        no_clip = args.term_no_clip,
                        width   = args.term_width,
                        format  = args.format)
        prompt.cmdloop_with_keyboard_interrupt()
    

if __name__ == "__main__":
    cli_main()
        
