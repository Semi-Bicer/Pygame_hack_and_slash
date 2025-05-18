### firstGame.py
import pygame
import constants
import os
from character import Character
from boss import Boss
from functions import *
from Background import SamuraiBackground
from menu import Menu
from sfx import SoundManager

pygame.init()

win = pygame.display.set_mode((constants.screenWidth, constants.screenHeight))
pygame.display.set_caption("Boss Fight")


sfx_manager = SoundManager()
sfx_manager.play_music("menu")

# Arkaplan
bg = SamuraiBackground(constants.screenWidth, constants.screenHeight)
#bg = pygame.image.load(os.path.join("pygame_hack&slash","assets", "PixelArtForest", "Preview", "Background.png"))

bullets = []

# Oyuncu
player = Character(constants.CHAR_X, constants.CHAR_Y, 96, 84, constants.screenWidth, constants.screenHeight, 0)
player.set_sfx_manager(sfx_manager)

# Boss
boss = Boss(constants.BOSS_START_X, constants.BOSS_START_Y, player, sfx_manager)

# Pixel font yükleme
try:
    font_path = constants.FONT_PATH
    if os.path.exists(font_path):
        font = pygame.font.Font(font_path, 30)
        print(f"Pixel font yüklendi: {font_path}")
    else:
        # Fallback font
        font = pygame.font.SysFont("comicsans", 30)
        print("Pixel font bulunamadı, varsayılan font kullanılıyor.")
except Exception as e:
    print(f"Font yüklenirken hata oluştu: {e}")
    # Fallback font
    font = pygame.font.SysFont("comicsans", 30)

