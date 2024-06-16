import pygame
import sys
from pygame.locals import *
from game_loop import *
from utility import *

clock = pygame.time.Clock()
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen_width = 1280
screen_height = 720

button_width = 200

pygame.display.set_caption('Visual novel game')
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

center_x = screen_width // 2
center_y = screen_height // 2
pradeti_zaidima_button = Button(center_x - button_width // 2,
								center_y - 100,
								button_width,
								WHITE,
								BLACK,
								GREEN,
								'Pradėti žaidimą')
iseiti_button = Button(center_x - button_width // 2,
					   center_y,
					   button_width,
					   WHITE,
					   BLACK,
					   RED,
					   'Išeiti')

run = True

while run:
	screen.fill((0, 0, 0))
	if pradeti_zaidima_button.draw(screen):
		loop = GameLoop(screen)
		loop.runLoop()
		break
	if iseiti_button.draw(screen):
		pygame.quit()
		sys.exit()

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()