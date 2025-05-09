import pygame
import os
from character import Player
import constants
from weapon import Weapon

pygame.init()

constants.screenWidth = 800
constants.screenHeight = 600

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






#######
# Define necessary functions
#######
game_active = False

font = pygame.font.SysFont("comicsans", 30)

def draw_start_button():
    btn_rect = pygame.Rect(constants.screenWidth//2 - 100, constants.screenHeight//2 - 25, 200,50)
    pygame.draw.rect(win, (0, 200, 0), btn_rect)
    text = font.render("Start", True, (255, 255, 255))
    win.blit(text, (btn_rect.x + 50, btn_rect.y + 4))
    return btn_rect

# draw_health_bar is now imported from character.py


# Load background image
bg = pygame.image.load(os.path.join("pygame_hack&slash","assets", "PixelArtForest", "Preview", "Background.png"))


def update():
    #win.fill((0,0,0)) # this will fill the screen with black color
    win.blit(bg, (0, 0))

    # Draw the player character
    Character.draw(win, font)
    Character.update()
    axe.draw(win)
    axe.update(Character)


    # Bullets
    for bullet in bullets:
        # Move the bullet based on its facing direction
        bullet.x += (bullet.vel * bullet.facing)

        # Remove bullets that go off-screen
        if bullet.x > constants.screenWidth or bullet.x < 0:
            bullets.pop(bullets.index(bullet))
        else:
            bullet.draw(win)


    pygame.display.update()


###
# Projectile class
###
class Projectile(object):
    def __init__(self, x, y, width, height, facing, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.facing = facing  # 1 for right, -1 for left
        self.frameCount = 0
        self.sprites = enemyFly

    def draw(self, win):
        if self.frameCount >= len(self.sprites):
            self.frameCount = 0

        current_sprite = self.sprites[self.frameCount]

        # If facing left, flip the sprite
        if self.facing == 1:
            current_sprite = pygame.transform.flip(current_sprite, True, False)

        win.blit(current_sprite, (self.x, self.y))

        # Update the frame count for animation
        self.frameCount = (self.frameCount + 1) % len(self.sprites)


#create clock for maintaning frame rate
clock = pygame.time.Clock()



#####################################################################################
# this is the main loop of the game
#####################################################################################
Character = Player(constants.screenWidth//2, constants.screenHeight//2, 96, 84, constants.screenWidth, constants.screenHeight,mob_animations, 0)

axe = Weapon(weapon_image)
bullets = []
run = True
while run:
    #control frame rate
    clock.tick(constants.FPS)

    # events means keyboard click or mouse movements or even keyboard movements
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            run = False
        if not game_active and event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            if draw_start_button().collidepoint(mousePos):
                game_active = True
        

    if not game_active:
        win.fill((0, 0, 0))
        draw_start_button()
        pygame.display.update()
        continue

    # Game over text is now handled in Character.draw()



    keys = pygame.key.get_pressed()
    Character.move(keys)

    # Shoot projectiles (limited to 5 at a time)
    if keys[pygame.K_v] and len(bullets) < 5:
        # Determine facing direction based on player state
        facing = -1 if Character.leftIdle or Character.left else 1

        # Get sprite dimensions (using the first enemyFly sprite)
        sprite_width = enemyFly[0].get_width()
        sprite_height = enemyFly[0].get_height()

        # Create a new projectile at front of the player
        # remember player location is on the top left of sprite sheet
        if facing == 1:
            bullet_x = Character.x + Character.width
        else:
            bullet_x = Character.x - sprite_width

        bullet_y = Character.y + Character.height // 2 - sprite_height // 2

        bullets.append(Projectile(bullet_x, bullet_y, sprite_width, sprite_height, facing, 10))

    

    # Add a small delay when taking damage with space key
    if keys[pygame.K_SPACE] and Character.health > 0:
        pygame.time.delay(100)



    update()


pygame.quit()