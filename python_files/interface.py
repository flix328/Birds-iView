from plan_flight import generate_flight_plan
from Objects_2D import *
from classes import *

def edge_point_dist(S, p):
    '''returns the distance between a LineSegment and a point'''
    L0 = Line(S)
    L1 = Line(-L0.b, L0.a, -L0.b * p.x + L0.a * p.y)
    p_int = L0.intersection(L1)
    if S.contains(p_int):
        # p_int is the closest point
        return p.dist(p_int)

def format_input_data(data):
    poly = Polygon()
    split = data.split(',')
    nums = []
    for value in split:
        try:
            nums.append(float(value))
        except ValueError:
            continue
    print("ASdlSD", poly)
    for i in range(0, len(nums), 3):
        poly.push_end(nums[i], Point(nums[i+1], nums[i+2]))
    return poly