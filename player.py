from setting import *

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
        self.speed = 500
        self.gravity = 1300 #value for gravity to allow player to fall
        self.jump = False # create attribute to be able to change when jumping
        self.jump_height = 900

        # collision detection
        self.collision_sprites = collision_sprites

        

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
   
   
    def move(self, dt):
        #horizontal
        self.rect.x += self.direction.x * self.speed * dt # take current position and increase speed in a direction
        self.collision('horizontal')

        #vertical
        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collision('vertical')

        if self.jump:
           self.direction.y = -self.jump_height
           self.jump = False


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
                    
                    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)