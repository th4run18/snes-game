from setting import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups) 
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('white') #filling the blocks with white to de able to deal with collisions easier
        self.rect = self.image.get_rect(topleft = pos)
