import os

# Genel ayarlar
FPS = 60
screenWidth = 800
screenHeight = 600
scale = 2
dash_delay = 2

# Renkler
OFFSET_X = 20
OFFSET_Y = 40
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Karakter sabitleri
CHAR_HEALTH           = 100
CHAR_MAX_HEALTH       = 100
CHAR_SPEED            = 5
CHAR_DASH_SPEED       = 15.0
CHAR_DASH_MULTIPLIER  = 10
CHAR_ANIM_COOLDOWN_MS = 100

# Boss sabitleri
BOSS_FRAME_WIDTH      = 128
BOSS_FRAME_HEIGHT     = 108
BOSS_NUM_FRAMES       = 6
BOSS_START_X          = 300
BOSS_START_Y          = 300
BOSS_SPEED            = 2.0
BOSS_FOLLOW_DISTANCE  = 400
BOSS_HEALTH           = 100
BOSS_SCALE = 2  # 1.5 kat büyük
BOSS_HITBOX_OFFSET_Y = 20  # Hitbox ayarı için

# Projeksil sabitleri
PROJECTILE_VELOCITY = 10
PROJECTILE_DAMAGE = 10

# Animasyon sabitleri
ANIMATION_COOLDOWN = 100
BOSS_ANIMATION_COOLDOWN = 100

# Diğer sabitler
START_BUTTON_WIDTH = 200
START_BUTTON_HEIGHT = 50




SAKURA_PINK = (255, 183, 197)
SUNSET_ORANGE = (253, 94, 83)
TREE_PURPLE = (54, 33, 89)
SUN_YELLOW = (255, 159, 28)

# Renkler
SKY_GRADIENT = [
    (32, 18, 59),   # Gece mavisi
    (253, 94, 83),  # Günbatımı turuncusu
    (255, 159, 28)  # Güneş sarısı
]
GROUND_GREEN = (45, 86, 44)
TREE_BROWN = (48, 28, 19)
