'''Module for generating flight plans. 
Started 18/06/2018, Finished 21/07/2018'''

from math import sqrt, ceil, log2

from Objects_2D import *
from trig_degrees import *

def longest_edge(poly):
    ''' Returns the longest edge in a polygon '''
    max_edge = LineSegment(poly[-1], poly[0])
    # Iterates the edges, where edge i is between points (i - 1) and i
    for p1_num, p1 in enumerate(poly):
        p0 = poly[p1_num - 1]
        edge = LineSegment(p0, p1)
        # Compares the current edge length to existing maximum
        if edge.length() > max_edge.length():
            max_edge = edge
    return max_edge

def line_range(line, ps, direction="perpendicular"):
    ''' Returns min and max distances from points in ps to line, or 
    from points in ps to perpendicular line through origin'''
    if direction == "perpendicular":
        # Points will be evaluated based on their distance from the line
        dist_function = lambda p: line.distance_to(p)
    elif direction == "parallel":
        # Points will be evaluated based on their distance along the line
        dist_function = lambda p: line.distance_along(p)
    else:
        # direction parameter is not valid
        raise ValueError("line_range direction arg is invalid")
    
    # Set up initial min and max values
    min_dist, max_dist = [dist_function(ps[0])] * 2
    for p in ps:
        dist = dist_function(p)
        # Compare distance to existing min and max values
        min_dist = min(min_dist, dist)
        max_dist = max(max_dist, dist)
    return min_dist, max_dist

def truncate_poly(poly, line, width):
    ''' Returns the part of poly inside boundary defined by line and width
    Expected: poly edges intercept the boundaries once, no self-intersection
    Boundary: point on boundary, edge intercepts both boundaries e.g. order
              poly fully inside/outside boundary
    '''
    
    upper_boundary = line.offset(+width / 2)
    lower_boundary = line.offset(-width / 2)
    
    upper_nums, lower_nums, truncated_num = [], [], []
    num_bounds, num_ps = 0, 0
    
    truncated_poly = []
    for p1_num, p1 in enumerate(poly):
        p0 = poly[p1_num - 1]
        edge = LineSegment(p0, p1)
        upper_intercept = upper_boundary.intersection(edge)
        lower_intercept = lower_boundary.intersection(edge)
        
        # if edge intercepts both boundaries 
        if upper_intercept is not None and lower_intercept is not None:
            # add intercept points in order
            if p1.dist(upper_intercept) > p1.dist(lower_intercept):
                truncated_poly.append(upper_intercept)
                truncated_poly.append(lower_intercept)
                upper_nums.append(num_bounds)
                lower_nums.append(num_bounds + 1)
                truncated_num.append(num_ps)
                truncated_num.append(num_ps + 1)
                num_bounds += 2
                num_ps += 2
            else:
                truncated_poly.append(lower_intercept)
                truncated_poly.append(upper_intercept)
                lower_nums.append(num_bounds)
                upper_nums.append(num_bounds + 1)
                truncated_num.append(num_ps)
                truncated_num.append(num_ps + 1)
                num_bounds += 2
                num_ps += 2
        elif upper_intercept is not None:
            truncated_poly.append(upper_intercept)
            upper_nums.append(num_bounds)
            truncated_num.append(num_ps)
            num_bounds += 1
            num_ps += 1
        elif lower_intercept is not None:
            truncated_poly.append(lower_intercept)
            lower_nums.append(num_bounds)
            truncated_num.append(num_ps)
            num_bounds += 1
            num_ps += 1
        
        # if p in within boundaries
        if -width / 2 <= line.distance_to(p1) <= width / 2:
            # add p
            truncated_poly.append(p1)
            num_ps += 1
    
    return truncated_poly, upper_nums, lower_nums, truncated_num

def boundary_pairs(upper_nums, lower_nums):
    ''' Returns a list that maps each boundary point to its pair '''
    num_bounds = len(upper_nums) + len(lower_nums)
    bound_pair = [None] * num_bounds
    for index, num0 in enumerate(upper_nums[::2]):
        index *= 2
        num1 = upper_nums[index + 1]
        bound_pair[num0] = num1
        bound_pair[num1] = num0
    for index, num0 in enumerate(lower_nums[::2]):
        index *= 2
        num1 = lower_nums[index + 1]
        bound_pair[num0] = num1
        bound_pair[num1] = num0
    return bound_pair

