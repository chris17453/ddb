


def get_script_directory():
    script_dir       = os.path.dirname(os.path.realpath(__file__))
    return script_dir

def get_script_parent_directory():
    script_dir       = os.path.dirname(os.path.realpath(__file__))
    script_parent_dir= os.path.abspath(os.path.join(script_dir, os.pardir))
    