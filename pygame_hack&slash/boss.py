import pygame
import math
import constants
from functions import *
from character import draw_health_bar  # ⚠️ Sağlık çubuğu için

class Boss:
    def __init__(self, x, y):
        sheet = constants.BOSS_SPRITE_SHEET
        self.idleSprites = load_sprite_sheet(
            sheet,
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
        # Animasyon sayaç kontrolü
        if self.idleCount >= len(self.idleSprites):
            self.idleCount = 0
        win.blit(self.idleSprites[self.idleCount], (self.x, self.y))
        self.idleCount += 1

        # 💥 Sağlık çubuğunu çiz
        draw_health_bar(win, self.x, self.y, self.health, self.maxHealth)