class Projectile:
    def __init__(self, x, y, width, height, facing, vel, sprite=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.facing = facing
        self.frameCount = 0
        self.sprite = sprite
        self.sprites = [sprite] if sprite else []

    def draw(self, win):
        if not self.sprites or len(self.sprites) == 0:
            #pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))
            return

        if self.frameCount >= len(self.sprites):
            self.frameCount = 0

        sprite = self.sprites[self.frameCount]
        if self.facing == 1:
            sprite = pygame.transform.flip(sprite, True, False)
        win.blit(sprite, (self.x, self.y))
        self.frameCount = (self.frameCount + 1) % len(self.sprites)

# Menü sistemi                                                                                                      #💥
menu = Menu(constants.screenWidth, constants.screenHeight)                                                          #💥

# Oyun Değişkenleri
clock = pygame.time.Clock()
run = True
game_active = False
game_paused = False  
start_button = None  

def redrawGameWindow():
    bg.update()
    bg.draw(win)
    # win.blit(bg, (0, 0))

    boss.update(player)
    boss.draw(win)
    player.draw(win, font)
    player.update()

    
    #pygame.draw.rect(win, constants.RED, boss.rect, 1)

    if player.is_attacking:
        #pygame.draw.rect(win, (0, 255, 0), player.attack_rect, 2)
        if player.frame_index == player.attack_frame and not player.has_dealt_damage:
            if player.attack_rect.colliderect(boss.rect):
                combo_damage = player.attack_damage * (1 + player.combo_count * 0.2)  
                boss.take_damage(combo_damage)
                player.has_dealt_damage = True

    elif player.is_air_attacking:
        # Debug için
        #pygame.draw.rect(win, (0, 255, 0), player.attack_rect, 2)

        if player.frame_index == player.air_attack_frame and not player.has_dealt_damage:
            if player.attack_rect.colliderect(boss.rect):
                boss.take_damage(player.air_attack_damage)
                player.has_dealt_damage = True

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
            continue

        bullet.draw(win)

    if (boss.action.startswith("attack") or boss.action == "jump_attack"):
        # debug için
        #pygame.draw.rect(win, (255, 0, 0), boss.attack_rect, 2)

        attack_key = boss.action
        if "_flame" in attack_key:
            attack_key = attack_key.replace("_flame", "")

        if attack_key in boss.attack_frames and boss.frame_index in boss.attack_frames[attack_key] and not boss.has_dealt_damage:
            if boss.attack_rect.colliderect(player.rect):
                if player.health > 0 and not boss.invincible:
                    dmg = constants.DAMAGE_BOSS_PHASE_2 if boss.phase == 2 else constants.DAMAGE_BOSS_PHASE_1
                    player.health -= dmg
                    boss.has_dealt_damage = True
                    player.play_hurt_animation()

    
    pygame.display.update()

while run:
    clock.tick(constants.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break                                                                                 

        if not game_active:
            result = menu.handle_event(event, (constants.screenWidth, constants.screenHeight), sfx_manager)

            if result == "play":
                game_active = True
                game_paused = False
                sfx_manager.stop_music(fade_ms=500)
                # Menüdeki ses seviyesi ayarlarını kullan
                sfx_manager.set_music_volume(menu.music_volume)
                sfx_manager.set_sfx_volume(menu.sfx_volume)
                sfx_manager.play_music("battle", fade_ms=1000)
            elif result == "quit":
                run = False
                break
            elif isinstance(result, tuple) and result[0] == "resolution":
                # Çözünürlük değiştirme
                if result[1] == "fullscreen":
                    # Tam ekran modu
                    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    # Ekran boyutlarını al
                    display_info = pygame.display.Info()
                    constants.screenWidth = display_info.current_w
                    constants.screenHeight = display_info.current_h
                else:
                    # Normal pencere modu
                    new_width, new_height = result[1]
                    win = pygame.display.set_mode((new_width, new_height))
                    constants.screenWidth = new_width
                    constants.screenHeight = new_height

                # Arkaplanı yeniden oluştur
                bg = SamuraiBackground(constants.screenWidth, constants.screenHeight)
                # Menü boyutlarını güncelle
                menu = Menu(constants.screenWidth, constants.screenHeight)
        elif game_paused:
            # Pause menü olaylarını işle
            result = menu.handle_event(event, (constants.screenWidth, constants.screenHeight), sfx_manager)

            if result == "resume":
                game_paused = False
            elif result == "try_again":
                # Oyunu yeniden başlat
                player.health = constants.CHAR_HEALTH
                boss.health = constants.BOSS_HEALTH
                boss.phase = 1 
                boss.action = "idle"  
                boss.phase_transition = False  
                boss.invincible = False 
                boss.attack_cooldown = 2000  
                boss.dash_speed = constants.BOSS_SPEED * 5 
                player.x = constants.CHAR_X
                player.y = constants.CHAR_Y
                boss.x = constants.BOSS_START_X
                boss.y = constants.BOSS_START_Y
                game_paused = False
            elif isinstance(result, tuple) and result[0] == "resolution":
                # Çözünürlük değiştirme - pause menüsünden
                if result[1] == "fullscreen":
                    # Tam ekran modu
                    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    # Ekran boyutlarını al
                    display_info = pygame.display.Info()
                    constants.screenWidth = display_info.current_w
                    constants.screenHeight = display_info.current_h
                else:
                    # Normal pencere modu
                    new_width, new_height = result[1]
                    win = pygame.display.set_mode((new_width, new_height))
                    constants.screenWidth = new_width
                    constants.screenHeight = new_height

                
                bg = SamuraiBackground(constants.screenWidth, constants.screenHeight)
                menu = Menu(constants.screenWidth, constants.screenHeight)
                # Pause menüsüne geri dön
                menu.current_menu = "pause"
                menu.selected_item = 0
            elif result == "back":
                # Menüler arası geçiş için bir şey yapmaya gerek yok
                # Menü sınıfı içinde current_menu zaten güncelleniyor
                pass
            elif result == "quit":
                run = False
                break
        elif event.type == pygame.KEYDOWN and game_active and not game_paused:
            if event.key == pygame.K_ESCAPE:  # ESC tuşuna basıldığında pause menüsünü aç
                game_paused = True
                menu.current_menu = "pause"
                menu.selected_item = 0
        elif event.type == pygame.MOUSEBUTTONDOWN and game_active and not game_paused:
            if event.button == 1:  # Sol tık ve oyun aktifse
                sfx_manager.play_sound("attack1")                                                 # 💥 burdan yukarısı

    # Karakter öldüğünde death menüsünü göster
    if player.health <= 0:
        game_paused = True
        menu.current_menu = "death"
        menu.selected_item = 0

    # Boss öldüğünde win menüsünü göster
    if boss.health <= 0 and boss.action == "death" and boss.frame_index >= len(boss.get_animation()) - 1:
        game_paused = True
        menu.current_menu = "win"
        menu.selected_item = 0

    if not game_active or game_paused:
        menu_rects = menu.draw(win, constants, sfx_manager)                                                         #💥
        pygame.display.update()
        continue

    keys = pygame.key.get_pressed()
    clicks = pygame.mouse.get_pressed()
    player.move(keys, clicks)

    # Player'ın boss içerisine girmesini engelle
    boss.collision_with_player(player)

    # V tuşuna basıldığında shuriken fırlat
    if keys[pygame.K_v]:
        player.throw_shuriken(bullets, Projectile)


    redrawGameWindow()

pygame.quit()