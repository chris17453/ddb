from cli import cli_main
import os


from .engine import engine

# main import


def engine(config_file=None, mode='array'):

    if config_file is None:
        home = os.path.expanduser("~")
        config_file = os.path.join(os.path.join(home, '.ddb'), 'ddb.conf')
    return engine(config_file=config_file, mode=mode)


if __name__ == "__main__":
    cli_main()
