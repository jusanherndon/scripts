import os
import subprocess
import json

# step 1: send video file or files with input list to this directory



# step 2: take all needed inputs for this script

#shows_path = os.path.abspath("/home/justin/git/scripts/transcoding/shows.txt")
show_path = os.path.abspath("/home/justin/git/shows.txt")
with open(show_path, 'r') as shows:
    for show in shows.readlines():

        # step 3: find all ffmpeg streams inside of the video file or files


        # step 4: use the json output to generate the needed map identifying how many streams are needed for transcoding comamnd
        # and figure out placement of said strams like this ex. 0:0 video  0:1 audio 0:2 sub 0:x end of subtitles



        # step 5: use ffmeg to transcode the video file from HEV.264 to HEVC.265 with perserving the video, audio, and subtitle streams