def get_next_fraction(fraction):
    ''' Get the next fraction in the sequence 1/2, 1/4, 3/4, 1/8... '''
    numerator, denominator = fraction
    if numerator == denominator - 1:
        numerator = 1
        denominator *= 2
    else:
        numerator += 2
    return numerator, denominator

def num_range(num_set, n):
    ''' if num_set contains all the numbers in a continuous sequence, 
    wrapped by the max number n, returns its inclusive, exclusive range.
    eg. {1, 0, 6} with n = 7 is continuous
    Expected: a small amount of numbers within range are present
    Boundary: all numbers in range are present - e.g. infinite loop
    Invalid: numbers outside range present, empty num_set
    '''
    
    if num_set == set():
        # Invalid input case: empty set
        raise ValueError("num_range() arg is an empty set")
    if not num_set.issubset(set(range(0, n))):
        # Invalid input case: num_set contains numbers outside range(0, n)
        raise ValueError("numbers not in range(0, {}) in num_set".format(n))
    
    # n_ceil = smallest power of 2 greater than or equal to n
    n_ceil = 2 ** ceil(log2(n))
    
    # Initialise what part of range(0, n) to search first
    search_fraction = 1, 2
    search_num = n_ceil // 2
    
    while search_num not in num_set:
        # Get the next place to search (these places are maximally spread out)
        search_fraction = get_next_fraction(search_fraction)
        numerator, denominator = search_fraction
        search_num = n_ceil * numerator // denominator
    
    # Find the smallest integer below search_num (wrapped by n) in num_set
    if (search_num - 1) % n in num_set:
        min_num = (search_num - 1) % n
    else:
        min_num = search_num
    while (min_num - 1) % n in num_set and min_num != search_num:
        min_num = (min_num - 1) % n
    
    # Find the smallest integer above search_num (wrapped by n) not in num_set
    max_num = (search_num + 1) % n
    while max_num in num_set and max_num != search_num:
        max_num = (max_num + 1) % n
    
    # Get range of values between min_num and max_num
    if max_num <= min_num:
        final_set = set(range(min_num, n)) | set(range(0, max_num))
    else:
        final_set = set(range(min_num, max_num))
    
    # return the range boundaries if this range is equal to num_set
    if num_set == final_set:
        return min_num, max_num

def min_of_firsts(list1, list2):
    ''' Returns the minimum value of the first elements of list1 and list2,
    where at most one may be empty '''
    # If both lists contain elements
    if list1 != [] and list2 != []:
        # use the min value out of their first elements
        result = min(list1[0], list2[0])
    elif list1 != []:
        result = list1[0]
    else:
        result = list2[0]
    return result

def sub_poly_bound_ranges(upper_nums, lower_nums):
    ''' Returns a set of boundary number ranges of sub-polygons'''
    # get the list that maps each boundary point to its pair
    bound_pair = boundary_pairs(upper_nums, lower_nums)
    num_bounds = len(bound_pair)
    
    # get the lowest-index boundary point which is least far along its boundary
    start_num = min_of_firsts(upper_nums, lower_nums)
    bound_ranges = set()
    
    # Initialise the first pairs of boundary indexes to add
    bound_num0 = start_num
    bound_num1 = (bound_num0 + 1) % num_bounds
    bound_set = set([bound_num0, bound_pair[bound_num0], 
                     bound_num1, bound_pair[bound_num1]])
    bound_range = num_range(bound_set, num_bounds)
    # If this set of boundary points form a closed polygon
    if bound_range is not None:
        # Record their min and max boundary indexes and reset
        bound_ranges.add(bound_range)
        bound_set = set()
    
    # set up iterator variable
    bound_num0 = (bound_num0 + 2) % num_bounds
    
    # Iterate through all pairs of boundary points
    while bound_num0 != start_num:
        bound_num1 = (bound_num0 + 1) % num_bounds
        
        # Add new boundary indexes
        bound_set |= set([bound_num0, bound_pair[bound_num0], 
                          bound_num1, bound_pair[bound_num1]])
        bound_range = num_range(bound_set, num_bounds)
        
        # If this set of boundary points form a closed polygon
        if bound_range is not None:
            # Record their min and max boundary indexes and reset
            bound_ranges.add(bound_range)
            bound_set = set()
        # Increment iterator variable
        bound_num0 = (bound_num0 + 2) % num_bounds
    return bound_ranges

