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
CHAR_X                = 100  # Solda başlasın
CHAR_Y                = screenHeight // 2 + 100  # Ayakları zemine hizalı
CHAR_HEALTH           = 100
CHAR_MAX_HEALTH       = 100
CHAR_SPEED            = 6
CHAR_DASH_SPEED       = 8.0
CHAR_DASH_MULTIPLIER  = 1
CHAR_DASH_DELAY       = 480
CHAR_DASH_COOLDOWN   = 1500  # ms cinsinden dash bekleme süresi
CHAR_ANIM_COOLDOWN_MS = 60
CHAR_ATTACK_COOLDOWN = 500  # ms cinsinden saldırı bekleme süresi
CHAR_ATTACK_FRAME_DURATION = 50  # ms cinsinden saldırı süresi
CHAR_ATTACK_DAMAGE = 20
CHAR_ATTACK_FRAME = 3
CHAR_HEALING_AMOUNT = 20  # İyileştirme miktarı
CHAR_HEALING_COOLDOWN = 3000  # İyileştirme bekleme süresi (ms)

# Boss sabitleri
BOSS_FRAME_WIDTH      = 128
BOSS_FRAME_HEIGHT     = 108
BOSS_NUM_FRAMES       = 6
BOSS_START_X          = screenWidth - 100  # Sağda başlasın
BOSS_START_Y          = screenHeight // 2 + 100  # Ayakları zemine hizalı
BOSS_SPEED            = 2.0
BOSS_FOLLOW_DISTANCE  = 800
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

# Renk paleti - Sakura vadisi için pastel gün batımı renkleri
SAKURA_PINK = (255, 183, 197)  # Açık pembe
SAKURA_DARK = (255, 150, 180)  # Orta pembe
SAKURA_RED = (255, 120, 150)   # Koyu pembe/açık kırmızı
SAKURA_WHITE = (255, 240, 245) # Beyazımsı pembe
SUNSET_ORANGE = (253, 94, 83)  # Turuncu
SUNSET_PINK = (255, 145, 175)  # Gün batımı pembesi
SUNSET_YELLOW = (255, 190, 130) # Gün batımı sarısı
SUN_YELLOW = (255, 200, 120)   # Daha yumuşak sarı

# Pastel gün batımı gökyüzü gradienti
SKY_GRADIENT = [(70, 40, 80), (180, 80, 110), (255, 190, 130)]

# Zemin renkleri
GROUND_PINK = (255, 230, 240)  # Sakura çiçekleriyle kaplı zemin
TREE_BROWN = (80, 50, 35)      # Daha koyu ağaç gövdesi

# Sis ve bulut renkleri
MIST_COLORS = [(255, 255, 255, 40), (255, 240, 250, 30), (255, 230, 240, 20)]
CLOUD_COLORS = [(255, 230, 240, 60), (255, 220, 230, 50), (255, 210, 220, 40)]

# Sakura yaprak renkleri - daha kırmızımsı tonlar
SAKURA_COLORS = [(255, 120, 150), (255, 100, 130), (255, 80, 120), (255, 60, 100), (255, 40, 80)]

# Dağ silueti renkleri
MOUNTAIN_COLORS = [(80, 50, 80), (100, 60, 90), (120, 70, 100)]