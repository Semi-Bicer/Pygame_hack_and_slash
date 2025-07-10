import os

# Genel ayarlar
FPS = 60
screenWidth = 1920
screenHeight = 1080
scale = 2

# Font ve ses yolları
FONT_PATH = os.path.join("assets", "fonts", "SchoonSquare-Regular.ttf")
SFX_PATH = os.path.join("assets", "sfx")

# Renkler
OFFSET_X = 20
OFFSET_Y = 40
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Çözünürlük bazlı konum sabitleri
# Her çözünürlük için karakter ve boss konumları
POSITIONS = {
    # 800x600 için konumlar
    (800, 600): {
        "CHAR_X": 200,
        "CHAR_Y": 100,
        "BOSS_X": 450,
        "BOSS_Y": 340
    },
    # 1000x800 için konumlar
    (1000, 800): {
        "CHAR_X": 300,
        "CHAR_Y": 500,
        "BOSS_X": 700,
        "BOSS_Y": 550
    },
    # 1280x720 için konumlar
    (1280, 720): {
        "CHAR_X": 400,
        "CHAR_Y": 450,
        "BOSS_X": 880,
        "BOSS_Y": 500
    },
    # Tam ekran için konumlar (varsayılan 1920x1080 olarak kabul edildi)
    "fullscreen": {
        "CHAR_X": 700,
        "CHAR_Y": 650,
        "BOSS_X": 1100,
        "BOSS_Y": 575
    }
}
ORAN_W = (80/198, 100/192, 2/3, 1)
ORAN_H = (60/108, 80/108, 2/3, 1)

# Mevcut çözünürlük için konumları al
def get_positions(width, height, is_fullscreen=True):
    if is_fullscreen:
        return POSITIONS["fullscreen"]

    # Mevcut çözünürlük için tanımlı konum var mı?
    if (width, height) in POSITIONS:
        return POSITIONS[(width, height)]

    # Yoksa en yakın çözünürlüğü bul
    closest = (1919, 1079)  # Varsayılan
    for res in POSITIONS:
        if res != "fullscreen":
            if abs(res[0] - width) + abs(res[1] - height) < abs(closest[0] - width) + abs(closest[1] - height):
                closest = res

    return POSITIONS[closest]

# Karakter ve boss konumlarını fonksiyon olarak tanımla
def get_char_x():
    return get_positions(screenWidth, screenHeight)["CHAR_X"]

def get_char_y():
    return get_positions(screenWidth, screenHeight)["CHAR_Y"]

def get_boss_x():
    return get_positions(screenWidth, screenHeight)["BOSS_X"]

def get_boss_y():
    return get_positions(screenWidth, screenHeight)["BOSS_Y"]

# Karakter sabitleri
CHAR_X                = get_char_x()
CHAR_Y                = get_char_y()
CHAR_HEALTH           = 100
CHAR_MAX_HEALTH       = 100
CHAR_SPEED            = 6
CHAR_DASH_SPEED       = 8.0
CHAR_DASH_MULTIPLIER  = 1
CHAR_DASH_DELAY       = 480
CHAR_DASH_COOLDOWN    = 1500  # ms cinsinden dash bekleme süresi
CHAR_ANIM_COOLDOWN_MS = 60
CHAR_ATTACK_COOLDOWN  = 500  # ms cinsinden saldırı bekleme süresi
CHAR_ATTACK_FRAME_DURATION = 50  # ms cinsinden saldırı süresi
CHAR_ATTACK_DAMAGE    = 20
CHAR_ATTACK_FRAME     = 3
CHAR_HEALING_AMOUNT   = 20  # İyileştirme miktarı
CHAR_HEALING_COOLDOWN = 2000  # İyileştirme bekleme süresi (ms)
CHAR_HEALING_LIMIT    = 3  # Maksimum iyileştirme sayısı

# Boss sabitleri
BOSS_FRAME_WIDTH      = 128
BOSS_FRAME_HEIGHT     = 108
BOSS_START_X          = get_boss_x()
BOSS_START_Y          = get_boss_y()
BOSS_SPEED            = 5.0
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

# Blade Rift Projectile sabitleri
BLADE_RIFT_SPEED = 10                # Projectile hareket hızı
BLADE_RIFT_DAMAGE_PER_SECOND = 10    # Saniyede verilen hasar: 20
BLADE_RIFT_LIFETIME = 5000          # Projectile yaşam süresi (ms)
BLADE_RIFT_COOLDOWN = 5000          # Boss'un blade rift fırlatma cooldown'u (ms)
BLADE_RIFT_DAMAGE_INTERVAL = 500   # Hasar verme aralığı (ms)