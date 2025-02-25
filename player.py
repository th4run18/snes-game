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
        if input_vector.length() > 0:  
            self.direction = input_vector.normalize()
        else:
            self.direction = vector()

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt # take current position and increase speed in a direction
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')

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
                else: 
                    pass

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)