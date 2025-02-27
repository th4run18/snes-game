from setting import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join


class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('super pirate world')
		self.clock =  pygame.time.Clock()

		self.tmx_maps = {0: load_pygame(join('Super-Pirate-World-main', 'data','levels', 'omni.tmx'))}
		
		self.current_stage = Level(self.tmx_maps[0])

	def run(self):
		while True:
			dt = self.clock.tick() / 1000 # ensures game always runs at the same speed
			for event in pygame.event.get():
				if event.type == pygame.QUIT: # allows program to be exited using the X
					pygame.quit()
					sys.exit()

			self.current_stage.run(dt)
			
			pygame.display.update()

if __name__ == '__main__':			
	game = Game()
	game.run() 