import os

FPS = 60
screenWidth = 800
screenHeight = 600
scale = 1
dash_delay = 2

OFFSET_X = 40
OFFSET_Y = 80
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ─── BOSS SABİTLERİ ────────────────────────────────────────────────────────────
BOSS_SPRITE_SHEET   = os.path.join("pygame_hack&slash","assets", "Boss", "skeletonIdle-Sheet64x64.png")
BOSS_FRAME_WIDTH    = 64
BOSS_FRAME_HEIGHT   = 64
BOSS_NUM_FRAMES     = 8
BOSS_START_X        = 300
BOSS_START_Y        = 100
BOSS_SPEED          = 2.0                # 💥 Boss takip hızı
BOSS_FOLLOW_DISTANCE= 200                # 💥 Kaç piksele kadar takip edecek
BOSS_HEALTH         = 100                # 💥 Boss sağlık değeri