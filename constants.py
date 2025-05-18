#constants.py
import os

# Genel ayarlar
FPS = 60
screenWidth = 1000
screenHeight = 800
scale = 2


# Font ve ses yolları
FONT_PATH = os.path.join("assets", "fonts", "pixel.ttf")
SFX_PATH = os.path.join("assets", "sfx")

# Renkler
OFFSET_X = 20
OFFSET_Y = 40
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Karakter sabitleri
CHAR_X                = 500
CHAR_Y                = 700
CHAR_HEALTH           = 100
CHAR_MAX_HEALTH       = 100
CHAR_SPEED            = 6
CHAR_DASH_SPEED       = 8.0
CHAR_DASH_MULTIPLIER  = 1
CHAR_DASH_DELAY       = 480
CHAR_DASH_COOLDOWN   = 3000  # ms cinsinden dash bekleme süresi
CHAR_ANIM_COOLDOWN_MS = 60
CHAR_ATTACK_COOLDOWN = 500  # ms cinsinden saldırı bekleme süresi
CHAR_ATTACK_FRAME_DURATION = 50  # ms cinsinden saldırı süresi
CHAR_ATTACK_DAMAGE = 20
CHAR_ATTACK_FRAME = 3

# Boss sabitleri
BOSS_FRAME_WIDTH      = 128
BOSS_FRAME_HEIGHT     = 108
BOSS_NUM_FRAMES       = 6
BOSS_START_X          = 300
BOSS_START_Y          = 300
BOSS_SPEED            = 2.0
BOSS_FOLLOW_DISTANCE  = 300
BOSS_HEALTH           = 300
BOSS_SCALE            = 2  # 1.5 kat büyük
BOSS_HITBOX_OFFSET_Y  = 25  # Hitbox ayarı için
BOSS_HITBOX_OFFSET_X  = 10

DAMAGE_BOSS_PHASE_1 = 1
DAMAGE_BOSS_PHASE_2 = 2

# Projeksil sabitleri
PROJECTILE_VELOCITY = 10
PROJECTILE_DAMAGE = 2

# Animasyon sabitleri
ANIMATION_COOLDOWN = 100
BOSS_ANIMATION_COOLDOWN = 100

# Diğer sabitler
START_BUTTON_WIDTH = 200
START_BUTTON_HEIGHT = 50

# Renk paleti
SAKURA_PINK = (255, 183, 197)
SUNSET_ORANGE = (253, 94, 83)
TREE_PURPLE = (54, 33, 89)
SUN_YELLOW = (255, 159, 28)
SKY_GRADIENT = [(32, 18, 59), (253, 94, 83), (255, 159, 28)]
GROUND_GREEN = (45, 86, 44)
TREE_BROWN = (48, 28, 19)