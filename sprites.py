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
        self.rect.center = start_pos
        self.start_pos = start_pos
        self.end_pos = end_pos
        speed = 100  

        # movement
        self.speed = speed
        self.direction = vector(1,0) if move_dir == 'x' else vector(0,1)
        self.move_dir = move_dir

    def check_border(self):
         if self.move_dir == 'x':
             if self.rect.right >= self.end_pos[0] and self.direction.x == 1: # introduce and end position to the game.
                 self.direction = -1
                 self.rect.right = self.end_pos[0]



    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.direction = pygame.math.Vector2(self.direction)  # Ensure it's a Vector2
        self.rect.topleft += self.direction * self.speed * dt
        self.check_border()
      