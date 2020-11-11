import xlsxwriter
import requests
import lxml
import time
import json 

from hashlib import sha1
from bs4 import BeautifulSoup as Soup
from configparser import ConfigParser
from bigbluebutton_api_python import BigBlueButton

# soup4 lib docs
# https://pypi.org/project/beautifulsoup4/

# bbb api docs
# https://github.com/yunkaiwang/bigbluebutton-api-python

# rawXml docs
# https://jxmlease.readthedocs.io/en/stable/dict_objects.html

# get config file
config_object = ConfigParser()
config_object.read('config.ini')

# config
config = config_object["CONFIG"]

# bbb instance
b = BigBlueButton(config['bbb_api'], config['secret'])

# setup xlsx doc
workbook = xlsxwriter.Workbook('bbb-recordings.xlsx')
worksheet = workbook.add_worksheet()

# open recordings list
file = open("recordings.txt", "r")
lines = file.readlines()

recording_ids = []
worksheet_data = []

count = 0
# Strips the newline character 
for line in lines: 
    recording_info = line.split()

    # extract only meeting info
    if len(recording_info) == 10 or len(recording_info) == 11 or len(recording_info) == 12:
        if len(recording_info[0]) == 54:
            item = {
                'internal_id': recording_info[0],
                'external_id': recording_info[len(recording_info) - 1],
                'date': recording_info[1] + ',' + recording_info[2] + ' ' + recording_info[3] + ' ' + recording_info[4] + ' ' + recording_info[5] + ' ' + recording_info[6]
            }
            worksheet_data.append(item)
            count+=1

row = 0
col = 0

header = False
for item in worksheet_data:
    # set doc header
    if header == False:
        worksheet.write(row, col, "Ime predavanja")
        worksheet.write(row, col + 1, "Link")
        header = True
    else:
        try:
            # get bbb meeting recording
            res = b.get_recordings(item["external_id"]);
            xml = res.rawXml
            meetingName = ""
            url = ""
            # get meeting name
            for node in xml.find_nodes_with_tag('meetingName'):
                meetingName = node

            # get meeting playback url
            for node2 in xml.find_nodes_with_tag('url'):
                url = node2

            # add to doc if name and url present
            if meetingName != "" and url != "":  
                worksheet.write(row, col, meetingName)
                worksheet.write(row, col + 1, url)
                row += 1
        except TimeoutError as e: #
            print(e)

workbook.close()
    