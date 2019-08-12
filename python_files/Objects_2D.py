'''Module containing useful 2D geometric objects'''

from math import isclose, sqrt

SQUARED_SYMBOL = u"\u00B2"

class Point():
    def __init__(self, x, y=None):
        '''Initialises the Point object'''
        if [type(arg) in [int, float] for arg in [x, y]] == [True] * 2:
            # Point constructor can be passed x, y values to store
            self.x = x
            self.y = y
        elif type(x) is Point and y is None:
            # Point constructor can be passed another Point to copy
            p = x
            self.x = p.x
            self.y = p.y
    
    def __str__(self):
        '''returns a string of the Point object'''
        return "Point: ({}, {})".format(self.x, self.y)
    
    def __repr__(self):
        '''returns a representation of the Point object'''
        return "Point({}, {})".format(self.x, self.y)
    
    def __eq__(p0, p1):
        return isclose(p0.x, p1.x) and isclose(p0.y, p1.y)
    
    def dist(p0, p1):
        '''returns the distance between p0 and p1'''
        return sqrt((p1.x - p0.x) ** 2 + 
                    (p1.y - p0.y) ** 2)

class Vector():
    def __init__(v, a, b=None):
        if type(a) in [Point, Vector] and not b:
            p = a
            v.x = p.x
            v.y = p.y
        else:
            v.x = a
            v.y = b
    def __add__(v0, v1):
        return Vector(v0.x + v1.x, v0.y + v1.y)
    def __mul__(v, k):
        return Vector(v.x * k, v.y * k)
    def __sub__(v0, v1):
        return v0 + v1 * -1
    def dot(v0, v1):
        return v0.x * v1.x + v0.y * v1.y
    def size(v):
        return sqrt(v.x**2 + v.y**2)
    def __repr__(v):
        return "Vector({}, {})".format(v.x, v.y)

class Line():
    def __init__(self, a, b=None, c=None):
        '''Initialises the Line object'''
        if type(a) is Point and type(b) is Point:
            # Line constructor can be passed two Points on the line
            p0, p1 = a, b
            self.a = p0.y - p1.y
            self.b = p1.x - p0.x
            self.c = p1.x * p0.y - p0.x * p1.y
        elif [type(x) is float or type(x) is int for x in [a, b, c]] == [True] * 3:
            # Line constructor can be passed the a, b, c values to store
            self.a = a
            self.b = b
            self.c = c
        elif type(a) is LineSegment and not (b or c):
            # Line constructor can be passed a line segment on the line
            S = a
            p0, p1 = S.p0, S.p1
            self.a = p0.y - p1.y
            self.b = p1.x - p0.x
            self.c = p1.x * p0.y - p0.x * p1.y
        else:
            # Line constructor hasn't been given valid parameters
            raise TypeError("Invalid Arguments Given. Must be three floating values (a, b, c) or two Point objects.")
    
    def __str__(self):
        '''returns a string of the Line object'''
        return "Line: {}x + {}y = {}".format(self.a, self.b, self.c)
    
    def __repr__(self):
        '''returns a representation of the Line object'''
        return "Line({}, {}, {})".format(self.a, self.b, self.c)
    
    def __eq__(L0, L1):
        '''returns if L0 and L1 are equivalent'''
        return isclose(L0.c * L1.a, L1.c * L0.a) and isclose(L0.c * L1.b, L1.c * L0.b)
    
    def distance_to(L0, p):
        '''returns the perpendicular distance between self and p'''
        if type(p) is Point:
            dist = (L0.a * p.x + L0.b * p.y - L0.c) / sqrt(L0.a ** 2 + L0.b ** 2)
            return dist
        elif type(p) is Line:
            L1 = p
            if L0.is_parallel(L1):
                return (L1.c / sqrt(L1.a ** 2 + L1.b ** 2) - 
                        L0.c / sqrt(L0.a ** 2 + L0.b ** 2))
    
    def distance_along(L, p):
        '''returns the distance between the perpendicular line to L through 
        the origin and p'''
        return (L.b * p.x - L.a * p.y) / sqrt(L.a ** 2 + L.b ** 2)
    
    def intersection(L0, L1):
        '''returns the point of intersection of L0 and L1'''
        if type(L1) is LineSegment:
            # Intersection can be between a Line and a LineSegment
            S1 = L1
            p = L0.intersection(Line(S1))
            if p is not None and S1.contains(p):
                return p
            return None
        elif type(L1) is Line:
             # Intersection can be between two Lines
            try:
                x = (L1.b * L0.c - L0.b * L1.c) / (L1.b * L0.a - L0.b * L1.a)
                y = (L1.a * L0.c - L0.a * L1.c) / (L1.a * L0.b - L0.a * L1.b)
            except ZeroDivisionError:
                return None
            else:
                return Point(x, y)
    
    def is_parallel(L0, L1):
        '''returns if L0 and L1 are parallel'''
        # Useful for Debugging
        return isclose(L1.a * L0.b, L0.a * L1.b)
    
    def offset(L, d):
        ''' returns a line that is parallel to and d units away from L '''
        return Line(L.a, L.b, L.c + d * sqrt(L.a ** 2 + L.b ** 2))
    
    def point_along(L, d):
        ''' returns the point on the Line that is on L and 
        d units away from the perpendicular line to L through the origin'''
        x = L.a * L.c / (L.a ** 2 + L.b ** 2) + L.b * d / sqrt(L.a ** 2 + L.b ** 2)
        y = L.b * L.c / (L.a ** 2 + L.b ** 2) - L.a * d / sqrt(L.a ** 2 + L.b ** 2)
        return Point(x, y)
    
    def contains(L, p):
        '''returns if p is on the Line object'''
        # Useful for Debugging
        return isclose(L.a * p.x + L.b * p.y, L.c)

class LineSegment():
    def __init__(self, p0, p1):
        '''Initialises the Line object'''
        self.p0 = p0
        self.p1 = p1
    
    def __str__(self):
        '''returns a string of the Line object'''
        return "Line Segment: {}, {}".format(self.p0, self.p1)
    
    def __repr__(self):
        '''returns a representation of the Line object'''
        return "LineSegment({}, {})".format(self.p0, self.p1)
    
    def __eq__(S0, S1):
        '''returns if S0 and S1 are equivalent'''
        return ((S0.p0 == S1.p0 and S0.p1 == S1.p1) or 
                (S0.p0 == S1.p1 and S0.p1 == S1.p0))
    
    def length(S):
        '''returns the length of the Line Segment'''
        return S.p0.dist(S.p1)
    
    def intersection(S0, S1):
        '''returns the point of intersection of S0 and S1, if they intersect'''
        L0, L1 = Line(S0), Line(S1)
        p = L0.intersection(L1)
        if p is not None and S0.contains(p):
            return p
        return None
    
    def is_parallel(S0, S1):
        '''returns if S0 and S1 are parallel'''
        # Useful for Debugging
        L0, L1 = Line(S0), Line(S1)
        return L0.is_parallel(L1)
    
    def contains(S, p):
        '''returns if p is on the LineSegment object'''
        # Useful for Debugging
        L = Line(S)
        is_on_line = L.contains(p)
        is_in_range = (min(S.p0.x, S.p1.x) <= p.x <= max(S.p0.x, S.p1.x) and 
                       min(S.p0.y, S.p1.y) <= p.y <= max(S.p0.y, S.p1.y))
        return is_on_line and is_in_range


if __name__ == "__main__":
    print("This is just a handy module with points and lines.\nHave a nice day!")