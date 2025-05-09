import pygame
import os
from character import Player, enemyFly
from boss import Boss                                                                                       # YENİ
import constants

pygame.init()

win = pygame.display.set_mode((constants.screenWidth, constants.screenHeight))
pygame.display.set_caption("First")

game_active = False
font = pygame.font.SysFont("comicsans", 30)

def draw_start_button():
    btn_rect = pygame.Rect(constants.screenWidth//2 - 100, constants.screenHeight//2 - 25, 200, 50)
    pygame.draw.rect(win, (0, 200, 0), btn_rect)
    text = font.render("Start", True, constants.WHITE)
    win.blit(text, (btn_rect.x + 50, btn_rect.y + 4))
    return btn_rect

# Arkaplan
bg = pygame.image.load(os.path.join("assets", "PixelArtForest", "Preview", "Background.png"))

# Boss örneğini sabitlerden alınan konumla oluştur                                                      # YENİ EKLENDİ
boss = Boss(constants.BOSS_START_X, constants.BOSS_START_Y)

def redrawGameWindow():
    win.blit(bg, (0, 0))

    # ─── BOSS ÇİZİMİ ──────────────────────────────────────────                                        # YENİ
    boss.draw(win)

    # ─── HERO ÇİZİMİ ──────────────────────────────────────────
    Character.draw(win, font)

    # Mermiler
    for bullet in bullets:
        bullet.x += (bullet.vel * bullet.facing)
        if bullet.x > constants.screenWidth or bullet.x < 0:
            bullets.pop(bullets.index(bullet))
        else:
            bullet.draw(win)

    pygame.display.update()

class Projectile(object):
    def __init__(self, x, y, width, height, facing, vel):
        self.x = x; self.y = y
        self.width = width; self.height = height
        self.vel = vel; self.facing = facing                # 1 for right, -1 for left
        self.frameCount = 0
        self.sprites = enemyFly

    def draw(self, win):
        # Animate the projectile using the enemyFly sprites
        if self.frameCount >= len(self.sprites):
            self.frameCount = 0
        sprite = self.sprites[self.frameCount]

        # If facing left, flip the sprite
        if self.facing == 1:
            sprite = pygame.transform.flip(sprite, True, False)
        win.blit(sprite, (self.x, self.y))
        self.frameCount = (self.frameCount + 1) % len(self.sprites)

clock = pygame.time.Clock()

Character = Player(constants.screenWidth//2,
                   constants.screenHeight//2,
                   64, 64,
                   constants.screenWidth,
                   constants.screenHeight)
bullets = []
run = True

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
    Character.move(keys)

    if keys[pygame.K_v] and len(bullets) < 5:
        facing = -1 if Character.leftIdle or Character.left else 1
        w = enemyFly[0].get_width()
        h = enemyFly[0].get_height()
        bx = Character.x + Character.width if facing == 1 else Character.x - w
        by = Character.y + Character.height//2 - h//2
        bullets.append(Projectile(bx, by, w, h, facing, 10))

    if keys[pygame.K_SPACE] and Character.health > 0:
        pygame.time.delay(100)

    redrawGameWindow()

pygame.quit()