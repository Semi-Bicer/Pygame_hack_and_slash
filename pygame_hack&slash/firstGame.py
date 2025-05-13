import pygame
import os
import constants
from character import Character
from boss import Boss
from functions import *
import math
#from Background import SamuraiBackground

pygame.init()

win = pygame.display.set_mode((constants.screenWidth, constants.screenHeight))
pygame.display.set_caption("Boss Fight")

bg = pygame.image.load(os.path.join("assets", "PixelArtForest", "Preview", "Background.png"))
#bg = SamuraiBackground(constants.screenWidth, constants.screenHeight)              # geçici bg gibi (silinebilir)

walkRight = load_individual_sprites(os.path.join("assets", "Roguelike Dungeon - Asset Bundle", "Sprites", "Player", "Axe", "Defence0", "Walk"))
charIdle = load_individual_sprites(os.path.join("assets", "Roguelike Dungeon - Asset Bundle", "Sprites", "Player", "Axe", "Defence0", "Idle"))

walkRight = [pygame.transform.scale(frame, (frame.get_width() * constants.scale, frame.get_height() * constants.scale)) for frame in walkRight]
charIdle = [pygame.transform.scale(frame, (frame.get_width() * constants.scale, frame.get_height() * constants.scale)) for frame in charIdle]

enemyFly = load_individual_sprites(os.path.join("assets", "Knight", "Sprites", "EnemyFly"))
dungeonMasterWalk = load_individual_sprites(os.path.join("assets", "Roguelike Dungeon - Asset Bundle", "Sprites", "Bosses", "Dungeon Master", "Walk"))

mob_types = ["knight", "flyEye"]
animation_list = [charIdle, walkRight]
animation_list2 = [enemyFly, enemyFly]
animation_list3 = [dungeonMasterWalk, dungeonMasterWalk]
mob_animations = [animation_list, animation_list2, animation_list3]

game_active = False
font = pygame.font.SysFont("comicsans", 30)

def draw_start_button(win, font):  # Parametre ekleyin
    btn_rect = pygame.Rect(constants.screenWidth // 2 - 100, constants.screenHeight // 2 - 25,
                         constants.START_BUTTON_WIDTH, constants.START_BUTTON_HEIGHT)
    pygame.draw.rect(win, (0, 200, 0), btn_rect)
    text = font.render("Start", True, constants.WHITE)
    win.blit(text, (btn_rect.x + 50, btn_rect.y + 4))
    return btn_rect

class Projectile:
    def __init__(self, x, y, width, height, facing, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.facing = facing
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

player = Character(constants.screenWidth // 2, constants.screenHeight // 2, 96, 84, constants.screenWidth, constants.screenHeight, mob_animations, 0)
boss = Boss(constants.BOSS_START_X, constants.BOSS_START_Y - 50)
bullets = []
run = True

def redrawGameWindow():
    #bg.update()
    #bg.draw(win)
    win.blit(bg, (0, 0))

    boss.update(player)
    boss.draw(win)
    player.draw(win, font)
    player.update()

    for bullet in bullets[:]:
        bullet.x += (bullet.vel * bullet.facing)

        if bullet.x > constants.screenWidth or bullet.x < 0:
            bullets.remove(bullet)
            continue

        bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
        boss_rect = pygame.Rect(boss.x, boss.y, constants.BOSS_FRAME_WIDTH, constants.BOSS_FRAME_HEIGHT)

        if bullet_rect.colliderect(boss_rect):
            bullets.remove(bullet)
            boss.take_damage(10)  # Eski: boss.health -= 10
            print("Boss hit! Sağlık:", boss.health)
            continue

        if (boss.action.startswith("attack") or boss.action == "jump_attack") and boss.rect.colliderect(player.rect):
            if player.health > 0 and not boss.invincible:
                player.health -= 1

        bullet.draw(win)

    pygame.display.update()

# Yeni: boss saldırısı oyuncuya temas ederse hasar
    if boss.action.startswith("attack") or boss.action == "jump_attack":
        boss_rect = pygame.Rect(boss.x + 20, boss.y + 20, 80, 80)  # hasar kutusu
        if boss_rect.colliderect(player.rect):
            if player.health > 0:
                player.health -= 1  # her frame 1 can

while run:
    clock.tick(constants.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if not game_active and event.type == pygame.MOUSEBUTTONDOWN:
            if draw_start_button(win, font).collidepoint(pygame.mouse.get_pos()):
                game_active = True

    if not game_active:
        win.fill(constants.BLACK)
        draw_start_button(win, font)
        pygame.display.update()
        continue

    keys = pygame.key.get_pressed()
    player.move(keys)

    if keys[pygame.K_v] and len(bullets) < 1:
        facing = -1 if player.leftIdle or player.left else 1
        w = enemyFly[0].get_width()
        h = enemyFly[0].get_height()
        bx = player.x + player.width if facing == 1 else player.x - w
        by = player.y + player.height // 2 - h // 2
        bullets.append(Projectile(bx, by, w, h, facing, 10))

    if keys[pygame.K_SPACE] and player.health > 0:
        pygame.time.delay(100)

    redrawGameWindow()

pygame.quit()