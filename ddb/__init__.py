from cli import cli_main
from .engine.sql_engine import sql_engine

#main import
def engine(config_dir):
    return sql_engine(config_dir)


if __name__ == "__main__":
    cli_main()