import os

FPS = 120
screenWidth = 800
screenHeight = 600
dash_delay = 2

RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ─── BOSS SABİTLERİ ────────────────────────────────────────────────────────────
BOSS_SPRITE_SHEET = os.path.join("assets", "Boss", "skeletonIdle-Sheet64x64.png")

# Her bir kare 64×64, toplam 8 kare
BOSS_FRAME_WIDTH  = 64
BOSS_FRAME_HEIGHT = 64
BOSS_NUM_FRAMES   = 8

# Sahnedeki başlangıç konumu
BOSS_START_X = 300
BOSS_START_Y = 100
