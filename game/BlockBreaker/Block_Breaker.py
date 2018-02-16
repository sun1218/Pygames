# 导入模块
import sys, time, random, math, pygame
from pygame.locals import *
from library import *
# 创建‘关卡集’信息
levels = (
(1,1,1,1,1,1,1,1,1,1,1,1, 
 1,1,1,1,1,1,1,1,1,1,1,1, 
 1,1,1,1,1,1,1,1,1,1,1,1, 
 1,1,1,1,1,1,1,1,1,1,1,1, 
 1,1,1,1,1,0,0,1,1,1,1,1, 
 1,1,1,1,1,0,0,1,1,1,1,1, 
 1,1,1,1,1,1,1,1,1,1,1,1, 
 1,1,1,1,1,1,1,1,1,1,1,1, 
 1,1,1,1,1,1,1,1,1,1,1,1, 
 1,1,1,1,1,1,1,1,1,1,1,1),

(2,2,2,2,2,2,2,2,2,2,2,2, 
 2,0,0,2,2,2,2,2,2,0,0,2, 
 2,0,0,2,2,2,2,2,2,0,0,2, 
 2,2,2,2,2,2,2,2,2,2,2,2, 
 2,2,2,2,2,2,2,2,2,2,2,2, 
 2,2,2,2,2,2,2,2,2,2,2,2, 
 2,2,2,2,2,2,2,2,2,2,2,2, 
 2,0,0,2,2,2,2,2,2,0,0,2, 
 2,0,0,2,2,2,2,2,2,0,0,2, 
 2,2,2,2,2,2,2,2,2,2,2,2),

(3,3,3,3,3,3,3,3,3,3,3,3, 
 3,3,0,0,0,3,3,0,0,0,3,3, 
 3,3,0,0,0,3,3,0,0,0,3,3, 
 3,3,0,0,0,3,3,0,0,0,3,3, 
 3,3,3,3,3,3,3,3,3,3,3,3, 
 3,3,3,3,3,3,3,3,3,3,3,3, 
 3,3,0,0,0,3,3,0,0,0,3,3, 
 3,3,0,0,0,3,3,0,0,0,3,3, 
 3,3,0,0,0,3,3,0,0,0,3,3, 
 3,3,3,3,3,3,3,3,3,3,3,3),
)
    
#this function increments the level
def goto_next_level():
    global level, levels
    level += 1 # ‘关卡数’计入下一个关卡
    if level > len(levels)-1: level = 0 # 重新开始关卡集
    load_level() # 加载新的关卡的有关信息

#this function updates the blocks in play
def update_blocks():
    global block_group, waiting
    if len(block_group) == 0: # 所有的'block'是否都被击碎
        goto_next_level() # 进入下一关
        waiting = True # 将球重新放在‘挡板’上
    block_group.update(ticks, 50)
        
#this function sets up the blocks for the level
def load_level():
    global level, block, block_image, block_group, levels
    block_group.empty() #reset block group
    
    for bx in range(0, 12):
        for by in range(0,10): # 放置每一个‘block’
            block = Sprite()
            block.load('blocks.png', 58, 28, 4)
            x = 40 + bx * (block.frame_width+1)
            y = 60 + by * (block.frame_height+1)
            block.position = x,y

            #read blocks from level data
            num = levels[level][by*12+bx] # 获得图片的第几个 
            block.first_frame = num-1
            block.last_frame = num-1
            if num > 0: # 如果不为空
                block_group.add(block)

    print(len(block_group)) # 输出还有多少个‘block’

    
#this function initializes the game
def game_init(): # 初始化
    global screen, font, timer
    global paddle_group, block_group, ball_group
    global paddle, block_image, block, ball

    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Block Breaker Game")
    font = pygame.font.Font(None, 36)
    pygame.mouse.set_visible(False)
    timer = pygame.time.Clock()

    #create sprite groups
    paddle_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    ball_group = pygame.sprite.Group()

    #create the paddle sprite
    paddle = Sprite()
    paddle.load("paddle.png", 90, 26, 1)
    paddle.position = 400, 540
    paddle_group.add(paddle)

    #create ball sprite
    ball = Sprite()
    ball.load("ball.png", 16, 16, 1)
    ball.position = 400,300
    ball_group.add(ball)



