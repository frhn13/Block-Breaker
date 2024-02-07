import pygame as pg
from Player import Player
from Ball import Ball

from Constants import *

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Block Breaker")


def draw_bg():
    screen.fill(BG)


# Set the frame rate
clock = pg.time.Clock()

running = True

# Make objects
player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT-50, 10, 100, 20)
ball = Ball(player.rect.centerx, player.rect.top, 5)

# Make the sprite groups
ball_group = pg.sprite.Group()
ball_group.add(ball)

while running:
    clock.tick(FPS)
    draw_bg()  # Background redrawn every iteration
    player.update()

    screen.blit(player.image, player.rect)

    ball_group.update()
    ball_group.draw(screen)

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
