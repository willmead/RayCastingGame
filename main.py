import math

import pyglet

from raycaster import Ray, cast_rays, floor_casting
import renderer
import resources
from utility import Vector


MAP_WIDTH = 10
MAP_HEIGHT = 10
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# PYGLET
pyglet.options["dpi_scaling"] = "real"  # necessary for retina displays
window = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
main_batch = pyglet.graphics.Batch()


# TILEMAP
EMPTY_TILE = 0

with open("map.txt") as map_file:
    world_map = map_file.read().split("\n")

def get_tile_at(world_map: list[str], position: Vector) -> int:
    return int(world_map[int(position.x)][int(position.y)])

def has_hit_wall(grid_space: Vector) -> bool:
    return get_tile_at(world_map, grid_space) is not EMPTY_TILE


# CAMERA
camera_position = Vector(2, 2)
camera_direction = Vector(-1, 0)

# GRAPHICS
FOV = 0.66
columns = [pyglet.sprite.Sprite(resources.brick, x, SCREEN_HEIGHT // 2, batch=main_batch) for x in range(SCREEN_WIDTH)]
image = pyglet.image.ImageData(
    320,
    240,
    'RGB',
    bytes(renderer.pixels),
    pitch=320 * 3
)

def calculate_column_texture(ray: Ray) -> pyglet.image.TextureRegion:
    wall_x = ray.final_position.y if ray.hit_vertical_wall else ray.final_position.x
    wall_fraction = wall_x - math.floor(wall_x)
    texture_x = int(wall_fraction * resources.TEXTURE_SIZE)

    reverse_direction = (not ray.hit_vertical_wall and ray.direction.x > 0) or (ray.hit_vertical_wall and ray.direction.y < 0)
    if reverse_direction:
        texture_x = resources.TEXTURE_SIZE - texture_x - 1

    # -1 so we can use a texture at index 0
    texture = resources.TEXTURES[get_tile_at(world_map, ray.grid_space) - 1]

    return texture.get_region(x=texture_x, y=0, width=1, height=resources.TEXTURE_SIZE)


def update_column(column_index: int, ray: Ray) -> None:
    line_height = SCREEN_HEIGHT // ray.length
    column = columns[column_index]
    column.height = line_height
    column.y = SCREEN_HEIGHT // 2 - line_height // 2
    column.image = calculate_column_texture(ray)


def handle_input(dt) -> None:
    global camera_position

    movement_speed = 5 * dt
    rotation_speed = 3 * dt

    if keys[pyglet.window.key.W]:
        camera_position += camera_direction * movement_speed
    if keys[pyglet.window.key.S]:
        camera_position -= camera_direction * movement_speed
    if keys[pyglet.window.key.D]:
        camera_direction.rotate(-1 * rotation_speed)
    if keys[pyglet.window.key.A]:
        camera_direction.rotate(rotation_speed)


@window.event
def on_draw():
    window.clear()
    image.blit(0, 0, width=640, height=480)
    main_batch.draw()


def update(dt) -> None:

    handle_input(dt)

    # draw walls
    rays = cast_rays(camera_position, camera_direction, number_of_rays=SCREEN_WIDTH, angular_range=FOV, stop_condition=has_hit_wall)
    for i, ray in enumerate(rays):
        update_column(i, ray)

    # draw floors
    pixels = floor_casting(camera_position, camera_direction)
    global image
    image.set_data(
        'RGB',
        320 * 3,
        bytes(pixels),
    )

pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()