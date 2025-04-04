import pygame
from setting import *
from timer import Timer
from os.path import join


class Player(pygame.sprite.Sprite): 
    def __init__(self, pos, groups, collision_sprites, semi_collision_sprites, frames):
        #General set-up
        super().__init__(groups)
        self.z = Z_LAYERS['main']


        # the image
        self.frames, self.frame_index = frames, 0
        # idle sets the initial animation state to idle 
        self.state, self.facing_right = 'idle', True
        #used a boolean True to keep track of left anf right movement
        self.image = self.frames[self.state][self.frame_index]
        # frame_index determines the specific frame, which is drawn on the screen


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
        self.attacking = False

        # Collision detection
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.platform = None

        # Timer
        self.timers = {
            'wall jump': Timer(400),
            'wall slide block': Timer(250),
            'platform skip' : Timer(100),
            'attack block' : Timer(500)
        }

    def input(self):
        keys = pygame.key.get_pressed()  # Key presses to control character
        input_vector = vector(0, 0)


        if not self.timers['wall jump'].active:
            if keys[pygame.K_RIGHT]:
                input_vector.x += 1  # Moving to the right by 1 increment
                self.facing_right = True
            if keys[pygame.K_LEFT]:
                input_vector.x -= 1  # Moving to the left by 1 increment
                self.facing_right = False #switches images and faces player left when arrow is clicked
            if keys[pygame.K_DOWN]:
                self.timers['platform skip'].activate()

            if keys[pygame.K_a]:
                self.attack()

            self.direction.x = input_vector.normalize().x if input_vector else 0

        if keys[pygame.K_SPACE]:
            self.jump = True
            self.timers['wall jump'].activate()

    def attack(self):
        if not self.timers['attack block'].active:
            self.attacking = True
            self.frame_index = 0
            self.timers['attack block'].activate()


    def move(self, dt):

        # Horizontal movement
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # Vertical movement
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
            self.direction.y = 0
            self.hitbox_rect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 1.5 * dt 
            self.hitbox_rect.y += self.direction.y * dt 
            self.direction.y += self.gravity / 1.5 * dt
       

        # Jumping
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers['wall slide block'].activate()
                self.hitbox_rect.bottom -= 1
                
         #  # elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block']:
         #       self.timers['wall jump'].activate()
         #       self.direction.y = -self.jump_height
          #      self.direction.x = 1 if self.on_surface['left'] else -1
          #  self.jump = False
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
                self.timers['wall jump'].activate()
                self.direction.y = -self.jump_height

    # Allow jumping away from the wall
        if self.on_surface['left']:
            self.direction.x = 1  # Push right
        elif self.on_surface['right']:
            self.direction.x = -1  # Push left

        self.timers['wall slide block'].activate()
        self.jump = False

        self.collision('vertical')
    
        self.semi_collision()
        self.rect.center = self.hitbox_rect.center


    def platform_move(self,dt):
        if self.platform:
            self.hitbox_rect.topleft += self.platform.direction * self.platform.speed * dt
            #self.hitbox_rect.x += self.platform.direction.x * self.platform.speed * dt
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
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.hitbox_rect.left = sprite.rect.right
                    # Right collision
                    elif self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <=int( sprite.old_rect.left):
                        self.hitbox_rect.right = sprite.rect.left
                else:  # Vertical collision
                    # Top collision
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom + 1
                        #self.direction.y = max(self.direction.y, 50)  # Small downward force to help fall
                        if hasattr(sprite, 'moving'):
                            self.hitbox_rect.top += 6
                        
                    # Bottom collision
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.direction.y = 0 
                       
                    self.on_surface['floor'] = True  # Player is on the ground

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

    def animate(self, dt):

        self.frame_index += ANIMATION_SPEED * dt #dt to progress at a consistant rate
        if self.state == 'attack' and self.frame_index >= len(self.frames[self.state]):
            self.state = 'idle' # resest player to 'idle'
            self.attacking = False #resets attack to false to its doesnt attack at the time
        elif self.state == 'air_attack' and self.frame_index >= len(self.frames[self.state]):
            self.attacking = False  # Also reset after air attack
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]

        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False) 
        #flipping image in horizontal axis

    def get_state(self):
        if self.on_surface['floor']:
            if self.attacking:
                self.state = 'attack'
            else:
                self.state = 'idle' if self.direction.x == 0 else 'run'
                # if the player isnt attacking it returns to its idle state
        else:
            if self.attacking:
                self.state = 'air_attack'
            else:
                if any((self.on_surface['left'], self.on_surface['right'])):
                    self.state = 'wall' # goes to wall state if it touches a wall
                else:
                    self.state = 'jump' if self.direction.y < 0 else 'fall'
                    # it falls or jump is it not attacking


    def update(self, dt):
        self.old_rect = self.hitbox_rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)  # Then apply player's own movement
        self.platform_move(dt)  # Move with platform first
        self.check_contact()
        self.get_state()
        self.animate(dt)
       
       