from cli import cli_main
import os


from .engine.sql_engine import sql_engine

#main import
def engine(config_file=None):

    if None==config_file:
        home = os.path.expanduser("~")
        config_file=os.path.join(os.path.join(home, '.ddb'),'ddb.conf')
    return sql_engine(config_file=config_file)


if __name__ == "__main__":
    cli_main()