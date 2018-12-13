import argparse
import tempfile
import os
import flextable
from engine.sql_engine  import sql_engine
from engine.interactive import ddbPrompt
from engine.structure.database import database
from engine.structure.table import table

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
    
    args = parser.parse_args()


    home = expanduser("~")
    config_file=os.path.join(os.path.join(home, '.ddb'),'ddb.conf')


    if None != args.query:
        if None != args.config:
            e=sql_engine(config_file=args.config,debug=args.debug,mode="full")
        else:
            e=sql_engine(config_file=config_file,debug=args.debug,mode="full")
            results=e.query(args.query)
            if results!=None:
                config=flextable.table_config()
                config.columns=results.get_columns_display()
                flextable.table(data=results.results,args=config)

    else:
        # interactive session
        prompt=ddbPrompt()
        prompt.set_vars(config_file =config_file,
                        debug       = args.debug)
        prompt.cmdloop_with_keyboard_interrupt()
    

if __name__ == "__main__":
    cli_main()
        
