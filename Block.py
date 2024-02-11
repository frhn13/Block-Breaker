import pygame as pg


class Block(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(image, (width, height))
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.health = 2

    def update_damage(self, image):
        self.image = pg.transform.scale(image, (self.width, self.height))
