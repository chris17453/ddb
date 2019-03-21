from cli import cli_main
import os


from .engine import engine as ddb_engine

# main import


def engine(config_file=None, mode='array',debug=False):

    return ddb_engine(config_file=config_file,mode=mode,debug=debug)


if __name__ == "__main__":
    cli_main()
