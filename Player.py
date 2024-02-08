import pygame as pg

from Constants import SCREEN_WIDTH


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, speed, width, height, image):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.moving_left = False
        self.moving_right = False

    def update(self):
        dx = 0
        if self.moving_left and self.rect.left >= 0:
            dx = -self.speed
        if self.moving_right and self.rect.right <= SCREEN_WIDTH:
            dx = self.speed
        self.rect.x += dx
