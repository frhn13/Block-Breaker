import pygame as pg

ball_img = pg.image.load("img/playerBlock.png").convert_alpha()


class Ball(pg.sprite.Sprite):
    def __init__(self, x, y, speed):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.xDirection = 1
        self.yDirection = -1
        self.speed = speed
        self.image = pg.transform.scale(ball_img, (int(ball_img.get_width() * 0.1), int(ball_img.get_height()*0.1)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        dx = self.xDirection * self.speed
        dy = self.yDirection * self.speed

        self.rect.x += dx
        self.rect.y += dy