def create_sub_poly(bound_range, truncated_num, truncated_poly):
    ''' Returns the sub_polygon in a given bound range'''
    min_num, max_num = bound_range
    
    # Get position in the truncated polygon of the min and mix boundary indexes
    min_p_num, max_p_num = truncated_num[min_num], truncated_num[max_num]
    
    # Slice truncated polygon for closed polygon between min_p_num and max_p_num
    if min_p_num >= max_p_num:
        sub_poly = truncated_poly[min_p_num:] + truncated_poly[:max_p_num]
    else:
        sub_poly = truncated_poly[min_p_num : max_p_num]
    return sub_poly

def merge_ranges(ranges):
    ''' Returns ranges with any overlapping ranges merged'''
    for r in ranges:
        if type(r) is not tuple:
            raise ValueError("merge_ranges parameter ranges is invalid")
    
    ranges.sort()
    r_num = 0
    
    # Iterate the pairs of consecutive ranges
    while r_num < len(ranges) - 1:
        r0 = ranges[r_num]
        r1 = ranges[r_num + 1]
        
        if not r0[1]:
            # check next pair of ranges
            r_num += 1
        elif not r1[1]:
            if r0[1] >= r1[0]:
                # merge r0 and r1
                ranges[r_num : r_num + 2] = [r0]
            else:
                # check next pair of ranges
                r_num += 1
        else:
            # If r1 starts before r0 ends
            if r0[1] >= r1[0]:
                # merge r0 and r1
                ranges[r_num : r_num + 2] = [(r0[0], max(r1[1], r0[1]))]
            else:
                # check next pair of ranges
                r_num += 1

def split_row(poly, row, G_w, G_h, overlap):
    '''returns a range of distance values that cover the entire area'''
    # get part of poly inside drone's field of view
    truncated_poly, upper_nums, lower_nums, truncated_num = truncate_poly(poly, row, G_w)
    
    # If poly is completely inside row-G_w boundary
    if len(upper_nums) == 0 and len(lower_nums) == 0:
        # get min and max distance along the boundary
        dist_ranges = [line_range(row, poly, direction="parallel")]
    else:
        # get function mapping a boundary index to a point on the truncated_poly
        bound_num_p = lambda bound_num: truncated_poly[truncated_num[bound_num]]
        # get function mapping a boundary index to a distance along the boundary
        dist_along = lambda bound_num: row.distance_along(bound_num_p(bound_num))
        
        # sort boundary points by distance along boundary
        upper_nums.sort(key=dist_along)
        lower_nums.sort(key=dist_along)
        
        # divide truncated_poly by bound index ranges of separate closed polygons
        bound_ranges = sub_poly_bound_ranges(upper_nums, lower_nums)
        dist_ranges = []
        for bound_range in bound_ranges:
            # create the closed polygon given by bound_range
            sub_poly = create_sub_poly(bound_range, truncated_num, truncated_poly)
            # get its min and max distance along the boundary and record it
            min_dist, max_dist = line_range(row, sub_poly, direction="parallel")
            min_dist += 0.5 * G_h
            max_dist -= 0.5 * G_h
            if max_dist > min_dist:
                dist_ranges.append((min_dist, max_dist))
            else:
                dist_ranges.append((0.5 * (min_dist + max_dist), None))
        # join any two ranges that intersect
        merge_ranges(dist_ranges)
    return dist_ranges

def flight_path_dist(ps):
    ''' Returns the distance a flight path covers'''
    total_dist = 0
    # Iterate each edge between points in the flight plan
    for p0_num, p1 in enumerate(ps[1:]):
        p0 = ps[p0_num]
        # calculate the length of the edge
        dist = p0.dist(p1)
        # add it to the running total 
        total_dist += dist
    return total_dist

