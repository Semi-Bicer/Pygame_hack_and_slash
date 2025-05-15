#boss.py
import pygame
import math
import os
import random
import constants
from functions import load_and_scale_sheet, draw_health_bar


class Boss:
    def __init__(self, x, y):
        self.scale = constants.BOSS_SCALE
        self.original_width = constants.BOSS_FRAME_WIDTH
        self.original_height = constants.BOSS_FRAME_HEIGHT
        self.width = int(self.original_width * self.scale)
        self.height = int(self.original_height * self.scale)

        # Hitbox için offset değerleri
        self.hitbox_offset_x = constants.BOSS_HITBOX_OFFSET_X * self.scale
        self.hitbox_offset_y = constants.BOSS_HITBOX_OFFSET_Y * self.scale
        self.hitbox_width = constants.BOSS_FRAME_WIDTH * self.scale - self.hitbox_offset_x * self.scale
        self.hitbox_height = constants.BOSS_FRAME_HEIGHT * self.scale - self.hitbox_offset_y * self.scale

        # Pozisyon ayarları
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.rect = pygame.Rect(self.x + self.hitbox_offset_x,
                                self.y + self.hitbox_offset_y,
                                self.hitbox_width,
                                self.hitbox_height)

        self.idleCount = 0
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.flip = False

        self.phase = 1
        self.action = "idle"
        self.health = constants.BOSS_HEALTH
        self.maxHealth = constants.BOSS_HEALTH
        self.invincible = False
        self.phase_transition = False

        self.min_follow_distance = 75
        self.follow_distance = constants.BOSS_FOLLOW_DISTANCE


        self.phase2_speed_multiplier = 3
        self.phase2_damage_multiplier = 2
        self.dash_cooldown = 3000
        self.last_dash_time = 0
        self.is_dashing = False
        self.dash_duration = 300
        self.dash_start_time = 0
        self.dash_direction = (0, 0)
        self.dash_speed = 15
        self.attack_cooldown = 2000
        self.last_attack_time = pygame.time.get_ticks()

        assets = os.path.join("assets", "Boss")
        self.animations = {
            "attack1": load_and_scale_sheet(os.path.join(assets, "ATTACK 1.png"), self.original_width, self.original_height, 7, self.scale),
            "attack1_flame": load_and_scale_sheet(os.path.join(assets, "ATTACK 1 (FLAMING SWORD).png"), self.original_width, self.original_height, 7, self.scale),
            "attack2": load_and_scale_sheet(os.path.join(assets, "ATTACK 2.png"), self.original_width, self.original_height, 5, self.scale),
            "attack2_flame": load_and_scale_sheet(os.path.join(assets, "ATTACK 2 (FLAMING SWORD).png"), self.original_width, self.original_height, 6, self.scale),
            "attack3": load_and_scale_sheet(os.path.join(assets, "ATTACK 3.png"), self.original_width, self.original_height, 7, self.scale),
            "attack3_flame": load_and_scale_sheet(os.path.join(assets, "ATTACK 3 (FLAMING SWORD).png"), self.original_width, self.original_height, 7, self.scale),
            "jump_attack": load_and_scale_sheet(os.path.join(assets, "JUMP ATTACK.png"), self.original_width, self.original_height, 12, self.scale),
            "jump_attack_flame": load_and_scale_sheet(os.path.join(assets, "JUMP ATTACK (FLAMING SWORD).png"), self.original_width, self.original_height, 11, self.scale),
            "idle": load_and_scale_sheet(os.path.join(assets, "IDLE.png"), self.original_width, self.original_height, 6, self.scale),
            "idle_flame": load_and_scale_sheet(os.path.join(assets, "IDLE (FLAMING SWORD).png"), self.original_width, self.original_height, 6, self.scale),
            "run": load_and_scale_sheet(os.path.join(assets, "RUN.png"), self.original_width, self.original_height, 8, self.scale),
            "run_flame": load_and_scale_sheet(os.path.join(assets, "RUN (FLAMING SWORD).png"), self.original_width, self.original_height, 8, self.scale),
            "dash": load_and_scale_sheet(os.path.join(assets, "RUN.png"), self.original_width, self.original_height, 8, self.scale),
            "dash_flame": load_and_scale_sheet(os.path.join(assets, "RUN (FLAMING SWORD).png"), self.original_width, self.original_height, 8, self.scale),
            "hurt": load_and_scale_sheet(os.path.join(assets, "HURT.png"), self.original_width, self.original_height, 4, self.scale),
            "hurt_flame": load_and_scale_sheet(os.path.join(assets, "HURT (FLAMING SWORD).png"), self.original_width, self.original_height, 4, self.scale),
            "death": load_and_scale_sheet(os.path.join(assets, "DEATH.png"), self.original_width, self.original_height, 26, self.scale),
            "shout": load_and_scale_sheet(os.path.join(assets, "SHOUT.png"), self.original_width, self.original_height, 17, self.scale),
        }

        # Atak için çarpışma dikdörtgeni
        self.attack_rect = pygame.Rect(0, 0, 50, 50)  # Saldırı hitbox'ı

    def get_animation(self):
        anim_key = self.action
        if self.phase == 2 and self.action in ["idle", "run", "hurt", "attack1", "attack2", "attack3", "jump_attack", "dash"]:
            anim_key += "_flame"
        return self.animations.get(anim_key, self.animations["idle"])

    def take_damage(self, amount):
        if not self.invincible and self.action != "death":
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.action = "death"
            else:
                self.action = "hurt_flame" if self.phase == 2 else "hurt"

            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()

            if self.phase == 1 and self.health <= self.maxHealth // 2:
                self.phase_transition = True
                self.invincible = True
                self.action = "shout"
                self.frame_index = 0
                self.last_update = pygame.time.get_ticks()

    def dash_to_player(self, player):
        if self.is_dashing:
            return

        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)

        if dist <= self.min_follow_distance:
            return

        self.dash_direction = (dx / dist, dy / dist) if dist else (0, 0)
        self.is_dashing = True
        self.dash_start_time = pygame.time.get_ticks()
        self.action = "dash_flame" if self.phase == 2 else "dash"
        self.frame_index = 0
        self.last_dash_time = pygame.time.get_ticks()

    def update(self, player):
        now = pygame.time.get_ticks()
        self.rect.x = self.x + self.hitbox_offset_x
        self.rect.y = self.y + self.hitbox_offset_y

        if self.health <= 0:
            self.action = "death"
            return

        if self.phase_transition:
            if self.frame_index >= len(self.get_animation()):
                self.phase_transition = False
                self.invincible = False
                self.phase = 2
                self.action = "idle"
                self.attack_cooldown = int(self.attack_cooldown / self.phase2_speed_multiplier)
                self.dash_speed *= 1.5
            return

        if self.action in ["shout", "death"]:
            if self.frame_index >= len(self.get_animation()):
                self.action = "idle"
            return

        if self.is_dashing:
            if now - self.dash_start_time < self.dash_duration:
                self.x += self.dash_direction[0] * self.dash_speed
                self.y += self.dash_direction[1] * self.dash_speed
                self.x = max(0, min(self.x, constants.screenWidth - self.width))
                self.y = max(0, min(self.y, constants.screenHeight - self.height))
            else:
                self.is_dashing = False
                self.action = "idle"
            return

        if self.action.startswith("attack") or self.action == "jump_attack":
            if self.frame_index < len(self.get_animation()):
                return
            else:
                self.action = "idle"

        if self.action in ["hurt", "hurt_flame"]:
            if self.frame_index < len(self.get_animation()):
                return
            else:
                self.action = "idle"

        if self.phase == 2 and now - self.last_dash_time > self.dash_cooldown:
            if random.random() < 0.3:
                self.dash_to_player(player)
                return

        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        self.flip = dx < 0

        should_move = False

        if dist < 100 and now - self.last_attack_time > self.attack_cooldown:
            self.choose_attack()
            self.last_attack_time = now
            self.frame_index = 0
            self.last_update = now
            return

        if (self.phase == 2) or (self.phase == 1 and dist < constants.BOSS_FOLLOW_DISTANCE):
            if dist > self.min_follow_distance:  # Çok yakına gelmesin
                speed = constants.BOSS_SPEED * (self.phase2_speed_multiplier if self.phase == 2 else 1)
                self.x += speed * (dx / dist)
                self.y += speed * (dy / dist)
                should_move = True
            elif now - self.last_dash_time > self.dash_cooldown:
                self.dash_to_player(player)
                return

        if self.is_dashing:
            self.action = "dash_flame" if self.phase == 2 else "dash"
        elif should_move:
            self.action = "run_flame" if self.phase == 2 else "run"
        else:
            self.action = "idle_flame" if self.phase == 2 else "idle"

    def choose_attack(self):
        options = ["attack1", "attack2", "attack3", "jump_attack"] * (2 if self.phase == 2 else 1)
        self.action = random.choice(options)

    def draw(self, win):
        animation_cooldown = constants.BOSS_ANIMATION_COOLDOWN
        if self.phase == 2:
            animation_cooldown = int(animation_cooldown / self.phase2_speed_multiplier)

        frames = self.get_animation()
        if self.frame_index >= len(frames):
            if self.action in ["death", "shout"]:
                self.frame_index = len(frames) - 1
            else:
                self.frame_index = 0

        sprite = frames[self.frame_index]
        flipped_sprite = pygame.transform.flip(sprite, self.flip, False)
        win.blit(flipped_sprite, (self.x - self.hitbox_offset_x * self.scale, self.y - self.hitbox_offset_y * self.scale))


        draw_health_bar(win, self.x - 10, self.y - 10, self.health, self.maxHealth)

        if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
            self.last_update = pygame.time.get_ticks()
            self.frame_index += 1