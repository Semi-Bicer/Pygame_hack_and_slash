### firstGame.py
import pygame
import os
import constants
from character import Character
from boss import Boss
from functions import *
from Background import SamuraiBackground
from sfx import SoundManager

pygame.init()

def draw_start_menu(win, constants, fonts):
    """Samuray temalı başlangıç menüsü"""
    win.fill((20, 0, 0))
    pygame.draw.rect(win, (40, 0, 0), (0, constants.screenHeight // 2, constants.screenWidth, constants.screenHeight // 2))

    title_text = fonts["large"].render("SHADOW FIGHT", True, (255, 215, 0))
    title_shadow = fonts["large"].render("SHADOW FIGHT", True, (100, 0, 0))
    win.blit(title_shadow, (constants.screenWidth // 2 - title_text.get_width() // 2 + 3, 100 + 3))
    win.blit(title_text, (constants.screenWidth // 2 - title_text.get_width() // 2, 100))

    subtitle_text = fonts["medium"].render("İki Kılıcın Kader Savaşı", True, (200, 200, 200))
    win.blit(subtitle_text, (constants.screenWidth // 2 - subtitle_text.get_width() // 2, 180))

    btn_width, btn_height = 300, 60
    btn_x = constants.screenWidth // 2 - btn_width // 2
    btn_y = constants.screenHeight // 2 + 50

    pygame.draw.rect(win, (100, 0, 0), (btn_x + 5, btn_y + 5, btn_width, btn_height))
    mouse_pos = pygame.mouse.get_pos()
    btn_hover = pygame.Rect(btn_x, btn_y, btn_width, btn_height).collidepoint(mouse_pos)
    btn_color = (180, 0, 0) if not btn_hover else (220, 0, 0)
    pygame.draw.rect(win, btn_color, (btn_x, btn_y, btn_width, btn_height))
    pygame.draw.rect(win, (255, 215, 0), (btn_x, btn_y, btn_width, btn_height), 3)

    btn_text = fonts["medium"].render("Savaşa Başla", True, constants.WHITE)
    win.blit(btn_text, (constants.screenWidth // 2 - btn_text.get_width() // 2, btn_y + btn_height // 2 - btn_text.get_height() // 2))

    info_text = fonts["small"].render("WASD: Hareket | F: Saldırı | V: Shuriken | L-Shift: Dash", True, (150, 150, 150))
    win.blit(info_text, (constants.screenWidth // 2 - info_text.get_width() // 2, constants.screenHeight - 50))

    pygame.draw.polygon(win, (80, 80, 80), [(50, 300), (100, 200), (150, 300)])
    pygame.draw.polygon(win, (80, 80, 80), [(constants.screenWidth - 50, 300), (constants.screenWidth - 100, 200), (constants.screenWidth - 150, 300)])

    return pygame.Rect(btn_x, btn_y, btn_width, btn_height)

# Pencere
win = pygame.display.set_mode((constants.screenWidth, constants.screenHeight))
pygame.display.set_caption("Boss Fight")

# Ses
sfx_manager = SoundManager()
sfx_manager.play_music("menu")

# Arkaplan
bg = SamuraiBackground(constants.screenWidth, constants.screenHeight)
#bg = pygame.image.load(os.path.join("pygame_hack&slash","assets", "PixelArtForest", "Preview", "Background.png"))

# Mermiler
bullets = []

attack = load_and_scale_sheet(os.path.join("assets", "Player", "Sprites", "ATTACK 1.png"),96,84,7)
dash = load_and_scale_sheet(os.path.join("assets", "Player", "Sprites", "DASH.png"),95,84,8)
runRight = load_and_scale_sheet(os.path.join("assets", "Player", "Sprites", "RUN.png"),96,84,16)
walkRight = load_and_scale_sheet(os.path.join("assets", "Player", "Sprites", "WALK.png"),96,84,12)
charIdle = load_and_scale_sheet(os.path.join("assets", "Player", "Sprites", "IDLE.png"),96,84,10)
shuriken = load_single_image(os.path.join("assets", "Player", "shuriken.png"), constants.scale)

animation_list = [charIdle, walkRight, runRight, dash, attack]
animation_list2 = [shuriken, shuriken]

mob_animations = [animation_list, animation_list2]

# Oyuncu
player = Character(constants.CHAR_X, constants.CHAR_Y, 96, 84, constants.screenWidth, constants.screenHeight, mob_animations, 0)
#player.set_sfx_manager(sfx_manager)

# Boss
boss = Boss(constants.BOSS_START_X, constants.BOSS_START_Y - 50,player)





font = pygame.font.SysFont("comicsans", 30)


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

# Oyun Değişkenleri
clock = pygame.time.Clock()
run = True
game_active = False


def redrawGameWindow():
    bg.update()
    bg.draw(win)
    # win.blit(bg, (0, 0))

    boss.update(player)
    boss.draw(win)
    player.draw(win, font)
    player.update()

    # Boss'un hitbox'ını göster
    pygame.draw.rect(win, constants.RED, boss.rect, 1)
    # print(f"Player attacking: {player.is_attacking}, Frame: {player.frame_index}, Attack frame: {player.attack_frame}, Has dealt damage: {player.has_dealt_damage}")

    if player.is_attacking:
        if player.frame_index == player.attack_frame and not player.has_dealt_damage:
            if player.attack_rect.colliderect(boss.rect):
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

        if bullet_rect.colliderect(boss.rect):
            bullets.remove(bullet)
            boss.take_damage(constants.PROJECTILE_DAMAGE)
            print("Boss hit! Sağlık:", boss.health)
            continue

        bullet.draw(win)

    # Boss saldırısı
    if (boss.action.startswith("attack") or boss.action == "jump_attack"):
        # Saldırı hitbox'ını göster (debug için)
        pygame.draw.rect(win, (255, 0, 0), boss.attack_rect, 2)

        # Saldırı frame'i kontrolü
        attack_key = boss.action
        if "_flame" in attack_key:
            attack_key = attack_key.replace("_flame", "")

        if attack_key in boss.attack_frames and boss.frame_index in boss.attack_frames[attack_key] and not boss.has_dealt_damage:
            # Çarpışma kontrolü
            if boss.attack_rect.colliderect(player.rect):
                if player.health > 0 and not boss.invincible:
                    dmg = constants.DAMAGE_BOSS_PHASE_2 if boss.phase == 2 else constants.DAMAGE_BOSS_PHASE_1
                    player.health -= dmg
                    boss.has_dealt_damage = True
                    print("Player hit! Sağlık:", player.health)

    #pygame.draw.rect(win, constants.RED, boss_rect, 2)
    pygame.display.update()


    # Zehir/ alev efekti boss etrafında
    # if boss.action.startswith("attack") or boss.action == "jump_attack":
    #     boss_rect = pygame.Rect(boss.x + 20, boss.y + 20, 80, 80)  # hasar kutusu
    #     pygame.draw.rect(win, constants.RED, boss_rect, 2)
    #     if boss_rect.colliderect(player.rect):
    #         if player.health > 0:
    #             player.health -= 1  # her frame 1 can

while run:
    clock.tick(constants.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if not game_active and event.type == pygame.MOUSEBUTTONDOWN:
            if draw_start_button().collidepoint(pygame.mouse.get_pos()):
                game_active = True
                sfx_manager.stop_music(fade_ms=500)
                sfx_manager.play_music("battle", fade_ms=1000)

    if not game_active:
        win.fill(constants.BLACK)
        draw_start_button()
        pygame.display.update()
        continue

    keys = pygame.key.get_pressed()
    clicks = pygame.mouse.get_pressed()
    player.move(keys, clicks)

    # Player'ın boss içerisine girmesini engelle
    boss.collision_with_player(player)

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

    

    redrawGameWindow()

pygame.quit()