import pygame
import os
import constants
from character import Character
from boss import Boss
from functions import *
from weapon import Weapon

pygame.init()

win = pygame.display.set_mode((constants.screenWidth, constants.screenHeight))
pygame.display.set_caption("First")

# Load weapon image
weapon_image =  pygame.image.load(os.path.join("assets","Roguelike Dungeon - Asset Bundle", "Items", "Axe", "Axe_0.png"))

# Load animation frames
walkRight = load_individual_sprites(os.path.join("assets","Roguelike Dungeon - Asset Bundle","Sprites","Player", "Axe","Defence0","Walk"))
charIdle = load_individual_sprites(os.path.join("assets","Roguelike Dungeon - Asset Bundle","Sprites","Player", "Axe","Defence0","Idle"))
walkRight = [pygame.transform.scale(frame, (frame.get_width() * constants.scale, frame.get_height() * constants.scale)) for frame in walkRight]
charIdle = [pygame.transform.scale(frame, (frame.get_width() * constants.scale, frame.get_height() * constants.scale)) for frame in charIdle]

# Load enemy sprites
enemyFly = load_individual_sprites(os.path.join("assets", "Knight", "Sprites", "EnemyFly"))

dungeonMasterWalk = load_individual_sprites(os.path.join("assets", "Roguelike Dungeon - Asset Bundle", "Sprites", "Bosses", "Dungeon Master","Walk"))


mob_types = ["knight", "flyEye"]
animation_types = ["idle", "walk"]
animation_list = [charIdle, walkRight] # for Character
animation_list2 = [enemyFly,enemyFly] # for first enemy
animation_list3 = [dungeonMasterWalk,dungeonMasterWalk] # for first boss
mob_animations = [animation_list, animation_list2,animation_list3]

game_active = False
font = pygame.font.SysFont("comicsans", 30)

def draw_start_button():
    btn_rect = pygame.Rect(constants.screenWidth//2 - 100, constants.screenHeight//2 - 25, 200,50)
    pygame.draw.rect(win, (0, 200, 0), btn_rect)
    text = font.render("Start", True, constants.WHITE)
    win.blit(text, (btn_rect.x + 50, btn_rect.y + 4))
    return btn_rect

# Arkaplan
bg = pygame.image.load(os.path.join("assets", "PixelArtForest", "Preview", "Background.png"))

###
# Projectile class
###
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

        # If facing left, flip the sprite
        if self.facing == 1:
            sprite = pygame.transform.flip(sprite, True, False)
        win.blit(sprite, (self.x, self.y))
        self.frameCount = (self.frameCount + 1) % len(self.sprites)

clock = pygame.time.Clock()



#####################################################################################
# this is the main loop of the game
#####################################################################################
Character = Character(constants.screenWidth//2, constants.screenHeight//2, 96, 84, constants.screenWidth, constants.screenHeight,mob_animations, 0)
axe = Weapon(weapon_image)

boss = Boss(constants.BOSS_START_X, constants.BOSS_START_Y)
bullets = []
run = True

def redrawGameWindow():
    win.blit(bg, (0, 0))

    # ─── BOSS TAKİP ve ÇİZİMİ ──────────────────────────────────────────
    boss.update(Character)       # 💥 Oyuncuyu takip et
    boss.draw(win)

    # ─── OYUNCU ÇİZİMİ ───────────────────────────────────────────────
    Character.draw(win, font)
    Character.update()
    axe.draw(win)
    axe.update(Character)

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
    Character.move(keys)  # ⬅️ Character ➞ Character

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
