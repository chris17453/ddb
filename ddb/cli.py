import argparse
import tempfile
import os
import flextable
from ddb.engine.sql_engine  import sql_engine
from ddb.engine.interactive import ddbPrompt
from ddb.engine.structure.database import database
from ddb.engine.structure.table import table

from os.path import expanduser
    

def cli_main():
    parser = argparse.ArgumentParser("ddb", usage='%(prog)s [options]'
                    ,description=
                    """flat file database access
                    """, epilog="And that's how you ddb")

    # actions
    parser.add_argument('-v'      ,'--debug'            , help='show debuging statistics',action='store_true')
    parser.add_argument('-c'      ,'--config'           , help='yaml configuration file')
    parser.add_argument('query'            , help='query to return data' ,nargs="?")
    #parser.add_argument('-s'      ,'--show-config'      , help='yaml configuration file' ,action='store_true')
    #parser.add_argument('-d'      ,'--config'           , help='yaml configuration directory or file (all files ending with .ddb.yml')
    #parser.add_argument('-f'      ,'--format'           , help='How to output the data, CSV,ARRAY,YAML,JSONI,TERM. Default TERM')
    #parser.add_argument('-e'      ,'--show-errors'      , help='display errors encourtered in system processing',action='store_true')
    #parser.add_argument('-tw'     ,'--term-width'       , help='Terminal output, width per column, auto')
    #parser.add_argument('-cl'     ,'--term-no-clip'     , help='Terminal output, dont clip fields'              ,action='store_true')
    
    
    #parser.add_argument('-ac'     ,'--add-config'        , help='Add a yaml configuration file')
    #parser.add_argument('-ac'     ,'--add-config'        , help='Add a yaml configuration file')
    #parser.add_argument('-rc'     ,'--remove-config'     , help='Remove a yaml configuration file')
    
    args = parser.parse_args()


    home = expanduser("~")
    config_file=os.path.join(os.path.join(home, '.ddb'),'ddb.conf')

    #home = expanduser("~")
    #if not os.path.exists(os.path.join(home, '.ddb')):
    #    os.makedirs(os.path.join(home, '.ddb'))
    #home=os.path.join(home, '.ddb')
    
    # everything is accessable as a query, so why make line arguments?

    #if None != args.add_config:
    #    db=database(config_file=config_file)
    #    db.add_config(args.add_config)
    #    exit(1)

    #if None != args.remove_config:
    #    db=database(config_file=config_file)
    #    db.remove_config(args.remove_config)
    #    exit(1)


    
    if None != args.query:
        if None != args.config:
            e=sql_engine(database_dir=args.config,debug=args.debug,mode="full")
        else:
            e=sql_engine(config_file=config_file,debug=args.debug,mode="full")
            results=e.query(args.query)
            if results!=None:
                config=flextable.table_config()
                config.columns=results.get_columns()
                flextable.table(data=results.results,args=config)

    else:
        # interactive session
        prompt=ddbPrompt()
        prompt.set_vars(database    = args.config,
                        config_file =config_file,
                        debug       = args.debug)
        prompt.cmdloop_with_keyboard_interrupt()
    

if __name__ == "__main__":
    cli_main()
        
