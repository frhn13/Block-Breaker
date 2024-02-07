import pygame as pg

from Constants import SCREEN_WIDTH

pg.init()
screen = pg.display.set_mode((1, 1))
player_img = pg.image.load("img/playerBlock.png").convert_alpha()


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, speed, width, height):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pg.transform.scale(player_img, (int(player_img.get_width() * 1), int(player_img.get_height()*0.4)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.width = width
        self.height = height
        self.moving_left = False
        self.moving_right = False

    def update(self):
        dx = 0
        if self.moving_left and self.rect.left >= 0:
            dx = -self.speed
        if self.moving_right and self.rect.right <= SCREEN_WIDTH:
            dx = self.speed
        self.rect.x += dx
