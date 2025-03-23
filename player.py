from setting import *
from timer import Timer
from os.path import join


class Player(pygame.sprite.Sprite): 
    def __init__(self, pos, groups, collision_sprites, semi_collision_sprites):
        super().__init__(groups)
        self.image =  pygame.image.load(join( 'Super-Pirate-World-main','graphics', 'player','idle','0.png'))
        
        

        # Rect
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-76, -36)
        self.old_rect = self.hitbox_rect.copy()

        # Movement
        self.direction = vector()
        self.speed = 400
        self.gravity = 1300  # Value for gravity to allow player to fall
        self.jump = False  # Attribute to change when jumping
        self.jump_height = 900

        # Collision detection
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.platform = None

        # Timer
        self.timers = {
            'wall jump': Timer(400),
            'wall slide block': Timer(250),
            'platform skip' : Timer(300)
        }

    def input(self):
        keys = pygame.key.get_pressed()  # Key presses to control character
        input_vector = vector(0, 0)
        if not self.timers['wall jump'].active:
            if keys[pygame.K_RIGHT]:
                input_vector.x += 1  # Moving to the right by 1 increment
            if keys[pygame.K_LEFT]:
                input_vector.x -= 1  # Moving to the left by 1 increment
            if keys[pygame.K_DOWN]:
                self.timers['platform skip'].activate()
            self.direction.x = input_vector.normalize().x if input_vector else 0

        if keys[pygame.K_SPACE]:
            self.jump = True
            self.timers['wall jump'].activate()

    def move(self, dt):

        # Horizontal movement
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # Vertical movement
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
            self.direction.y = 0
            self.hitbox_rect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt 
            self.hitbox_rect.y += self.direction.y * dt 
            self.direction.y += self.gravity / 2 * dt
        #self.direction.y += self.gravity * dt
        #self.rect.y += self.direction.y * dt
        #self.collision('vertical')

         # If on a platform, stay locked to it
       # if self.platform:
            #self.rect.bottom = self.platform.rect.top
            #self.direction.y = 0  # Prevents gravity from pulling down

        # Jumping
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                #self.timers['wall slide block'].activate()
                self.hitbox_rect.bottom -= 1
                
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block']:
                self.timers['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False
        
        self.collision('vertical')
    
        self.semi_collision()
        self.rect.center = self.hitbox_rect.center


    def platform_move(self,dt):
        if self.platform:
            self.hitbox_rect.topleft += self.platform.direction * self.platform.speed * dt
           # self.hitbox_rect.x += self.platform.direction.x * self.platform.speed * dt
            #self.hitbox_rect.y += self.platform.direction.y * self.platform.speed * dt

    def check_contact(self):
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))
        right_rect = pygame.Rect(self.hitbox_rect.topright + vector(0, self.hitbox_rect.height / 4), (2, self.hitbox_rect.height / 2))
        left_rect = pygame.Rect(self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4), (2, self.hitbox_rect.height / 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semi_collide_rect = [sprite.rect for sprite in self.semi_collision_sprites]

        # Collisions
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 or floor_rect.collidelist(semi_collide_rect) >= 0 and self.direction.y >= 0 and self.direction.y >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False 
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False

        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()
        # can use a plus to add as sprites() ensures that they are strings 
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == 'horizontal':
                    # Left collision
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= sprite.old_rect.right:
                        self.hitbox_rect.left = sprite.rect.right
                    # Right collision
                    elif self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= sprite.old_rect.left:
                        self.hitbox_rect.right = sprite.rect.left
                else:  # Vertical collision
                    # Top collision
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= sprite.old_rect.bottom:
                        self.hitbox_rect.top = sprite.rect.bottom + 1
                        #self.direction.y = max(self.direction.y, 50)  # Small downward force to help fall
                        if hasattr(sprite, 'moving'):
                            self.hitbox_rect.top += 6
                        
                    # Bottom collision
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.direction.y = 0 
                       
                    #self.on_surface['floor'] = True  # Player is on the ground

    def semi_collision(self):
        if not self.timers['platform skip'].active:
            for sprite in self.semi_collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                            self.hitbox_rect.bottom = sprite.rect.top
                            if self.direction.y > 0:
                                self.direction.y = 0 # to eunsure that gravity does not increase while on the platform

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.hitbox_rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)  # Then apply player's own movement
        self.platform_move(dt)  # Move with platform first
        self.check_contact()
       
       