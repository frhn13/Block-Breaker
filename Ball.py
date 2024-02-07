import pygame as pg

from Constants import SCREEN_WIDTH, SCREEN_HEIGHT

ball_img = pg.image.load("img/playerBlock.png").convert_alpha()


class Ball(pg.sprite.Sprite):
    def __init__(self, x, y, speed, width, height):
        pg.sprite.Sprite.__init__(self)
        self.xDirection = 1
        self.yDirection = -1
        self.speed = speed
        self.image = pg.transform.scale(ball_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        dx = self.xDirection * self.speed
        dy = self.yDirection * self.speed

        if self.rect.left <= 0:
            self.xDirection = 1
        if self.rect.right >= SCREEN_WIDTH:
            self.xDirection = -1
        if self.rect.top <= 0:
            self.yDirection = 1
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.yDirection = -1
            self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        self.rect.x += dx
        self.rect.y += dy