def split_edge(edge, width):
    ''' splits edge into a minimal number segments of maximum length width '''
    p0, p1 = edge
    
    # get the line that passes through the edge
    S = LineSegment(p0, p1)
    L = Line(S)
    
    # get the min and max distance along the line of the endpoints
    dist_bounds = L.distance_along(p0), L.distance_along(p1)
    min_dist, max_dist = min(*dist_bounds), max(*dist_bounds)
    
    # get the distance halfway between the endpoints
    mid_dist = (min_dist + max_dist) / 2
    
    # Initialise the incremental distance variable
    dist = mid_dist + width / 2
    
    # set up a list to record each distance along the line
    dists = [min_dist, max_dist]
    
    # while the largest endpoint hasn't been reached
    while dist < max_dist:
        # add the two distance values along the line on either side of mid_dist
        dists.append(dist)
        dists.append(2 * mid_dist - dist)
        
        # Increment dist by the maximum segment length
        dist += width
    # sort the distance values
    dists.sort()
    
    # get the point at each distance value along the line
    points = [L.point_along(dist) for dist in dists]
    return points

def generate_flight_plan(poly, camera, altitude, overlap, heading):
    if len(poly) < 3:
        return [], 0
    
    # unpack values
    R_w, R_h = camera["resolution"].split('x')
    R_w, R_h = int(R_w), int(R_h)
    a = camera["view angle"]
    h = altitude
    
    # calculate ground pixel size and ground image dimensions
    G = 2 * h * tan(a / 2) / sqrt(R_w ** 2 + R_h ** 2)
    G_w = G * R_w
    G_h = G * R_h
    
    row_r = Line(cos(heading), -sin(heading), 0)
    
    # get the min and max distances from the row_r line, derive the midway value
    min_dist, max_dist = line_range(row_r, poly)
    mid_dist = (min_dist + max_dist) / 2
    
    # get list of parallel lines that will cover the polygon
    rows = [row_r.offset(mid_dist)]
    row_dist = mid_dist + G_w * (1 - overlap)
    # while the maximum distance from the row_r line has not been exceeded
    while row_dist - G_w / 2 < max_dist:
        # add the parallel lines to row_r on either side of it to rows
        rows.append(row_r.offset(row_dist))
        rows.append(row_r.offset(2 * mid_dist - row_dist))
        # increment the distance from row_r
        row_dist += G_w * (1 - overlap)
    
    # sort the rows by distance from the origin
    rows.sort(key=lambda row: row.c)
    
    edges = []
    # Iterate through the parallel lines
    for row in rows:
        # split the row into ranges of distances along the boundaries
        row_sections = split_row(poly, row, G_w, G_h, overlap)
        
        # ignore sub_ranges for simplicity, take overall range from whole row
        min_dist, max_dist = row_sections[0][0], row_sections[-1][1]
        p_min = row.point_along(min_dist)
        if not max_dist:
            p_max = None
        else:
            p_max = row.point_along(max_dist)
        
        edges.append((p_min, p_max))
    print("edges:",edges)
    
    # Try zig-zagging in both directions and take the shortest option
    flight_path0 = []
    for edge_num, edge in enumerate(edges):
        if not edge[1]:
            flight_path0 += [edge[0]]
        else:
            # split the edge so that it can be fully covered by images
            edge_points = split_edge(edge, G_h * (1 - overlap))
            # Option 1: Even-numbered edges go in normal order, else reversed
            if edge_num % 2 == 0 and edge_points[0] == edge[1]:
                edge_points.reverse()
            elif edge_num % 2 == 1 and edge_points[0] == edge[0]:
                edge_points.reverse()
            flight_path0 += edge_points
    flight_path1 = []
    for edge_num, edge in enumerate(edges):
        if not edge[1]:
            flight_path1 += [edge[0]]
        else:
            # split the edge so that it can be fully covered by images
            print(edge)
            edge_points = split_edge(edge, G_h * (1 - overlap))
            # Option 2: Odd-numbered edges go in normal order, else reversed
            if edge_num % 2 == 1 and edge_points[0] == edge[1]:
                edge_points.reverse()
            elif edge_num % 2 == 0 and edge_points[0] == edge[0]:
                edge_points.reverse()
            flight_path1 += edge_points
    # use whichever option is shorter
    if flight_path_dist(flight_path0) < flight_path_dist(flight_path1):
        flight_path = flight_path0
    else:
        flight_path = flight_path1
    return flight_path

if __name__ == "__main__":
    print("This is just a handy module for generating flight plans over polygon areas. \nHave a nice day!")