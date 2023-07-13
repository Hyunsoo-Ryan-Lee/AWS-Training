from PIL import Image
from PIL.ExifTags import TAGS

imagename = "/home/ubuntu/AWS-Training/Flet/others/images/KakaoTalk_20230705_140133474.jpg"
# open the image
image = Image.open(imagename)
exifdata = image.getexif()
for tagid in exifdata:
    tagname = TAGS.get(tagid, tagid)
    value = exifdata.get(tagid)
    print(f"{tagname:25}: {value}")