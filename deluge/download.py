import xml.etree.ElementTree as ET
import requests
import os
import shutil
import xmltodict

# Getting xml from SubsPlease and converting it into a dictionary
url = "https://subsplease.org/rss/?t&r=1080"
xml_rss_feed = requests.get(url)
xml_dict = xmltodict.parse(xml_rss_feed.content)
# This section is to get the show title and make them searchable, since python3 can search through 
# lists but not dictionaries
show_list = []
for num in range(0, len(xml_dict['rss']['channel']['item'])):
        show_list.append(xml_dict['rss']['channel']['item'][num]['title'])
# Creating new dictionary and a list to hold show names and torrent tracker info
trackers = {}
show_names = []

#importing show names and implementing logic to check for each show name within the xml file
show_path = os.path.abspath("/home/justin/git/scripts/deluge/shows.txt")
with open(show_path, 'r') as shows:
    for show in shows.readlines():
        for num in range(0, len(xml_dict['rss']['channel']['item'])):
            if show.strip() in show_list[num]:
                torrent_file_link = requests.get(xml_dict['rss']['channel']['item'][num]['link'])
                show_names.append(show_list[num].strip())
                trackers.update({show_list[num].strip():torrent_file_link.content})
# moving completed torrents to the watch directory for my torrenting client and removing the file if the torrent
# already exists
for name in show_names:
    with open(f"{name}.torrent", "wb") as torrent_file:
        torrent_file.write(trackers[name])
    with open(f"show_names.txt", "wb") as show_names_output:
        show_names_output.append(f'{name}.mkv')
    
    path = os.path.join('/home/justin/watch',f"{name}.torrent.invalid")
    if(os.path.isfile(path)):
        os.remove(f"{name}.torrent")
    else:
        final_path = os.path.join('/home/justin/watch',f"{name}.torrent")
        file_name = os.path.join(os.getcwd(),f"{name}.torrent")
        shutil.move(file_name,final_path)
