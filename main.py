import pyglet

from raycaster import Ray, cast_rays
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

textures = pyglet.image.load('textures.png')
textures = pyglet.image.ImageGrid(textures, 1, 8)
brick = textures[1]
atlas = pyglet.image.atlas.TextureAtlas()
brick = atlas.add(brick)

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
columns = [pyglet.sprite.Sprite(brick, x, SCREEN_HEIGHT // 2, batch=main_batch) for x in range(SCREEN_WIDTH)]


def update_column(column_index: int, ray: Ray) -> None:
    line_height = SCREEN_HEIGHT // ray.length
    columns[column_index].height = line_height
    columns[column_index].y = SCREEN_HEIGHT // 2 - line_height // 2
    
    texture_x = ray.wall_fraction * 64
    if not ray.hit_vertical_wall and ray.direction.x > 0: texture_x = 64 - texture_x - 1
    if ray.hit_vertical_wall and ray.direction.y < 0: texture_x = 64 - texture_x - 1
    columns[column_index].image = brick.get_region(int(texture_x), 0, 1, 64)


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

    # draw walls
    rays = cast_rays(camera_position, camera_direction, number_of_rays=SCREEN_WIDTH, angular_range=FOV, stop_condition=has_hit_wall)
    for i, ray in enumerate(rays):
        update_column(i, ray)


pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()