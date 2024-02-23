import pygame
import os
import random

# import random
# pygame.font.init()
pygame.init()
# sounds by: Kastenfrosch, AbdrTar from free sound
#                                   variables begin
# Admin = "G"
# Login_attempt = 3         1100, 700
winWidth, winHeight = 1200, 700
BACKGROUND_SCALE = 2
BACKGROUND_POS_X, BACKGROUND_POS_Y = -0, -60
DisplayName = "First Game"
White = (255, 255, 255)
BLACK = (0, 100, 0)
BackgroundRGB = White
GAME = 1
SMASH_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Grenade+1.mp3'))
CATCH_SOUND = pygame.mixer.Sound(os.path.join('Assets', '519421_catch.mp3'))
WINNER_SOUND = pygame.mixer.Sound(os.path.join('Assets', '162458__kastenfrosch__gewonnen2.mp3'))
print("Getting sound")
BACKGROUND_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Music Pieces Test.mp3'))
print("Done")
TOTAL_SCORE = 0
RED_HIT = pygame.USEREVENT + 1
EGG_SMASH = pygame.USEREVENT + 2
HEATH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
COOLDOWN = 1
FPS = 60
CHARACTER_WIDTH, CHARACTER_HEIGHT = 70, 70
VEL = 10
BULLET_VEL = 2
MAX_BULLETS = 10
WINNING_SCORE = 10

# BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Grenade+1.mp3'))
# BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Gun+Silencer.mp3'))

# images
RED_JEDI_FIGHTER_IMAGE = pygame.image.load(
    os.path.join('Assets', 'character_1_front.png'))
RED_JEDI_FIGHTER = pygame.transform.rotate(
    pygame.transform.scale(RED_JEDI_FIGHTER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT)), 0)

EGG_IMAGE = pygame.image.load(
    os.path.join('Assets', 'pack-pixel-easter-eggs-8.png'))
EGG = pygame.transform.scale(EGG_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

BACKGROUND_IMAGE = pygame.image.load(
    os.path.join('Assets', 'Stardew-Valley-farm-stars-pixel-art-700x394.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (700 * BACKGROUND_SCALE, 394 * BACKGROUND_SCALE))

BACKGROUND_SOUND.play(100)
WIN = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption(DisplayName)
# variables end
#                                                       functions


def draw_window(red, blue_bullet, red_health, egg_surface, cycle, total_score):
    # total_score broken, need working calculations
    WIN.blit(BACKGROUND, (BACKGROUND_POS_X, BACKGROUND_POS_Y))

    red_health_text = HEATH_FONT.render(
        "Total Score: " + str(total_score) + " Game: " + str(cycle) +
        " Score: " + str(red_health) + "/" + str(WINNING_SCORE*cycle), True, White)
    WIN.blit(red_health_text, (10, 10))

    WIN.blit(RED_JEDI_FIGHTER, (red.x, red.y))

    for bullet in blue_bullet:
        WIN.blit(egg_surface, bullet)

    pygame.display.update()


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:  # (red) left ship moves <--
        red.x -= VEL  # (red) left ship moves -->
    if keys_pressed[pygame.K_d] and red.x + VEL + CHARACTER_WIDTH < winWidth:
        red.x += VEL


def handle_grid(grid_list_x):
    for line_x in range(10, winWidth - CHARACTER_WIDTH, 50):
        grid_list_x.append(line_x)


def handle_bullets(blue_bullet, red):
    for bullet in blue_bullet:
        bullet.y += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullet.remove(bullet)
        elif bullet.y > winHeight:
            blue_bullet.remove(bullet)
            pygame.event.post(pygame.event.Event(EGG_SMASH))


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, White)
    WIN.blit(draw_text, (winWidth / 2 - draw_text.get_width() / 2, winHeight / 2 - draw_text.get_height()))
    pygame.display.update()
    pygame.time.delay(5000)


def get_image(sheet, width, height):
    egg_pos_width, egg_pos_height = 26, 35
    image = pygame.Surface((egg_pos_width, egg_pos_height)).convert_alpha()
    image.blit(sheet, (0, 0), (0, 0, egg_pos_width, egg_pos_height))
    image = pygame.transform.scale(image, (width, height))
    image.set_colorkey((255, 255, 255))
    return image


def create_egg(egg, egg_lis, egg_spawn_pos_list):
    ran_int = random.randint(0, len(egg_spawn_pos_list))
    bullet = pygame.Rect(
        egg.x + egg_spawn_pos_list[ran_int - 1], egg.y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    egg_lis.append(bullet)


def main(game=GAME, total_score=TOTAL_SCORE):
    player = pygame.Rect(100, winHeight - (CHARACTER_HEIGHT + 20), CHARACTER_WIDTH, CHARACTER_HEIGHT)
    egg_spawn = pygame.Rect(0, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    player_points = 0
    blue_bullet = []
    jump = False
    vel_g = 20
    vel_g_origin = vel_g
    egg_spawn_pos = []
    egg = get_image(EGG, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    handle_grid(egg_spawn_pos)
    print(egg_spawn_pos)
    print(str(len(egg_spawn_pos)) + " = list length")
    print("Generated Egg spawns")
    cool_down = COOLDOWN
    cool_down = cool_down * FPS
    clock = pygame.time.Clock()
    egg_fall_on_off = True
    # Important Quit Button
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RCTRL:
                    egg_fall_on_off = not egg_fall_on_off
                    print(egg_fall_on_off)

                if event.key == pygame.K_w:
                    if not jump:
                        jump = True

            if event.type == RED_HIT:
                player_points += 1
                total_score += 1
                CATCH_SOUND.play()
            if event.type == EGG_SMASH:
                player_points = 0
                SMASH_SOUND.play()
        cool_down -= 1
        if cool_down <= 0:
            cool_down = COOLDOWN*FPS
            if len(blue_bullet) < MAX_BULLETS:
                if egg_fall_on_off:
                    create_egg(egg_spawn, blue_bullet, egg_spawn_pos)

        if jump:
            player.y -= vel_g
            vel_g -= 1
            if vel_g < -vel_g_origin:
                vel_g = vel_g_origin
                jump = False
        winner_text = ""
        if player_points >= WINNING_SCORE*game:
            winner_text = "You Win! Game "
            game += 1
        if winner_text != "":
            WINNER_SOUND.play()
            draw_winner(winner_text + str(game - 1))
            break
        keys_pressed = pygame.key.get_pressed()
        handle_red_movement(keys_pressed, player)
        handle_bullets(blue_bullet, player)
        draw_window(player, blue_bullet, player_points, egg, game, total_score)

    main(game, total_score)


if __name__ == "__main__":
    main()
