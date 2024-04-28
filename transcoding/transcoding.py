import os
import subprocess
import re

# step 1: send video file or files with input list to this directory



# step 2: take all needed inputs for this script

#shows_path = os.path.abspath("/home/justin/git/scripts/transcoding/shows.txt")
show_path = os.path.abspath("/home/justin/git/shows.txt")
with open(show_path, 'r') as shows:
    for show in shows.readlines():

        show_name_and_episode = re.findall("(?<=\])(.*?)(?=\()", show)

        if(re_match):
            transcoded_show_name = str(show_name_and_episode[0]).replace("-", " ").replace(" ", "_" )

        # I think a found a flag that can invalidate steps 3 and 4, so here is the new order
        # step 3: Transcode the video using the old video as its base

        ffmpeg_cmd = f'ffmpeg -vaapi_device /dev/dri/renderD128 -i {show} -c:v hevc_amf -x265-params "pass=1:lossless=1" -an -f null /dev/null && ffmpeg -vaapi_device /dev/dri/renderD128 -i {show} -c:v hevc_amf -c:a aac -map_metadata 0:g -x265-params "pass=2:lossless=1" {transcoded_show_name}.mkv'
        process = subprocess.Popen(ffprobe_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)

        # step 4: send new video file to the jellyfin media server


