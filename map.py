from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
geolocator = Nominatim(user_agent="main.py")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
import info_twitter


def get_locations_and_names(f_dict):
    """
    (dict) -> dict
    This function returns a dictionary where the keys are
    the location of the friend and the values are
    their screen names (nicknames).
    """
    locations_dict = {}
    for friend in f_dict["users"]:
        location = info_twitter.analyze_dictionary(friend['screen_name'],
                                                         "location", f_dict)
        if location[-1] == ' ':
            location = location[:-1]

        if location not in locations_dict:
            locations_dict[location] = []
        locations_dict[location].append(friend['screen_name'])
    return locations_dict


def find_coordinates(location):
    """
    (str) -> (str, str)
    This function returns the coordinates of the location.
    >>> find_coordinates('Lviv, Ukraine')
    (49.841952, 24.0315921)
    >>> find_coordinates('Toronto')
    (43.653963, -79.387207)
    >>> find_coordinates('')

    """
    try:
        coordinates = geolocator.geocode(location, timeout=3)
        return (coordinates.latitude, coordinates.longitude)
    except Exception:
        return None


def prepearing(f_dict):
    """
    (dict) -> list, list, list
    This function returns individual lists of
    longitudes, latitudes, and nicknames (screen names)
    of user friends.
    """
    lat_lst = []
    lon_lst = []
    name_lst = []
    counter = 0

    locations_dict = get_locations_and_names(f_dict)
    for location in locations_dict:
        name = locations_dict[location]
        name_str = ""
        for el in name:
            name_str += el + ", "
        name_lst.append(name_str[:-2])

    for location in locations_dict:
        if find_coordinates(location) == None:
            name_lst.pop(counter)
            continue
        else:
            lat, lon = find_coordinates(location)
            lat_lst.append(lat)
            lon_lst.append(lon)
        counter += 1

    return lat_lst, lon_lst, name_lst


def web_map(f_dict):
    """
    (dict, str, str) ->
    This function generates a web map (html page)
    by using module folium.
    """
    lat_lst, lon_lst, name_lst = prepearing(f_dict)

    map = folium.Map(min_zoom=2)
    fg = folium.FeatureGroup(name='Locations of your friends on Twitter')

    for lt, ln, fl in zip(lat_lst, lon_lst, name_lst):
        fg.add_child(folium.Marker(location=[lt, ln], radius=10, popup=fl))

    map.add_child(fg)
    map.add_child(folium.LayerControl())

    html_string = map.get_root().render()
    return html_string
