from collections.abc import Callable
from dataclasses import dataclass
import math
from resources import wood

import resources
from utility import Vector, sign


@dataclass
class FloorRay:
    x: int
    y: int
    floor: Vector
    cell: Vector


@dataclass
class Ray:
    """
    Class containing information about a completed ray.
    """
    origin: Vector
    length: float
    direction: Vector
    grid_space: Vector
    hit_vertical_wall: bool

    @property
    def final_position(self) -> Vector:
        return self.origin + self.direction * self.length
    
    @property
    def hit_horizontal_wall(self) -> bool:
        return not self.hit_vertical_wall


def calculate_ray_direction(direction: Vector, x: int, number_of_rays: int, angular_range: float) -> Vector:
    """
    Normalise camera plane: left side = -1, center = 0, right side = 1
    then find direction from origin to point on plane
    """
    camera_plane = direction.perpendicular * angular_range
    fraction_along_camera_plane = x / float(number_of_rays)
    normalised_fraction_along_camera_plane = 2 * fraction_along_camera_plane - 1
    direction_to_point_on_camera_plane = camera_plane * normalised_fraction_along_camera_plane
    return direction + direction_to_point_on_camera_plane


def cast_ray(ray_origin: Vector, ray_direction: Vector, stop_condition: Callable) -> Ray:
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
        # instead of an if statement the results of the bools are stored as floats in a vector mask
        mask = Vector(float(ray_length.x < ray_length.y), float(ray_length.y <= ray_length.x))
        grid_space += step * mask
        ray_length += ray_unit_step_size * mask
 
        if stop_condition(grid_space):
            break

    distance = ray_length - ray_unit_step_size
    hit_vertical_wall = bool(mask.x)
    ray_distance = distance.x if hit_vertical_wall else distance.y

    return Ray(ray_origin, ray_distance, ray_direction, grid_space, hit_vertical_wall)


def cast_rays(origin: Vector, direction: Vector, number_of_rays: int, angular_range: float, stop_condition: Callable) -> list[Ray]:
    """
    Casts a given number of rays starting at the origin 
    equally spread across the given angular range,
    and equally spread either side of the given direction.
    The rays will travel until the stop condition is reached.
    """
    ray_direction = lambda x: calculate_ray_direction(direction, x, number_of_rays, angular_range)
    return [cast_ray(origin, ray_direction(x), stop_condition) for x in range(number_of_rays)]



tex_pixels = resources.tex_pixels
pix = bytearray(320 * 240 * 3)  # RGB

def floor_casting(origin: Vector, direction: Vector) -> bytearray:

    camera_plane = direction.perpendicular * 0.66
    left_ray_direction = direction - camera_plane
    right_ray_direction = direction + camera_plane
    tw = resources.tex_width
    half_height = 240 // 2
    for y in range(240):
        y_position = y - half_height
        vertical_camera_position = half_height

        if y_position == 0:
            continue

        row_distance = vertical_camera_position / y_position

        floor_step_x = row_distance * (right_ray_direction.x - left_ray_direction.x) / 640
        floor_step_y = row_distance * (right_ray_direction.y - left_ray_direction.y) / 640
        floor_x = origin.x + row_distance * left_ray_direction.x
        floor_y = origin.y + row_distance * left_ray_direction.y

        for x in range(320):
            cell_x = int(floor_x)
            cell_y = int(floor_y)

            texture_x = int(64 * (floor_x - cell_x)) & (64 - 1)
            texture_y = int(64 * (floor_y - cell_y)) & (64 - 1)
            
            index = (texture_y * tw + texture_x) * 3
            r = tex_pixels[index]
            g = tex_pixels[index + 1]
            b = tex_pixels[index + 2]

            i = (y * 320 + x) * 3
            pix[i] = r
            pix[i + 1] = g
            pix[i + 2] = b

            floor_x += floor_step_x
            floor_y += floor_step_y
    return pix