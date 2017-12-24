import pygame, sys
from pygame.locals import *

class MySprite(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)# extend the base  Sprite class
        self.master_image = None
        self.frame = 0
        self.ord_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        
    # x property
    def _getx(self): return self.rect.x
    def _setx(self, value): self.rect.x = value
    x = property(_getx, _setx)
    
    # y property
    def _gety(self): return self.rect.y
    def _sety(self, value): self.rect.y = value
    y = property(_gety, _sety)
    
    # position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self, pos): self.rect.topleft = pos
    position = property(_getpos, _setpos)
    
    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0, 0, width, height)
        self.columns = columns
        # try to auto-calculate total frames
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1
        
    def update(self, current_time, rate=30):
        # upate animation frame number
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame   
            self.last_time = current_time
        # build current frame only if it changed
        if self.frame != self.ord_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.ord_frame = self.frame
            
    def __str__(self):
        return str(self.frame) + ',' + str(self.first_frame) + \
               ',' + str(self.last_frame) + ',' + str(self.frame_width) + \
               ',' + str(self.frame_height) + ',' + str(self.columns) + \
               ',' + str(self.rect)


    
def reset_arrow():
    y = random.randint(250, 350)
    arrow.position = 800, y
def print_text(font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Demo')
font = pygame.font.Font(None, 18)
famerate = pygame.time.Clock()

# create the dragon sprite
dragon = MySprite(screen)
dragon.load('dragon.png', 260, 150, 3)
group = pygame.sprite.Group()
group.add(dragon)

# main loop
while True:
    famerate.tick(30)
    ticks = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
    key = pygame.key.get_pressed()
    if key[K_ESCAPE]: sys.exit()
    screen.fill((0,0,100))
    group.update(ticks)
    group.draw(screen)
    print_text(font, 0, 0, 'Sprite: ' + str(dragon))
    pygame.display.update()