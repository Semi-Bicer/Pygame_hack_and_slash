import pygame
import math
import constants
from functions import *
from character import draw_health_bar  # ⚠️ Sağlık çubuğu için

class Boss:
    def __init__(self, x, y):
        self.idleSprites = load_sprite_sheet(
            constants.BOSS_SPRITE_SHEET,
            constants.BOSS_FRAME_WIDTH,
            constants.BOSS_FRAME_HEIGHT,
            constants.BOSS_NUM_FRAMES
        )
        self.x = x
        self.y = y
        self.idleCount = 0

        # 💥 Sağlık ve takip
        self.health = constants.BOSS_HEALTH
        self.maxHealth = constants.BOSS_HEALTH

    # 💥YENİ💥
    def update(self, player):
        """
        💥 Oyuncu ile aradaki mesafe constants.BOSS_FOLLOW_DISTANCE'den küçükse
        sabit hızla (BOSS_SPEED) oyuncuya doğru hareket et.
        """
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist < constants.BOSS_FOLLOW_DISTANCE and dist > 0:
            self.x += constants.BOSS_SPEED * (dx / dist)
            self.y += constants.BOSS_SPEED * (dy / dist)

    def draw(self, win):
        if self.idleCount >= len(self.idleSprites):
            self.idleCount = 0
        sprite = self.idleSprites[self.idleCount]
        win.blit(sprite, (self.x, self.y))
        self.idleCount += 1

        # 🛠 DEBUG: Sprite çizim alanını göster
        pygame.draw.rect(win, (255, 0, 255), (self.x, self.y, sprite.get_width(), sprite.get_height()), 1)

        draw_health_bar(win, self.x, self.y, self.health, self.maxHealth)
