import pygame
import os
import constants
from character import Character
from boss import Boss
from functions import *
import math
from Background import SamuraiBackground

pygame.init()

win = pygame.display.set_mode((constants.screenWidth, constants.screenHeight))
pygame.display.set_caption("Boss Fight")

#bg = pygame.image.load(os.path.join("pygame_hack&slash","assets", "PixelArtForest", "Preview", "Background.png"))
bg = SamuraiBackground(constants.screenWidth, constants.screenHeight)              # geçici bg gibi (silinebilir)
attack = load_and_scale_sheet(os.path.join("pygame_hack&slash","assets", "FULL_Samurai 2D Pixel Art v1.2", "Sprites", "ATTACK 1.png"),96,84,7)
dash = load_and_scale_sheet(os.path.join("pygame_hack&slash","assets", "FULL_Samurai 2D Pixel Art v1.2", "Sprites", "DASH.png"),95,84,8)
walkRight = load_and_scale_sheet(os.path.join("pygame_hack&slash","assets", "FULL_Samurai 2D Pixel Art v1.2", "Sprites", "WALK.png"),96,84,12)
charIdle = load_and_scale_sheet(os.path.join("pygame_hack&slash","assets", "FULL_Samurai 2D Pixel Art v1.2", "Sprites", "IDLE.png"),96,84,10)


shuriken = load_single_image(os.path.join("pygame_hack&slash","assets", "FULL_Samurai 2D Pixel Art v1.2", "shuriken.png"), constants.scale)

dungeonMasterWalk = load_individual_sprites(os.path.join("pygame_hack&slash","assets", "Roguelike Dungeon - Asset Bundle", "Sprites", "Bosses", "Dungeon Master","Walk"))


mob_types = ["knight", "flyEye"]
animation_list = [charIdle, walkRight, dash, attack]
animation_list2 = [shuriken, shuriken]
animation_list3 = [dungeonMasterWalk, dungeonMasterWalk]
mob_animations = [animation_list, animation_list2, animation_list3]

game_active = False
font = pygame.font.SysFont("comicsans", 30)

def draw_start_button():
    btn_rect = pygame.Rect(constants.screenWidth//2 - 100, constants.screenHeight//2 - 25, 200,50)
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
        self.sprites = shuriken

    def draw(self, win):
        # Check if sprites list is not empty
        if not self.sprites or len(self.sprites) == 0:
            # Draw a simple rectangle if no sprites are available
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))
            return

        if self.frameCount >= len(self.sprites):
            self.frameCount = 0

        sprite = self.sprites[self.frameCount]
        if self.facing == 1:
            sprite = pygame.transform.flip(sprite, True, False)
        win.blit(sprite, (self.x, self.y))
        self.frameCount = (self.frameCount + 1) % len(self.sprites)

clock = pygame.time.Clock()

player = Character(constants.CHAR_X, constants.CHAR_Y, 96, 84, constants.screenWidth, constants.screenHeight, mob_animations, 0)
boss = Boss(constants.BOSS_START_X, constants.BOSS_START_Y - 50)
bullets = []
run = True

def redrawGameWindow():
    bg.update()
    bg.draw(win)
    #win.blit(bg, (0, 0))

    boss.update(player)
    boss.draw(win)
    player.draw(win, font)
    player.update()
    
    boss_rect = pygame.Rect(boss.x, boss.y, boss.rect.width- constants.BOSS_HITBOX_OFFSET_X * 3, boss.rect.height - constants.BOSS_HITBOX_OFFSET_Y)
    pygame.draw.rect(win, constants.RED, boss_rect, 1)
    #print(f"Player attacking: {player.is_attacking}, Frame: {player.frame_index}, Attack frame: {player.attack_frame}, Has dealt damage: {player.has_dealt_damage}")
    
    if player.is_attacking:
        if player.frame_index == player.attack_frame and not player.has_dealt_damage:
            if player.attack_rect.colliderect(boss_rect):
                boss.take_damage(player.attack_damage)
                player.has_dealt_damage = True
                print("Boss hit! Sağlık:", boss.health)

    for bullet in bullets[:]:
        bullet.x += (bullet.vel * bullet.facing)

        # Ekran dışına çıkan mermiler
        if bullet.x > constants.screenWidth or bullet.x < 0:
            bullets.remove(bullet)
            continue

        bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
        

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
            if draw_start_button().collidepoint(pygame.mouse.get_pos()):
                game_active = True

    if not game_active:
        win.fill(constants.BLACK)
        draw_start_button()
        pygame.display.update()
        continue

    keys = pygame.key.get_pressed()
    player.move(keys)

    if keys[pygame.K_v] and len(bullets) < 1:

        facing = -1 if player.leftIdle or player.left else 1
        # Check if shuriken list is not empty before accessing elements
        if shuriken and len(shuriken) > 0:
            w = shuriken[0].get_width()
            h = shuriken[0].get_height()
            bx = player.x + player.width if facing == 1 else player.x - w
            by = player.y + player.height // 2 - h // 2
            bullets.append(Projectile(bx, by, w, h, facing, 10))
        else:
            print("Warning: shuriken list is empty. Cannot create projectile.")
            # Use default values if shuriken is not available
            w, h = 20, 20  # Default size
            bx = player.x + player.width if facing == 1 else player.x - w
            by = player.y + player.height // 2 - h // 2
            bullets.append(Projectile(bx, by, w, h, facing, 10))

    if keys[pygame.K_SPACE] and player.health > 0:
        pygame.time.delay(100)

    redrawGameWindow()

pygame.quit()