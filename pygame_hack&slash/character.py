import pygame
import os
import math
from functions import *

# Load animation frames
walkRight = load_sprite_sheet(os.path.join("assets","Knight","Sprites","without_outline", "WALK.png"), 96, 80, 8)
walkLeft = [pygame.transform.flip(frame, True, False) for frame in walkRight]
charIdle = load_sprite_sheet(os.path.join("assets","Knight","Sprites","without_outline", "IDLE.png"), 96, 80, 7)
flipCharIdle = [pygame.transform.flip(frame, True, False) for frame in charIdle]

# Load enemy sprites
enemyFly = load_individual_sprites(os.path.join("assets", "Knight", "Sprites", "EnemyFly"))

def draw_health_bar(surface, x, y, health, maxHealth):
    barWidth = 100
    barHeight = 10
    fill = (health / maxHealth) * barWidth
    border_rect = pygame.Rect(x, y - 20, barWidth, barHeight)
    fill_rect = pygame.Rect(x, y - 20, fill, barHeight)
    pygame.draw.rect(surface, (255, 0, 0), fill_rect)
    pygame.draw.rect(surface, (255, 255, 255), border_rect, 2)

class Player(object):
    def __init__(self, x, y, width, height, screenWidth, screenHeight):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.dashVel = 15.0
        self.health = 100
        self.maxHealth = 100
        self.isDashing = False
        self.dashMultiplier = 10
        # rotation of the player
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.leftIdle = False
        self.rightIdle = False
        self.walkCount = 0
        self.idleCount = 0
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.horizontal = 0
        self.vertical = 0

    def move(self, keys):
        # horizontal boolean
        self.horizontal = int (keys[pygame.K_d]) - int (keys[pygame.K_a])
        #vertical boolean
        self.vertical = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if abs(self.horizontal) and abs(self.vertical):
            self.x += self.horizontal * self.vel/math.sqrt(2)
            self.y += self.vertical * self.vel /math.sqrt(2)
        else:
            self.x += self.horizontal * self.vel
            self.y += self.vertical * self.vel


        if keys[pygame.K_a] and self.x > self.vel:  # left
            self.left = True
            self.leftIdle = True

        elif keys[pygame.K_d] and self.x < (self.screenWidth - self.width - self.vel):  # right
            self.left = False
            self.leftIdle = False
        else:  # start the idle animation
            if self.left:
                self.leftIdle = True
                self.rightIdle = False
            else:
                self.rightIdle = True
                self.leftIdle = False
            
            self.walkCount = 0

        if keys[pygame.K_w] and self.y > self.vel:  # up
            self.up = True

        else:
            self.up = False

        if keys[pygame.K_s] and self.y < (self.screenHeight - self.height - self.vel):  # down
            self.down = True

        else:
            self.down = False

        # Dash movement
        if keys[pygame.K_LSHIFT]: 
            self.isDashing = True
            self.left = False
            self.walkCount = 0

        # Apply dash if active
        if self.isDashing:
            if keys[pygame.K_a]:
                self.x -= self.dashVel
            if keys[pygame.K_d]:
                self.x += self.dashVel
            if keys[pygame.K_w]:
                self.y -= self.dashVel
            if keys[pygame.K_s]:
                self.y += self.dashVel
            self.isDashing = False


        # Take damage with space key
        if keys[pygame.K_SPACE] and self.health > 0:
            self.health -= 10
            

    def draw(self, win, font):
        # draw the player
        if self.walkCount + 1 >= len(walkRight):
            self.walkCount = 0
        if self.idleCount + 1 >= len(charIdle):
            self.idleCount = 0
        if abs(self.horizontal) or abs(self.vertical):
            if self.left:
                win.blit(walkLeft[self.walkCount], (self.x, self.y))
                self.walkCount = (self.walkCount + 1) % len(walkLeft)
            else:
                win.blit(walkRight[self.walkCount], (self.x, self.y))
                self.walkCount = (self.walkCount + 1) % len(walkRight)
        else:
            
            if self.leftIdle:
                win.blit(flipCharIdle[self.idleCount], (self.x, self.y))
                self.idleCount = (self.idleCount + 1) % len(flipCharIdle)
            else:
                win.blit(charIdle[self.idleCount], (self.x, self.y))
                self.idleCount = (self.idleCount + 1) % len(charIdle)

        # health bar
        draw_health_bar(win, self.x, self.y, self.health, self.maxHealth)

        # Draw game over text if health is depleted
        if self.health <= 0:
            gameOverText = font.render("GAME OVER", True, (255, 255, 255))
            win.blit(gameOverText, ((self.screenWidth // 2 - gameOverText.get_width() // 2), 300))