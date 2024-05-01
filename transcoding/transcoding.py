import os
import subprocess
import re

# step 1: send show_names.txt to this machine
scp_cmd = "scp justin@192.168.1.115:/home/justin/show_names.txt /home/justin/show_names.txt"
process = subprocess.run(scp_cmd, shell=True, check=True)

# step 2: take all needed inputs for this script

show_path = os.path.abspath("/home/justin/show_names.txt")
with open(show_path, 'r') as shows:
    for show in shows.readlines():

        # Match on just the show name so that was the file name looks nicer for the jellyfin server
        show_name_and_episode = re.findall("(?<=\ )(.*?)(?=\()", show.strip())
        show_name = str(show_name_and_episode[0] + ".mkv")
        transcoded_show_name = f"transcoded_{show_name}"

        #copy over the video file to this pc
        scp_video_cmd = f"scp justin@192.168.1.115:/mnt/jellyfin/shows/'{show.strip()}' /home/justin/{show_name}"
        process = subprocess.run(scp_video_cmd, shell=True, check=True)

        # step 3: Transcode the video using the old video as its base

        ffmpeg_cmd = f'ffmpeg -vaapi_device /dev/dri/renderD128 -i {show_name} -c:v hevc_amf -x265-params "pass=1:lossless=1" -an -f null /dev/null && ffmpeg -vaapi_device /dev/dri/renderD128 -quality quality -i {show_name} -c:v hevc_amf -c:a aac -map_metadata 0:g -x265-params "pass=2:lossless=1" {transcoded_show_name}'
        process = subprocess.run(ffmpeg_cmd, shell=True, check=True)

        # step 4: send new video file to the jellyfin media server
        scp_transcode_video_cmd = f"scp {transcoded_show_name} justin@192.168.1.115:/mnt/jellyfin/shows"
        process = subprocess.run(scp_transcode_video_cmd, shell=True, check=True)
        
        # step 5 clean up any left over files
        os.remove("show_names.txt")
        os.remove(show_name)
        os.remove(transcoded_show_name)

