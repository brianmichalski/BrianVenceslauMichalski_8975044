import plane_geometry
import pytest
from pytest import approx

# test cases for integration testing the combination of "plane_geometry.distance_between_points()"
# and "plane_geometry.test_rectangle_area()" functions
@pytest.mark.parametrize("width_line,height_line,area", [
    ([{ "x" : 2, "y": 4 }, { "x" : 12, "y": 4 }], [{ "x" : 12, "y": 4 }, { "x" : 12, "y": 0 }], 40),
])
def test_distance_rectangle_area_from_drawing_points(width_line, height_line, area):
    height = plane_geometry.distance_between_points(
        x1=width_line[0]["x"], y1=width_line[0]["y"], 
        x2=width_line[1]["x"], y2=width_line[1]["y"])
    
    width = plane_geometry.distance_between_points(
        x1=height_line[0]["x"], y1=height_line[0]["y"], 
        x2=height_line[1]["x"], y2=height_line[1]["y"])
    
    assert plane_geometry.rectangle_area(width, height) == area


# test cases for unit testing the "plane_geometry.distance_between_points()" function
@pytest.mark.parametrize("points,distance,tolerance", [
    ([{ "x" : 2, "y": 4 }, { "x" : -4, "y": -1 }], 7.8102496, 1e-7),
    ([{ "x" : 0, "y": 0 }, { "x" : 0, "y": 0 }], 0, 0),
])
def test_distance_between_points(points, distance, tolerance):
    assert plane_geometry.distance_between_points(
        x1=points[0]["x"], y1=points[0]["y"], 
        x2=points[1]["x"], y2=points[1]["y"]) == approx(distance, abs=tolerance) 


# test cases for unit testing of "plane_geometry.test_rectangle_area()" function
@pytest.mark.parametrize("width,height,area", [
    (20, 25, 500),
    (1.2, 43.1, 51.72),
    (0, 0, 0)
])
def test_rectangle_area(width, height, area):
    assert plane_geometry.rectangle_area(width, height) == area