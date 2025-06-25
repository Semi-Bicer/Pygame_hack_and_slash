import pygame
import constants
import os
from character import Character
from boss import Boss
from functions import *
from Background import SamuraiBackground
from menu import Menu, Button
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

# Başlangıç konumlarını çözünürlüğe göre ayarla
char_x = 300
char_y = 500
boss_x = 700
boss_y = 550

# 800x600 için
if constants.screenWidth == 800 and constants.screenHeight == 600:
    char_x = 200
    char_y = 400
    boss_x = 600
    boss_y = 450
# 1280x720 için
elif constants.screenWidth == 1280 and constants.screenHeight == 720:
    char_x = 400
    char_y = 450
    boss_x = 880
    boss_y = 500
# Tam ekran veya diğer çözünürlükler için
elif constants.screenWidth > 1280 or constants.screenHeight > 800:
    char_x = 600
    char_y = 700
    boss_x = 1100
    boss_y = 750

print(f"Baslangic cozunurluk: {constants.screenWidth}x{constants.screenHeight}")
print(f"Baslangic konumlari: Karakter({char_x}, {char_y}), Boss({boss_x}, {boss_y})")

# Oyuncu
player = Character(constants.CHAR_X, constants.CHAR_Y, 96, 84, constants.screenWidth, constants.screenHeight, 0)
player.set_sfx_manager(sfx_manager)

# Boss
boss = Boss(constants.BOSS_START_X, constants.BOSS_START_Y, player, sfx_manager)
# Boss'un başlangıçta sola bakmasını sağla
boss.flip = True

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

# Intro değişkenleri
intro_active = False
intro_start_time = 0
intro_duration = 15000  # 15 saniye (ms cinsinden)

# Skip butonu için değişkenler
skip_button_rect = pygame.Rect(0, 0, 100, 40)  # Başlangıçta boş, daha sonra konumlandırılacak

