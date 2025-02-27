from setting import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((48,56)) # general dimensions of the character
        
        self.image.fill('red') # red to allow player to be seen in the black background

        #rect
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy 
        # creating the movement
        self.direction = vector()
        self.speed = 200
        self.gravity = 1300 #value for gravity to allow player to fall
        self.jump = False # create attribute to be able to change when jumping
        self.jump_height = 900

        # collision detection
        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right' : False}

        self.display_surface = pygame.display.get_surface()

        # timer 
        self.timers = {
            'wall jump' : Timer(200)
        }
        

    def input(self):
        keys = pygame.key.get_pressed() # introducing key presses to control character
        input_vector = vector(0,0)

        if keys[pygame.K_RIGHT]:
            input_vector.x += 1 #moving to the right by 1 increment

        if keys[pygame.K_LEFT]:
            input_vector.x -= 1 #moving to the left by 1 increment
        
        # if input_vector else input_vector is needed as (0,0) cannot be normalised
      
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_SPACE]:
           self.jump = True
           self.timers['wall jump'].activate()

   
   
    def move(self, dt):
        #horizontal
        self.rect.x += self.direction.x * self.speed * dt # take current position and increase speed in a direction
        self.collision('horizontal')

        #vertical
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])):
            self.direction.y = 0
            self.rect.y += self.gravity / 10* dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
        

        if self.jump:
           if self.on_surface['floor']:
                self.direction.y = -self.jump_height
        elif any((self.on_surface['left'], self.on_surface['right'])):
               self.direction.y = -self.jump_height
               self.direction.x = 1 if self.on_surface['left'] else -1
        self.jump = False



        self.collision('vertical')

    def check_contact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft,(self.rect.width,2))
        right_rect = pygame.Rect(self.rect.topright + vector(0,self.rect.height / 4),(2, self.rect.height / 2))
        left_rect = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height / 4), (2,self.rect.height/2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]


        #collisions
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        print(self.on_surface)


    def collision(self,axis):
        for sprites in self.collision_sprites:
            if sprites.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    #left
                    if self.rect.left <= sprites.rect.right and self.old_rect.left >= sprites.old_rect.right:
                        self.rect.left = sprites.rect.right
                    #right
                    if self.rect.right >= sprites.rect.left and self.old_rect.right <= sprites.old_rect.left:
                        self.rect.right = sprites.rect.left
                else: #vertical
                    if self.rect.top <= sprites.rect.bottom and self.old_rect.top >= sprites.old_rect.bottom:
                        self.rect.top = sprites.rect.bottom

                    #bottom collision
                    if self.rect.bottom >= sprites.rect.top and self.old_rect.bottom <= sprites.old_rect.top:
                        self.rect.bottom = sprites.rect.top 
                    self.direction.y = 0  # to keep gravity constant while playing the game             
            
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

        
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.check_contact()
        print(self.timers['wall jump'].active)