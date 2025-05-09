import pygame
import os
from character import Player, enemyFly
from boss import Boss
import constants
from weapon import Weapon

pygame.init()

win = pygame.display.set_mode((constants.screenWidth, constants.screenHeight))
pygame.display.set_caption("First")


# Sprite loading functions
def load_sprite_sheet(sheet_path, sprite_width, sprite_height, num_sprites):
    sheet = pygame.image.load(sheet_path)
    frames = []
    for i in range(num_sprites):
        frame = sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
        frames.append(frame)
    return frames

def load_individual_sprites(directory_path):
    frames = []

    try:
        # Get all files in the directory
        files = os.listdir(directory_path)
        # Filter for PNG files and sort them
        png_files = sorted([f for f in files if f.lower().endswith('.png')])

        for file_name in png_files:
            file_path = os.path.join(directory_path, file_name)
            frame = pygame.image.load(file_path)
            frames.append(frame)
    except Exception as e:
        print(f"Error loading sprites from {directory_path}: {e}")

    return frames

# Load weapon image
weapon_image =  pygame.image.load(os.path.join("pygame_hack&slash","assets","Roguelike Dungeon - Asset Bundle", "Items","Axe","Axe_0.png"))


# Load animation frames
walkRight = load_individual_sprites(os.path.join("pygame_hack&slash" ,"assets","Roguelike Dungeon - Asset Bundle","Sprites","Player", "Axe","Defence0","Walk"))
charIdle = load_individual_sprites(os.path.join("pygame_hack&slash" ,"assets","Roguelike Dungeon - Asset Bundle","Sprites","Player", "Axe","Defence0","Idle"))
walkRight = [pygame.transform.scale(frame, (frame.get_width() * constants.scale, frame.get_height() * constants.scale)) for frame in walkRight]
charIdle = [pygame.transform.scale(frame, (frame.get_width() * constants.scale, frame.get_height() * constants.scale)) for frame in charIdle]

# Load enemy sprites
enemyFly = load_individual_sprites(os.path.join("pygame_hack&slash","assets", "Knight", "Sprites", "EnemyFly"))

dungeonMasterWalk = load_individual_sprites(os.path.join("pygame_hack&slash","assets", "Roguelike Dungeon - Asset Bundle", "Sprites", "Bosses", "Dungeon Master","Walk"))


mob_types = ["knight", "flyEye"]
animation_types = ["idle", "walk"]
animation_list = [charIdle, walkRight] # for player
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


def redrawGameWindow():
    #win.fill((0,0,0)) # this will fill the screen with black color
    win.blit(bg, (0, 0))

    # Draw the player character
    Character.draw(win, font)
    

    # Bullets
    for bullet in bullets:
        # Move the bullet based on its facing direction
        bullet.x += (bullet.vel * bullet.facing)

        # Remove bullets that go off-screen
        if bullet.x > screenWidth or bullet.x < 0:
            bullets.pop(bullets.index(bullet))
        else:
            bullet.draw(win)

    pygame.display.update()


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

        current_sprite = self.sprites[self.frameCount]

        # If facing left, flip the sprite
        if self.facing == 1:
            sprite = pygame.transform.flip(sprite, True, False)
        win.blit(sprite, (self.x, self.y))
        self.frameCount = (self.frameCount + 1) % len(self.sprites)

clock = pygame.time.Clock()



#####################################################################################
# this is the main loop of the game
#####################################################################################
Character = Player(constants.screenWidth//2, constants.screenHeight//2, 96, 84, constants.screenWidth, constants.screenHeight,mob_animations, 0)

axe = Weapon(weapon_image)
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
