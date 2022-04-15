import pygame
import math
from random import randint, choice
from player import Player
from fish import Fish

from sys import exit

def display_timer():
    display_time = math.ceil(time_left / 100)
    time = font.render(f'Time Left: {display_time}', True, lineart_colour)
    time_rect = time.get_rect(topright = (SCREEN_WIDTH - 20, 40))
    screen.blit(time, time_rect)
    return display_time

def display_score():
    score_text = font.render(f'Score: {score}', True, lineart_colour)
    score_rect = score_text.get_rect(topleft = (20, 40))
    screen.blit(score_text, score_rect)
    return score

pygame.init()

SCREEN_WIDTH = 950
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("fish eater simuleator")

high_score = 0 # haven't used yet
score = 0
time_limit_in_seconds = 15
time_limit = time_limit_in_seconds * 100 # made it easier for me and my tiny brain to debug
time_left = 0

clock = pygame.time.Clock()
start_time = 0

font = pygame.font.Font('fonts/ComicHelvetic_Medium.ttf', 40)
smaller_font = pygame.font.Font('fonts/ComicHelvetic_Medium.ttf', 13)
lineart_colour = "#240238"

# GAME AUDIO
game_over_sound = pygame.mixer.Sound('audio/dingding.ogg')
game_over_sound.set_volume(0.3)
background_music = pygame.mixer.Sound('audio/presenterator.ogg')
background_music.set_volume(0.1)

background_music.play(loops = -1)

# BACKGROUND
background_img = pygame.image.load('graphics/background.png').convert()

# PLAYER
PLAYER_SPEED = 4
player_sprite = Player(SCREEN_WIDTH, PLAYER_SPEED)
player = pygame.sprite.GroupSingle(player_sprite)

# player audio
bite_sound = pygame.mixer.Sound('audio/bite.ogg')
bite_sound.set_volume(0.25)

# FISH
fish_sprite = Fish(SCREEN_WIDTH, SCREEN_HEIGHT, player.sprite.image.get_width(), player.sprite.image.get_height())
fish = pygame.sprite.GroupSingle(fish_sprite)

game_active = False
played_once = False

# TITLE SCREEN
game_main = pygame.image.load('graphics/menu.png').convert_alpha()
game_over = pygame.image.load('graphics/gameover.png').convert_alpha()

game_instructions = font.render('Press \'space\' to start', True, lineart_colour)
game_instructions_rect = game_instructions.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 80))
game_instructions_again = smaller_font.render('(Press \'space\' to start again)', True, lineart_colour)
game_instructions_again_rect = game_instructions_again.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 40))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.sprite.jump()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    time_left = time_limit
                    score = 0
                    if not played_once:
                        played_once = True

    if game_active:
        screen.blit(background_img, (0, 0))

        player.draw(screen)
        player.update()

        fish.draw(screen)
        fish.update()

        time_left -= 1.75
        '''
        Absolutely messed up the time system, because
        it's obvious that each 'second' lasted longer than
        a second when I just decreased the
        time by 1. I had (and have) no idea what I did wrong,
        so I awkwardly worked around it.
        Please be nice to me.
        '''
        display_timer()

        display_score()

        # FISH EATING
        if player.sprite.rect.colliderect(fish.sprite.rect):
            bite_sound.play()
            score += fish.sprite.fish_mode
            fish.sprite.change_fish()

        # TIME UP
        if (time_left <= 0):
            game_active = False
            game_over_sound.play()
            player.sprite.x = SCREEN_WIDTH / 2
            player.sprite.y = 650
            player.sprite.gravity = 0

    else:
        screen.fill("#A2D3ED")
        player.sprite.x = SCREEN_WIDTH / 2
        player.sprite.y = 650
        player.sprite.gravity = 0
        # tried to make character reset after a game over
        # doesn't work and I have no idea why
        fish.sprite.change_fish()

        if high_score < score:
            high_score = score

        score_message = font.render(f'Score: {score}', True, lineart_colour)
        score_message_rect = score_message.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 140))
        high_score_message = font.render(f'High Score: {high_score}', True, lineart_colour)
        high_score_message_rect = high_score_message.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 80))

        if not played_once:
            screen.blit(game_main, (0, 0))
            screen.blit(game_instructions, game_instructions_rect)
        else:
            screen.blit(game_over, (0, 0))
            screen.blit(score_message, score_message_rect)
            screen.blit(high_score_message, high_score_message_rect)
            screen.blit(game_instructions_again, game_instructions_again_rect)

    pygame.display.flip()
    # literally forgot to add this and i had no idea why i couldn't
    # see anything i am *so* dumb
    clock.tick(60)
