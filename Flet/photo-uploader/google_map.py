import requests, os
from dotenv import load_dotenv

load_dotenv()

def get_location_info(latitude, longitude):
    
    api_key = os.environ.get("GOOGLE_MAP_API_KEY")
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if data["status"] == "OK":
            country, region, city, detail = '','','',''
            results = data["results"]
            for result in results:
                for component in result["address_components"]:
                    if "country" in component["types"]:
                        country = component["long_name"]
                    if "administrative_area_level_1" in component["types"]:
                        region = component["long_name"]
                    if "locality" in component["types"]:
                        city = component["long_name"]
                    if "sublocality" in component["types"]:
                        detail = component["long_name"]
            return country, region, city, detail
        else:
            print("Geocoding API request failed.")
            return None, None

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None, None


if __name__ == "__main__":
    print(get_location_info(37.6205122,126.6988405))
    
    