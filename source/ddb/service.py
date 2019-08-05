import os
import getpass
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
        # something else raised the socket.error exception
        print(e)

    s.close()



def install_service(ddb_ip,ddb_port):
    try:
        if os.path.exists(path)==False:
            os.mkdir(path)

        service_template="""
[Unit]
Description=delimited database (ddb) service for user {0}
After=multi-user.target

[Service]
Environment=PYTHONUNBUFFERED=1
Restart=on-failure
RestartSec=2
Type=notify
Environment=DDB_DATA='{1}'
Environment=DDB_PORT='{2}'
ExecStartddb-server start
ExecStop=ddb-server stop
ExecReload=ddb-server restart

[Install]
WantedBy=default.target
    """.format(username,user_data_dir,ddb_port)
        with open(service_path,"w",) as service:
            service.write(service_template)
        os.chmod(service_path, 644)

        restart_systemd()
    except Exception:
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
    os.exec

def cli_main():
    parser = argparse.ArgumentParser("ddb-service", usage='%(prog)s [options]', description="""flat file database access""", epilog="And that's how you ddb")

    parser.add_argument('--install' , help='install the service to the user systemd directory'), action='store_true')
    parser.add_argument('--remove'  , help='remove  the service from the user systemd directory'),action='store_true')
    parser.add_argument('--ip'      , help='the ip to bind to: Default "{0}"'.format(default_ddb_ip), default=default_ddb_ip)
    parser.add_argument('--port'    , help='the port to bind to: Default "{0}"'.format(default_ddb_port), default=default_ddb_port)

    
    args = parser.parse_args()
    
    ddb_ip  =args.ip
    ddb_port=args.port
    if args.install==True:
        install_service(ddb_ip,ddb_port)
    
    if args.remove==True:
        remove_service()
    

if __name__=='main':
    cli_main()
