from setting import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)), groups = None, z = Z_LAYERS['main']):
        super().__init__(groups) 
        self.image = surf # ensure that the surf will not be ignored
        
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = z #creating a attribute
        #putting objects in a class so we can display it 




class MovingSprite(Sprite):
    def __init__(self,groups, start_pos , end_pos, move_dir, speed):
        surf = pygame.Surface((200,50))
        super().__init__(start_pos, surf, groups)
        self.image.fill('light blue')
        if move_dir == 'x':
            self.rect.midleft = start_pos
        else:
            self.rect.midtop = start_pos
        self.start_pos = start_pos
        self.end_pos = end_pos
        speed = 100   

        # movement
        self.moving = True
        self.speed = speed
        self.direction = vector(1,0) if move_dir == 'x' else vector(0,1)
        self.move_dir = move_dir

    def check_border(self):
        if self.move_dir == 'x':
            if self.rect.right >= self.end_pos[0] and self.direction.x == 1: # introduce and end position to the game.
                 self.direction.x = -1 # didnt write X 
                 self.rect.right = self.end_pos[0]
            if self.rect.left <= self.start_pos[0] and self.direction.x == -1:
                self.direction.x = 1
                self.rect.left = self.start_pos[0]
        else:
            if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1: # introduce and end position to the game.
                    self.direction.y = -1 # didnt write X 
                    self.rect.bottom = self.end_pos[1]
            if self.rect.top <= self.start_pos[1] and self.direction.y == -1:
                    self.direction.y = 1
                    self.rect.top = self.start_pos[1]



    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * dt
        self.check_border()
      