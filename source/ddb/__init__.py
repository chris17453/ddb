from cli import cli_main
import os


from .engine import engine as ddb_engine

# main import


def engine(config_file=None, mode='array',debug=False):

    if config_file is None:
        home = os.path.expanduser("~")
        config_file = os.path.join(os.path.join(home, '.ddb'), 'ddb.conf')
    return ddb_engine(config_file=config_file, mode=mode,debug=debug)


if __name__ == "__main__":
    cli_main()
