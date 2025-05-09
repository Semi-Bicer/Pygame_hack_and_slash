import pygame
import os
from character import Player, enemyFly  # Player ve mermi sprite'ları
from boss import Boss                   # ⚡️ YENİ
import constants

pygame.init()

win = pygame.display.set_mode((constants.screenWidth, constants.screenHeight))
pygame.display.set_caption("First")

game_active = False
font = pygame.font.SysFont("comicsans", 30)

def draw_start_button():
    btn_rect = pygame.Rect(
        constants.screenWidth//2 - 100,
        constants.screenHeight//2 - 25,
        200, 50
    )
    pygame.draw.rect(win, (0, 200, 0), btn_rect)
    text = font.render("Start", True, constants.WHITE)
    win.blit(text, (btn_rect.x + 50, btn_rect.y + 4))
    return btn_rect

# Arkaplan
bg = pygame.image.load(os.path.join("assets", "PixelArtForest", "Preview", "Background.png"))

# ⬇️ YENİ: Player adıyla yeniden isimlendirildi (önceki Character)
player = Player(
    constants.screenWidth//2,
    constants.screenHeight//2,
    64, 64,
    constants.screenWidth,
    constants.screenHeight
)

# ⬇️ YENİ: Boss nesnesi
boss = Boss(constants.BOSS_START_X, constants.BOSS_START_Y)

class Projectile(object):
    def __init__(self, x, y, width, height, facing, vel):
        self.x = x; self.y = y
        self.width = width; self.height = height
        self.vel = vel; self.facing = facing
        self.frameCount = 0
        self.sprites = enemyFly

    def draw(self, win):
        if self.frameCount >= len(self.sprites):
            self.frameCount = 0
        sprite = self.sprites[self.frameCount]
        if self.facing == 1:
            sprite = pygame.transform.flip(sprite, True, False)
        win.blit(sprite, (self.x, self.y))
        self.frameCount = (self.frameCount + 1) % len(self.sprites)

clock = pygame.time.Clock()
bullets = []
run = True

def redrawGameWindow():
    win.blit(bg, (0, 0))

    # ─── BOSS TAKİP ve ÇİZİMİ ──────────────────────────────────────────
    boss.update(player)       # 💥 Oyuncuyu takip et
    boss.draw(win)

    # ─── OYUNCU ÇİZİMİ ───────────────────────────────────────────────
    player.draw(win, font)

    # ─── MERMİLER ve ÇARPIMA BAK ───────────────────────────────────
    for bullet in bullets[:]:
        bullet.x += (bullet.vel * bullet.facing)

        # Ekran dışına çıkan mermiler
        if bullet.x > constants.screenWidth or bullet.x < 0:
            bullets.remove(bullet)
            continue

        # 🛡️ Boss ile çarpışma kontrolü
        bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
        boss_rect   = pygame.Rect(
            boss.x, boss.y,
            constants.BOSS_FRAME_WIDTH, constants.BOSS_FRAME_HEIGHT
        )
        if bullet_rect.colliderect(boss_rect):
            bullets.remove(bullet)
            boss.health -= 10  # 💥 Boss hasar alır
            print("Boss hit! Sağlık:", boss.health)
            continue

        bullet.draw(win)

    pygame.display.update()

while run:
    clock.tick(constants.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if not game_active and event.type == pygame.MOUSEBUTTONDOWN:
            if draw_start_button().collidepoint(pygame.mouse.get_pos()):
                game_active = True

    if not game_active:
        win.fill(constants.BLACK)
        draw_start_button()
        pygame.display.update()
        continue

    keys = pygame.key.get_pressed()
    player.move(keys)  # ⬅️ Character ➞ player

    if keys[pygame.K_v] and len(bullets) < 5:
        facing = -1 if player.leftIdle or player.left else 1
        w = enemyFly[0].get_width()
        h = enemyFly[0].get_height()
        bx = player.x + player.width if facing == 1 else player.x - w
        by = player.y + player.height//2 - h//2
        bullets.append(Projectile(bx, by, w, h, facing, 10))

    if keys[pygame.K_SPACE] and player.health > 0:
        pygame.time.delay(100)

    redrawGameWindow()

pygame.quit()
