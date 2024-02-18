import pygame as pg
import random
import time
from tkinter import messagebox

from Block import Block
from Player import Player
from Ball import Ball
from Constants import *
from Powerup import PowerUp
from Button import Button
from database_functions import *

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Block Breaker")


def write_text(text_x, text_y, contents, colour, font):
    text = font.render(contents, True, colour)
    screen.blit(text, (text_x, text_y))


def draw_bg(bg_colour):
    screen.fill(bg_colour)


def sign_up_page():
    pass


class FadeScreen:
    def __init__(self, colour, speed, fade_type):
        self.colour = colour
        self.fade_counter = 0
        self.speed = speed
        self.fade_type = fade_type

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        match self.fade_type:
            case "GameOver":
                pg.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))  # Moves top to bottom
                pg.draw.rect(screen, self.colour,
                             (0, SCREEN_HEIGHT - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))  # Moves bottom to top
                pg.draw.rect(screen, self.colour, (0, 0, 0 + self.fade_counter, SCREEN_HEIGHT))  # Moves left to right
                pg.draw.rect(screen, self.colour,
                             (SCREEN_WIDTH - self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))  # Moves right to left
                if self.fade_counter > SCREEN_WIDTH // 1.5:
                    fade_complete = True
            case "NextLevel":
                pg.draw.rect(screen, self.colour, (0, 0, 0 + self.fade_counter, SCREEN_HEIGHT))  # Moves left to right
                pg.draw.rect(screen, self.colour,
                             (SCREEN_WIDTH - self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))  # Moves right to left
                if self.fade_counter > SCREEN_WIDTH // 2:
                    fade_complete = True
            case "GameFinished":
                pg.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))  # Moves top to bottom
                pg.draw.rect(screen, self.colour,
                             (0, SCREEN_HEIGHT - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))  # Moves bottom to top
                if self.fade_counter > SCREEN_WIDTH // 2:
                    fade_complete = True
        return fade_complete


# Set the frame rate
clock = pg.time.Clock()

# Game variables
running = True
in_menu = True
in_game = False
setup_level = False
endless = False
player_x = 0
player_y = 0
game_state = GAME_STATES[5]
game_level = 1
ball_speed = 5
player_lives = 3
block_damage = 2
score = 0
max_blocks = 25
username = ""
password = ""
username_active = False
password_active = False
player_added = True
login_valid = True
username_rect = pg.Rect(250, 80, 200, 50)
password_rect = pg.Rect(250, 180, 300, 50)

# Images
player_img = pg.image.load("img/playerBlock.png").convert_alpha()
block_img = pg.image.load("img/Block.png").convert_alpha()
damaged_block_img = pg.image.load("img/CrackedBlock.png").convert_alpha()
ball_img = pg.image.load("img/playerBlock.png").convert_alpha()
power_up_imgs = [pg.image.load("img/bigger.png").convert_alpha(),
                 pg.image.load("img/smaller.png").convert_alpha(),
                 pg.image.load("img/ball.png").convert_alpha(),
                 pg.image.load("img/life.png").convert_alpha(),
                 pg.image.load("img/more_ball.png").convert_alpha()]
lives_img = pg.transform.scale(pg.image.load("img/heart.png").convert_alpha(), (20, 20))
start_button_img = pg.image.load("img/start_btn.png").convert_alpha()
end_button_img = pg.image.load("img/exit_btn.png").convert_alpha()
restart_button_img = pg.transform.scale(pg.image.load("img/restart_btn.png").convert_alpha(), (261, 99))
endless_button_img = pg.transform.scale(pg.image.load("img/endless_btn.png").convert_alpha(), (261, 99))
leaderboard_button_img = pg.transform.scale(pg.image.load("img/leaderboard_btn.png").convert_alpha(), (261, 99))
login_button_img = pg.transform.scale(pg.image.load("img/login_btn.png").convert_alpha(), (261, 99))
sign_up_button_img = pg.transform.scale(pg.image.load("img/sign_up_btn.png").convert_alpha(), (261, 99))
menu_button_img = pg.transform.scale(pg.image.load("img/menu_btn.png").convert_alpha(), (261, 99))

