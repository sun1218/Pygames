import pygame
import sys
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((600, 500))
myfont = pygame.font.Font(None, 60)
WHITE = 255, 255, 255
BLUE = 0,0,255
textImage = myfont.render('hello pygame', True, WHITE)

while True:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()
    screen.fill(BLUE)
    screen.blit(textImage, (100, 100))
    pygame.display.update()
    