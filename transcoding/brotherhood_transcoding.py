import os
import subprocess
import time

show_path = os.path.abspath("/home/justin/show_names_fma.txt")
with open(show_path, 'r') as shows:
    for show in shows.readlines():

        # Match on just the show name so that was the file name looks nicer for the jellyfin server
        transcoded_show_name = f"transcoded_{show.strip()}"

        # step 3: Transcode the video using the old video as its base

        ffmpeg_cmd = f'ffmpeg -vaapi_device /dev/dri/renderD128 -i ~/Fullmetal_Alchemist_Brotherhood/"{show.strip()}" -x265-params "pass=1" -c:v hevc_amf -min_qp_p 20 -max_qp_p 23 -min_qp_i 20 -max_qp_i 23 -an -f null /dev/null && ffmpeg -vaapi_device /dev/dri/renderD128 -i ~/Fullmetal_Alchemist_Brotherhood/"{show.strip()}" -map_metadata 0:g -x265-params "pass=2" -map 0:0 -c:v hevc_amf -min_qp_p 20 -max_qp_p 23 -min_qp_i 20 -max_qp_i 23 -map 0:1 -c:a copy -map 0:2 -c:a copy -map 0:3 -c:a copy -map 0:4 -c:a copy -map 0:5 -c:a copy -map 0:6 -c:s copy -map 0:7 -c:s copy "{transcoded_show_name}"'
        process = subprocess.run(ffmpeg_cmd, shell=True, check=True)

        # step 4: send new video file to the jellyfin media server
        scp_transcode_video_cmd = f"scp '{transcoded_show_name}' justin@192.168.1.115:/mnt/jellyfin/shows/Fullmetal\ Alchemist\ Brotherhood/"
        process = subprocess.run(scp_transcode_video_cmd, shell=True, check=True)
        
        # step 5 clean up any left over files
        os.remove(f'Fullmetal_Alchemist_Brotherhood/{show.strip()}')
        os.remove(f'{transcoded_show_name}')
        time.sleep(240)
# Do this removal at the end, since its the enitre show name file
os.remove("show_names.txt")
