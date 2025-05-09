import pygame
from setting import *
from sprites import Sprite,AnimatedSprite, MovingSprite
from player import Player # importing player to allow it to be able to interact with the level
from groups import AllSprites #importing the camera


class Level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites=pygame.sprite.Group() #creates an empty group of sprites that you can later add objects to.
        self.semi_collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):#printing the tile map  


        for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles(): # being able to connect tiled to my terminal
                groups = [self.all_sprites]
                if layer == 'Terrain': groups.append(self.collision_sprites)
                if layer == 'Platforms': groups.append(self.semi_collision_sprites)
                
                z= Z_LAYERS['bg tiles'] #all tiles will be in the background
                Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, groups, z )

                    
		    
        
        # OBJECTS
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player': # introduces the players start position   
                self.player = Player(
                    pos = (obj.x,obj.y), 
                    groups = self.all_sprites,
                    collision_sprites= self.collision_sprites, 
                    semi_collision_sprites= self.semi_collision_sprites,
                    frames = level_frames['player']) # retreive frames for player
            else:
                if obj.name in ('barrel', 'crate'):
                    Sprite((obj.x, obj.y), obj.image , (self.all_sprites, self.collision_sprites))
                else:
                    if 'palm' not in obj.name:
                        frames = level_frames[obj.name]
                        AnimatedSprite((obj.x, obj.y), frames, self.all_sprites)

            

        # Moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == 'helicopter':
                if obj.width > obj.height: # horizontal
                    move_dir = 'x'
                    start_pos = (obj.x , obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width,obj.y + obj.height / 2)
                   
                else: # vertical
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width/2 , obj.y)
                    end_pos = (obj.x + obj.width/ 2 ,obj.y + obj.height)
                speed = obj.properties['speed']
                MovingSprite((self.all_sprites, self.semi_collision_sprites), start_pos , end_pos, move_dir, speed)

                
              

                

    def run(self, dt):
        self.display_surface.fill('black') # setting a black ground to black to be able to see the platform clearly
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player.hitbox_rect.center)
        