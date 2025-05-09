from setting import *


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface() 
        self.offset = vector() #moved the coordinates of the window

    def draw(self, target_pos): 
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
        # to keep the player in the middle
        
        for sprite in sorted(self, key = lambda sprite: sprite.z ):
            #sorts all sprite based on their Z value
            offset_pos = sprite.rect.topleft + self.offset 
            # drawing with offset creates a camera
            self.display_surface.blit(sprite.image, offset_pos)
                # this