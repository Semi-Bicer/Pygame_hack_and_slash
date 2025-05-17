### firstGame.py
import pygame
import constants
from character import Character
from boss import Boss
from functions import *
from Background import SamuraiBackground
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

# Fontlar
fonts = {
    "small": pygame.font.Font(None, 24),
    "medium": pygame.font.Font(None, 36),
    "large": pygame.font.Font(None, 72)
}

# Oyun Değişkenleri
clock = pygame.time.Clock()
run = True
game_active = False
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Sol tık
                if game_active:
                    sfx_manager.play_sound("attack1")
                elif start_button and start_button.collidepoint(pygame.mouse.get_pos()):
                    # Start butonuna tıklandı mı kontrol et
                    game_active = True
                    sfx_manager.stop_music(fade_ms=500)
                    sfx_manager.play_music("battle", fade_ms=1000)

    if not game_active:
        # Start menüsünü çiz ve buton rect'ini al
        start_button = draw_start_menu(win, constants, fonts)
        pygame.display.update()
        continue

    keys = pygame.key.get_pressed()
    clicks = pygame.mouse.get_pressed()

    # Ölüm durumunda R tuşu ile oyunu yeniden başlat
    if player.death_animation_finished and keys[pygame.K_r]:
        # Oyunu yeniden başlat
        player = Character(constants.CHAR_X, constants.CHAR_Y, 96, 84, constants.screenWidth, constants.screenHeight, 0)
        player.set_sfx_manager(sfx_manager)
        boss = Boss(constants.BOSS_START_X, constants.BOSS_START_Y - 50, player, sfx_manager)
        bullets = []
        continue

    player.move(keys, clicks)

    # Player'ın boss içerisine girmesini engelle
    boss.collision_with_player(player)

    # V tuşuna basıldığında shuriken fırlat
    if keys[pygame.K_v]:
        player.throw_shuriken(bullets, Projectile)


    redrawGameWindow()

pygame.quit()