from setting import *
from sprites import Sprite
from player import Player # importing player to allow it to be able to interact with the level

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites=pygame.sprite.Group() #creates an empty group of sprites that you can later add objects to.

        self.setup(tmx_map)

    def setup(self, tmx_map):#pritning the tile map
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles(): # being able to connect tiled to my terminal
            Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, (self.all_sprites, self.collision_sprites))

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player': # introduces the players start position
                Player((obj.x,obj.y), self.all_sprites, self.collision_sprites) # PLAYER is not in collision_sprites, stops Player from colliding with itself
                

    def run(self, dt):
        self.all_sprites.update(dt)
        self.display_surface.fill('black') # setting a black ground to black to be able to see the platform clearly
        self.all_sprites.draw(self.display_surface)
        