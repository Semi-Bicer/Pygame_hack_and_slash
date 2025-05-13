import pygame
import os
import math
import constants
from functions import draw_health_bar

class Character(object):
    def __init__(self, x, y, width, height, screenWidth, screenHeight, mob_animations, char_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.center = (self.x + self.width / 2 , self.y + self.height / 2)

        # Sabitler constants.py'den
        self.vel = constants.CHAR_SPEED
        self.dashVel = constants.CHAR_DASH_SPEED
        self.health = constants.CHAR_HEALTH
        self.maxHealth = constants.CHAR_MAX_HEALTH
        self.dashMultiplier = constants.CHAR_DASH_MULTIPLIER

        self.isDashing = False

        # Animasyon
        self.char_type = char_type
        self.animation_list = mob_animations[char_type]
        self.last_update = pygame.time.get_ticks()
        self.flip = False
        self.frame_index = 0
        self.action = 0
        self.walking = False
        self.image = self.animation_list[self.action][self.frame_index]
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.leftIdle = False
        self.walkCount = 0
        self.idleCount = 0

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.horizontal = 0
        self.vertical = 0

    def move(self, keys):
        self.walking = False
        self.horizontal = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.vertical = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        if abs(self.horizontal) or abs(self.vertical):
            self.walking = True

        if abs(self.horizontal) and abs(self.vertical):
            self.x += self.horizontal * self.vel / math.sqrt(2)
            self.y += self.vertical * self.vel / math.sqrt(2)
        else:
            self.x += self.horizontal * self.vel
            self.y += self.vertical * self.vel

        if keys[pygame.K_a] and self.x > self.vel:
            self.left = True
            self.leftIdle = True
            self.flip = True
        elif keys[pygame.K_d] and self.x < (self.screenWidth - self.width - self.vel):
            self.left = False
            self.leftIdle = False
            self.flip = False
        else:
            if self.left:
                self.leftIdle = True
                self.rightIdle = False
                self.flip = True
            else:
                self.rightIdle = True
                self.leftIdle = False
                self.flip = False
            self.walkCount = 0

        self.up = keys[pygame.K_w] and self.y > self.vel
        self.down = keys[pygame.K_s] and self.y < (self.screenHeight - self.height - self.vel)

        if keys[pygame.K_LSHIFT]:
            self.isDashing = True
            self.left = False
            self.walkCount = 0

        if self.isDashing:
            if keys[pygame.K_a]:
                self.x -= self.dashVel
            if keys[pygame.K_d]:
                self.x += self.dashVel
            if keys[pygame.K_w]:
                self.y -= self.dashVel
            if keys[pygame.K_s]:
                self.y += self.dashVel
            self.isDashing = False

        if keys[pygame.K_SPACE] and self.health > 0:
            self.health -= 10

    def update(self):
        self.rect.center = (self.x + self.width / 2 , self.y + self.height / 2)
        self.update_action(1 if self.walking else 0)

        animation_cooldown = constants.CHAR_ANIM_COOLDOWN_MS

        if self.frame_index + 1 >= len(self.animation_list[1]):
            self.frame_index = 0

        if abs(self.horizontal) or abs(self.vertical):
            self.image = self.animation_list[1][self.frame_index]
        else:
            self.image = self.animation_list[0][self.frame_index]

        if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
            self.last_update = pygame.time.get_ticks()
            self.frame_index = (self.frame_index + 1) % len(self.animation_list[self.action])

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()

    def draw(self, win, font):
        pygame.draw.rect(win, constants.RED, self.rect, 1)
        flipped_image = pygame.transform.flip(self.image, self.flip, False)

        if self.char_type == 0:
            win.blit(flipped_image, (self.rect.x - constants.scale * constants.OFFSET_X, self.rect.y - constants.scale * constants.OFFSET_Y))
        else:
            win.blit(flipped_image, self.rect)

        draw_health_bar(win, self.x, self.y, self.health, self.maxHealth)

        if self.health <= 0:
            gameOverText = font.render("GAME OVER", True, (255, 255, 255))
            win.blit(gameOverText, ((self.screenWidth // 2 - gameOverText.get_width() // 2), 300))
