from plan_flight import generate_flight_plan
from Objects_2D import *

def edge_point_dist(S, p):
    '''returns the distance between a LineSegment and a point'''
    L0 = Line(S)
    L1 = Line(-L0.b, L0.a, -L0.b * p.x + L0.a * p.y)
    p_int = L0.intersection(L1)
    if S.contains(p_int):
        # p_int is the closest point
        return p.dist(p_int)

def closest_edge_point(poly, p):
    '''Returns the closest point in a polygon to a given point, 
    accounting for the angle each vertex's edges'''
    closest_edge_num = 0
    dist = float('inf')
    # Iterates the edges, where edge i is between points (i - 1) and i
    for i in range(len(poly)):
        edge = LineSegment(poly[i-1], poly[i])
        edge_dist = edge_point_dist(edge, p)
        if edge_dist and edge_dist < dist:
            dist = edge_dist
            closest_edge_num = i
        elif p.dist(poly[i]) < dist:
            dist = p.dist(poly[i])
            # choose best edge from i
            u = Vector(poly[i]) - Vector(poly[i-1])
            v = Vector(poly[i]) - Vector(poly[(i+1)%len(poly)])
            w = Vector(p) - Vector(poly[i])
            if u.dot(w)/u.size() < v.dot(w)/v.size():
                # u is closer, therefore edge i is best
                closest_edge_num = i
            else:
                # v is closer, therefore edge i+1 is best
                closest_edge_num = (i + 1) % len(poly)
            
    return closest_edge_num

def add_point(poly, p):
    if len(poly) > 1:
        closest_edge_num = closest_edge_point(poly, p)
        poly.insert(closest_edge_num, p)
    else:
        poly.append(p)
    return poly

def format_input_poly(poly):
    if not poly:
        return []
    poly = [float(num) for num in poly.split(',')]
    result = []
    for i in range(0, len(poly), 2):
        result.append(Point(poly[i], poly[i+1]))
    return result