import pygame
import constants
from functions import *

class Boss:
    def __init__(self, x, y):
        # Sprite sheet’i yükleyip karelerine ayırıyoruz
        sheet_path = constants.BOSS_SPRITE_SHEET
        self.idleSprites = load_sprite_sheet(
            sheet_path,
            constants.BOSS_FRAME_WIDTH,
            constants.BOSS_FRAME_HEIGHT,
            constants.BOSS_NUM_FRAMES
        )
        self.x = x
        self.y = y
        self.idleCount = 0

    def draw(self, win):
        # Animasyon sayaç kontrolü
        if self.idleCount >= len(self.idleSprites):
            self.idleCount = 0
        # O anki kareyi çiz
        win.blit(self.idleSprites[self.idleCount], (self.x, self.y))
        # Bir sonraki kareye geç
        self.idleCount += 1
