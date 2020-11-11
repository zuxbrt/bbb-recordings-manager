import os

logs = os.listdir('nginx')

logged_ips = []
# iterate over logs
for log in logs:
    # open recordings list (ignore ds_store)
    if log != '.DS_Store':
        content = open("nginx/"+str(log), "r")
        lines = content.readlines()
        for line in lines: 
            splitted1 = line.split('"')
            for item in splitted1:
                ip = item.split(" ")
                print(ip)
                if not ip[0] in logged_ips:
                    #print(ip[0])
                    logged_ips.append(ip[0])



recording_ids = []
worksheet_data = []

count = 0
# Strips the newline character 
for line in lines: 
    print(line)