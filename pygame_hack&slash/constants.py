import os

FPS = 30
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

# ─── HERO SABİTLERİ ──────────────────────────────────────────────────────────
CHAR_HEALTH           = 100
CHAR_MAX_HEALTH       = 100
CHAR_SPEED            = 5
CHAR_DASH_SPEED       = 15.0
CHAR_DASH_MULTIPLIER  = 10
CHAR_ANIM_COOLDOWN_MS = 100

# ─── BOSS SABİTLERİ ────────────────────────────────────────────────────────────
BOSS_SPRITE_SHEET   = os.path.join("assets", "Boss", "IDLE.png")
BOSS_FRAME_WIDTH    = 128
BOSS_FRAME_HEIGHT   = 108
BOSS_NUM_FRAMES     = 6
BOSS_START_X        = 300
BOSS_START_Y        = 100
BOSS_SPEED          = 5                  # 💥 Boss takip hızı
BOSS_FOLLOW_DISTANCE= 200                # 💥 Kaç piksele kadar takip edecek
BOSS_HEALTH         = 100                # 💥 Boss sağlık değeri