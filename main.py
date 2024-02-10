import pygame as pg
import random

from Block import Block
from Player import Player
from Ball import Ball
from Constants import *
from Powerup import PowerUp
from Button import Button

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Block Breaker")


def write_text(text_x, text_y, contents, colour, font):
    text = font.render(contents, True, colour)
    screen.blit(text, (text_x, text_y))


def draw_bg(bg_colour):
    screen.fill(bg_colour)


class FadeOut:
    def __init__(self, colour, speed):
        self.colour = colour
        self.fade_counter = 0
        self.speed = speed

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        pg.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))  # Moves top to bottom
        pg.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))  # Moves bottom to top
        pg.draw.rect(screen, self.colour, (0, 0, 0 + self.fade_counter, SCREEN_HEIGHT))  # Moves left to right
        pg.draw.rect(screen, self.colour, (SCREEN_WIDTH - self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))  # Moves right to left
        if self.fade_counter > SCREEN_WIDTH // 2:
            fade_complete = True
        return fade_complete


# Set the frame rate
clock = pg.time.Clock()

# Game variables
running = True
in_menu = True
in_game = False

# Images
player_img = pg.image.load("img/playerBlock.png").convert_alpha()
block_img = pg.image.load("img/Block.png").convert_alpha()
ball_img = pg.image.load("img/playerBlock.png").convert_alpha()
power_up_imgs = [pg.image.load("img/bigger.png").convert_alpha(),
                pg.image.load("img/smaller.png").convert_alpha(),
                pg.image.load("img/ball.png").convert_alpha(),
                pg.image.load("img/life.png").convert_alpha(),
                pg.image.load("img/more_ball.png").convert_alpha()]
lives_img = pg.transform.scale(pg.image.load("img/heart.png").convert_alpha(), (20, 20))
start_button_img = pg.image.load("img/start_btn.png").convert_alpha()
end_button_img = pg.image.load("img/exit_btn.png").convert_alpha()
restart_button_img = pg.image.load("img/restart_btn.png").convert_alpha()

# Fonts
lives_font = pg.font.SysFont("Futura", 40)
game_over_font = pg.font.SysFont("Futura", 50)

# Make the sprite groups
all_sprites = pg.sprite.Group()
ball_group = pg.sprite.Group()
block_group = pg.sprite.Group()
power_up_group = pg.sprite.Group()

start_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200, start_button_img)
end_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200, end_button_img)
restart_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, restart_button_img)
lives_lost_fade = FadeOut(BLACK, 5)

while running:
    clock.tick(FPS)
    if in_menu:
        draw_bg(MENU_BG)
        if start_button.display(screen):
            in_menu = False
            # Initial game setup
            player_lives = 1
            player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75, 10, 150, 15, player_img)
            ball = Ball(player.rect.centerx, player.rect.top, 5, 5, 5, ball_img)
            all_sprites.add(player)
            all_sprites.add(ball)
            ball_group.add(ball)
            for x in range(5):
                for y in range(5):
                    block = Block(y * SCREEN_WIDTH // 5, x * 25, SCREEN_WIDTH // 5, 25, block_img)
                    block_group.add(block)
                    all_sprites.add(block)
            in_game = True
        if end_button.display(screen):
            running = False

    if in_game:
        draw_bg(GAME_BG)  # Background redrawn every iteration
        player.update()

        all_sprites.update()
        all_sprites.draw(screen)

        write_text(10, SCREEN_HEIGHT - 50, f"LIVES: ", BLACK, lives_font)
        for x in range(player_lives):
            screen.blit(lives_img, (100 + (x*30), SCREEN_HEIGHT - 45))

        # Collisions
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

        playerPowerUpCollision = pg.sprite.spritecollide(player, power_up_group, True)
        for collision in playerPowerUpCollision:
            match collision.power_up_type:
                case "IncreaseSize":
                    player.image = pg.transform.scale(player.image, (player.image.get_width() + 10, player.image.get_height()))
                    if player.image.get_width() > 250:
                        player.image = pg.transform.scale(player.image, (250, player.image.get_height()))
                case "DecreaseSize":
                    player.image = pg.transform.scale(player.image, (player.image.get_width() - 10, player.image.get_height()))
                    if player.image.get_width() < 80:
                        player.image = pg.transform.scale(player.image, (80, player.image.get_height()))
                case "AddBall":
                    ball = Ball(player.rect.centerx, player.rect.top, 5, 5, 5, ball_img)
                    ball_group.add(ball)
                    all_sprites.add(ball)
                case "ExtraLife":
                    if player_lives < 5:
                        player_lives += 1
                case "AddManyBalls":
                    no_balls = random.randint(2, 5)
                    for x in range(no_balls):
                        ball = Ball(player.rect.right-(player.image.get_width()//(x+1)), player.rect.top, 5, 5, 5, ball_img)
                        ball_group.add(ball)
                        all_sprites.add(ball)

        for ball in ball_group:
            ballBlockCollision = pg.sprite.spritecollide(ball, block_group, True)
            for collision in ballBlockCollision:
                if random.random() < 0.2:
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
                elif (collision.rect.centerx - (
                        collision.rect.centerx // 6)) <= ball.rect.centerx < collision.rect.centerx:
                    ball.xDirection = -0.5
                elif (
                        collision.rect.centerx + collision.rect.centerx // 6) >= ball.rect.centerx > collision.rect.centerx:
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

        if len(block_group) == 0:
            all_sprites.empty()
            in_game = False
            in_menu = True  # Game ends when all balls hit

        if len(ball_group) == 0:
            player_lives -= 1
            ball = Ball(player.rect.centerx, player.rect.top, 5, 5, 5, ball_img)
            ball_group.add(ball)
            all_sprites.add(ball)

        if player_lives <= 0:
            all_sprites.empty()
            if lives_lost_fade.fade():
                write_text(SCREEN_WIDTH // 2 - 100, 100, "Game Over!", WHITE, game_over_font)
                if restart_button.display(screen):
                    in_game = False
                    in_menu = True

    # Events
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
