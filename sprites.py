from setting import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)), groups = None):
        super().__init__(groups) 
        self.image = surf # ensure that the surf will not be ignored
        self.image.fill('white') #filling the blocks with white to de able to deal with collisions easier
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        #putting objects in a class so we can display it 
class MovingSprite(Sprite):
    def __init__(self,groups, start_pos , end_pos, move_dir, speed):
        surf = pygame.Surface((200,50))
        super().__init__(start_pos, surf, groups)
