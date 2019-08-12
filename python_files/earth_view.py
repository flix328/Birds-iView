'''Module for transforming GPS points onto the XY plane. 
Started 22/5/18, Finished 29/5/18'''

from math import sqrt

import Objects_3D
import Objects_2D
import Objects_GPS
from trig_degrees import *

# Equatorial/Polar radii of Earth
MAJOR_RADIUS = 6378137
MINOR_RADIUS = 6356752

# Ellipsoid to encapsulate shape of the Earth
EARTH = Objects_3D.Ellipsoid(MAJOR_RADIUS, MAJOR_RADIUS, MINOR_RADIUS)

def gps_to_xyz(g):
    '''returns a 3D Point of the GPS Point object on the earth's surface'''
    z = sqrt((MAJOR_RADIUS ** 2 * MINOR_RADIUS ** 2 * tan(g.lat) ** 2) / 
             (MINOR_RADIUS ** 2 + MAJOR_RADIUS ** 2 * tan(g.lat) ** 2))
    if g.lat < 0:
        z = -z
    
    # r = result point projected onto the z-plane's distance to the origin
    r = sqrt((MAJOR_RADIUS ** 2 * MINOR_RADIUS ** 2) / 
             (MINOR_RADIUS ** 2 + MAJOR_RADIUS ** 2 * tan(g.lat) ** 2))
    x = r * cos(g.lon)
    y = r * sin(g.lon)
    return Objects_3D.Point(x, y, z)

def centre_point(ps):
    '''returns the centre of the smallest bounding sphere around points
    uses a modified version of Ritter's algorithm, where first pass
    considers all pairs of points in O(n^2), second pass as normal - O(n)'''
    for p in ps:
        if type(p) is not Objects_3D.Point:
            raise ValueError("centre_point arg ps contains non-Point objects")
    
    # If there are no points given
    if len(ps) == 0:
        raise ValueError("ps arg in centre_point has no Points")
    
    # If there is only one point given
    if len(ps) == 1:
        # Return it
        return ps[0]
    
    max_square_distance = 0
    p0_num, p1_num = 0, 1
    # Iterates every pair of points (i, j) in ps
    for i in range(len(ps)):
        for j in range(i + 1, len(ps)):
            square_distance = ps[i].square_dist(ps[j])
            # Compares square distances to avoid time-costly sqrt
            if square_distance > max_square_distance:
                max_square_distance = square_distance
                p0_num, p1_num = i, j
    
    # Get furthest apart pair of points (p0, p1)
    p0 = ps[p0_num]
    p1 = ps[p1_num]
    
    # Create minimal bounding sphere around this pair of points 
    S = Objects_3D.Sphere(p0, p1)
    for p in ps:
        if not S.inside(p):
            # Create sphere including p
            p0 = p
            direction = Objects_3D.Vector(S.c) - Objects_3D.Vector(p)
            p1 = Objects_3D.Point(Objects_3D.Vector(S.c) + 
                                  direction * (S.r / direction.length()))
            S = Objects_3D.Sphere(p0, p1)
    
    # Return centre of bounding sphere, which is central point of ps
    return S.c

def xyz_to_xy(p_r, p):
    '''returns translation of Point p onto the XY plane with reference p_r'''
    # get GPS values for p_r (point of reference)
    g_r = Objects_GPS.Point(p_r)
    
    # Get tangent plane to Earth at p_r
    P = EARTH.tangent(p_r)
    
    # Project p to this plane, rotate it around z and x axes onto the xy plane
    p = P.project(p)
    p = Objects_3D.Point(+p.y * cos(g_r.lon) - p.x * sin(g_r.lon), 
                         -p.x * cos(g_r.lon) - p.y * sin(g_r.lon), p.z)
    return Objects_2D.Point(p.x, p.y * sin(g_r.lat) + p.z * cos(g_r.lat))

def xy_to_gps(p_r, p):
    '''returns the translation of 2D point on the XY Plane into 3D space'''
    # get GPS values for p_r (point of reference)
    g_r = Objects_GPS.Point(p_r)

    # Get tangent plane to Earth at p_r, and its normal vector
    P = EARTH.tangent(p_r)
    n = P.normal()
    
    # Rotate p around the x and z axes
    p = Objects_3D.Point(p.x, p.y * sin(g_r.lat), p.y * cos(g_r.lat))
    p = Objects_3D.Point(-p.x * sin(g_r.lon) - p.y * cos(g_r.lon), 
                         +p.x * cos(g_r.lon) - p.y * sin(g_r.lon), p.z)
    
    # Find the point p + kn on the Earth's surface
    p = EARTH.scale_to_surface(p, n)
    
    # Return the GPS Point at this location
    return Objects_GPS.Point(p)

if __name__ == "__main__":
    print("This is just a handy library to do with viewing points on the Earth's surface.\nHave a nice day!")