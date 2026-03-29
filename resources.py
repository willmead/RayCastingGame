import pyglet


textures = pyglet.image.load('textures.png')
textures = pyglet.image.ImageGrid(textures, 1, 8)
atlas = pyglet.image.atlas.TextureAtlas()
flag = atlas.add(textures[0])
brick = atlas.add(textures[1])
moss = atlas.add(textures[2])
cobblestone = atlas.add(textures[3])
square_stone = atlas.add(textures[4])
mossy_cobblestone = atlas.add(textures[5])
wood = atlas.add(textures[6])
dry_stone = atlas.add(textures[7])
TEXTURE_SIZE = 64
TEXTURES = [flag, brick, moss, cobblestone, square_stone, mossy_cobblestone, wood, dry_stone]