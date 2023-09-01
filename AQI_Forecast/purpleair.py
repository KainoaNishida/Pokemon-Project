from pathlib import Path
import json
from calculations import equirectangular_distance
from calculations import lat_and_lon_boundary
from calculations import concentration_to_AQI
import urllib.parse
import urllib.request

'''The purpleair interface allows two classes,
   the File class and the Url class, to have two similar methods
   called sensors() and data(). While the implementation is
   different depending on the type of object it is called
   by, it produces the same result. The sensors() method returns
   all sensors in a restricted area and the data() method
   returns the data of all the sensors in that same restricted area'''


class File:
    def __init__(self, path: str, mile_radius: int, center: tuple, max_number, threshold):
        self._path = path
        self._range = mile_radius
        self._lat = float(center[0])
        self._lon = float(center[1])
        self._max = max_number
        self._threshold = threshold
        
    def sensors(self) -> dict:
        'Returns a dictionary containing all of the sensors in a restricted area'
        return _file_sensors(self._path, self._lat, self._lon, self._range)

    def data(self) -> dict:
        'Returns the information of sensors in a restricted area'
        sensors = _file_sensors(self._path, self._lat, self._lon, self._range)
        if not sensors:
            return
        return _file_data(sensors, self._max, self._threshold)
            
class Url:
    def __init__(self, radius: int, center: tuple, threshold_aqi: float, max_number: int, purpleair_key: str):
        self._range = radius
        self._lat, self._lon = center
        self._threshold_aqi = threshold_aqi
        self._max = max_number
        self._purpleair_key = purpleair_key
        
    def sensors(self) -> dict:
        'Returns a dictionary containing all of the sensors in a restricted area'
        return _get_sensors(self._range, (self._lat, self._lon), self._purpleair_key)
    
    def data(self) -> dict:
        'Returns the information of sensors in a restricted area'
        sensors = _url_sensors(self._range, (self._lat, self._lon), self._purpleair_key)
        indexes = _limit_results(sensors, self._max, self._threshold_aqi)
        return _url_data(indexes, self._purpleair_key)
    
def _file_sensors(path: str, lat: float, lon: float, mile_range: int) -> list:
    '''Returns a list containing all of the sensors in bounded area
    for the File class'''
    file = None
    try:
        file = open(Path(path), 'r')
        try:
            content = file.read()
            data = json.loads(content)
        except json.decoder.JSONDecodeError:
            print('FAIlED')
            print(path)
            print('FORMAT')
            return None
        d = []
        for x in data['data']:
            try:
                distance = equirectangular_distance((lat, lon), (x[2], x[3]))
                if distance < mile_range:
                    d.append(x)
            except TypeError:
                pass
        return d
    except FileNotFoundError:
        pass
    finally:
        if file != None:
            file.close()

def _file_data(sensors: list, max_number: int, threshold: int) -> list:
    '''Returns the data of all sensors that are in a bounded area for
    the File class'''
    
    sensor_data = []
    for sensor in sensors:
        try:
            if concentration_to_AQI(sensor[4]) > threshold:
                sensor_data.append(sensor)
        except:
            pass
    return sensor_data[:max_number]

def _url_sensors(radius: int, center: tuple, purpleair_key: str) -> dict:
    '''Returns the sensors that are in a bounded area for
    the Url class'''
    
    selat, selng = lat_and_lon_boundary(radius, center)[0]
    nwlat, nwlng = lat_and_lon_boundary(radius, center)[1]
    query = urllib.parse.urlencode([('fields', 'latitude,longitude,pm2.5'),('nwlat', nwlat),('nwlng', nwlng),('selat', selat),('selng', selng)])
    url = f'https://api.purpleair.com/v1/sensors?{query}'
    request = urllib.request.Request(
            url,
            headers = { 'X-API-Key': purpleair_key }
            )
    response = None
    try:
        response = urllib.request.urlopen(request)
        obj = json.loads(response.read())
        return obj
    except urllib.error.HTTPError as error:
        print('ERROR')
        print(f'{error.status} {url}')
        print('NOT 200')
    finally:
        if response != None:
            response.close()

def _url_data(sensors: list, purpleair_key: str) -> list:
    '''Returns the data of all sensors that are in a bounded area for
    the Url class'''
    
    sensor_data = []
    for index in sensors:
        url = f'https://api.purpleair.com/v1/sensors/{index}?fields=latitude%2Clongitude%2Cpm2.5'
        request = urllib.request.Request(
            url,
            headers = { 'X-API-Key': purpleair_key }
            )
        response = None
        try:
            response = urllib.request.urlopen(request)
            obj = json.loads(response.read())
            sensor_data.append(obj['sensor'])
        except urllib.error.HTTPError as error:
            print('ERROR')
            print(f'{error.status} {url}')
            print('NOT 200')
        finally:
            if response != None:
                response.close()
    return sensor_data

def _limit_results(sensors: dict, max_number: int, threshold_aqi: int) -> list:
    'Limits the amount of interesting sensors to a specific amount'
    sensor_index = []
    for sensor in sensors['data']:
        try:
            if(concentration_to_AQI(sensor[3]) > threshold_aqi):
                sensor_index.append(sensor[0])
        except:
            pass
    return sensor_index[:max_number]

            
