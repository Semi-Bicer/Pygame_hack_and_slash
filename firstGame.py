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
boss = Boss(constants.BOSS_START_X, constants.BOSS_START_Y - 50, player, sfx_manager)

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

# Menü sistemi                                                                                                      #💥
menu = Menu(constants.screenWidth, constants.screenHeight)                                                          #💥

# Oyun Değişkenleri
clock = pygame.time.Clock()
run = True
game_active = False
game_paused = False  # Oyun duraklatıldı mı?
start_button = None  # Start butonu için rect

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

    # Normal saldırı hasar kontrolü
    if player.is_attacking:
        # Debug için attack_rect'i göster
        pygame.draw.rect(win, (0, 255, 0), player.attack_rect, 2)

        # Hasar verme frame'inde ve henüz hasar verilmemişse
        if player.frame_index == player.attack_frame and not player.has_dealt_damage:
            print(f"Checking attack collision, frame: {player.frame_index}")
            # Çarpışma kontrolü
            if player.attack_rect.colliderect(boss.rect):
                # Combo sayısına göre artan hasar
                combo_damage = player.attack_damage * (1 + player.combo_count * 0.2)  # Her combo %20 daha fazla hasar
                boss.take_damage(combo_damage)
                player.has_dealt_damage = True
                print(f"Boss hit! Combo {player.combo_count+1}, Hasar: {combo_damage}, Sağlık: {boss.health}")
            else:
                print("Attack missed! No collision with boss.")

    # Air attack hasar kontrolü
    elif player.is_air_attacking:
        # Debug için attack_rect'i göster
        pygame.draw.rect(win, (0, 255, 0), player.attack_rect, 2)

        # Hasar verme frame'inde ve henüz hasar verilmemişse
        if player.frame_index == player.air_attack_frame and not player.has_dealt_damage:
            print(f"Checking air attack collision, frame: {player.frame_index}")
            # Çarpışma kontrolü
            if player.attack_rect.colliderect(boss.rect):
                boss.take_damage(player.air_attack_damage)
                player.has_dealt_damage = True
                print(f"Boss air attack hit! Hasar: {player.air_attack_damage}, Sağlık: {boss.health}")
            else:
                print("Air attack missed! No collision with boss.")

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

while run:
    clock.tick(constants.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break                                                                                 #💥  burdan aşağısı

        if not game_active:
            # Ana menü olaylarını işle
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
                boss.phase = 1  # Boss'un phase değerini sıfırla
                boss.action = "idle"  # Boss'un action değerini sıfırla
                boss.phase_transition = False  # Phase geçişini sıfırla
                boss.invincible = False  # Yenilmezlik durumunu sıfırla
                boss.attack_cooldown = 2000  # Attack cooldown'u sıfırla
                boss.dash_speed = constants.BOSS_SPEED * 5  # Dash hızını sıfırla
                player.x = constants.CHAR_X
                player.y = constants.CHAR_Y
                boss.x = constants.BOSS_START_X
                boss.y = constants.BOSS_START_Y - 50
                game_paused = False
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