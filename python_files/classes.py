from Objects_2D import *


class Node():
    def __init__(self, _id, data):
        self._id = _id
        self.data = data
        self.next = None
        self.prev = None

def edge_point_dist(S, p):
    '''returns the distance between a LineSegment and a point'''
    L0 = Line(S)
    L1 = Line(-L0.b, L0.a, -L0.b * p.x + L0.a * p.y)
    p_int = L0.intersection(L1)
    if S.contains(p_int):
        # p_int is the closest point
        return p.dist(p_int)

class Polygon():
    def __init__(poly):
        ''' Initialise an empty polygon '''
        poly.head = None
        poly.length = 0
        poly._id_node = {}
    
    def push_end(poly, _id, data):
        ''' if poly is empty, create head, else add behind head '''
        if poly.head == None:
            poly.head = Node(_id, data)
            poly.head.prev = poly.head.next = poly.head
            poly._id_node[_id] = poly.head
        else:
            if _id in poly._id_node.keys():
                raise ValueError("Cannot add the same id twice")
            new_node = Node(_id, data)
            new_node.prev = poly.head.prev
            new_node.next = poly.head
            poly.head.prev.next = new_node
            poly.head.prev = new_node
            poly._id_node[_id] = new_node
        poly.length += 1
    def _push_between_nodes(poly, _id, data, node0, node1):
        if(node0.next != node1):
            raise ValueError("cannot push between {} and {} as they are not adjacent".format(v0, v1))
        
        new_node = Node(_id, data)
        new_node.prev = node0
        new_node.next = node1
        node0.next = new_node
        node1.prev = new_node
        poly._id_node[_id] = new_node
        poly.length += 1
    def push_between(poly, _id, data, _id0, _id1):
        if _id0 not in poly._id_node.keys() or _id1 not in poly._id_node.keys():
            raise ValueError("cannot push between, either id {} or {} is missing".format(_id0, _id1))
        if _id in poly._id_node.keys():
            raise ValueError("cannot push id {} that already exists".format(_id))
        node0 = poly._id_node[_id0]
        node1 = poly._id_node[_id1]
        poly._push_between_nodes(_id, data, node0, node1)
        
    def pop(poly, _id):
        if _id not in poly._id_node.keys():
            raise ValueError("Cannot remove id {} that's not there".format(_id))
        node = poly._id_node[_id]
        node.prev.next = node.next
        node.next.prev = node.prev
        if node == poly.head:
            poly.head = node.next
        poly._id_node.pop(_id) # Remove the id from the dictionary
        poly.length -= 1
    def listify(poly):
        if poly.head:
            result = [(poly.head._id, poly.head.data.x, poly.head.data.y)]
            node = poly.head.next
            while node != poly.head:
                result.append((node._id, node.data.x, node.data.y))
                node = node.next
        else:
            result= []
        return result
    def __str__(poly):
        return str(poly.listify())
    def closest_edge(poly, p):
        '''Returns the closest edge in poly to a given point, 
        accounting for the angle each vertex's edges'''
        result_node = poly.head
        result_dist = edge_point_dist(LineSegment(poly.head.prev.data, poly.head.data), p)
        if not result_dist:
            result_dist = p.dist(poly.head.data)
        # Iterates the edges, where edge i is between points (i - 1) and i
        node = poly.head.next
        while node != poly.head:
            p0 = node.prev.data
            p1 = node.data
            p2 = node.next.data
            
            edge = LineSegment(p0, p1)
            edge_dist = edge_point_dist(edge, p)
            p1_dist = p.dist(p1)
        
            if edge_dist and edge_dist < result_dist:
                result_dist = edge_dist
                result_node = node
            elif p1_dist < result_dist:
                result_dist = p1_dist
                # choose best edge from i
                u = Vector(p1) - Vector(p0)
                v = Vector(p1) - Vector(p2)
                w = Vector(p) - Vector(p1)
                if u.dot(w)/u.size() < v.dot(w)/v.size():
                    # u is closer, therefore edge i is best
                    result_node = node
                else:
                    # v is closer, therefore edge i+1 is best
                    result_node = node.next
            node = node.next
        return result_node
    def push(poly, _id, p):
        if poly.length > 1:
            edge_node = poly.closest_edge(p)
            poly._push_between_nodes(_id, p, edge_node.prev, edge_node)
        else:
            poly.push_end(_id, p)
        return poly


def main():
    A = Polygon()
    for _id, lat, lng in [(62, 73, -41), (65, 34, -38), (78, 43, 48)]:
        A.push_end(_id, Point(lat, lng))
    print(A.length, A)
    
    A.push_between(63, Point(20,23), 65, 78)
    print(A.length, A)
    
    A.push(82, Point(14,-72))
    print(A.length, A)


if __name__ == "__main__":
    main()