import xml.etree.ElementTree as ET
import requests
import os
import xmltodict

# Getting xml from SubsPlease amd saving it to a file
url = "https://subsplease.org/rss/?t&r=1080"
xml_rss_feed = requests.get(url)
with open('shows.xml','wb') as xml:
    xml.write(xml_rss_feed.content)
xml.close()

# Reimporting xml and translating it into a dict to be searchable
with open('shows.xml') as test:
    xml_dict = xmltodict.parse(test.read())
test.close()

#automatically removes the xml file so space is not wasted on the device
#os.remove('shows.xml')

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
                show_names.append(show.strip())
                trackers.update({show.strip():torrent_file_link.content})
shows.close()

with("{}.torrent".format(show_names[0])) as torrent:
    for show_name in show_names:
        torrent.write(trackers[show_name])
        #torrent.write(trackers[show_name])
    #torrent.close()
#"{}.torrent".format(show_name),
# ToDo: once show is found add logic to download the torrent file from the link and move to the wacth directory so that deluge can automatically download the torrent






#ToDo: add logic to remove .torrent files automatically, so I don't have to clean them up later





#tree = ET.parse('shows.xml')
#root = tree.getroot()

#attribArray = [element.attrib.get('title','') for element in root.findall('./channel/item')]
#print(attribArray)

#for items in root.findall('.//*'):
    
    #for child in items: 
        #print(child.tag, child.attrib)
        #print()
