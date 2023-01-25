import xml.etree.ElementTree as ET
import requests
import os
import xmltodict

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name) 

def get_xml_data_and_return_a_dict(url):
    xml_rss_feed = requests.get(url)
    return xmltodict.parse(xml_rss_feed.content)

def make_show_list(url):
    xml_dict = get_xml_data_and_return_a_dict(url)
    list_show = []

    for num in range(0, len(xml_dict['rss']['channel']['item'])):
        list_show.append(xml_dict['rss']['channel']['item'][num]['title'])

    return list_show, xml_dict

def search_for_shows():
    torrent_link = {}
    names = []
    with open(show_path, 'r') as shows:
        for show in shows.readlines():
            for num in range(0, len(xml_dict['rss']['channel']['item'])):
                if show.strip() in show_list[num]:
                    torrent_file_link = requests.get(xml_dict['rss']['channel']['item'][num]['link'])
                    names.append(show_list[num].strip())
                    torrent_link[show_list[num].strip()] = torrent_file_link.content
    return names, torrent_link

def save_shows_and_move_shows(watch_directory):
    for name in show_names:
        with open(f"{name}.torrent", "wb") as torrent_file:
            torrent_file.write(trackers[name])

        path = os.path.join(watch_directory,f"{name}.torrent.invalid")
        curent_directory = os.getcwd()
        if(os.path.isfile(path)):
            os.remove(f"{name}.torrent")
        else:
            final_path = os.path.join(watch_directory,f"{name}.torrent")
            file_name = os.path.join(current_directory,f"{name}.torrent")
            os.replace(file_name,final_path)



show_list,xml_dict = make_show_list("https://subsplease.org/rss/?t&r=1080")
show_path = find_file('shows.txt','/home/pi/scripts')
show_names, trackers = search_for_shows()
save_shows_and_move_shows('~/jellyfin/watch') 
