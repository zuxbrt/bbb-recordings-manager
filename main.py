# server connection
from openssh_wrapper import SSHConnection
from configparser import ConfigParser

# get config file
config_object = ConfigParser()
config_object.read('config.ini')

# get ssh connection params
serverconfig = config_object["CONFIG"]

# connect to server
# conn = SSHConnection(serverconfig['host'], login=serverconfig['user'])
# recordslist = conn.run('bbb-record --list')

# save recordings list into a file
# with open('recordings.txt', 'r+') as f:
#     f.truncate(0) # need '0' when using r+
#     print(recordslist, file=f)


# ls = conn.run('cd /var/bigbluebutton/recording/raw && ls')
# stdout = vars(ls)['stdout']

# print(ls)