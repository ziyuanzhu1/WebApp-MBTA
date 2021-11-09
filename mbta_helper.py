# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
# MAPQUEST_API_KEY = "0q3lFn7pClG306mHknq4rBKmkbxLR1oM"
# MBTA_API_KEY = "657bf8f403c94b85840a00af815a4583"

import urllib.request
import json
from pprint import pprint

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """
    MAPQUEST_API_KEY = "0q3lFn7pClG306mHknq4rBKmkbxLR1oM"
    place = {'location': place_name}
    result = urllib.parse.urlencode(place)
    url = f"http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&{result}"
    json = get_json(url)
    latitude = json["results"][0]["locations"][0]["latLng"]["lat"]
    longitude = json["results"][0]["locations"][0]["latLng"]["lng"]
    return (latitude,longitude)

print(get_lat_long("malden"))

def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """
    MBTA_API_KEY = "657bf8f403c94b85840a00af815a4583"
    lat = {'latitude': latitude}
    long = {'longitude':longitude}
    result_lat = urllib.parse.urlencode(lat)
    result_long = urllib.parse.urlencode(long)
    url = f"https://api-v3.mbta.com/stops?api_key={MBTA_API_KEY}&{result_lat}&{result_long}"
    json = get_json(url)
    station_name = json['data'][0]['attributes']['name']
    wheelchair_accessible  = json['data'][0]['attributes']['wheelchair_boarding']
    return (station_name, wheelchair_accessible)

print(get_nearest_station(42.426499, -71.073534))


def find_stop_near(place_name):
    """" Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible."""
    latitude_longitude = get_lat_long(place_name)
    station = get_nearest_station(*latitude_longitude)
    if station[1] == 1: 
        return f'The nearest station is {station[0]} and it is wheelchair accessible.'
    if station[1] == 2: 
        return f'The nearest station is {station[0]} and it is not wheelchair accessible'
    if station[1] == 0: 
        return f'The nearest station is {station[0]} and there is no information on whether or not it is wheelchair accessible'
    if station == 1: 
        return "There are no close stations nearby"
    
print(find_stop_near('Malden'))

def main():
    pass
#     """
#     You can test all the functions here
#     """
#     print(get_lat_long('Boston College'))

#     print(find_stop_near('Walnut'))

if __name__ == '__main__':
    main()
