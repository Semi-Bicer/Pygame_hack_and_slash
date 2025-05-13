import pygame
import math
import constants
from functions import load_and_scale_sheet, draw_health_bar
import os
import random


class Boss:
    def __init__(self, x, y):
        self.scale = constants.BOSS_SCALE
        self.original_width = constants.BOSS_FRAME_WIDTH
        self.original_height = constants.BOSS_FRAME_HEIGHT
        self.width = int(self.original_width * self.scale)
        self.height = int(self.original_height * self.scale)

        # Hitbox için offset değerleri
        self.hitbox_offset_x = 20 * self.scale
        self.hitbox_offset_y = constants.BOSS_HITBOX_OFFSET_Y * self.scale
        self.hitbox_width = 80 * self.scale
        self.hitbox_height = 80 * self.scale

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

        self.attack_cooldown = 2000
        self.last_attack_time = pygame.time.get_ticks()

        # Animasyonları yükle
        self.animations = {
            "attack1": load_and_scale_sheet(os.path.join("assets", "Boss", "ATTACK 1.png"),
                                            self.original_width, self.original_height, 7, self.scale),
            "attack1_flame": load_and_scale_sheet(os.path.join("assets", "Boss", "ATTACK 1 (FLAMING SWORD).png"),
                                                  self.original_width, self.original_height, 7, self.scale),
            "attack2": load_and_scale_sheet(os.path.join("assets", "Boss", "ATTACK 2.png"),
                                            self.original_width, self.original_height, 5, self.scale),
            "attack2_flame": load_and_scale_sheet(os.path.join("assets", "Boss", "ATTACK 2 (FLAMING SWORD).png"),
                                                  self.original_width, self.original_height, 6, self.scale),
            "attack3": load_and_scale_sheet(os.path.join("assets", "Boss", "ATTACK 3.png"),
                                            self.original_width, self.original_height, 7, self.scale),
            "attack3_flame": load_and_scale_sheet(os.path.join("assets", "Boss", "ATTACK 3 (FLAMING SWORD).png"),
                                                  self.original_width, self.original_height, 7, self.scale),
            "jump_attack": load_and_scale_sheet(os.path.join("assets", "Boss", "JUMP ATTACK.png"),
                                                self.original_width, self.original_height, 12, self.scale),
            "jump_attack_flame": load_and_scale_sheet(os.path.join("assets", "Boss", "JUMP ATTACK (FLAMING SWORD).png"),
                                                      self.original_width, self.original_height, 11, self.scale),
            "idle": load_and_scale_sheet(os.path.join("assets", "Boss", "IDLE.png"),
                                         self.original_width, self.original_height, 6, self.scale),
            "idle_flame": load_and_scale_sheet(os.path.join("assets", "Boss", "IDLE (FLAMING SWORD).png"),
                                               self.original_width, self.original_height, 6, self.scale),
            "run": load_and_scale_sheet(os.path.join("assets", "Boss", "RUN.png"),
                                        self.original_width, self.original_height, 8, self.scale),
            "run_flame": load_and_scale_sheet(os.path.join("assets", "Boss", "RUN (FLAMING SWORD).png"),
                                              self.original_width, self.original_height, 8, self.scale),
            "hurt": load_and_scale_sheet(os.path.join("assets", "Boss", "HURT.png"),
                                         self.original_width, self.original_height, 4, self.scale),
            "hurt_flame": load_and_scale_sheet(os.path.join("assets", "Boss", "HURT (FLAMING SWORD).png"),
                                               self.original_width, self.original_height, 4, self.scale),
            "death": load_and_scale_sheet(os.path.join("assets", "Boss", "DEATH.png"),
                                          self.original_width, self.original_height, 26, self.scale),
            "shout": load_and_scale_sheet(os.path.join("assets", "Boss", "SHOUT.png"),
                                          self.original_width, self.original_height, 17, self.scale),
        }

    def get_animation(self):
        anim_key = self.action
        if self.phase == 2 and self.action in ["idle", "run", "hurt", "attack1", "attack2", "attack3"]:
            anim_key += "_flame"
        return self.animations.get(anim_key, self.animations["idle"])

    def take_damage(self, amount):
        if not self.invincible and self.action != "death":
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.action = "death"
                self.frame_index = 0
                self.last_update = pygame.time.get_ticks()
            else:
                hurt_anim = "hurt_flame" if self.phase == 2 else "hurt"
                self.action = hurt_anim
                self.frame_index = 0
                self.last_update = pygame.time.get_ticks()

            if self.phase == 1 and self.health <= self.maxHealth // 2:
                self.phase_transition = True
                self.invincible = True
                self.action = "shout"
                self.frame_index = 0
                self.last_update = pygame.time.get_ticks()

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
            return

        if self.action in ["shout", "death"]:
            if self.frame_index >= len(self.get_animation()):
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

        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)

        self.flip = dx < 0

        if dist < 100 and now - self.last_attack_time > self.attack_cooldown:
            self.choose_attack()
            self.last_attack_time = now
            self.frame_index = 0
            self.last_update = now
            return

        if dist < constants.BOSS_FOLLOW_DISTANCE and dist > 0:
            self.x += constants.BOSS_SPEED * (dx / dist)
            self.y += constants.BOSS_SPEED * (dy / dist)
            self.action = "run"
        else:
            self.action = "idle"

    def choose_attack(self):
        options = ["attack1", "attack2", "attack3", "jump_attack"]
        choice = random.choice(options)
        self.action = choice

    def draw(self, win):
        animation_cooldown = 100
        frames = self.get_animation()

        if self.frame_index >= len(frames):
            if self.action in ["death", "shout"]:
                self.frame_index = len(frames) - 1
            else:
                self.frame_index = 0

        sprite = frames[self.frame_index]
        flipped_sprite = pygame.transform.flip(sprite, self.flip, False)
        win.blit(flipped_sprite, (self.x, self.y))

        # Health bar
        health_bar_width = 100 * self.scale
        health_bar_x = self.x + (self.width - health_bar_width) // 2
        health_bar_y = self.y - 20
        draw_health_bar(win, health_bar_x, health_bar_y, self.health, self.maxHealth, health_bar_width)

        if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
            self.last_update = pygame.time.get_ticks()
            self.frame_index += 1