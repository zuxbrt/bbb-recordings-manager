import xlsxwriter
import requests
import lxml
from bs4 import BeautifulSoup as Soup
from configparser import ConfigParser

# https://pypi.org/project/beautifulsoup4/


# get config file
config_object = ConfigParser()
config_object.read('config.ini')

# get ssh connection params
config = config_object["CONFIG"]

# check if there are recordings for meeting
def has_recordings(meeting_id):
    url = config['bbb_api'] + "/getRecordings?meetingID=" + meeting_id + "&checksum=" + config['api_checksum']
    # if the server sent a Gzip or Deflate compressed response, decompress
    # as we read the raw stream:
    response = requests.get(url)
    string_xml = response.content
    soup = Soup(string_xml,'lxml')
    #extracting data between request_id Tag
    state = soup.response.returncode.get_text()
    if state == 'SUCCESS':
        has_rec = soup.response.messagekey.get_text()
        if has_rec != 'noRecordings':
            return soup.find('url');
    return 'no url';


workbook = xlsxwriter.Workbook('bbb-recordings.xlsx')
worksheet = workbook.add_worksheet()

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
    if header == False:
        worksheet.write(row, col, "Internal ID")
        worksheet.write(row, col + 1, "External ID")
        worksheet.write(row, col + 2, "Date")
        worksheet.write(row, col + 2, "URL")
        header = True
    else:
        rec_url = has_recordings(item["internal_id"])
        worksheet.write(row, col, item["internal_id"])
        worksheet.write(row, col + 1, item["external_id"])
        worksheet.write(row, col + 2, item["date"])
        worksheet.write(row, col + 2, rec_url)
    row += 1

workbook.close()
    