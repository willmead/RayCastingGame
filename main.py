import pyglet

from raycaster import cast_rays
from utility import Vector


MAP_WIDTH = 10
MAP_HEIGHT = 10
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Pyglet
window = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
main_batch = pyglet.graphics.Batch()

# TILEMAP
EMPTY_TILE = 0

with open("map.txt") as map_file:
    world_map = map_file.read().split("\n")

def get_tile_at(world_map: list[str], position: Vector) -> int:
    return int(world_map[position.x][position.y])

def has_hit_wall(grid_space: Vector) -> bool:
    return get_tile_at(world_map, grid_space) is not EMPTY_TILE


# CAMERA
camera_position = Vector(2, 2)
camera_direction = Vector(-1, 0)

# GRAPHICS
FOV = 0.66
columns = [pyglet.shapes.Rectangle(x, SCREEN_HEIGHT // 2, 1, 0, (255, 0, 0), batch=main_batch) for x in range(SCREEN_WIDTH)]


def update_column_height(column_index: int, ray_distance: float, is_vertical_wall: bool) -> None:
    line_height = SCREEN_HEIGHT // ray_distance
    columns[column_index].height = line_height
    columns[column_index].y = SCREEN_HEIGHT // 2 - line_height // 2
    columns[column_index].color = (255, 0, 0) if is_vertical_wall else (127, 0, 0)


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
    main_batch.draw()


def update(dt) -> None:
    handle_input(dt)

    rays = cast_rays(camera_position, camera_direction, number_of_rays=SCREEN_WIDTH, angular_range=FOV, stop_condition=has_hit_wall)
    for i, ray in enumerate(rays):
        update_column_height(i, ray.length, ray.hit_vertical_wall)


pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()