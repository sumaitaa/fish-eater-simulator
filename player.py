import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x_constraint, speed):
        super().__init__()
        # ANIMATIONS
        # (there's probably a better way to do this...
        # don't know about it yet though)

        # Idle
        player_idle1 = pygame.image.load('graphics/swimmer/idle/000.png').convert_alpha()
        player_idle2 = pygame.image.load('graphics/swimmer/idle/001.png').convert_alpha()
        self.idle = [player_idle1, player_idle2]

        # Swimming(?)
        player_swim1 = pygame.image.load('graphics/swimmer/swimming/000.png').convert_alpha()
        player_swim2 = pygame.image.load('graphics/swimmer/swimming/001.png').convert_alpha()
        player_swim3 = pygame.image.load('graphics/swimmer/swimming/002.png').convert_alpha()
        player_swim4 = pygame.image.load('graphics/swimmer/swimming/003.png').convert_alpha()
        self.swim = [player_swim1, player_swim2, player_swim3, player_swim4]

        # Eating
        player_eat1 = pygame.image.load('graphics/swimmer/eat/000.png').convert_alpha()
        player_eat2 = pygame.image.load('graphics/swimmer/eat/001.png').convert_alpha()
        player_eat3 = pygame.image.load('graphics/swimmer/eat/002.png').convert_alpha()
        player_eat4 = pygame.image.load('graphics/swimmer/eat/003.png').convert_alpha()
        self.eat = [player_eat1, player_eat2, player_eat3, player_eat4]

        self.anim_index = 0

        self.is_moving = False

        # POSITIONING
        self.x = x_constraint / 2
        self.y = 650
        self.max_y = 650
        self.x_constraint = x_constraint
        self.speed = speed

        # JUMPS
        self.jump_ready = True
        self.jump_cooldown = 400
        self.jump_time = 0

        self.image = self.idle[self.anim_index]
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))
        self.rect.inflate_ip(-70, -70)
        # Above code took me an embarassing
        # amount of time to figure out
        self.gravity = 0

        self.swim_sound = pygame.mixer.Sound('audio/swim.ogg')
        self.swim_sound.set_volume(0.3)

        self.swim_loop_sound = pygame.mixer.Sound('audio/swim_loop.ogg')
        self.swim_loop_sound.set_volume(0.32)
        self.swim_loop_cooldown =  self.swim_loop_sound.get_length() * 1000
        self.swim_loop_lastplayed = 0
        self.swim_loop_ready = True

    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.rect.right >= self.x_constraint:
                self.rect.right >= self.x_constraint
            else:
                self.rect.x += self.speed
            self.is_moving = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.rect.left <= 0:
                self.rect.left = 0
            else:
                self.rect.x -= self.speed
            self.is_moving = True
        else:
            self.is_moving = False

    def jump(self):
        if self.jump_ready:
            if self.rect.top > 0:
                self.swim_sound.play()
                self.gravity = -5
                self.jump_ready = False
                self.jump_time = pygame.time.get_ticks()

    def wait_for_jump(self):
        if not self.jump_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.jump_time >= self.jump_cooldown:
                self.jump_ready = True

    def apply_gravity(self):
        self.gravity += 0.2
        self.rect.y = self.rect.y + self.gravity
        if self.rect.bottom >= self.max_y:
            self.rect.bottom = self.max_y

    def animate(self):
        if self.is_moving:
            if not self.rect.bottom < self.max_y:
                self.anim_index += 0.1
                if self.anim_index >= len(self.swim): self.anim_index = 0
                self.image = self.swim[int(self.anim_index)]
            else:
                self.anim_index += 0.1
                if self.anim_index >= len(self.eat): self.anim_index = 0
                self.image = self.eat[int(self.anim_index)]
        elif self.rect.bottom < self.max_y:
            self.anim_index += 0.1
            if self.anim_index >= len(self.eat): self.anim_index = 0
            self.image = self.eat[int(self.anim_index)]
        else:
            self.anim_index += 0.1
            if self.anim_index >= len(self.idle): self.anim_index = 0
            self.image = self.idle[int(self.anim_index)]

    def play_swim_audio(self):
        if self.is_moving or self.rect.bottom < self.max_y:
            if self.swim_loop_ready:
                self.swim_loop_sound.play()
                self.swim_loop_ready = False
                self.swim_loop_lastplayed = pygame.time.get_ticks()
            else:
                current_time = pygame.time.get_ticks()
                if current_time - self.swim_loop_lastplayed >= self.swim_loop_cooldown:
                    self.swim_loop_ready = True
        else:
            if self.swim_loop_ready == False:
                # The if-statement above is asking if the sound is
                # currently playing
                self.swim_loop_sound.stop()
                self.swim_loop_ready = True

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.wait_for_jump()
        self.play_swim_audio()
        self.animate()
