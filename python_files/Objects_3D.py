'''Module containing useful 3D geometric objects'''

from math import isclose, sqrt

SQUARED_SYMBOL = u"\u00B2"

class Point():
    '''Defines a Point object in 3D space'''
    def __init__(self, x, y=None, z=None):
        '''Initialises the Point object'''
        if type(x) is Point and not (y or z):
            # Point constructor can be passed another Point object to copy
            p = x
            self.x = p.x
            self.y = p.y
            self.z = p.z        
        elif [type(arg) in [int, float] for arg in [x, y, z]] == [True] * 3:
            # Point constructor can be passed the x, y, z values to store
            self.x = x
            self.y = y
            self.z = z
        elif type(x) is Vector and not (y or z):
            # Point constructor can be passed a Vector to convert to a Point
            v = x
            self.x = v.x
            self.y = v.y
            self.z = v.z
        else:
            # Point constructor hasn't been given valid parameters
            raise ValueError("Invalid Arguments to Objects_3D.Point __init__ function")
    
    def __str__(self):
        '''returns a string of the Point object'''
        return "Point: ({}, {}, {})".format(self.x, self.y, self.z)
    
    def __repr__(self):
        '''returns a representation of the Point object'''
        return "Point({}, {}, {})".format(self.x, self.y, self.z)
    
    def dist(p0, p1):
        '''returns the distance between Points p0 and p1'''
        return sqrt((p1.x - p0.x) ** 2 + 
                    (p1.y - p0.y) ** 2 + 
                    (p1.z - p0.z) ** 2)
    
    def square_dist(p0, p1):
        '''returns the distance between p0 and p1 squared, to avoid sqrt'''
        return (p1.x - p0.x) ** 2 + (p1.y - p0.y) ** 2 + (p1.z - p0.z) ** 2

class Vector():
    '''Defines a Vector object in 3D space'''
    def __init__(self, x, y=None, z=None):
        '''Initialises the Vector object'''
        if type(x) is Vector and not (y or z):
            # Vector constructor can be passed another Vector object to copy
            v = x
            self.x = v.x
            self.y = v.y
            self.z = v.z
        elif [type(arg) in [int, float] for arg in [x, y, z]] == [True] * 3:
            # Vector constructor can be passed the x, y, z values to store
            self.x = x
            self.y = y
            self.z = z
        elif type(x) is Point and not (y or z):
            # Vector constructor can be passed a Point to convert to a Vector
            p = x
            self.x = p.x
            self.y = p.y
            self.z = p.z
        else:
            # Vector constructor hasn't been given valid parameters
            raise ValueError("Invalid Arguments to Vector __init__ function")
    
    def __str__(self):
        '''returns a string of the Vector object'''
        return "Vector: <{}, {}, {}>".format(self.x, self.y, self.z)
    
    def __repr__(self):
        '''returns a representation of the Vector object'''
        return "Vector({}, {}, {})".format(self.x, self.y, self.z)
    
    def __add__(v0, v1):
        '''returns v0 + v1'''
        return Vector(v0.x + v1.x,
                      v0.y + v1.y,
                      v0.z + v1.z)
    
    def __mul__(v, k):
        '''returns v scaled by k'''
        return Vector(v.x * k,
                      v.y * k,
                      v.z * k)
    
    def __sub__(v0, v1):
        '''returns v0 - v1'''
        return v0 + (v1 * -1)
    
    def length(v):
        '''returns the length of vector v'''
        return sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2)
    
    def dot(v0, v1):
        '''returns the dot product of v0 and v1'''
        return (v0.x * v1.x + 
                v0.y * v1.y + 
                v0.z * v1.z)
    
    def cross(v0, v1):
        '''returns the cross product of v0 and v1'''
        return Vector(v0.y * v1.z - v0.z * v1.y, 
                      v0.z * v1.x - v0.x * v1.z, 
                      v0.x * v1.y - v0.y * v1.x)

class Plane():
    '''Defines a Plane object in 3D space'''
    def __init__(self, a, b, c, d=None):
        '''Initialises the Plane object'''
        if [type(arg) in [Point, Vector] for arg in [a, b, c]] == [True] * 3 and not d:
            # Plane constructor can be passed 3 Points/Vectors on plane surface
            v0, v1, v2 = Vector(a), Vector(b), Vector(c)
            normal = (v1 - v0).cross(v2 - v1)
            self.a = normal.x
            self.b = normal.y
            self.c = normal.z
            self.d = v1.dot(Vector(self.a, self.b, self.c))
        elif [type(arg) in [int, float] for arg in [a, b, c, d]] == [True] * 4:
            # Plane constructor can be passed the a, b, c, d values to store
            self.a = a
            self.b = b
            self.c = c
            self.d = d
        else:
            # Plane constructor hasn't been given valid parameters
            raise ValueError("Invalid Arguments to Plane __init__ function")
    
    def __str__(self):
        '''Returns a string of the Plane object'''
        return "Plane: {}x + {}y + {}z = {}".format(self.a, self.b, self.c, self.d)
    
    def __repr__(self):
        '''Returns a representation of the Plane object'''
        return "Plane({}, {}, {}, {})".format(self.a, self.b, self.c, self.d)
    
    def __eq__(P0, P1):
        '''returns if P0 and P1 are equivalent'''
        return (isclose(P1.d * P0.a, P0.d * P1.a) and 
                isclose(P1.d * P0.b, P0.d * P1.b) and 
                isclose(P1.d * P0.c, P0.d * P1.c))
    
    def normal(self):
        '''Returns the normal vector of the Plane object'''
        return Vector(self.a, self.b, self.c)
    
    def project(self, p):
        '''Returns the orthogonal projection of p onto the Plane object'''
        v = Vector(p)
        orthogonal = v.dot(self.normal()) / (self.a ** 2 + self.b ** 2 + self.c ** 2)
        return Point(v - self.normal() * orthogonal)
    
    def contains(self, p):
        '''Returns if Point p is on the Plane object'''
        # Useful for Debugging
        return isclose(self.a * p.x + self.b * p.y + self.c * p.z, self.d)

