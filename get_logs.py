from openssh_wrapper import SSHConnection
from configparser import ConfigParser

# get config file
config_object = ConfigParser()
config_object.read('config.ini')

# get ssh connection params
serverconfig = config_object["CONFIG"]

# connect to server
conn = SSHConnection(serverconfig['host'], login=serverconfig['user'])
cmd1 = conn.run('cd /var/log/nginx && ls')

# save recordings list into a file
with open('nginx_logs.txt', 'w') as f:
    f.truncate(0) # need '0' when using r+
    print(cmd1, file=f)


# open recordings list
lognames = open("nginx_logs.txt", "r")
lines = lognames.readlines()

i = 0
for line in lines:
    if "bigbluebutton" in line:
        is_gzip = False
        ext = line.strip()[-3:]
        if ext == '.gz':
            is_gzip = True

        if is_gzip:
            cmd2 = conn.run('cd /var/log/nginx && zcat ' + line.strip())
        
            # save recordings list into a file
            with open("nginx/bbb-" + str(i) + ".txt", "w") as f:
                f.truncate(0) # need '0' when using r+
                print(cmd2, file=f)
        else:
            cmd2 = conn.run('cd /var/log/nginx && cat ' + line.strip())
        
            # save recordings list into a file
            with open("nginx/bbb-" + str(i) + ".txt", "w") as f:
                f.truncate(0) # need '0' when using r+
                print(cmd2, file=f)
            
        i+=1
