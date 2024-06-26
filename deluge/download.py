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
output_shows = []

#importing show names and implementing logic to check for each show name within the xml file
show_path = os.path.abspath("/home/justin/git/scripts/deluge/shows.txt")
with open(show_path, 'r') as shows:
    for show in shows.readlines():
        for num in range(0, len(xml_dict['rss']['channel']['item'])):
            if show.strip() in show_list[num]:
                torrent_file_link = requests.get(xml_dict['rss']['channel']['item'][num]['link'])
                show_names.append(show_list[num].strip())
                output_shows.append(f"{show_list[num].strip()}\n")
                trackers.update({show_list[num].strip():torrent_file_link.content})
# moving completed torrents to the watch directory for my torrenting client and removing the file if the torrent
# already exists
for name in show_names:
    with open(f"{name}.torrent", "wb") as torrent_file:
        torrent_file.write(trackers[name])
    
    path = os.path.join('/home/justin/watch',f"{name}.torrent.invalid")
    if (os.path.isfile(path)):
        os.remove(f"{name}.torrent")
        output_shows.remove(f"{name}\n")
    else:
        final_path = os.path.join('/home/justin/watch',f"{name}.torrent")
        file_name = os.path.join(os.getcwd(),f"{name}.torrent")
        shutil.move(file_name,final_path)

# New file to keep track of shows to trancode
if (output_shows):
    with open("show_names.txt", "w") as show_names_output:
        show_names_output.writelines(output_shows)
    shutil.move("/home/justin/show_names.txt","/mnt/nas/show_names.txt")
