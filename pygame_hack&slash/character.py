import pygame
import os
import math
import constants
from functions import *

class Character(object):
    def __init__(self, x, y, width, height, screenWidth, screenHeight, mob_animations, char_type):
        # Pozisyon ve boyutlar
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.center = (self.x + self.width / 2, self.y + self.height / 2)

        # Hareket ve hız
        self.vel = constants.CHAR_SPEED
        self.dashVel = constants.CHAR_DASH_SPEED
        self.isDashing = False
        self.dash_start_time = 0

        # Can ve sağlık
        self.health = constants.CHAR_HEALTH
        self.maxHealth = constants.CHAR_MAX_HEALTH

        # Saldırı
        self.is_attacking = False
        self.last_attack_time = 0
        self.attack_cooldown = constants.CHAR_ATTACK_COOLDOWN
        self.attack_frame_duration = constants.CHAR_ATTACK_FRAME_DURATION
        self.attack_damage = constants.CHAR_ATTACK_DAMAGE
        self.attack_frame = constants.CHAR_ATTACK_FRAME
        self.has_dealt_damage = False

        # Atak için çarpışma dikdörtgeni
        self.attack_rect = pygame.Rect(0, 0, 50, 50)  # Saldırı hitbox'ı

        # Animasyon kontrol
        self.last_update = pygame.time.get_ticks()
        self.frame_index = 0
        #self.action = "idle"
        self.flip = False

        # Yönelim
        self.horizontal = 0
        self.vertical = 0
        self.left = False

        # Ekran sınırları
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        # Karakter tipi (render offset vs.)
        self.char_type = char_type

        self.dashMultiplier = constants.CHAR_DASH_MULTIPLIER
        self.animation_list = mob_animations[char_type]  # idle, walk, dash, attack
        self.action = 0  # 0 idle , 1 run, 2 dash, 3 attack
        self.walking = False
        self.image = self.animation_list[self.action][self.frame_index]  # charIdle

        self.leftIdle = False

        # Animasyonları yükle
        #assets_path = os.path.join("assets", "Player", "Sprites")
        #self.animations = {
        #    "idle": load_and_scale_sheet(os.path.join(assets_path, "IDLE.png"), 96, 80, 10),
        #    "walk": load_and_scale_sheet(os.path.join(assets_path, "WALK.png"), 96, 80, 12),
        #    "dash": load_and_scale_sheet(os.path.join(assets_path, "DASH.png"), 95, 80, 8),
        #    "attack": load_and_scale_sheet(os.path.join(assets_path, "ATTACK 1.png"), 96, 80, 7),
        #    "shuriken": load_single_image(os.path.join(assets_path, "shuriken.png"), constants.scale)
        #}
        #self.image = self.animations["idle"][0]

        # SFX yöneticisi (opsiyonel)
        self.sfx_manager = None


    def set_sfx_manager(self, sfx_manager):
        self.sfx_manager = sfx_manager

    def move(self, keys):
        self.walking = False

        self.horizontal = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.vertical   = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        if abs(self.horizontal) or abs(self.vertical): # if moving
            self.walking = True
        if abs(self.horizontal) and abs(self.vertical): # if moving diagonally
            self.x += self.horizontal * self.vel/math.sqrt(2)
            self.y += self.vertical * self.vel /math.sqrt(2)
        else:
            self.x += self.horizontal * self.vel
            self.y += self.vertical * self.vel

        # Hangi yöne baktığını belirle
        if self.horizontal < 0:
            self.left = True
            self.flip = True
        elif self.horizontal > 0:
            self.left = False
            self.flip = False

        # Dash movement
        if keys[pygame.K_LSHIFT]:
            self.isDashing = True

        # Apply dash if active
        if self.isDashing:
            if keys[pygame.K_a]:
                self.x -= self.dashVel
            if keys[pygame.K_d]:
                self.x += self.dashVel
            if keys[pygame.K_w]:
                self.y -= self.dashVel
            if keys[pygame.K_s]:
                self.y += self.dashVel
            if self.last_update - self.dash_start_time > constants.dash_delay:
                self.isDashing = False
                self.dash_start_time = self.last_update


        if keys[pygame.K_f]:
            if not self.is_attacking and self.last_update - self.last_attack_time > self.attack_cooldown:
                self.is_attacking = True
                self.last_attack_time = self.last_update
                # Eğer SFX eklenmek istenirse:
                # if self.sfx_manager: self.sfx_manager.play_sound("attack")


        # Take damage with space key
        if keys[pygame.K_SPACE] and self.health > 0:
            self.health -= 10

    def update(self):
        self.rect.center = (self.x + self.width / 2 , self.y + self.height / 2)
        # checking action
        if self.is_attacking:
            self.update_action(3)
        elif self.isDashing:
            self.update_action(2)
        elif self.walking:
            self.update_action(1)
        else:
            self.update_action(0)

        # Saldırı hitbox'ını karakterin yönüne göre güncelle
        if self.flip:
            self.attack_rect.midright = self.rect.midleft
        else:
            self.attack_rect.midleft = self.rect.midright

        # animation delay
        animation_cooldown = constants.CHAR_ANIM_COOLDOWN_MS

        if self.is_attacking: # attack animation
            #print("attacking")
            self.image = self.animation_list[3][self.frame_index]
            if pygame.time.get_ticks() - self.last_update >= self.attack_frame_duration:
                print("attack frame: ", self.frame_index)
                self.last_update = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.animation_list[3])

                if self.frame_index == self.attack_frame:
                    self.has_dealt_damage = False # after attack frame damage dealt off



        elif abs(self.horizontal) or abs(self.vertical): # walking/dashing animation
            if self.isDashing:
                # print("dashing")
                self.image = self.animation_list[2][self.frame_index]
                if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
                    self.last_update = pygame.time.get_ticks()
                    self.frame_index = (self.frame_index + 1) % len(self.animation_list[2])

            elif self.left:
                self.image = self.animation_list[1][self.frame_index]
                if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
                    self.last_update = pygame.time.get_ticks()
                    self.frame_index = (self.frame_index + 1) % len(self.animation_list[1])
            else:
                self.image = self.animation_list[1][self.frame_index]
                if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
                    self.last_update = pygame.time.get_ticks()
                    self.frame_index = (self.frame_index + 1) % len(self.animation_list[1])
        else: # idle animation
            #print("idle")
            if self.leftIdle:
                self.image = self.animation_list[0][self.frame_index]
                if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
                    self.last_update = pygame.time.get_ticks()
                    self.frame_index = (self.frame_index + 1) % len(self.animation_list[0])
            else:
                self.image = self.animation_list[0][self.frame_index]
                if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
                    self.last_update = pygame.time.get_ticks()
                    self.frame_index = (self.frame_index + 1) % len(self.animation_list[0])

        # Saldırı süresi kontrolü
        if self.is_attacking and self.last_update - self.last_attack_time > self.attack_cooldown:
            self.is_attacking = False

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()

    def draw(self, win, font):
        #pygame.draw.rect(win, constants.RED, self.rect, 1)
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if(self.char_type == 0):
            win.blit(flipped_image, (self.rect.x - constants.scale *constants.OFFSET_X, self.rect.y - constants.scale *constants.OFFSET_Y))
        else:
            win.blit(flipped_image, self.rect)
        # health bar
        draw_health_bar(win, self.x, self.y, self.health, self.maxHealth)

        # Draw game over text if health is depleted
        if self.health <= 0:
            gameOverText = font.render("GAME OVER", True, (255, 255, 255))
            win.blit(gameOverText, ((self.screenWidth // 2 - gameOverText.get_width() // 2), 300))

        if self.is_attacking:
            pygame.draw.rect(win, constants.RED, self.attack_rect, 2)