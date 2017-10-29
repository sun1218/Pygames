import pygame, sys, random, math
from pygame.locals import *
# main program begins
pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption('draw circle')
font1 = pygame.font.Font(None, 24)
red = 220, 50, 50
black = 0, 0, 0
pos_x = 300
pos_y = 250
radius = 200
angle = 360

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    angle += 1 
    if angle >= 360:
        angle = 0
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = r, g, b
        
    x = math.cos(math.radians(angle)) * radius
    y = math.sin(math.radians(angle)) * radius 
    
    
    pos = (int(pos_x+x), int(pos_y+y))
    print(pos)
    screen.fill((0,0,0))
    pygame.draw.circle(screen, color, pos, 10, 0)
    
    pygame.display.update()