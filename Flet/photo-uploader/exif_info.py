import os, re
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS

upload_path = "hyunsoo-files"

# Helper function
def create_google_maps_url(gps_coords):
    # Exif data stores coordinates in degree/minutes/seconds format. To convert to decimal degrees.
    # We extract the data from the dictionary we sent to this function for latitudinal data.
    dec_deg_lat = convert_decimal_degrees(
        float(gps_coords["lat"][0]),
        float(gps_coords["lat"][1]),
        float(gps_coords["lat"][2]),
        gps_coords["lat_ref"],
    )
    # We extract the data from the dictionary we sent to this function for longitudinal data.
    dec_deg_lon = convert_decimal_degrees(
        float(gps_coords["lon"][0]),
        float(gps_coords["lon"][1]),
        float(gps_coords["lon"][2]),
        gps_coords["lon_ref"],
    )
    # We return a search string which can be used in Google Maps
    return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"


# Converting to decimal degrees for latitude and longitude is from degree/minutes/seconds format is the same for latitude and longitude. So we use DRY principles, and create a seperate function.
def convert_decimal_degrees(degree, minutes, seconds, direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    # A value of "S" for South or West will be multiplied by -1
    if direction == "S" or direction == "W":
        decimal_degrees *= -1
    return decimal_degrees


def get_exif(file):
    exif_dict = {}
    try:
        gps_coords = {}
        _path = os.path.join(upload_path, file)
        image = Image.open(_path)
        exif_dict['type'] = 'photos'
        if image._getexif() == None:
            print(f"{file} contains no exif data.")
            # Strongly fix the datetime string type with regex
            pattern = r"202([0-9])(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])"
            match = re.search(pattern, file)
            try:
                if len(match.group()) == 8:
                    exif_dict['DateTime'] = match.group()
                else: pass
            except:
                print(f"{file} : (Photo)정규표현식 추출가능 문자열 없음")
        # If exif data are defined we can cycle through the tag, and value for the file.
        else:
            pattern = r"202([0-9])(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])"
            match = re.search(pattern, file)
            for tag, value in image._getexif().items():
                tag_name = TAGS.get(tag)
                try:
                    if 'DateTime' in tag_name:
                        exif_dict['DateTime'] = value
                except Exception as e:
                    print(e)
            if len(exif_dict) == 1:
                if match:
                    exif_dict['DateTime'] = match.group()
                # if tag_name == "GPSInfo":
                #     for key, val in value.items():
                #         exif_dict[GPSTAGS.get(key)] = val
                #         if GPSTAGS.get(key) == "GPSLatitude":
                #             gps_coords["lat"] = val
                #         elif GPSTAGS.get(key) == "GPSLongitude":
                #             gps_coords["lon"] = val
                #         elif GPSTAGS.get(key) == "GPSLatitudeRef":
                #             gps_coords["lat_ref"] = val
                #         elif GPSTAGS.get(key) == "GPSLongitudeRef":
                #             gps_coords["lon_ref"] = val
                # else:
                #     exif_dict[tag_name] = value
            # if gps_coords:
            #     try:
            #         # print(create_google_maps_url(gps_coords))
            #         exif_dict["google_map"] = create_google_maps_url(gps_coords)
            #     except:
            #         exif_dict["google_map"] = ""
    except IOError:
        print("Video Format")
        exif_dict['type'] = 'video'
        pattern = r"202([0-9])(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])"
        match = re.search(pattern, file)
        try:
            if match:
                exif_dict['DateTime'] = match.group()
            else:
                print(f"{file} : (Video)정규표현식 추출가능 문자열 없음")
        except Exception as e:
            print(e)
    return exif_dict
        
if __name__ == "__main__":
    files = os.listdir(upload_path)
    for file in files:
        print(
                f"_______________________________________________________________{file}_______________________________________________________________"
            )
        exif_dict = get_exif(file)
        print(exif_dict)