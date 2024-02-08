import pygame as pg

from Constants import SCREEN_HEIGHT


class PowerUp(pg.sprite.Sprite):
    def __init__(self, x, y, image, power_up_type, speed):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.power_up_type = power_up_type
        self.speed = speed

    def update(self):
        dy = self.speed
        self.rect.y += dy
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
