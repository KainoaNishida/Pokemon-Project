
from pathlib import Path
import json
import urllib.request

'''The nominatim interface allows two classes,
   the File class and the Url class, to share two
   method called forward_geocode() and
   reverse_geocode(). While the implementation
   for each class is different, the two methods
   produce the same results for objects of both classes.'''

class File:
    def __init__(self, s: str):
        self._path = Path(s)
        data = _download_data(self._path)
        self._data = data

    def forward_geocode(self):
        'Returns latitude and longitude of location'
        if self._data != None:
            return self._data[0]['lat'], self._data[0]['lon']

    def reverse_geocode(self):
        'Returns name of location'
        if self._data != None:
            return self._data['display_name']

class Url:
    def __init__(self, location, lat, lon):
        self._location = location
        self._lat = lat
        self._lon = lon

    def forward_geocode(self):
        'Returns latitude and longitude of location'
        
        query = urllib.parse.urlencode([('q', self._location), ('format', 'json')])
        _url = f'https://nominatim.openstreetmap.org/search?{query}'
        request = urllib.request.Request(_url)
        response = None
        try:
            response = urllib.request.urlopen(request)
            obj = json.loads(response.read())[0]
            self._lat = float(obj['lat'])
            self._lon = float(obj['lon'])
            return self._lat, self._lon
        
        except urllib.error.HTTPError as error:
            print('FAILED')
            print(f'{error.status} {url}')
            print('NOT 200')

        except urllib.error.URLError:
            print('FAILED')
            print(_url)
            print('NETWORK')
        
        finally:
            if response != None:
                response.close()

    def reverse_geocode(self):
        'Returns name of location'
        
        query = urllib.parse.urlencode([('lat', self._lat), ('lon', self._lon),('format', 'json')])
        request = urllib.request.Request(f'https://nominatim.openstreetmap.org/reverse?{query}')
        response = None
        try:
            response = urllib.request.urlopen(request)
            obj = json.loads(response.read())
            name = obj['display_name']
            self._location = name
            return name
        except urllib.error.HTTPError as error:
            print('FAILED')
            print(f'{error.status} {url}')
            print('NOT 200')
        finally:
            if response != None:
                response.close()



def _download_data(path: Path) -> dict:
    'Returns a dictionary with the information from a file'
    try:
        x = open(path, 'r')
        y = json.loads(x.read())
        return y
    except FileNotFoundError:
        print('FAILED')
        print(path)
        print('MISSING')
    
