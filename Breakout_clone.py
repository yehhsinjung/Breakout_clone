import pygame
import random
import os

FPS = 60
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("打磚塊遊戲")
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
WHITE = pygame.Color(255,255,255)
BLACK = pygame.Color(0,0,0)
clock = pygame.time.Clock()

# 載入音效
shooting_sound = pygame.mixer.Sound(os.path.join("sound", "shooting.wav"))
collision_sound = pygame.mixer.Sound(os.path.join("sound", "collision.wav"))

#定義物件
class Board (pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,width,height)

    def draw (self):
        pygame.draw.rect(screen,WHITE,self.rect)

class Ball (pygame.sprite.Sprite):
    def __init__(self,x,y,radius):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.rect = pygame.Rect(x,y,radius*2,radius*2)

    def draw (self):
        circle_pos = (self.rect.left + self.radius, self.rect.top + self.radius)
        ball_color = (102, 204, 255)
        pygame.draw.circle(screen,ball_color,circle_pos,self.radius)

class Brick (pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,width,height)
        self.visible = True

    def draw (self):
        if self.visible:
            pygame.draw.rect(screen,self.color,self.rect)

#定義文字
class Text():
    def __init__(self,text,size,color,position=(0,0)):
        self.font = pygame.font.SysFont('Lato', size)
        self.surface = self.font.render(text,True, WHITE)
        self.rect = self.surface.get_rect()
        self.rect.midtop = position

    def display(self):
        screen.blit(self.surface, self.rect)

#遊戲初始 & 更新
def restGame():
    global game_mode, brick_num, bricks_group, score, life, dx, dy

    for brick in bricks_group:
        r = random.randint(100,200)
        g = random.randint(100,200)
        b = random.randint(100,200)
        brick.color = [r,g,b]
        brick.visible = True

    # 0: 待開球/ 1: 遊戲開始
    game_mode = 0
    score = 0
    life = 3
    # 移動速度
    dx = 8
    dy = -8

game_mode = 0
score = 0
life = 3
# 移動速度
dx = 8
dy = -8


#板子
board_width = 120
board_height = 22
board_x = WIDTH-board_width/2
board_y = HEIGHT-board_height-10
board = Board(board_x, board_y, board_width, board_height)

#球
ball_radius = 9
ball_x = board.rect.centerx - ball_radius
ball_y = board.rect.top - ball_radius*2
ball = Ball(ball_x, ball_y, ball_radius)

#磚塊們
bricks_group = []
brick_num = 0
brick_width = 60
brick_height = 16
brick_a, brick_b = 25,25
brick_c, brick_d = 0,0

for i in range (0,108):
    if (i%12) == 0:
        brick_c = 0
        brick_d += 18

    brick_x = brick_a + brick_c
    brick_y = brick_b + brick_d
    bricks_group.append(Brick(brick_x, brick_y, brick_width, brick_height))
    brick_c += 60

#用函式初始遊戲
restGame()
#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        #判斷mouse:用pygame.mouse.get_pos()取得游標移動的X值；-50讓游標指定在板子中間
        if event.type == pygame.MOUSEMOTION:
            board_x = pygame.mouse.get_pos()[0]-50
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_mode == 0:
                game_mode = 1
                shooting_sound.play()
                shooting_sound.set_volume(0.6)
    screen.fill(BLACK)

    #分數文字
    score_text_pos = (WIDTH//15, HEIGHT//60)
    score_text = Text("SCORE:" + str(score), 26, WHITE, score_text_pos)
    score_text.display()

    #生命文字
    life_text_pos = (WIDTH//6, HEIGHT//60)
    life_text = Text("LIFE:" + str(life), 26, WHITE, life_text_pos)
    life_text.display()

    # 畫出磚塊
    for bricks in bricks_group:
        #判斷球跟磚塊是否碰撞
        if pygame.sprite.collide_rect(ball, bricks):
            collision_sound.play()
            collision_sound.set_volume(0.7)
            if bricks.visible:
                brick_num -= 1
                score += 1
                if brick_num ==0:
                    restGame()
                    break
                #球反彈路徑
                dy = -dy
            bricks.visible = False
        bricks.draw()

    # 畫出板子
    board.rect[0] = board_x
    board.draw()

    #球 V.S. 板子的碰撞
    if pygame.sprite.collide_rect(ball, board):
        dy = -dy


    #球的狀態
    #0:待開球(球隨板子移動)
    if game_mode == 0:
        ball_x = board.rect[0] + board_width/2 - ball_radius
        ball_y = board.rect[1] - ball_radius*2
        ball.rect[0] = ball_x
        ball.rect[1] = ball_y

    #1:遊戲開始，球持續移動
    elif game_mode == 1:
        ball_x += dx
        ball_y += dy

    #球掉出板子外:死亡
        if ball_y + dy > HEIGHT - ball_radius:
            game_mode = 0
            life = life - 1
            if life == 0:
                restGame()

    #球 V.S. 牆壁的碰撞
        if ball_x + dx > WIDTH - ball_radius or ball_x + dx < ball_radius:
            dx = -dx
        if ball_y + dy > WIDTH - ball_radius or ball_y + dy < ball_radius:
            dy = -dy


        ball.rect[0] = ball_x
        ball.rect[1] = ball_y

    ball.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
