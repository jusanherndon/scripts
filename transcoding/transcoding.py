import os
import shutil
import subprocess
import re
import time

# Step 1: get the show names file from the NAS
show_path = os.path.abspath("/mnt/nas/show_names.txt")
with open(show_path, 'r') as shows:
    for show in shows.readlines():

        # Match on two things: show name and episode and just the show name
        show_name_and_episode_list = re.findall("(?=\ )(.*?)(?=\()", show.strip())
        # Adding this try except block to handle shows names with (year) in their names
        try:
            show_name_and_episode = f"{show_name_and_episode_list[0]}{show_name_and_episode_list[1].strip()}"
        except:
            show_name_and_episode = f"{show_name_and_episode_list[0]}")

        show_name_regex = re.findall("(?<=\ )(.*?)(?=\ - [0-9][0-9])", show_name_and_episode)
        show_name = f"{show_name_regex[0].strip()}.mkv"
        transcoded_show_name = f"transcoded_{show_name_and_episode.strip()}"

        #copy over the video file to this pc
        scp_video_cmd = f"scp justin@192.168.1.237:/media/deluge/Downloads/'{show.strip()}' /home/justin/'{show_name_and_episode}'"
        process = subprocess.run(scp_video_cmd, shell=True, check=True)

        # step 3: Transcode the video using the old video as its base

        ffmpeg_cmd = f'ffmpeg -vaapi_device /dev/dri/renderD128 -i "{show_name_and_episode}" -x265-params "pass=1" -c:v hevc_amf -rc cqp -qp_i 20 -qp_p 20 -an -f null /dev/null && ffmpeg -vaapi_device /dev/dri/renderD128 -i "{show_name_and_episode}" -map_metadata 0:g -x265-params "pass=2" -c:v hevc_amf -rc cqp -qp_p 20 -qp_i 20 -c:a aac "{transcoded_show_name}"'
        process = subprocess.run(ffmpeg_cmd, shell=True, check=True)

        # step 4: send new video file to the NAS
        if(os.path.isdir(f'/mnt/nas/seasonal_shows/{show_name}')):
            shutil.move(f'/home/justin/{transcoded_show_name}', f'/mnt/nas/seasonal_shows/{show_name}')
        else:
            os.makedirs(f'/mnt/nas/seasonal_shows/{show_name}')
            shutil.move(f'/home/justin/{transcoded_show_name}', f'/mnt/nas/seasonal_shows/{show_name}')

        # step 5 clean up any left over files
        os.remove(f'{show_name_and_episode}')

        time.sleep(300)
# Do this removal at the end, since its the enitre show name file
os.remove("/mnt/nas/show_names.txt")

