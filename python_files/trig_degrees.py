'''Module containing versions of common trigonometric functions that 
either input or output angles in degrees, instead of radians'''

import math

def sin(a):
    '''Returns the sin of degree angle a'''
    return math.sin(math.radians(a))
def cos(a):
    '''Returns the cosine of degree angle a'''
    return math.cos(math.radians(a))
def tan(a):
    '''Returns the tangent of degree angle a'''
    return math.tan(math.radians(a))

def atan(m):
    '''Returns the arctangent of m in degrees'''
    return math.degrees(math.atan(m))
def atan2(y, x):
    '''Returns the angle between vector <x, y> and positive x-axis in degrees'''
    return math.degrees(math.atan2(y, x))