#this function moves the paddle
def move_paddle(): # 移动‘挡板’ 
    global movex,movey,keys,waiting

    paddle_group.update(ticks, 50)

    if keys[K_SPACE]:
        if waiting: # 球放在‘挡板’上
            waiting = False # 让球起飞
            reset_ball()
    elif keys[K_LEFT]: paddle.velocity.x = -10.0
    elif keys[K_RIGHT]: paddle.velocity.x = 10.0
    else: # 跟随鼠标的'x'轴
        if movex < -2: paddle.velocity.x = movex
        elif movex > 2: paddle.velocity.x = movex
        else: paddle.velocity.x = 0
    
    paddle.x += paddle.velocity.x # 移动
    # 出界检查
    if paddle.x < 0: paddle.x = 0
    elif paddle.x > 710: paddle.x = 710

#this function resets the ball's velocity
def reset_ball():
    ball.velocity = Point(4.5, -7.0) # 让球获得速度

#this function moves the ball
def move_ball(): # 移动球
    global waiting, ball, game_over, lives

    #move the ball            
    ball_group.update(ticks, 50) # 刷新球的位置
    if waiting: # 如果‘球’在挡板上
        # 跟随‘挡板’
        ball.x = paddle.x + 40
        ball.y = paddle.y - 20
    # 移动球    
    ball.x += ball.velocity.x
    ball.y += ball.velocity.y
    # 出界，则移动方向取反
    if ball.x < 0:
        ball.x = 0
        ball.velocity.x *= -1
    elif ball.x > 780:
        ball.x = 780
        ball.velocity.x *= -1
    if ball.y < 0:
        ball.y = 0
        ball.velocity.y *= -1
    elif ball.y > 580: #missed paddle
        waiting = True
        lives -= 1
        # if lives < 1: game_over = True

#this function test for collision between ball and paddle
def collision_ball_paddle():
    if pygame.sprite.collide_rect(ball, paddle):
        ball.velocity.y = -abs(ball.velocity.y)
        bx = ball.x + 8
        by = ball.y + 8
        px = paddle.x + paddle.frame_width/2
        py = paddle.y + paddle.frame_height/2
        if bx < px: #left side of paddle?
            ball.velocity.x = -abs(ball.velocity.x)
        else: #right side of paddle?
            ball.velocity.x = abs(ball.velocity.x)

#this function tests for collision between ball and blocks
def collision_ball_blocks():
    global score, block_group, ball
    
    hit_block = pygame.sprite.spritecollideany(ball, block_group)
    if hit_block != None:
        score += 10
        block_group.remove(hit_block)
        bx = ball.x + 8
        by = ball.y + 8

        #hit middle of block from above or below?
        if bx > hit_block.x+5 and bx < hit_block.x + hit_block.frame_width-5:
            if by < hit_block.y + hit_block.frame_height/2: #above?
                ball.velocity.y = -abs(ball.velocity.y)
            else: #below?
                ball.velocity.y = abs(ball.velocity.y)

        #hit left side of block?
        elif bx < hit_block.x + 5:
            ball.velocity.x = -abs(ball.velocity.x)
        #hit right side of block?
        elif bx > hit_block.x + hit_block.frame_width - 5:
            ball.velocity.x = abs(ball.velocity.x)

        #handle any other situation
        else:
            ball.velocity.y *= -1
    
    
#main program begins
game_init()
game_over = False
waiting = True
score = 0
lives = 3
level = 0
load_level()

#repeating loop
while True:
    timer.tick(30)
    ticks = pygame.time.get_ticks()

    #handle events
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
        elif event.type == MOUSEMOTION:
            movex,movey = event.rel
        elif event.type == MOUSEBUTTONUP:
            if waiting:
                waiting = False
                reset_ball()
        elif event.type == KEYUP:
            if event.key == K_RETURN: goto_next_level()

    #handle key presses
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: sys.exit()

    #do updates
    if not game_over:
        update_blocks()
        move_paddle()
        move_ball()
        collision_ball_paddle()
        collision_ball_blocks()

    #do drawing
    screen.fill((50,50,100))
    block_group.draw(screen)
    ball_group.draw(screen)
    paddle_group.draw(screen)
    print_text(font, screen, 0, 0, "SCORE " + str(score))
    print_text(font, screen, 200, 0, "LEVEL " + str(level+1))
    print_text(font, screen, 400, 0, "BLOCKS " + str(len(block_group)))
    print_text(font, screen, 670, 0, "BALLS " + str(lives))
    if game_over:
        print_text(font, screen, 300, 380, "G A M E   O V E R")
    pygame.display.update()
    

