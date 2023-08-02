import os, subprocess
from datetime import datetime

def get_exif_creation_dates_video(path):
    EXIFTOOL_DATE_TAG_VIDEOS = "Create Date"
    EXIF_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    absolute_path = os.path.join( os.getcwd(), path )

    process = subprocess.Popen(["exiftool", absolute_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    lines = out.decode("utf-8").split("\n")
    for l in lines:
        if EXIFTOOL_DATE_TAG_VIDEOS in str(l):
                datetime_str = str(l.split(" : ")[1].strip())
                dt = datetime.strptime(datetime_str, EXIF_DATE_FORMAT)
                print(dt) #you will get 3 dates: Create Date, Track Create Date and Media Create Date 
                
get_exif_creation_dates_video('/home/ubuntu/AWS-Training/Flet/photo_uploader/hyunsoo-files/20211013_111135.mp4')