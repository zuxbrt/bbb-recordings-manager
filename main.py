# server connection
from openssh_wrapper import SSHConnection
from configparser import ConfigParser

# get config file
config_object = ConfigParser()
config_object.read('config.ini')

# get ssh connection params
serverconfig = config_object["SSH_CONFIG"]

# connect to server
conn = SSHConnection(serverconfig['host'], login=serverconfig['user'])
ret = conn.run('bbb-record --list')

# save recordings list into a file
with open('recordings.txt', 'a') as f:
    print(ret, file=f)