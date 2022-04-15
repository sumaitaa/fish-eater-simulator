import pygame
import random

class Fish(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, player_width, player_height):
        super().__init__()

        # FISH MODE
        self.fish_mode = random.randint(1,3)
        #self.fish_mode = 2

        # ANIMATIONS
        # FISH 1 (MOST COMMON)
        fish_1_1 = pygame.image.load('graphics/fish_1/000.png').convert_alpha()
        fish_1_2 = pygame.image.load('graphics/fish_1/001.png').convert_alpha()
        self.fish_1_idle = [fish_1_1, fish_1_2]

        # FISH 2 (LESS COMMON)
        fish_2_1 = pygame.image.load('graphics/fish_2/000.png').convert_alpha()
        fish_2_2 = pygame.image.load('graphics/fish_2/001.png').convert_alpha()
        self.fish_2_idle = [fish_2_1, fish_2_2]

        # FISH 3 (the cool one)
        fish_3_1 = pygame.image.load('graphics/fish_3/000.png').convert_alpha()
        fish_3_2 = pygame.image.load('graphics/fish_3/001.png').convert_alpha()
        self.fish_3_idle = [fish_3_1, fish_3_2]

        self.anim_index = 0

        # Positioning
        # (too many variables? ...maybe)
        self.width = fish_1_1.get_width()
        self.height = fish_1_1.get_height()
        self.MIN_X = self.width
        self.MAX_X = screen_width - self.width
        self.MIN_Y = self.height
        self.MAX_Y = screen_height - 400

        self.player_width = player_width
        self.player_height = player_height

        self.x = random.randint(self.MIN_X, self.MAX_X)
        self.y = random.randint(self.MIN_Y, self.MAX_Y)

        if self.fish_mode == 1:
            self.image = self.fish_1_idle[self.anim_index]
        elif self.fish_mode == 2:
            self.image = self.fish_2_idle[self.anim_index]
        else:
            self.image = self.fish_3_idle[self.anim_index]

        self.change_times = 0

        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.rect.inflate_ip(-60, -60)

    def animate(self):
        if self.fish_mode == 1:
            self.anim_index += 0.09
            if self.anim_index >= len(self.fish_1_idle): self.anim_index = 0
            self.image = self.fish_1_idle[int(self.anim_index)]

        elif self.fish_mode == 2:
            self.anim_index += 0.09
            if self.anim_index >= len(self.fish_2_idle): self.anim_index = 0
            self.image = self.fish_2_idle[int(self.anim_index)]

        else:
            self.anim_index += 0.09
            if self.anim_index >= len(self.fish_3_idle): self.anim_index = 0
            self.image = self.fish_3_idle[int(self.anim_index)]

    def change_fish(self):
        self.rect.x = random.randint(self.MIN_X, self.MAX_X)
        self.rect.y = random.randint(self.MIN_Y, self.MAX_Y)
        self.fish_mode = random.choice([1, 1, 1, 2, 2, 3])

    def update(self):
        self.animate()
