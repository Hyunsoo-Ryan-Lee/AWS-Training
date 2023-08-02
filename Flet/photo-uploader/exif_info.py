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
            for tag, value in image._getexif().items():
                # If you print the tag without running it through the TAGS.get() method you'll get numerical values for every tag. We want the tags in human-readable form.
                # You can see the tags and the associated decimal number in the exif standard here: https://exiv2.org/tags.html
                tag_name = TAGS.get(tag)
                if tag_name == "GPSInfo":
                    for key, val in value.items():
                        # Print the GPS Data value for every key to the screen.
                        # print(f"{GPSTAGS.get(key)} - {val}")
                        exif_dict[GPSTAGS.get(key)] = val
                        # We add Latitude data to the gps_coord dictionary which we initialized in line 110.
                        if GPSTAGS.get(key) == "GPSLatitude":
                            gps_coords["lat"] = val
                        # We add Longitude data to the gps_coord dictionary which we initialized in line 110.
                        elif GPSTAGS.get(key) == "GPSLongitude":
                            gps_coords["lon"] = val
                        # We add Latitude reference data to the gps_coord dictionary which we initialized in line 110.
                        elif GPSTAGS.get(key) == "GPSLatitudeRef":
                            gps_coords["lat_ref"] = val
                        # We add Longitude reference data to the gps_coord dictionary which we initialized in line 110.
                        elif GPSTAGS.get(key) == "GPSLongitudeRef":
                            gps_coords["lon_ref"] = val
                else:
                    # We print data not related to the GPSInfo.
                    # print(f"{tag_name} - {value}")
                    exif_dict[tag_name] = value
            # We print the longitudinal and latitudinal data which has been formatted for Google Maps. We only do so if the GPS Coordinates exists.
            if gps_coords:
                try:
                    # print(create_google_maps_url(gps_coords))
                    exif_dict["google_map"] = create_google_maps_url(gps_coords)
                except:
                    exif_dict["google_map"] = ""
        # Change back to the original working directory.
    except IOError:
        print("Video Format")
        pattern = r"202([0-9])(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])"
        match = re.search(pattern, file)
        try:
            if len(match.group()) == 8:
                exif_dict['DateTime'] = match.group()
                exif_dict['type'] = 'video'
            else: pass
        except:
            print(f"{file} : (Video)정규표현식 추출가능 문자열 없음")
    return exif_dict
        
if __name__ == "__main__":
    files = os.listdir(upload_path)
    for file in files:
        print(
                f"_______________________________________________________________{file}_______________________________________________________________"
            )
        exif_dict = get_exif(file)
        print(exif_dict)
