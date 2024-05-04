import pygame, sys, os
from pytmx import load_pygame
from settings import *
from level import Level


class Game:
	def __init__(self):
		pygame.init()
		screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		pygame.display.set_caption('gravity')
		self.clock = pygame.time.Clock()
		self.tmx_maps = {0: load_pygame("./maps/tmx/level.tmx")}
		self.level = Level(self.tmx_maps[0])

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			dt = self.clock.tick() / 1000
			self.level.run(dt)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()
