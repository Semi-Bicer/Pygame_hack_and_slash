import pygame
import os


pygame.init()

screenWidth = 800
screenHeight = 600

win = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("First")

# player variables
x = 200
y = 150
width = 10 
height = 10
vel = 20
dashVel = 40
health = 100
maxHealth = 100
## rotation of the player
left = False
right = False
leftIdle = False
rightIdle = False
walkCount = 0
idleCount = 0

game_active = False

font = pygame.font.SysFont("comicsans", 30)

def draw_start_button():
    btn_rect = pygame.Rect(screenWidth//2 - 100, screenHeight//2 - 25, 200,50)
    pygame.draw.rect(win, (0, 200, 0), btn_rect)
    text = font.render("Start", True, (255, 255, 255))
    win.blit(text, (btn_rect.x + 50, btn_rect.y + 4))
    return btn_rect

def draw_health_bar(surface, x ,y,health, maxHealth ):
    barWidth = 100
    barHeight = 10
    fill = (health / maxHealth) * barWidth
    border_rect = pygame.Rect(x, y -20, barWidth, barHeight)
    fill_rect = pygame.Rect(x, y -20, fill, barHeight)
    pygame.draw.rect(surface, (255, 0, 0), fill_rect)
    pygame.draw.rect(surface, (255, 255, 255), border_rect, 2)


def load_sprite_sheet(sheet_path, sprite_width, sprite_height, num_sprites):
    sheet = pygame.image.load(sheet_path)
    frames = []
    for i in range(num_sprites):
        frame = sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
        frames.append(frame)
    return frames

# laod animation frames
walkRight = load_sprite_sheet(os.path.join("assets","Knight","Sprites","without_outline", "WALK.png"), 96, 80, 8) # load the sprite sheet and get the frames
walkLeft = [pygame.transform.flip(frame, True, False) for frame in walkRight] # flip the image to make it look like left
charIdle = load_sprite_sheet(os.path.join("assets","Knight","Sprites","without_outline", "IDLE.png"), 96, 80, 7) 
flipCharIdle = [pygame.transform.flip(frame, True, False) for frame in charIdle] # bunu ekleme sebebimiz normal idle animasyonunda karakter sağa bakıyor ama solda bakması lazım o yüzden bunu ekledik
bg = pygame.image.load(os.path.join("assets", "PixelArtForest", "Preview", "Background.png"))

isDashing = False
dashMultiplier = 10

def redrawGameWindow():
    global walkCount
    global idleCount
    #win.fill((0,0,0)) # this will fill the screen with black color
    win.blit(bg, (0, 0))
    # draw the player
    if walkCount + 1 >= len(walkRight):
        walkCount = 0
    if idleCount + 1 >= len(charIdle):
        idleCount = 0
    if left:
        win.blit(walkLeft[walkCount], (x, y))
        walkCount = (walkCount + 1) % len(walkLeft)
    elif right:
        win.blit(walkRight[walkCount], (x, y))
        walkCount = (walkCount + 1) % len(walkRight)
    else:
        if leftIdle:
            win.blit(flipCharIdle[idleCount], (x, y))
            idleCount = (idleCount + 1) % len(flipCharIdle)
        else:
            win.blit(charIdle[idleCount], (x, y))
            idleCount = (idleCount + 1) % len(charIdle)


    draw_health_bar(win, x, y, health, maxHealth)

    if health <= 0:
        gameOverText = font.render("GAME OVER", True, (255, 255, 255))
        win.blit(gameOverText, ((screenWidth // 2 -gameOverText.get_width() // 2) , 300))

    
    pygame.display.update()

#main loop
run = True 
while run:
    pygame.time.delay(100)
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



    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a] and x > vel: # left
        x -= vel
        left = True
        right = False
    elif keys[pygame.K_d] and x < (screenWidth - width -vel) : # right
        x += vel
        right = True
        left = False
    else:
        if left == True:
            leftIdle = True
            rightIdle = False
        if right == True:
            rightIdle = True
            leftIdle = False
        left = False
        right = False
        walkCount = 0
    #else:
        # start the idle animation

    if keys[pygame.K_w] and y > vel: # up
        y -= vel 
    if keys[pygame.K_s] and y < (screenHeight - height -vel): # down
        y += vel
    if keys[pygame.K_LSHIFT]: # our game will be top-down so no need for restriction during dash
        isDashing = True
        print("dashed")
        left = False
        right = False
        walkCount = 0


    if (isDashing):
        if keys[pygame.K_a]:
            x -= dashVel
        if keys[pygame.K_d]:
            x += dashVel
        if keys[pygame.K_w]:
            y -= dashVel
        if keys[pygame.K_s]:
            y += dashVel
        isDashing = False

    if keys[pygame.K_SPACE] and health > 0:
            health -= 10
            pygame.time.delay(100)



    redrawGameWindow()

    
pygame.quit()