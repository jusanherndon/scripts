import xml.etree.ElementTree as ET
import requests
import os
import xmltodict

# Getting xml from SubsPlease amd saving it to a file
url = "https://subsplease.org/rss/?t&r=1080"
xml_rss_feed = requests.get(url)
with open('shows.xml','wb') as xml:
    xml.write(xml_rss_feed.content)

# Reimporting xml and translating it into a dict to be searchable
with open('shows.xml') as test:
    xml_dict = xmltodict.parse(test.read())

#automatically removes the xml file so space is not wasted on the device
os.remove('shows.xml')

# This section is to get the show title and make them searchable, since python3.9 can search through 
# lists but not dictionaries
show_list = []
for num in range(0, len(xml_dict['rss']['channel']['item'])):
        show_list.append(xml_dict['rss']['channel']['item'][num]['title'])

# Creating new dictionary and a list to hold show names and torrent tracker info
trackers = {}
show_names = []

#importing show names and implementing logic to check for each show name within the xml file
with open("shows.txt", 'r') as shows:
    for show in shows.readlines():
        for num in range(0, len(xml_dict['rss']['channel']['item'])):
            if show.strip() in show_list[num]:
                torrent_file_link = requests.get(xml_dict['rss']['channel']['item'][num]['link'])
                show_names.append(show_list[num].strip())
                trackers.update({show_list[num].strip():torrent_file_link.content})

for name in show_names:
    with open(f"{name}.torrent", "wb") as torrent_file:
        torrent_file.write(trackers[name])

