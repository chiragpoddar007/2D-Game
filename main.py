from player import Player
from button import Button
from bullet import Bullet
from enemy import Enemy
from explosion import Explosion
import settings
import pygame
import sys

def draw_hearts(screen, health):
    for i in range(health):
        x = WIDTH - 40 - (i * 40)
        y = 20

        # Draw heart using two circles + triangle
        pygame.draw.circle(screen,(255,0,0),(x,y),10)
        pygame.draw.circle(screen,(255,0,0),(x + 15,y),10)

        points = [
            (x - 10, y),
            (x + 25, y),
            (x + 7, y + 25)
        ]

        pygame.draw.polygon(screen,(255,0,0),points)

def draw_home_button(screen, rect, bg_color = (40,40,40), icon_color = (255,255,255)):
    # ROUNDED SQUARE BG
    pygame.draw.rect(screen, bg_color, rect, border_radius = 20)

    cx, cy = rect.center

    # ROOF
    roof_points = [
        (cx - 20, cy - 5),
        (cx, cy - 25),
        (cx + 20, cy - 5)
    ]
    pygame.draw.polygon(screen, icon_color, roof_points, width=4)

    # HOUSE BODY
    body_rect = pygame.Rect(0,0,28,22)
    body_rect.center = (cx,cy + 10)
    pygame.draw.rect(screen, icon_color, body_rect, width=4)

    # DOOR
    door_rect = pygame.Rect(0,0,8,12)
    door_rect.midbottom = body_rect.midbottom
    pygame.draw.rect(screen, icon_color,door_rect)

def draw_restart_button(screen, rect, bg_color = (40,40,40), icon_color = (255,255,255)):
    pygame.draw.rect(screen,bg_color,rect,border_radius=20)

    cx,cy = rect.center

    # CIRCULAR ARROW
    pygame.draw.circle(screen, icon_color, (cx, cy), 18,4)

    arrow_points = [
        (cx + 15, cy - 5),
        (cx + 15, cy - 5),
        (cx + 20, cy + 5)
    ]
    pygame.draw.polygon(screen, icon_color, arrow_points)

def draw_settings_button(screen, rect, bg_color = (40,40,40),icon_color=(255,255,255)):
    pygame.draw.rect(screen,bg_color,rect,border_radius=20)

    cx,cy = rect.center

    pygame.draw.circle(screen, icon_color, (cx, cy), 15,4)

    for angle in range(0,360,45):
        x = cx + 22 * pygame.math.Vector2(1,0).rotate(angle).x
        y = cy + 22 * pygame.math.Vector2(1,0).rotate(angle).x
        pygame.draw.circle(screen, icon_color, (int(x), int(y)),3)

#---------------------------------------------------------------------------------------------

pygame.init()
pygame.mixer.init()

try:
    with open("highscore.txt","r") as file:
        high_score = int(file.read())
except:
    high_score = 0

WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT

