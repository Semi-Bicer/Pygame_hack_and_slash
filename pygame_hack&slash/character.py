import pygame
import os
import math
import constants

def draw_health_bar(surface, x, y, health, maxHealth):
    barWidth = 100
    barHeight = 10
    fill = (health / maxHealth) * barWidth
    border_rect = pygame.Rect(x, y - 20, barWidth, barHeight)
    fill_rect = pygame.Rect(x, y - 20, fill, barHeight)
    pygame.draw.rect(surface, (255, 0, 0), fill_rect)
    pygame.draw.rect(surface, (255, 255, 255), border_rect, 2)

class Character(object):
    def __init__(self, x, y, width, height, screenWidth, screenHeight, mob_animations, char_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.center = (self.x + self.width / 2 , self.y + self.height / 2)
        self.vel = constants.CHAR_SPEED
        self.dashVel = constants.CHAR_DASH_SPEED
        self.health = constants.CHAR_HEALTH
        self.maxHealth = constants.CHAR_MAX_HEALTH
        self.isDashing = False
        self.dashMultiplier = constants.CHAR_DASH_MULTIPLIER
        # Animation
        # rotation of the player
        self.char_type = char_type
        self.animation_list = mob_animations[char_type] # walkLeft, walkRight, charIdle, flipCharIdle
        # to know how much time passed since last time udpated frame
        self.last_update = pygame.time.get_ticks()
        self.flip = False
        self.frame_index = 0
        self.action = 0 #0 idle , 1 run
        self.walking = False
        self.image = self.animation_list[self.action][self.frame_index] # charIdle
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.leftIdle = False
        self.walkCount = 0
        self.idleCount = 0
        
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.horizontal = 0
        self.vertical = 0

    def move(self, keys):
        self.walking = False
        # horizontal boolean
        self.horizontal = int (keys[pygame.K_d]) - int (keys[pygame.K_a])
        #vertical boolean
        self.vertical = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        if abs(self.horizontal) or abs(self.vertical): # if moving
            self.walking = True
        if abs(self.horizontal) and abs(self.vertical): # if moving diagonally
            self.x += self.horizontal * self.vel/math.sqrt(2)
            self.y += self.vertical * self.vel /math.sqrt(2)
        else:
            self.x += self.horizontal * self.vel
            self.y += self.vertical * self.vel


        if keys[pygame.K_a] and self.x > self.vel:  # left
            self.left = True
            self.leftIdle = True
            self.flip = True

        elif keys[pygame.K_d] and self.x < (self.screenWidth - self.width - self.vel):  # right
            self.left = False
            self.leftIdle = False
            self.flip = False
        else:  # start the idle animation
            if self.left:
                self.leftIdle = True
                self.rightIdle = False
                self.flip = True
            else:
                self.rightIdle = True
                self.leftIdle = False
                self.flip = False
            
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
            
        
        
    def update(self):
        self.rect.center = (self.x + self.width / 2 , self.y + self.height / 2)
        # checking action
        if self.walking:
            self.update_action(1)
        else:
            self.update_action(0)
        # animation delay
        animation_cooldown = constants.CHAR_ANIM_COOLDOWN_MS
        # update player
        if self.frame_index + 1 >= len(self.animation_list[1]):
            self.frame_index = 0
        if abs(self.horizontal) or abs(self.vertical):
            if self.left:                
                self.image = self.animation_list[1][self.frame_index] 
                if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
                    self.last_update = pygame.time.get_ticks()
                    self.frame_index = (self.frame_index + 1) % len(self.animation_list[1])
            else:
                self.image = self.animation_list[1][self.frame_index]
                if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
                    self.last_update = pygame.time.get_ticks()
                    self.frame_index = (self.frame_index + 1) % len(self.animation_list[1])
        else:

            if self.leftIdle:
                self.image = self.animation_list[0][self.frame_index]
                if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
                    self.last_update = pygame.time.get_ticks()
                    self.frame_index = (self.frame_index + 1) % len(self.animation_list[0])
            else:
                self.image = self.animation_list[0][self.frame_index]
                if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
                    self.last_update = pygame.time.get_ticks()
                    self.frame_index = (self.frame_index + 1) % len(self.animation_list[0])

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()

    def draw(self, win, font):
        pygame.draw.rect(win, constants.RED, self.rect, 1)
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if(self.char_type == 0):
            win.blit(flipped_image, (self.rect.x - constants.scale *constants.OFFSET_X, self.rect.y - constants.scale *constants.OFFSET_Y))
        else:
            win.blit(flipped_image, self.rect)
        # health bar
        draw_health_bar(win, self.x, self.y, self.health, self.maxHealth)

        # Draw game over text if health is depleted
        if self.health <= 0:
            gameOverText = font.render("GAME OVER", True, (255, 255, 255))
            win.blit(gameOverText, ((self.screenWidth // 2 - gameOverText.get_width() // 2), 300))