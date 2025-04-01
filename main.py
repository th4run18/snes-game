from setting import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join

from support import *


class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('super pirate World')
		self.clock =  pygame.time.Clock()
		self.import_assets()
      
		self.tmx_maps = {0: load_pygame(join('GAME_1', 'data','levels', 'omni.tmx'))}
		
		self.current_stage = Level(self.tmx_maps[0], self.level_frames)

	def import_assets(self):
		self.level_frames = {
			'flag': import_folder('GAME_1','graphics','level','flag'),
			'saw' : import_folder('GAME_1','graphics','enemies','saw','animation'),
			'floor_spike' : import_folder('GAME_1','graphics','enemies','floor_spikes'),
		}
		print(self.level_frames)

	def run(self):
		while True:
			dt = self.clock.tick(60) / 1000 # ensures game always runs at the same speed
			for event in pygame.event.get():
				if event.type == pygame.QUIT: # allows program to be exited using the X
					pygame.quit()
					sys.exit()

			self.current_stage.run(dt)

			pygame.display.update()

if __name__ == '__main__':			
	game = Game()
	game.run()   