# Fonts
lives_font = pg.font.SysFont("Futura", 40)
game_over_font = pg.font.SysFont("Futura", 50)
winning_font = pg.font.SysFont("Futura", 50)
title_font = pg.font.SysFont("Futura", 50)

# Make the sprite groups
all_sprites = pg.sprite.Group()
ball_group = pg.sprite.Group()
block_group = pg.sprite.Group()
power_up_group = pg.sprite.Group()

# Game buttons
start_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200, start_button_img)
end_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200, end_button_img)
restart_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, restart_button_img)
next_level_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, start_button_img)
end_game_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, end_button_img)
endless_button = Button(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2, endless_button_img)
leaderboard_button = Button(SCREEN_WIDTH // 2 + 250, SCREEN_HEIGHT // 2, leaderboard_button_img)
login_button = Button(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2, login_button_img)
sign_up_button = Button(SCREEN_WIDTH // 2 + 250, SCREEN_HEIGHT // 2, sign_up_button_img)
sign_up_page_button = Button(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 200, sign_up_button_img)
login_page_button = Button(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 200, login_button_img)
menu_button = Button(SCREEN_WIDTH // 2 + 250, SCREEN_HEIGHT // 2 + 200, menu_button_img)
leaderboard_menu_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, menu_button_img)

# Fade animations
lives_lost_fade = FadeScreen(BLACK, 5, "GameOver")
next_level_fade = FadeScreen(GREEN, 4, "NextLevel")
beat_game_fade = FadeScreen(MENU_BG, 4, "GameFinished")

# Creates tables
tables_setup()

while running:
    clock.tick(FPS)
    match game_state:
        case "Register":
            draw_bg(MENU_BG)
            player_added = True
            login_valid = True
            username = ""
            password = ""
            if login_button.display(screen):
                game_state = GAME_STATES[7]
            if sign_up_button.display(screen):
                game_state = GAME_STATES[6]

        case "SignUp":
            draw_bg(MENU_BG)
            pg.draw.rect(screen, WHITE, username_rect)
            pg.draw.rect(screen, WHITE, password_rect)
            write_text(100, 100, f"Username: {username}", BLACK, lives_font)
            write_text(100, 200, f"Password:  {password}", BLACK, lives_font)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if username_rect.collidepoint(event.pos):
                        username_active = True
                        password_active = False
                    elif password_rect.collidepoint(event.pos):
                        username_active = False
                        password_active = True
                    else:
                        username_active = False
                        password_active = False

                if event.type == pg.KEYDOWN:
                    # Can only be alphanumeric
                    if (97 <= event.key <= 122 or 48 <= event.key <= 57) and username_active and len(username) < 10:
                        username += event.unicode
                    elif 33 <= event.key <= 126 and password_active and len(password) < 15:
                        password += event.unicode
                    elif event.key == pg.K_BACKSPACE:
                        if username_active:
                            username = username[:-1]
                        elif password_active:
                            password = password[:-1]
                    elif event.key == pg.K_ESCAPE:
                        running = False
                    else:
                        if username_active:
                            messagebox.showerror("Details invalid", "Username can only contain numbers or letters")
                        else:
                            messagebox.showerror("Details invalid", "Password can't contain that character")
            if sign_up_page_button.display(screen):
                if 4 <= len(username) <= 10 and 6 <= len(password) <= 15:
                    player_added = add_new_player(username, password)
                    if player_added:
                        game_state = GAME_STATES[5]
                    else:
                        messagebox.showerror("Details invalid", "Username already in use")
                else:
                    messagebox.showerror("Details invalid", "Username or password is too short")
            if menu_button.display(screen):
                game_state = GAME_STATES[5]
            if not player_added:
                write_text(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 100, "Username already in use", BLACK,
                           lives_font)

        case "Login":
            draw_bg(MENU_BG)
            pg.draw.rect(screen, WHITE, username_rect)
            pg.draw.rect(screen, WHITE, password_rect)
            write_text(100, 100, f"Username: {username}", BLACK, lives_font)
            write_text(100, 200, f"Password:  {password}", BLACK, lives_font)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if username_rect.collidepoint(event.pos):
                        username_active = True
                        password_active = False
                    elif password_rect.collidepoint(event.pos):
                        username_active = False
                        password_active = True
                    else:
                        username_active = False
                        password_active = False
                if event.type == pg.KEYDOWN:
                    # Can only be alphanumeric
                    if (97 <= event.key <= 122 or 48 <= event.key <= 57) and username_active and len(username) < 10:
                        username += event.unicode
                    elif 33 <= event.key <= 126 and password_active and len(password) < 15:
                        password += event.unicode
                    elif event.key == pg.K_BACKSPACE:
                        if username_active:
                            username = username[:-1]
                        elif password_active:
                            password = password[:-1]
                    elif event.key == pg.K_ESCAPE:
                        running = False
                    else:
                        if username_active:
                            messagebox.showerror("Details invalid", "Username can only contain numbers or letters")
                        else:
                            messagebox.showerror("Details invalid", "Password can't contain that character")
            if login_page_button.display(screen):
                login_valid = login_player(username, password)
                if login_valid:
                    game_state = GAME_STATES[0]
                else:
                    messagebox.showerror("Login details invalid", "Login details don't match any existing users")
            if menu_button.display(screen):
                game_state = GAME_STATES[5]

        case "MainMenu":
            draw_bg(MENU_BG)
            if start_button.display(screen):
                endless = False
                game_level = 1
                score = 0
                game_state = GAME_STATES[1]
            if end_button.display(screen):
                game_state = GAME_STATES[4]
            if endless_button.display(screen):
                endless = True
                game_level = 5
                score = 0
                start_time = time.perf_counter()
                game_state = GAME_STATES[1]
            if leaderboard_button.display(screen):
                game_state = GAME_STATES[8]

        case "Leaderboard":
            draw_bg(MENU_BG)
            top_scores = retrieve_top_scores()
            write_text(SCREEN_WIDTH // 2 - 100, 25, "Top 5 Scores", BLACK, title_font)
            for i in range(0, len(top_scores)):
                write_text(SCREEN_WIDTH // 2 - 300, (100 * (1 + i)) + 25, f"Username: {top_scores[i][2]}, Score: {top_scores[i][0]}, Time: {top_scores[i][1]}",
                           BLACK, lives_font)
            if leaderboard_menu_button.display(screen):
                game_state = GAME_STATES[0]

        case "Setup":
            # Initial game setup
            match game_level:
                case 1:
                    ball_speed = 5
                    player_lives = 3
                    block_damage = 2

                    for x in range(5):
                        for y in range(5):
                            block = Block(y * SCREEN_WIDTH // 5, x * 25, SCREEN_WIDTH // 5, 25, block_img)
                            block_group.add(block)
                            all_sprites.add(block)
                    max_blocks = len(block_group) - 1
                    game_state = GAME_STATES[2]
                case 2:
                    if next_level_fade.fade():
                        write_text(SCREEN_WIDTH // 2 - 100, 100, "Next Level", BLACK, winning_font)
                        if next_level_button.display(screen):
                            next_level_fade.fade_counter = 0
                            ball_speed = 7
                            player_lives = 3
                            block_damage = 1

                            for x in range(6):
                                for y in range(7):
                                    block = Block(y * SCREEN_WIDTH // 7, x * 25, SCREEN_WIDTH // 7, 25, block_img)
                                    block_group.add(block)
                                    all_sprites.add(block)
                            max_blocks = len(block_group) - 1
                            game_state = GAME_STATES[2]
                case 3:
                    if next_level_fade.fade():
                        write_text(SCREEN_WIDTH // 2 - 100, 100, "Next Level", BLACK, winning_font)
                        if next_level_button.display(screen):
                            next_level_fade.fade_counter = 0
                            ball_speed = 9
                            player_lives = 2
                            block_damage = 1

                            for x in range(7):
                                for y in range(10):
                                    block = Block(y * SCREEN_WIDTH // 10, x * 25, SCREEN_WIDTH // 10, 25, block_img)
                                    block_group.add(block)
                                    all_sprites.add(block)
                            max_blocks = len(block_group) - 1
                            game_state = GAME_STATES[2]
                case 5:
                    ball_speed = 5
                    player_lives = 3
                    block_damage = 2

                    for x in range(5):
                        for y in range(5):
                            # if x == 3 or x==4:
                            block = Block(y * SCREEN_WIDTH // 5, x * 25, SCREEN_WIDTH // 5, 25, block_img)
                            block_group.add(block)
                            all_sprites.add(block)
                    max_blocks = len(block_group) - 1
                    game_state = GAME_STATES[2]
                case 6:
                    ball_speed = 7
                    player_lives = 3
                    block_damage = 1

                    for x in range(6):
                        for y in range(7):
                            block = Block(y * SCREEN_WIDTH // 7, x * 25, SCREEN_WIDTH // 7, 25, block_img)
                            block_group.add(block)
                            all_sprites.add(block)
                    max_blocks = len(block_group) - 1
                    game_state = GAME_STATES[2]
                case 7:
                    ball_speed = 9
                    player_lives = 2
                    block_damage = 1

                    for x in range(7):
                        for y in range(10):
                            block = Block(y * SCREEN_WIDTH // 10, x * 25, SCREEN_WIDTH // 10, 25, block_img)
                            block_group.add(block)
                            all_sprites.add(block)
                    max_blocks = len(block_group) - 1
                    game_state = GAME_STATES[2]
                case _:
                    if beat_game_fade.fade():
                        write_text(SCREEN_WIDTH // 2 - 100, 100, "You Won!", BLACK, winning_font)
                        if end_game_button.display(screen):
                            game_state = GAME_STATES[0]
                            game_level = 1
                            beat_game_fade.fade_counter = 0
            if game_state == GAME_STATES[2]:
                if not endless or game_level == 5:
                    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75, 10, 150, 15, player_img)
                else:
                    player = Player(player_x, player_y, 10, 150, 15, player_img)
                all_sprites.add(player)
                ball = Ball(player.rect.centerx, player.rect.top, ball_speed, 5, 5, ball_img)
                all_sprites.add(ball)
                ball_group.add(ball)

        case "InGame":
            draw_bg(GAME_BG)  # Background redrawn every iteration
            player.update()

            all_sprites.update()
            all_sprites.draw(screen)

            write_text(10, SCREEN_HEIGHT - 50, f"LIVES: ", BLACK, lives_font)
            for x in range(player_lives):
                screen.blit(lives_img, (100 + (x * 30), SCREEN_HEIGHT - 45))

            if endless:
                write_text(SCREEN_WIDTH - 170, SCREEN_HEIGHT - 50, f"SCORE: {score}", BLACK, lives_font)

            # Collisions
            playerBallCollision = pg.sprite.spritecollide(player, ball_group, False)
            for collision in playerBallCollision:
                if collision.rect.centerx < (player.rect.centerx - (player.rect.centerx // 4)):
                    collision.xDirection = -1
                elif (player.rect.centerx - (player.rect.centerx // 4)) <= collision.rect.centerx < (
                        player.rect.centerx - (player.rect.centerx // 6)):
                    collision.xDirection = -0.75
                elif (player.rect.centerx - (player.rect.centerx // 6)) <= collision.rect.centerx < player.rect.centerx:
                    collision.xDirection = -0.5
                elif (player.rect.centerx + player.rect.centerx // 6) >= collision.rect.centerx > player.rect.centerx:
                    collision.xDirection = 0.5
                elif (player.rect.centerx + player.rect.centerx // 4) >= collision.rect.centerx > (
                        player.rect.centerx + player.rect.centerx // 6):
                    collision.xDirection = 0.75
                elif collision.rect.centerx > (player.rect.centerx + player.rect.centerx // 4):
                    collision.xDirection = 1
                collision.yDirection = -1

            playerPowerUpCollision = pg.sprite.spritecollide(player, power_up_group, True)
            for collision in playerPowerUpCollision:
                match collision.power_up_type:
                    case "IncreaseSize":
                        player.image = pg.transform.scale(player.image,
                                                          (player.image.get_width() + 10, player.image.get_height()))
                        if player.image.get_width() > 250:
                            player.image = pg.transform.scale(player.image, (250, player.image.get_height()))
                    case "DecreaseSize":
                        player.image = pg.transform.scale(player.image,
                                                          (player.image.get_width() - 10, player.image.get_height()))
                        if player.image.get_width() < 80:
                            player.image = pg.transform.scale(player.image, (80, player.image.get_height()))
                    case "AddBall":
                        ball = Ball(player.rect.centerx, player.rect.top, ball_speed, 5, 5, ball_img)
                        ball_group.add(ball)
                        all_sprites.add(ball)
                    case "ExtraLife":
                        if player_lives < 5:
                            player_lives += 1
                    case "AddManyBalls":
                        no_balls = random.randint(2, 5)
                        for x in range(no_balls):
                            ball = Ball(player.rect.right - (player.image.get_width() // (x + 1)), player.rect.top,
                                        ball_speed, 5, 5, ball_img)
                            ball_group.add(ball)
                            all_sprites.add(ball)

            for ball in ball_group:
                ballBlockCollision = pg.sprite.spritecollide(ball, block_group, False)
                for collision in ballBlockCollision:
                    collision.health -= block_damage
                    if collision.health <= 0:
                        collision.kill()
                        score += 1
                        if random.random() < 1:
                            power_up_type = random.randint(0, 4)
                            power_up_speed = random.randint(1, 5)
                            power_up = PowerUp(collision.rect.centerx, collision.rect.bottom,
                                               power_up_imgs[power_up_type],
                                               POWER_UPS[power_up_type], power_up_speed)
                            power_up_group.add(power_up)
                            all_sprites.add(power_up)
                    else:
                        collision.update_damage(damaged_block_img)
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
                    if ball.rect.left <= collision.rect.right or ball.rect.right >= collision.rect.left:
                        ball.xDirection *= -1
                    if ball.rect.bottom <= collision.rect.bottom:
                        ball.yDirection = -1
                    else:
                        ball.yDirection = 1

            if len(block_group) <= 0:
                if endless:
                    player_x = player.rect.centerx
                    player_y = player.rect.centery
                if not endless or game_level < 7:
                    game_level += 1
                all_sprites.empty()
                block_group.empty()
                power_up_group.empty()
                ball_group.empty()
                game_state = GAME_STATES[1]

            if len(ball_group) == 0 and game_state == GAME_STATES[2]:
                player_lives -= 1
                if player_lives > 0:
                    ball = Ball(player.rect.centerx, player.rect.top, ball_speed, 5, 5, ball_img)
                    ball_group.add(ball)
                    all_sprites.add(ball)

            if player_lives <= 0 and game_state == GAME_STATES[2]:
                end_time = time.perf_counter()
                if lives_lost_fade.fade():
                    write_text(SCREEN_WIDTH // 2 - 100, 100, "Game Over!", WHITE, game_over_font)
                    if restart_button.display(screen):
                        if endless:
                            total_time = round(end_time - start_time, 2)
                            add_player_score(username, score, total_time)
                        endless = False
                        all_sprites.empty()
                        block_group.empty()
                        power_up_group.empty()
                        ball_group.empty()
                        game_state = GAME_STATES[0]
                        lives_lost_fade.fade_counter = 0

        case "ExitGame":
            running = False

    # Events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_state = GAME_STATES[4]
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
