import math
from typing import NamedTuple

from utility import Vector, sign


class Ray(NamedTuple):
    """
    Class containing information about a completed ray.
    """
    length: float
    direction: Vector
    hit_vertical_wall: bool
    grid_space: Vector
    wall_fraction: float


def calculate_ray_direction(direction: Vector, x: int, number_of_rays: int, angular_range: int) -> Vector:
    """
    Normalise camera plane: left side = -1, center = 0, right side = 1
    then find direction from origin to point on plane
    """
    camera_plane = direction.perpendicular * angular_range
    fraction_along_camera_plane = x / float(number_of_rays)
    normalised_fraction_along_camera_plane = 2 * fraction_along_camera_plane - 1
    direction_to_point_on_camera_plane = camera_plane * normalised_fraction_along_camera_plane
    return direction + direction_to_point_on_camera_plane


def cast_ray(ray_origin: Vector, ray_direction: Vector, stop_condition: callable) -> Ray:
    """
    casts a ray until the ray hits a wall
    returns:
        distance to the wall: float
        hit vertical wall: bool
    """
    step = ray_direction.apply(sign)
    ray_unit_step_size = (1 / ray_direction).apply(abs)
    grid_space = ray_origin.apply(math.floor)
    ray_origin_fractional = ray_origin - grid_space

    scale = Vector(0, 0)
    scale.y = ray_origin_fractional.y if ray_direction.y < 0 else 1 - ray_origin_fractional.y
    scale.x = ray_origin_fractional.x if ray_direction.x < 0 else 1 - ray_origin_fractional.x
    
    ray_length = scale * ray_unit_step_size

    while True:
        mask = Vector(ray_length.x < ray_length.y, ray_length.y <= ray_length.x)
        grid_space += step * mask
        ray_length += ray_unit_step_size * mask
 
        if stop_condition(grid_space):
            break

    distance = ray_length - ray_unit_step_size
    ray_distance = distance.x if mask.x else distance.y
    hit_vertical_wall = mask.x

    wall_coords = ray_origin + ray_direction * ray_distance
    wall_x = wall_coords.y if hit_vertical_wall else wall_coords.x

    wall_fraction = wall_x - math.floor(wall_x)

    return Ray(ray_distance, ray_direction, hit_vertical_wall, grid_space, wall_fraction)


def cast_rays(origin: Vector, direction: Vector, number_of_rays: int, angular_range: float, stop_condition: callable) -> list[Ray]:
    """
    Casts a given number of rays starting at the origin 
    equally spread across the given angular range,
    and equally spread either side of the given direction.
    The rays will travel until the stop condition is reached.
    """
    ray_direction = lambda x: calculate_ray_direction(direction, x, number_of_rays, angular_range)
    return [cast_ray(origin, ray_direction(x), stop_condition) for x in range(number_of_rays)]