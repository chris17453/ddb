import os
import getpass
import argparse
from subprocess import Popen,PIPE
import ddb

username = getpass.getuser()


path="~/.config/systemd/user"
path=os.path.abspath(os.path.expanduser(path))
service_path=os.path.join(path,"ddb.service")

user_dir=os.path.expanduser('~')
user_data_dir=os.path.join(user_dir,".ddb")

default_ddb_port=17453
default_ddb_ip='0.0.0.0'



def try_bind(ddb_ip,ddb_port):
    try:
        s.bind((ddb_ip, ddb_port))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            print("Port is already in use: '{0}:{1}'".format(ddb_ip,ddb_port))
    else:
        print(e)

    s.close()

def get_ddb_cli():
    t_path=os.path.dirname(ddb.__file__)
    include_directory =os.path.abspath(os.path.join(t_path,os.pardir))
    print ( include_directory)
    cmd=["which","ddb-server"]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    if rc!=0:
        raise Exception("ddb not found in the local path")
    return output.strip()

def install_service(ddb_ip,ddb_port):
    try:
        if os.path.exists(path)==False:
            os.makedirs(path)
        cli_path=get_ddb_cli()

        service_template="""
[Unit]
Description=delimited database (ddb) service for user {0}
After=network.target

[Service]
Environment=PYTHONUNBUFFERED=1
Restart=on-failure
RestartSec=2
Type=idle
Environment=DDB_DATA='{1}'
Environment=DDB_PORT='{2}'
ExecStart={3} start
#ExecStop={3} stop
#ExecReload={3} restart
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=default.target
    """.format(username,user_data_dir,ddb_port,cli_path)
        with open(service_path,"w",) as service:
            service.write(service_template)
        os.chmod(service_path, 0644)

        restart_systemd()
    except Exception as ex:
        print ex
        print("Failed to init ddb service for user")
        exit(1)


def remove_service():
    try:
        if os.path.exists(service_path):
            os.remove(service_path)
    except Exception:
        print("Failed to remove ddb service for user")
        exit(1)

def restart_systemd():
    print ("You need to do a  ")
    print ("  # systemctl --user enable {0}".format(service_path))
    print ("  # systemctl daemon-reload")
    print ("  # systemctl --user ddb start")
    print ("  #    if you want the service to run after logout for this user enable linger....")
    print ("  # loginctl enable-linger {0}".format(username)

def cli_main():
    parser = argparse.ArgumentParser("ddb-service", usage='%(prog)s [options]', description="""flat file database access""", epilog="And that's how you ddb")

    parser.add_argument('action'    , help='[ install | remove ] the user service'                         , nargs='?')
    parser.add_argument('--ip'      , help='the ip to bind to: Default "{0}"'.format(default_ddb_ip)       , default=default_ddb_ip)
    parser.add_argument('--port'    , help='the port to bind to: Default "{0}"'.format(default_ddb_port)   , default=default_ddb_port)

    
    args = parser.parse_args()
    
    ddb_ip  =args.ip
    ddb_port=args.port
    if args.action=='install':
        install_service(ddb_ip,ddb_port)
    
    if args.action=='remove':
        remove_service()
    

if __name__=='main':
    cli_main()
