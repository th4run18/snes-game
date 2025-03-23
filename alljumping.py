#elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
#    self.timers['wall jump'].activate()
#    self.direction.y = -self.jump_height

    # Allow jumping away from the wall
 #   if self.on_surface['left']:
#        self.direction.x = 1  # Push right
 #   elif self.on_surface['right']:
 #       self.direction.x = -1  # Push left
 
#   instead of this 




 #elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block']:
#    self.timers['wall jump'].activate()
 #   self.direction.y = -self.jump_height
 #   #self.direction.x = 1 if self.on_surface['left'] else -1