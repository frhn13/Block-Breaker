import random

import pygame as pg

from Constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Ball(pg.sprite.Sprite):
    def __init__(self, x, y, speed, width, height, image):
        pg.sprite.Sprite.__init__(self)
        self.xDirection = random.choice([1, -1])
        self.yDirection = -1
        self.xSpeed = speed
        self.ySpeed = speed
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        dx = self.xDirection * self.xSpeed
        dy = self.yDirection * self.ySpeed

        if self.rect.left <= 0:
            self.xDirection = 1
        if self.rect.right >= SCREEN_WIDTH:
            self.xDirection = -1
        if self.rect.top <= 0:
            self.yDirection = 1
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()

        self.rect.x += dx
        self.rect.y += dy