home_button_rect = pygame.Rect(0,0,90,90)
home_button_rect.center = (WIDTH // 2 - 150, HEIGHT // 2 + 60)

restart_button_rect = pygame.Rect(0,0,90,90)
restart_button_rect.center = (WIDTH // 2, HEIGHT // 2 + 60)

settings_button_rect = pygame.Rect(0,0,90,90)
settings_button_rect.center = (WIDTH // 2 + 150, HEIGHT // 2 + 60)

# Center Layout
center_x = WIDTH // 2
center_y = HEIGHT // 2
start_y = 250
gap = 90
icon_y = center_y + 80

# Screen
screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("2D Space Shooting Game")

#Button
start_button = Button("START", center_x - 150, start_y, 300, 60, settings.BUTTON_COLOR)
settings_button = Button("SETTINGS", center_x - 150, start_y + gap, 300, 60, settings.BUTTON_COLOR)
back_button = Button("BACK", center_x - 150, start_y + gap * 3, 300, 60, settings.BUTTON_COLOR)

music_button = Button("MUISC: ON", center_x - 150, start_y, 300, 60, settings.BUTTON_COLOR)
volume_up = Button("VOL +", center_x - 160, start_y + gap, 140, 50, settings.BUTTON_COLOR)
volume_down = Button("VOL -", center_x + 20, start_y + gap, 140, 50, settings.BUTTON_COLOR)
keybind_button = Button("CHANGE SHOOT KEY", center_x - 150, start_y + gap * 2, 300, 60, settings.BUTTON_COLOR)

pause_resume_button = Button("RESUME", WIDTH // 2 - 150, 300, 300, 60, settings.BUTTON_COLOR)
pause_restart_button = Button("RESTART", WIDTH // 2 - 150, 380, 300, 60, settings.BUTTON_COLOR)
pause_home_button = Button("HOME", WIDTH // 2 - 150, 460, 300, 60, settings.BUTTON_COLOR)

# Background
background = pygame.image.load("assets//Image//space_background.png").convert()
background = pygame.transform.scale(background,(WIDTH,HEIGHT))

player = Player()

# Varibles
music_on = True
volume = 0.4

shoot_key = pygame.K_SPACE
waiting_for_key = False
new_high_score = False

bullets =[]
enemies = []
explosions = []

max_health = 3
health = max_health

invincible = False
invincible_timer = 0
invincible_duration = 1000 # ONE SECOND

score = 0

MENU = 0
SETTINGS = 1
PLAYING = 2
PAUSED = 3
GAME_OVER = 4

pygame.mixer_music.load("assets\\Music\\bg_music.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

shoot_sound = pygame.mixer.Sound("assets\\Sound\\laser.wav")
explosion_sound = pygame.mixer.Sound("assets\\Sound\\explosion.wav")
gameover_sound = pygame.mixer.Sound("assets\\Sound\\gameover.wav")

shoot_sound.set_volume(0.5)
explosion_sound.set_volume(0.5)
gameover_sound.set_volume(1)

game_state = MENU

font = pygame.font.SysFont(None,50)
title_font = pygame.font.SysFont("arialblack", 60)

enemy_spawn_delay = settings.ENEMY_SPAWN_DELAY
last_spawn_time = pygame.time.get_ticks()

clock = pygame.time.Clock()

FPS = settings.FPS

running = True
while running:
    clock.tick(FPS)

# EVENT BLOCK which is the core of the program

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # MOUSE SECTION

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if game_state == MENU:
                if start_button.is_clicked(mouse_pos):
                    game_state = PLAYING

                elif settings_button.is_clicked(mouse_pos):
                    pervious_state = game_state
                    game_state = SETTINGS

            elif game_state == SETTINGS:

        # MUSIC BUTTON

                if music_button.is_clicked(mouse_pos):
                    music_on = not music_on

                    if music_on:
                        pygame.mixer.music.play(-1)
                        music_button.text = "MUSIC: ON"
                        
                    else:
                        pygame.mixer.music.stop()
                        music_button.text = "MUSIC: OFF"

        # VOLUME BUTTON

                if volume_up.is_clicked(mouse_pos):
                        volume = min(1.0, volume + 0.1)
                        pygame.mixer.music.set_volume(volume)

                elif volume_down.is_clicked(mouse_pos):
                        volume = max(0.0, volume - 0.1)
                        pygame.mixer.music.set_volume(volume)

        # KEYBIND BUTTON

                if keybind_button.is_clicked(mouse_pos):
                    waiting_for_key = True

        # BACK BUTTON  

                if back_button.is_clicked(mouse_pos):
                    game_state = previous_state

        #PAUSE BUTTON

            elif game_state == PAUSED:

                if pause_resume_button.is_clicked(mouse_pos):
                    game_state = PLAYING

                elif pause_restart_button.is_clicked(mouse_pos):
                    enemies.clear()
                    bullets.clear()
                    score = 0
                    health = 3
                    player.rect.center = (WIDTH // 2, HEIGHT - 100)
                    pygame.mixer.music.play(-1)
                    game_state = PLAYING

                elif pause_home_button.is_clicked(mouse_pos):
                    enemies.clear()
                    bullets.clear()
                    score = 0
                    health = 3
                    pygame.mixer.music.play(-1)
                    game_state = MENU

            elif game_state == GAME_OVER:

                if home_button_rect.collidepoint(mouse_pos):
                    enemies.clear()
                    bullets.clear()
                    explosions.clear()
                    health = max_health
                    score = 0
                    game_state = MENU 

                elif restart_button_rect.collidepoint(mouse_pos):
                    enemies.clear()
                    bullets.clear()
                    explosions.clear()
                    health = max_health
                    score = 0
                    player.rect.center = (WIDTH // 2, HEIGHT - 100)
                    pygame.mixer.music.play(-1)
                    game_state = PLAYING

                elif settings_button_rect.collidepoint(mouse_pos):
                    previous_state = game_state
                    game_state = SETTINGS

    # KEYBOARD SECTION

        elif event.type == pygame.KEYDOWN:

            if waiting_for_key:
                shoot_key = event.key
                waiting_for_key = False

            elif game_state == GAME_OVER and event.key == pygame.K_SPACE:
                enemies.clear()
                bullets.clear()
                explosions.clear()
                health = max_health
                score = 0
                pygame.mixer.music.play(-1)
                game_state = PLAYING
            
            elif event.key == pygame.K_p:
                if game_state == PLAYING:
                    game_state = PAUSED
                elif game_state == PAUSED:
                    game_state = PLAYING

            elif game_state == PLAYING and event.key == shoot_key:
                bullet = Bullet(player.rect.centerx - 2, player.rect.top)
                bullets.append(bullet)
                shoot_sound.play()

    screen.blit(background,(0,0))

# DRAWING BLock which display item in screen

    if game_state == MENU:
        title = title_font.render("2D SPACE SHOOTER", True, settings.ACCENT)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        start_button.draw(screen)
        settings_button.draw(screen)

    elif game_state == SETTINGS:
        title = font.render("SETTINGS",True,(255,255,255))
        screen.blit(title,(WIDTH // 2 - 100,100))

        music_button.draw(screen)
        volume_up.draw(screen)
        volume_down.draw(screen)
        keybind_button.draw(screen)
        back_button.draw(screen)

    elif game_state == PLAYING:
        player.move(WIDTH,HEIGHT)

        if invincible:
            current_time = pygame.time.get_ticks()
            if current_time - invincible_timer > invincible_duration:
                invincible = False

        if not invincible or (pygame.time.get_ticks() // 100) % 2 == 0:
            player.draw(screen)
        
        draw_hearts(screen,health)

        for bullet in bullets[:]:
            bullet.move()
            bullet.draw(screen)

            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        current_time = pygame.time.get_ticks()

        if current_time - last_spawn_time > enemy_spawn_delay:
            enemy_spawn_delay = max(300, enemy_spawn_delay - 10)
            enemy = Enemy(WIDTH)
            enemies.append(enemy)
            last_spawn_time = current_time

        for enemy in enemies[:]:
            enemy.move()
            enemy.draw(screen)

            # Check collsion with player
            if enemy.rect.colliderect(player.rect) and not invincible:
                enemies.remove(enemy)
                health -= 1
                invincible - True
                invincible_timer = pygame.time.get_ticks()

                if health <= 0:
                    pygame.mixer.music.stop()
                    gameover_sound.play()

                    if score > high_score:
                        high_score = score
                        new_high_score = True
                        with open("highscore.txt", "w") as file:
                            file.write(str(high_score))
                    else:
                        new_high_score = False

                    game_state = GAME_OVER

            # Remove enemy if it goes off screen
            if enemy.rect.top > HEIGHT:
                enemies.remove(enemy)

            for bullet in bullets[:]:
                if enemy.rect.colliderect(bullet.rect):

                    # EXPLOSION
                    explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                    explosions.append(explosion)

                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                    explosion_sound.play()
                    break

            for explosion in explosions[:]:
                explosion.update()
                explosion.draw(screen)

                if explosion.finished:
                    explosions.remove(explosion)
            
        score_text = font.render(f"Score: {score}",True,(255,255,255))
        screen.blit(score_text,(10,10))

    elif game_state == PAUSED:
        player.draw(screen)
        draw_hearts(screen, health)

        for bullet in bullets:
            bullet.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        # DARK OVERLAY
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # PAUSE TITLE
        pause_title = title_font.render("GAME PAUSED", True, settings.ACCENT)
        screen.blit(pause_title, (WIDTH // 2 - pause_title.get_width() // 2, 200))

        pause_resume_button.draw(screen)
        pause_restart_button.draw(screen)
        pause_home_button.draw(screen)

    elif game_state == GAME_OVER:

        # DARK OVERLAY
        overlay = pygame.Surface((WIDTH,HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

        restart_text = font.render("Press Space Key Restart", True, (255,255,255))
        
        # TITLE
        score_text = font.render(f"Final Score: {score}", True, (255,255,255))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, center_y - 100))

        high_score_text = font.render(f"High Score: {high_score}", True, (255,255,255))
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, center_y - 60))

        if new_high_score:
            new_text = font.render("NEW HIGH SCORE!", True, (255,215,0))
            screen.blit(new_text, (WIDTH // 2 - new_text.get_width() // 2, center_y - 20))

        game_over_text = font.render("GAME OVER",True,(255,0,0))
        screen.blit(game_over_text,(WIDTH // 2 - game_over_text.get_width() // 2, center_y - 180))

        # HOVER CHECK HERE
        mouse_pos = pygame.mouse.get_pos()

        home_button_rect.center = (WIDTH // 2 - 150, icon_y)
        restart_button_rect.center = (WIDTH // 2, icon_y)
        settings_button_rect.center = (WIDTH // 2  + 150, icon_y)

        # HOME
        if home_button_rect.collidepoint(mouse_pos):
            draw_home_button(screen,home_button_rect, bg_color=(70,70,70))
        else:
            draw_home_button(screen, home_button_rect)

        # RESTART
        if restart_button_rect.collidepoint(mouse_pos):
            draw_restart_button(screen,restart_button_rect, bg_color=(70,70,70))
        else:
            draw_restart_button(screen, restart_button_rect)

        # SETTINGS
        if settings_button_rect .collidepoint(mouse_pos):
            draw_settings_button(screen,settings_button_rect, bg_color=(70,70,70))
        else:
            draw_settings_button(screen, settings_button_rect)

    pygame.display.update()

pygame.quit()
sys.exit()