def redrawGameWindow():
    bg.update()
    bg.draw(win)
    # win.blit(bg, (0, 0))

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

    # Parry kontrolü
    if boss.check_parry(player):
        # Başarılı parry durumunda hasar verilmez
        pass
    elif (boss.action.startswith("attack") or boss.action == "jump_attack"):
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

                    # Eğer parry sırasında hasar alındıysa parry_hit fonksiyonunu çağır
                    if player.is_parrying:
                        player.parry_hit()
                    else:
                        player.play_hurt_animation()
                        for _ in range(3):
                            impact_frame(win, alpha=100)

    # player ve boss'u harita sınırlarında ve zeminde tut
    if player.rect.bottom < constants.screenHeight // 2:
        player.y = constants.screenHeight // 2 - player.height
    if player.rect.left < 0:
        player.x = 0
    elif player.rect.bottom > constants.screenHeight:
        player.y = constants.screenHeight - player.height
    if player.rect.right > constants.screenWidth:
        player.x = constants.screenWidth - player.width

    if boss.rect.bottom < constants.screenHeight // 2:
        boss.y = boss.y
    elif boss.rect.bottom > constants.screenHeight:
        boss.y = boss.y
    if boss.rect.left < 0:
        boss.x = 0
    if boss.rect.right > constants.screenWidth:
        boss.x = constants.screenWidth - boss.original_width

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
                intro_active = True
                intro_start_time = pygame.time.get_ticks()
                # Arkaplan intro modunu aktifleştir
                bg.set_intro_active(True)
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
                is_fullscreen = False
                if result[1] == "fullscreen":
                    # Tam ekran modu
                    win = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
                    # Ekran boyutlarını al
                    display_info = pygame.display.Info()
                    constants.screenWidth = display_info.current_w
                    constants.screenHeight = display_info.current_h
                    is_fullscreen = True
                else:
                    # Normal pencere modu
                    new_width, new_height = result[1]
                    win = pygame.display.set_mode((new_width, new_height))
                    constants.screenWidth = new_width
                    constants.screenHeight = new_height


                player.x = 0.4*constants.screenWidth
                player.y = 0.6*constants.screenHeight
                boss.x = 0.6*constants.screenWidth
                boss.y = 0.55*constants.screenHeight
                player.rect.width = 96 * (constants.screenWidth / 1920)
                player.rect.height = 86 * (constants.screenHeight / 1080)
                boss.rect.width = 144 * (constants.screenWidth / 1920)
                boss.rect.height = 124 * (constants.screenHeight / 1080)



                # Çözünürlük değişiminde konumları sabit değerlerle ayarla


                print(f"Yeni çözünürlük: {constants.screenWidth}x{constants.screenHeight}")
                print(f"Boss un boyutu: {boss.rect.width}x{boss.rect.height}")
                print(f"MC nin boyutu: {player.rect.width}x{player.rect.height}")


                # Arkaplanı yeniden oluştur
                bg = SamuraiBackground(constants.screenWidth, constants.screenHeight)
                # Menü boyutlarını güncelle
                menu = Menu(constants.screenWidth, constants.screenHeight)
        elif game_paused:
            # Pause menü olaylarını işle
            playeroranx = player.x/constants.screenWidth
            playerorany = player.y/constants.screenHeight
            bossoranx = boss.x/constants.screenWidth
            bossorany = boss.y/constants.screenHeight
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
                # Mevcut çözünürlüğe göre konumları ayarla
                player.x = 0.4 * constants.screenWidth
                player.y = 0.6 * constants.screenHeight
                boss.x = 0.6 * constants.screenWidth
                boss.y = 0.55 * constants.screenHeight

                print(f"Oyun yeniden başlatıldı. Çözünürlük: {constants.screenWidth}x{constants.screenHeight}")
                print(f"Boss konumu: x={boss.x}, y={boss.y}")
                game_paused = False
            elif isinstance(result, tuple) and result[0] == "resolution":
                # Çözünürlük değiştirme - pause menüsünden
                is_fullscreen = False
                if result[1] == "fullscreen":
                    # Tam ekran modu
                    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    # Ekran boyutlarını al
                    display_info = pygame.display.Info()
                    constants.screenWidth = display_info.current_w
                    constants.screenHeight = display_info.current_h
                    is_fullscreen = True
                else:
                    # Normal pencere modu
                    new_width, new_height = result[1]
                    win = pygame.display.set_mode((new_width, new_height))
                    constants.screenWidth = new_width
                    constants.screenHeight = new_height
                player.rect.width = 96*(constants.screenWidth/1920)
                player.rect.height = 86*(constants.screenHeight/1080)
                boss.rect.width = 144*(constants.screenWidth/1920)
                boss.rect.height = 124*(constants.screenHeight/1080)
                player.x = playeroranx * constants.screenWidth
                player.y = playerorany * constants.screenHeight
                boss.x = bossoranx * constants.screenWidth
                boss.y = bossorany * constants.screenHeight


                # Çözünürlük değişiminde konumları sabit değerlerle ayarla


                print(f"Pause menüsünden yeni çözünürlük: {constants.screenWidth}x{constants.screenHeight}")
                print(f"Boss konumu: x={boss.x}, y={boss.y}")

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
                # Intro sırasında skip butonuna tıklandı mı kontrol et
                if intro_active and hasattr(redrawGameWindow, "skip_button") and redrawGameWindow.skip_button.rect.collidepoint(event.pos):
                    # Skip ses efekti
                    sfx_manager.play_sound("skip")

                    # Intro'yu atla
                    intro_active = False
                    bg.set_intro_active(False)

                    # Müziği 14. saniyeye atla
                    try:
                        # Müziği durdur ve yeniden başlat (14. saniyeden)
                        current_music = sfx_manager.current_music
                        sfx_manager.stop_music()
                        sfx_manager.play_music(current_music)
                        sfx_manager.set_music_position(14.8)
                    except Exception as e:
                        print(f"Müzik atlama hatası: {e}")
                else:
                    sfx_manager.play_sound("attack1")

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
        menu_rects = menu.draw(win, constants, sfx_manager)
        pygame.display.update()
        continue

    # Intro kontrolü
    current_time = pygame.time.get_ticks()
    if intro_active:
        # Intro süresi doldu mu kontrol et
        if current_time - intro_start_time > intro_duration:
            intro_active = False
            # Arkaplan intro modunu devre dışı bırak
            bg.set_intro_active(False)
        else:
            # Intro sırasında karakterler hareket edemez
            # Sadece arkaplan ve intro metni gösterilir
            redrawGameWindow()

            # Intro metni
            font_large = pygame.font.Font(constants.FONT_PATH, 72)
            intro_text = font_large.render("SAMURAI FIGHT", True, constants.WHITE)
            win.blit(intro_text, (constants.screenWidth // 2 - intro_text.get_width() // 2, constants.screenHeight // 3))

            # Kalan süre
            remaining_time = (intro_duration - (current_time - intro_start_time)) // 1000
            if remaining_time > 0:
                time_text = font.render(f"Battle begins in {remaining_time}...", True, constants.WHITE)
                win.blit(time_text, (constants.screenWidth // 2 - time_text.get_width() // 2, constants.screenHeight // 2))

            # SKIP butonu
            skip_font = pygame.font.Font(constants.FONT_PATH, 24)

            # Buton konumu - sağ alt köşe
            skip_button_x = constants.screenWidth - 100 - 20  # Yaklaşık buton genişliği ve kenar boşluğu
            skip_button_y = constants.screenHeight - 40 - 20  # Yaklaşık buton yüksekliği ve kenar boşluğu

            # Skip butonunu oluştur (eğer henüz oluşturulmadıysa)
            if not hasattr(redrawGameWindow, "skip_button"):
                redrawGameWindow.skip_button = Button(
                    text="SKIP",
                    font=skip_font,
                    position=(skip_button_x, skip_button_y),
                    text_color=constants.WHITE,
                    hover_color=constants.WHITE,
                    selected_color=constants.WHITE
                )

            # Buton arka planı
            pygame.draw.rect(win, (50, 50, 50), redrawGameWindow.skip_button.rect)
            pygame.draw.rect(win, constants.WHITE, redrawGameWindow.skip_button.rect, 2)  # Beyaz çerçeve

            # Mouse tıklamasını kontrol et
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]  # Sol tık

            # Butonu güncelle ve çiz
            hover = redrawGameWindow.skip_button.update(mouse_pos, sfx_manager)
            redrawGameWindow.skip_button.draw(win)

            # Buton dikdörtgenini güncelle (event handling için)
            skip_button_rect = redrawGameWindow.skip_button.rect

            # Tıklama kontrolü
            if hover and mouse_clicked:
                # Skip ses efekti
                sfx_manager.play_sound("skip")

                # Intro'yu atla
                intro_active = False
                bg.set_intro_active(False)

                # Müziği 14. saniyeye atla
                try:
                    # Müziği durdur ve yeniden başlat (14. saniyeden)
                    current_music = sfx_manager.current_music
                    sfx_manager.stop_music()
                    sfx_manager.play_music(current_music)
                    sfx_manager.set_music_position(14.8)
                except Exception as e:
                    print(f"Müzik atlama hatası: {e}")

            pygame.display.update()
            continue

    keys = pygame.key.get_pressed()
    clicks = pygame.mouse.get_pressed()
    if not player.is_healing:
        player.move(keys, clicks)

    # Intro sırasında boss hareket etmez
    if not intro_active:
        # Player'ın boss içerisine girmesini engelle
        boss.collision_with_player(player)

        # Boss'un hareketleri ve saldırıları
        boss.update(player)

    # V tuşuna basıldığında shuriken fırlat
    if keys[pygame.K_v]:
        player.throw_shuriken(bullets, Projectile)


    redrawGameWindow()

pygame.quit()