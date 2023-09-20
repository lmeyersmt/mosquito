import math
import numpy as np
from scipy.spatial.distance import cdist

# import logging
# logger = logging.getLogger(__name__)

def convex_hull(points):
    '''
    Selects the points that belong to the convex hull by finding the lower and
    upper hulls.
    Inputs:
        points: n x 2D array
            .
    Outputs:
        points_convex_hull: m x 2D array
            Points that belong to the convex hull.
    '''

    # Sort the points lexicographically
    points = sorted(set([tuple(point) for point in points]))
    points = np.vstack(points)

    # Build lower hull
    lower = []
    for point in points:
        while (len(lower) >= 2 and
               np.cross(lower[-1]-lower[-2], point-lower[-2]) <= 0):
            lower.pop()
        lower.append(point)

    # Build upper hull
    upper = []
    for point in reversed(points):
        while (len(upper) >= 2 and
               np.cross(upper[-1]-upper[-2], point-upper[-2]) <= 0):
            upper.pop()
        upper.append(point)

    # Join lower and upper hulls eliminating duplicates
    points_convex_hull = lower[:-1] + upper[:-1]

    # Convert to numpy array
    points_convex_hull = np.vstack(points_convex_hull)

    return points_convex_hull

def clockwise_sort_points(points):
    '''
    Sorts the vertices of a convex polygon in a clockwise way.
    Inputs:
        points: n x 2D array
            Vertices of a convex polygon.
    Outputs:
        sorted_points: n x 2D array
            Clockwise sorted points.
    '''

    # center of mass of all given points
    center_of_mass = np.mean(points,axis=0)

    # dictionary to store the angle of it point relative to the center of mass
    angle = dict()

    # iterate on each point
    for point_index in range(len(points)):

        # direction of the center of mass to the point
        direction = points[point_index]-center_of_mass

        # angle of the direction with the x-axis
        angle[point_index] = math.atan2(direction[1],direction[0])

    # sort angles in a clockwise way
    sorted_angle = sorted(angle, key=angle.get, reverse=True)

    # clockwise sorted points
    sorted_points = points[list(sorted_angle)]

    return sorted_points

def area_of_rectangle(rectangle_vertices):
    '''
    Calculates the area of a rectangle based on its vertices.
    Inputs:
        rectangle_vertices: 4 x 2D array
            Clockwise sorted vertices of a rectangle.
    Outputs:
        rectangle_area: float
            Area of the given rectangle.
    '''

    # Size of the sides of the rectangle
    side1 = np.linalg.norm(rectangle_vertices[0]-rectangle_vertices[1])
    side2 = np.linalg.norm(rectangle_vertices[1]-rectangle_vertices[2])

    # Rectangle area
    rectangle_area = side1*side2

    return rectangle_area

def minimum_bounding_rectangle(points):
    '''
    Computes the vertices of the rectangle with minimum area that contains a
    defined convex hull.
    Inputs:
        points: n x 2D array
            Vertices of a convex hull to be inside of the rectangle.
    Outputs:
        min_rectangle_vertices: 4 x 2D array
            Vertices of the rectangle with minimum area that contains all given
            points.
    '''

    def far_projections(points,
                        point,
                        direction):
        '''
        Inputs:
            points: n x 2D array
                Points to be inside of the rectangle.
            point: 2D array
                Point .
            direction: 2D array
                .
        Outputs:
            point1, point2: 2 x 2D array
                .
        '''

        # Quantity of points
        n_points = points.shape[0]

        # projections on side direction
        projections = []
        for j in range(n_points):
            projection = point + direction*np.dot(points[j] - point, direction)
            projections.append(projection)

        projections_distance = cdist(projections, projections, 'euclidean')
        max_distance_index = np.argmax(projections_distance)
        point1 = max_distance_index//n_points
        point2 = max_distance_index%n_points

        return projections[point1], projections[point2]

    # Quantity of points
    n_points = points.shape[0]

    # Clockwise sorted points
    points = clockwise_sort_points(points)

    # Dictionaries to store the area and vertices of each rectangle relative to
    # a side of the polygon composed of the given points
    areas = dict()
    vertices = dict()

    # Iterate on polygon's sides
    for i in range(n_points):

        # Normalized side direction
        nextt = i+1 if i!=n_points-1 else 0
        side_direction = points[nextt]-points[i]
        side_direction = 1/np.linalg.norm(side_direction)*side_direction

        # Vertices in side direction
        vertice1, vertice2 = far_projections(points, points[i], side_direction)

        # Direction perpendicular to the side direction
        perpendicular_side_direction = np.array([-side_direction[1],side_direction[0]])

        # Vertices in direction perpendicular to the side direction
        point1, point2 = far_projections(points, vertice1, perpendicular_side_direction)
        if np.allclose(point1,vertice1): vertice3 = point2
        else: vertice3 = point1

        point1, point2 = far_projections(points, vertice2, perpendicular_side_direction)
        if np.allclose(point1,vertice2): vertice4 = point2
        else: vertice4 = point1

        # Rectangle vertices
        rectangle_vertices = np.vstack([vertice1,vertice2,vertice3,vertice4])

        # Clockwise sorted vertices
        rectangle_vertices = clockwise_sort_points(rectangle_vertices)

        # Area of rectangle
        rectangle_area = area_of_rectangle(rectangle_vertices)

        # Add to dictionary
        areas[i] = rectangle_area
        vertices[i] = rectangle_vertices

    # Rectangle with minimum area
    min_rectangle_vertices_index = min(areas, key=areas.get)

    # Vertices of the rectangle with minimum area
    min_rectangle_vertices = vertices[min_rectangle_vertices_index]

    return min_rectangle_vertices

def gps_accurate_polygon(vertices,
                         gps_horizontal_accuracy=1.5):
    '''
    Function used to consider horizontal GPS error on the vertices of an
    polygon based on horizontal accuracy range with GPS positioning.
    Inputs:
        Vertices: n x 2D array
            Clockwise sorted vertices of a polygon.
        gps_horizontal_accuracy: float
            GPS horizontal accuracy in meters(m).
            Default 1.5m.
    Outputs:
        accurate_vertices: n x 2D array
            vertices of the rectangle increased by GPS horizontal error.
    '''

    # Quantity of vertices
    n_vertices = vertices.shape[0]

    accurate_vertices = []

    # Iterate on vertices
    for i in range(len(vertices)):

        # Selected vertice
        vertice = vertices[i]

        # Growth directions
        nextt = i+1 if i!=n_vertices-1 else 0
        before = i-1 if i!=0 else n_vertices-1
        x_direction = vertice-vertices[nextt]
        y_direction = vertice-vertices[before]

        # Normalized growth directions
        x_direction = 1/np.linalg.norm(x_direction)*x_direction
        y_direction = 1/np.linalg.norm(y_direction)*y_direction

        # Expanded vertice
        vertice = vertice + gps_horizontal_accuracy*(x_direction + y_direction)

        # Add to accurate rectangle vertices
        accurate_vertices.append(vertice)

    accurate_vertices = np.vstack(accurate_vertices)

    return accurate_vertices
