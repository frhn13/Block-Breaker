import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, speed, width, height):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height

    def update(self):
        pass
