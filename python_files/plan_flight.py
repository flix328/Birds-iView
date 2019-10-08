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

def split_range(r, dist, overlap, max_points=None):
    '''splits a range (min_dist, max_dist) into overlapping ranges of length dist'''
    min_dist, max_dist = r
    mid_dist = 0.5 * (min_dist + max_dist)
    result_min_dist = min_dist + (0.5 - overlap) * dist
    result_max_dist = max_dist - (0.5 - overlap) * dist
    
    if result_min_dist >= result_max_dist:
        if max_points is None or max_points > 0:
            result = [mid_dist]
        else:
            result = []
    else:
        num_gaps = ceil((result_max_dist - result_min_dist) / (1 - overlap) / dist)
        gap_size = (result_max_dist - result_min_dist) / (num_gaps)
        if max_points is not None:
            num_points = min(max_points, num_gaps + 1)
        else:
            num_points = num_gaps + 1
        result = [result_min_dist + i * gap_size for i in range(num_points)]
    return result

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
            dist_ranges.append((min_dist, max_dist))
        # join any two ranges that intersect
        merge_ranges(dist_ranges)
    return dist_ranges

def optimal_route(edges):
    ''' returns the route that zig-zags up and down the edges in the least distance. '''
    if len(edges) == 1:
        return edges[0]
    ends = [(edges[i][0], edges[i][-1]) for i in range(len(edges)) if len(edges[i]) > 0]
    
    # 0 means to iterate through a row in the normal direction
    # 1 means to iterate through a row in reverse
    
    # an "a -> b path" means a path that zig-zags through the rows 
    #     starting in the a direction and ending in the b direction
    
    # initialise the distance for each path
    # distance spanned by each row is ignored because this is constant 
    #     regardless of the zig-zag pattern
    prev_paths = [["00", "01"], ["10", "11"]]
    prev_dists = [[ends[0][1].dist(ends[1][0]),ends[0][1].dist(ends[1][1])],
                  [ends[0][0].dist(ends[1][0]),ends[0][0].dist(ends[1][1])]]
    
    # iterate through the rows, updating the possible optimal paths each time
    for i in range(2, len(ends)):
        new_paths = [[None, None], [None, None]]
        new_dists = [[None, None], [None, None]]
        
        for j in range(2):
            for k in range(2):
                # optimise j -> k path
                if(prev_dists[j][0] + ends[i-1][1].dist(ends[i][k]) < 
                   prev_dists[j][1] + ends[i-1][0].dist(ends[i][k])):
                    # using prev j -> 0 path is shorter
                    new_paths[j][k] = prev_paths[j][0] + str(k)
                    new_dists[j][k] = prev_dists[j][0] + ends[i-1][1].dist(ends[i][k])
                else:
                    # using prev j -> 1 path is shorter
                    new_paths[j][k] = prev_paths[j][1] + str(k)
                    new_dists[j][k] = prev_dists[j][1] + ends[i-1][0].dist(ends[i][k])
        
        prev_paths = new_paths
        prev_dists = new_dists
    
    # get shortest overall path out of 0 -> 0, 0 -> 1, 1 -> 0 and 1 -> 1
    best_path = prev_paths[0][0]
    best_dist = prev_dists[0][0]
    for i in range(2):
        for j in range(2):
            if prev_dists[i][j] < best_dist:
                best_path = prev_paths[i][j]
                best_dist = prev_dists[i][j]
    
    flight_path = []
    for edge_num, direction in enumerate(best_path):
        edge = edges[edge_num]
        if direction == "1":
            edge.reverse()
        flight_path += edge
    return flight_path

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

def generate_flight_plan(poly, camera, altitude, overlap, heading, max_points=None):
    if len(poly) < 3:
        return [], 0
    if overlap == 0:
        overlap = 0.0001
    
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
    
    row_dists = split_range((min_dist, max_dist), G_w, overlap)
    rows = [row_r.offset(dist) for dist in row_dists]
    
    edges = []
    num_points = 0
    # Iterate through the parallel lines
    for row in rows:
        # split the row into ranges of distances along the boundaries
        row_sections = split_row(poly, row, G_w, G_h, overlap)
        
        edge_points = []
        for row_section in row_sections:
            if max_points is not None:
                split = split_range(row_section, G_h, overlap, max_points=max(max_points - num_points,0))
            else:
                split = split_range(row_section, G_h, overlap)
            edge_points += [row.point_along(dist) for dist in split]
            num_points += len(split)
        edge_points.sort(key = lambda p: row.distance_along(p))
        edges.append(edge_points)
    
    flight_path = optimal_route(edges)
    return flight_path

if __name__ == "__main__":
    print("This is just a handy module for generating flight plans over polygon areas. \nHave a nice day!")