
import math
earth_radius = 3958.8

def lat_and_lon_boundary(mile: int, center: tuple) -> tuple:
    '''returns a tuple where the first element is a tuple representing
       the SE bounding coordinate,
       and the second element is the NW bounding coordinate'''
    lat = float(center[0])
    lon = float(center[1])
    d = distance_to_angle(int(mile))
    SE_bound = (lat - d, lon + d)
    NW_bound = (lat + d, lon - d)
    return SE_bound, NW_bound

def equirectangular_distance(p1: 'point', p2: 'point') -> float:
    dlat, alat = _latitude_distance_and_average(p1, p2)
    dlon = _longitude_distance(p1, p2)
    x = dlon * math.cos(alat)
    d = math.sqrt(x**2 + dlat**2) * earth_radius
    return d

def distance_to_angle(mile_radius: float) -> float:
    '''assume dlon and dlat are equal. We'll represent dlon and dlat as d'''
    return _mile_to_degrees(mile_radius)

def _degrees_to_radians(degrees: float) -> float:
    return degrees * math.pi / 180

def _latitude_distance_and_average(p1, p2) -> tuple:
    l1 = _degrees_to_radians(p1[0])
    l2 = _degrees_to_radians(p2[0])
    return abs(l2 - l1), (l2 + l1)/2

def _longitude_distance(p1, p2) -> float:
    l1 = _degrees_to_radians(p1[1])
    l2 = _degrees_to_radians(p2[1])
    return abs(l2 - l1)

def _mile_to_degrees(mile: int) -> float:
    'Converts a mile distance to a change in latitude and longitude degree'
    return mile/69.0
    
def _round(num: float) -> int:
    '''Consistently rounds a decimal according the rule
    that any decimal above or equal to 0.5 is rounded up.'''
    decimal = round(num % 1, 1)
    if decimal < .5:
        return math.floor(num)
    return math.ceil(num)
    
def _y_intercept(slope, y1, x1) -> float:
    '''Returns the y interecept of an equation
    that will determine the AQI value from
    a pm2.5 concentration'''
    return y1 - slope*x1

def _equation(y2, y1, x2, x1) -> tuple:
    '''Returns the slope and y_intercept of
    a linear equation that will determine the
    AQI value from a pm2.5 concentration'''
    slope = (y2 - y1)/(x2 - x1)
    y_intercept = _y_intercept(slope, y1, x1)
    return slope, y_intercept

def _calculate_AQI(equation: tuple, concentration: float) -> int:
    'Calculates the AQI of a specific pm2.5 concentration'
    slope, y_intercept = equation
    return _round(slope * concentration + y_intercept)

def concentration_to_AQI(concentration: float) -> int:
    'Calculates the AQI value of any pm2.5 concentration'
    if(12.1 > concentration >= 0):
        return _calculate_AQI(_equation(50,0,12.0,0), concentration)
    elif(concentration < 35.5):
        return _calculate_AQI(_equation(100,51,35.4,12.1), concentration)
    elif(concentration < 55.5):
        return _calculate_AQI(_equation(150,101,55.4,35.5), concentration)
    elif(concentration < 150.5):
        return _calculate_AQI(_equation(200,151,150.4,55.5), concentration)
    elif(concentration < 250.5):
        return _calculate_AQI(_equation(300,201,250.4,150.5), concentration)
    elif(concentration < 350.5):
        return _calculate_AQI(_equation(400,301,350.4,250.5), concentration)
    elif(concentration < 500.5):
        return _calculate_AQI(_equation(500,401,500.4,350.5), concentration)
    else:
        return 501


'''assert statements for the
   concentration_to_AQI() method'''

assert concentration_to_AQI(0) == 0
assert concentration_to_AQI(12.0) == 50
assert concentration_to_AQI(12.1) == 51
assert concentration_to_AQI(35.4) == 100
assert concentration_to_AQI(35.5) == 101
assert concentration_to_AQI(55.4) == 150
assert concentration_to_AQI(55.5) == 151
assert concentration_to_AQI(150.4) == 200
assert concentration_to_AQI(150.5) == 201
assert concentration_to_AQI(250.4) == 300
assert concentration_to_AQI(250.5) == 301
assert concentration_to_AQI(350.4) == 400
assert concentration_to_AQI(350.5) == 401
assert concentration_to_AQI(500.4) == 500
assert concentration_to_AQI(500.6) == 501
assert concentration_to_AQI(6.0) == 25
assert concentration_to_AQI(23.75) == 76
assert concentration_to_AQI(45.45) == 126
assert concentration_to_AQI(102.95) == 176
assert concentration_to_AQI(200.45) == 251
assert concentration_to_AQI(300.45) == 351
assert concentration_to_AQI(425.45) == 451

'''assert statements for the
   equirectangular_distance() method'''

assert equirectangular_distance((50.06639,5.714722),(58.64389,3.07)) == 602.1458822793489
assert equirectangular_distance((0,0),(0,0)) == 0

'''assert statements for the
   distance_to_angle() method and
   the lat_and_lon_boundary() method'''

assert distance_to_angle(50) == 0.7246376811594203
assert distance_to_angle(100) == 1.4492753623188406
assert lat_and_lon_boundary(100, (50, 50)) == ((48.55072463768116, 51.44927536231884), (51.44927536231884, 48.55072463768116))
assert equirectangular_distance((48.55072463768116, 51.44927536231884), (51.44927536231884, 48.55072463768116)) == 238.07837360240364
# The reason as to why lat_and_lon_boundary and equirectangular_distance are not exactly irreversible
# is because I treated longitude and latitude as identical measurements, when in reality they are not completely
# interchangable. This is to ensure that I did not leave any sensors out of data because I overcalculate the
# radius of interest.