class Ellipsoid():
    '''Defines an Ellipsoid object in 3D space, centered on the origin'''
    def __init__(self, a, b, c):
        '''Initialises the Ellipsoid object'''
        self.a = a
        self.b = b
        self.c = c
    
    def __str__(self):
        '''Returns a string of the Ellipsoid object'''
        fmt = "Ellipsoid: x{3}/{0}{3} + y{3}/{1}{3} + z{3}/{2}{3} = 1"
        return fmt.format(self.a, self.b, self.c, SQUARED_SYMBOL)
    
    def __repr__(self):
        '''Returns a representation of the Ellipsoid object'''
        return "Ellipsoid({}, {}, {})".format(self.a, self.b, self.c)
    
    def tangent(self, p):
        '''returns the tangent plane of the Ellipsoid object at point p'''
        return Plane(p.x * self.b ** 2 * self.c ** 2, 
                     p.y * self.c ** 2 * self.a ** 2, 
                     p.z * self.a ** 2 * self.b ** 2, 
                     self.a ** 2 * self.b ** 2 * self.c ** 2)
    
    def project(self, p):
        '''returns p projected onto the Ellipsoid object'''
        # NOTE: This doesn't project orthogonally (to the nearest point on the ellipse)
        v = Vector(p)
        v = v * (1 / sqrt((v.x / self.a) ** 2 + 
                          (v.y / self.b) ** 2 + 
                          (v.z / self.c) ** 2))
        return Point(v)
    
    def scale_to_surface(self, p, v):
        ''' scales v so that p + kv is on ellipse surface, returns p + kv'''
        # Unpack Values
        a, b, c = self.a, self.b, self.c
        
        part1 = (b * c * v.x) ** 2 + (c * a * v.y) ** 2 + (a * b * v.z) ** 2
        part2 = ((a * (p.y * v.z - p.z * v.y)) ** 2 +
                 (b * (p.z * v.x - p.x * v.z)) ** 2 + 
                 (c * (p.x * v.y - p.y * v.x)) ** 2)
        discriminant = part1 - part2
        part3 = ((b * c) ** 2 * p.x * v.x + 
                 (c * a) ** 2 * p.y * v.y + 
                 (a * b) ** 2 * p.z * v.z)
        part4 = ((b * c * v.x) ** 2 + (c * a * v.y) ** 2 + (a * b * v.z) ** 2)
        k = (a * b * c * sqrt(discriminant) - part3) / part4
        return Point(Vector(p) + v * k)
    
    def contains(self, p):
        '''Returns if Point p is on the Ellipsoid object'''
        # Useful for Debugging
        result = (p.x / self.a) ** 2 + (p.y / self.b) ** 2 + (p.z / self.c) ** 2
        return isclose(result, 1)

class Sphere():
    '''Defines a Sphere object in 3D space, not centred on the origin'''
    def __init__(self, x, y, z=None, r=None):
        '''Initialises the Sphere object'''
        if type(x) is Point and type(y) is Point:
            # Sphere constructor can be passed two points on opposite sides of sphere
            p0, p1 = x, y
            self.c = Point((Vector(p0) + Vector(p1)) * (1 / 2))
            self.r = self.c.dist(p0)        
        elif type(x) is Point and not (z or r):
            # Sphere constructor can be passed a centre Point and a radius
            self.c = x
            self.r = y
        else:
            # Sphere constructor can be passed x, y, z Point values and a radius
            self.c = Point(x, y, z)
            self.r = r
    
    def __str__(self):
        '''Returns a string of the Sphere object'''
        fmt = "Sphere: (x - {0}){4} + (y - {1}){4} + (z - {2}){4} = {3}{4}"
        return fmt.format(self.c.x, self.c.y, self.c.z, self.r, SQUARED_SYMBOL)
    
    def __repr__(self):
        '''returns a representation of the Sphere object'''
        return "Sphere({}, {})".format(self.c, self.r)
    
    def inside(S, p):
        '''returns if Point p is inside the sphere object'''
        return S.c.square_dist(p) <= S.r ** 2

if __name__ == "__main__":
    print("This is just a handy module with points and lines.\nHave a nice day!")