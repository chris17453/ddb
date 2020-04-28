
try:
    from .cli import cli_main
    from .engine import engine 
except:
    pass

if __name__ == "__main__":
    cli_main()
