
from pathlib import Path
import purpleair
import nominatim
import time
import urllib
from calculations import concentration_to_AQI

def run() -> None:
    'Main method for project 3'
    location, radius, threshold_aqi, max_number, _purpleair, reverse_geocode = _info()
    d = _create_dictionary(location, radius, threshold_aqi, max_number, _purpleair, reverse_geocode)
    data = None
    try:
        data = _get_data(d)
    except:
        pass
    if not data:
        return
    _handle_printing(d, data)
    

def _handle_printing(d: dict, data: list | dict) -> None:
    "Correctly prints the information of interst, including the location and AQI's of nearby sensors"
    _print_center(d['location'])
    if 'purpleair_key' in d.keys():
        _print_url_data(data, d)
    else:
        _print_file_data(data, d)
            

    
def _print_file_data(data: list, d: dict) -> None:
    'Prints the information of sensors when the purpleair.json file is used'
    for i in range(len(data)):
        try:
            print(f'AQI {int(concentration_to_AQI(data[i][4]))}')
            print(f"{data[i][2]}/N {-1*data[i][3]}/W")
            if Path(d['reverse'][i]).exists() == True:
                if type(d['reverse']) == list:
                    print(nominatim.File(d['reverse'][i]).reverse_geocode())
                else:
                    print(nominatim.Url(None, data[i][2], data[i][3]).reverse_geocode())
            else:
                _print_missing_issue(d['reverse'][i])
                
            time.sleep(1)
        except:
            _print_format_issue(d['reverse'][i])
            return

def _print_missing_issue(error_path: str) -> None:
    print('FAILED')
    print(error_path)
    print('MISSING')

def _print_format_issue(error_path: str) -> None:
    print('FAILED')
    print(error_path)
    print('FORMAT')

def _print_url_data(data: list, d: dict) -> None:
    'Prints the information of sensors when the purpleair API is used'
    for i in range(len(data)):
        print(f"AQI {int(concentration_to_AQI(data[i]['pm2.5']))}")
        print(f"{data[i]['latitude']}/N {-1*data[i]['longitude']}/W")
        if type(d['reverse']) == list:
            print(nominatim.File(d['reverse'][i]).reverse_geocode())
        else:
            print(nominatim.Url(None, data[i]['latitude'], data[i]['longitude']).reverse_geocode())
        time.sleep(1)
        
def _get_data(d: dict) -> dict:
    'Returns a ditionary containing all of the important information entered by the user'
    if 'purpleair_key' in d.keys():
        x = purpleair.Url(d['range'], d['center'], d['threshold_aqi'], d['max'], d['purpleair_key'])
        return x.data()
    else:
        x = purpleair.File(d['purpleair_path'], d['range'], d['center'], d['max'], d['threshold_aqi'])
        return x.data()


def _print_center(location) -> None:
    'Prints the center location'
    lat, lon = location.forward_geocode()
    print(f'CENTER {lat}/N {abs(float(lon))}/W')
    
def _info() -> tuple:
    'Returns a tuple containg the important information inputted by the user'
    location = input().split()[1:]
    radius = input().split()[1]
    threshold_aqi = input().split()[1]
    max_number = input().split()[1]
    purpleair = input().split()[1:]
    reverse_geocode = input().split()[1:]
    return location, radius, threshold_aqi, max_number, purpleair, reverse_geocode

def _create_dictionary(location, radius, threshold_aqi, max_number, purpleair, reverse_geocode) -> dict:
    'Creates a dictionary with the user entered information'
    d = {}
    d = _location(d, location)
    d['center'] = d['location'].forward_geocode()   
    d['range'] = int(radius)
    d['threshold_aqi'] = int(threshold_aqi)
    d['max'] = int(max_number)
    d = _get_purpleair(d, purpleair)
    d = _reverse(d, reverse_geocode)
    return d

def _location(d: dict, location: list) -> dict:
    '''Depending on the user input, makes a location key and assigns to it an
    object of either the nominatim.Url class or the nominatim.File class'''
    if location[0] == 'NOMINATIM':
        d['location'] = nominatim.Url(' '.join(location[1:]), None, None)
    else:
        d['location'] = nominatim.File(location[1])
    return d

def _get_purpleair(d: dict, purpleair: list) -> dict:
    'Depending on the user input, makes a key referring to the purpleair_key or the purpleair_path'
    if purpleair[0] == 'PURPLEAIR':
        d['purpleair_key'] = purpleair[1]
    else:
        d['purpleair_path'] = ' '.join(purpleair[1:])
    return d

def _reverse(d: dict, reverse_geocode: list) -> dict:
    ''''Depending on the user input, makes a reverse key and assigns to it
    either a list to files or "NOMINATIM", which will help us identify what
    to do for reverse geocoding'''
    if reverse_geocode[0] == 'NOMINATIM':
        d['reverse'] = reverse_geocode[0]
    else:
        d['reverse'] = reverse_geocode[1:]
    return d
        
if __name__ == '__main__':
    run()


