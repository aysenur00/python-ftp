from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

import json


def main():

    config = read_config('../config.json')
    host = config['host']
    port = config['port']
    username = config['username']
    password = config['password']

    authorizer = DummyAuthorizer()
    authorizer.add_user(username, password, '.', perm='elradfmwMT')

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "pyftpdlib based ftpd ready."

    address = (host, port)
    server = FTPServer(address, handler)

    server.serve_forever()


def read_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

if __name__ == '__main__':
    main()