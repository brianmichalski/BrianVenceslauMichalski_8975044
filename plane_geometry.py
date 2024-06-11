import math

# provide the distance from two cartesian coordinates
def distance_between_points(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def rectangle_area(width, height):
    return width * height