'''Module containing useful GPS-related objects'''

from math import sqrt

import Objects_3D
from trig_degrees import *

DEGREE_SYMBOL = u'\N{DEGREE SIGN}'

class Point():
    '''Defines a GPS_Point object'''
    def __init__(self, lat, lon=None):
        '''Initialises the GPS_Point object'''
        if type(lat) in [Objects_3D.Vector, Objects_3D.Point] and not lon:
            # Point constructor can be passed a Vector/Point to convert to GPS
            p = Objects_3D.Point(lat)
            self.lat = atan2(p.z, sqrt(p.x ** 2 + p.y ** 2))
            self.lon = atan2(p.y, p.x)
        elif type(lat) is Point and not lon:
            # Point constructor can be passed another GPS Point to copy
            g = lat
            self.lat = g.lat
            self.lon = g.lon
        elif [type(arg) in [int, float] for arg in [lat, lon]] == [True] * 2:
            # Point constructor can be passed lat, lon values to store
            self.lat = lat
            self.lon = lon
        else:
            # Point constructor hasn't been given valid parameters
            raise ValueError("Invalid Arguments to Objects_GPS.Point __init__ function")
    
    def __str__(self):
        '''Returns a string of the GPS_Point object'''
        return "GPS Point: {0}{4}{1}, {2}{4}{3}".format(abs(self.lat), ['S', 'N'][self.lat >= 0], abs(self.lon), ['W', 'E'][self.lon >= 0], DEGREE_SYMBOL)
    
    def __repr__(self):
        '''returns a representation of the GPS_Point object'''
        return "GPS_Point({}, {})".format(self.lat, self.lon)