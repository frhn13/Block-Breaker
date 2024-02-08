import pygame as pg
import random

from Block import Block
from Player import Player
from Ball import Ball
from Constants import *
from Powerup import PowerUp

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Block Breaker")


def draw_bg():
    screen.fill(BG)


# Set the frame rate
clock = pg.time.Clock()

running = True

# Images
player_img = pg.image.load("img/playerBlock.png").convert_alpha()
block_img = pg.image.load("img/Block.png").convert_alpha()
ball_img = pg.image.load("img/playerBlock.png").convert_alpha()
power_up_imgs = [pg.image.load("img/bigger.png").convert_alpha(),
                pg.image.load("img/smaller.png").convert_alpha(),
                pg.image.load("img/life.png").convert_alpha(),
                pg.image.load("img/ball.png").convert_alpha(),
                pg.image.load("img/more_ball.png").convert_alpha()]

# Make objects
player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT-50, 10, 150, 15, player_img)
ball = Ball(player.rect.centerx, player.rect.top, 5, 5, 5, ball_img)

# Make the sprite groups
all_sprites = pg.sprite.Group()
ball_group = pg.sprite.Group()
block_group = pg.sprite.Group()
power_up_group = pg.sprite.Group()

all_sprites.add(player)
all_sprites.add(ball)
ball_group.add(ball)

for x in range(5):
    for y in range(5):
        block = Block(y*SCREEN_WIDTH//5, x*15, SCREEN_WIDTH//5, 15, block_img)
        block_group.add(block)
        all_sprites.add(block)

while running:
    clock.tick(FPS)
    draw_bg()  # Background redrawn every iteration
    player.update()

    all_sprites.update()
    all_sprites.draw(screen)

    playerBallCollision = pg.sprite.spritecollide(player, ball_group, False)
    for collision in playerBallCollision:
        if collision.rect.centerx < (player.rect.centerx - (player.rect.centerx // 4)):
            collision.xDirection = -1
        if (player.rect.centerx - (player.rect.centerx // 4)) <= collision.rect.centerx < (player.rect.centerx - (player.rect.centerx // 6)):
            collision.xDirection = -0.75
        elif (player.rect.centerx - (player.rect.centerx // 6)) <= collision.rect.centerx < player.rect.centerx:
            collision.xDirection = -0.5
        elif (player.rect.centerx + player.rect.centerx // 6) >= collision.rect.centerx > player.rect.centerx:
            collision.xDirection = 0.5
        elif (player.rect.centerx + player.rect.centerx // 4) >= collision.rect.centerx > (player.rect.centerx + player.rect.centerx // 6):
            collision.xDirection = 0.75
        else:
            collision.xDirection = 1
        collision.yDirection = -1
        print(len(block_group))
        if len(block_group) == 0:
            running = False

    for ball in ball_group:
        ballBlockCollision = pg.sprite.spritecollide(ball, block_group, True)
        for collision in ballBlockCollision:
            if random.random() > 0:
                power_up_type = random.randint(0, 4)
                power_up_speed = random.randint(1, 5)
                power_up = PowerUp(collision.rect.centerx, collision.rect.bottom, power_up_imgs[power_up_type],
                                   POWER_UPS[power_up_type], power_up_speed)
                power_up_group.add(power_up)
                all_sprites.add(power_up)
            if ball.rect.centerx < (collision.rect.centerx - (collision.rect.centerx // 4)):
                ball.xDirection = -1
            if (collision.rect.centerx - (collision.rect.centerx // 4)) <= ball.rect.centerx < (
                    collision.rect.centerx - (collision.rect.centerx // 6)):
                ball.xDirection = -0.75
            elif (collision.rect.centerx - (collision.rect.centerx // 6)) <= ball.rect.centerx < collision.rect.centerx:
                ball.xDirection = -0.5
            elif (collision.rect.centerx + collision.rect.centerx // 6) >= ball.rect.centerx > collision.rect.centerx:
                ball.xDirection = 0.5
            elif (collision.rect.centerx + collision.rect.centerx // 4) >= ball.rect.centerx > (
                    collision.rect.centerx + collision.rect.centerx // 6):
                ball.xDirection = 0.75
            else:
                ball.xDirection = 1
            if abs(ball.rect.centery - collision.rect.top) < abs(ball.rect.centery - collision.rect.bottom):
                ball.yDirection = -1
            else:
                ball.yDirection = 1

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT and player.rect.left >= 0:
                player.moving_left = True
            if event.key == pg.K_RIGHT and player.rect.right <= SCREEN_WIDTH:
                player.moving_right = True
            if event.key == pg.K_ESCAPE:
                running = False

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                player.moving_left = False
            if event.key == pg.K_RIGHT:
                player.moving_right = False
    pg.display.update()
pg.quit()
