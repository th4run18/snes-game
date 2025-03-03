from setting import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((48, 56))  # General dimensions of the character
        self.image.fill('red')  # Red to allow player to be seen in the black background

        # Rect
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()

        # Movement
        self.direction = vector()
        self.speed = 400
        self.gravity = 1300  # Value for gravity to allow player to fall
        self.jump = False  # Attribute to change when jumping
        self.jump_height = 900

        # Collision detection
        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.platform = None

        # Timer
        self.timers = {
            'wall jump': Timer(400)
        }

    def input(self):
        keys = pygame.key.get_pressed()  # Key presses to control character
        input_vector = vector(0, 0)
        if not self.timers['wall jump'].active:
            if keys[pygame.K_RIGHT]:
                input_vector.x += 1  # Moving to the right by 1 increment
            if keys[pygame.K_LEFT]:
                input_vector.x -= 1  # Moving to the left by 1 increment

            self.direction.x = input_vector.normalize().x if input_vector else 0

        if keys[pygame.K_SPACE]:
            self.jump = True
            self.timers['wall jump'].activate()

    def move(self, dt):

        # Horizontal movement
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # Vertical movement
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y * dt
        self.collision('vertical')

         # If on a platform, stay locked to it
        if self.platform:
            self.rect.bottom = self.platform.rect.top
            self.direction.y = 0  # Prevents gravity from pulling down

        # Jumping
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                #self.timers['wall slide block'].activate()
                self.rect.bottom -= 1
            elif any((self.on_surface['left'], self.on_surface['right'])): #and not self.timers['wall slide block']:
                self.timers['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1.5 if self.on_surface['left'] else -1.5
        self.jump = False

    def platform_move(self,dt):
        if self.platform:
            self.rect.topleft += self.platform.direction * self.platform.speed * dt

    def check_contact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        right_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4), (2, self.rect.height / 2))
        left_rect = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height / 4), (2, self.rect.height / 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        # Collisions
        self.on_surface['floor'] = floor_rect.collidelist(collide_rects) >= 0
        self.on_surface['right'] = right_rect.collidelist(collide_rects) >= 0
        self.on_surface['left'] = left_rect.collidelist(collide_rects) >= 0

        self.platform = None
        for sprite in [sprite for sprite in self.collision_sprites.sprites() if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # Left collision
                    if self.direction.x < 0:  # Moving left
                        self.rect.left = sprite.rect.right
                    # Right collision
                    elif self.direction.x > 0:  # Moving right
                        self.rect.right = sprite.rect.left
                else:  # Vertical collision
                    # Top collision
                    if self.direction.y < 0:  # Moving up
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = 0  # Stop vertical movement
                    # Bottom collision
                    elif self.direction.y > 0:  # Moving down
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0  # Stop vertical movement
                        self.on_surface['floor'] = True  # Player is on the ground

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.input()
        self.platform_move(dt)  # Move with platform first
        self.move(dt)  # Then apply player's own movement
        self.check_contact()