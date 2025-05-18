import pygame
import os
import math
import constants
from functions import *

class Character(object):
    @staticmethod
    def load_animations():
        assets_path = os.path.join("assets", "Player", "Sprites")
        # Animasyonları yükle
        charIdle = load_and_scale_sheet(os.path.join(assets_path, "IDLE.png"), 96, 84, 10)
        walkRight = load_and_scale_sheet(os.path.join(assets_path, "WALK.png"), 96, 84, 12)
        runRight = load_and_scale_sheet(os.path.join(assets_path, "RUN.png"), 96, 84, 16)
        dash = load_and_scale_sheet(os.path.join(assets_path, "DASH.png"), 95, 84, 8)
        attack1 = load_and_scale_sheet(os.path.join(assets_path, "ATTACK 1.png"), 96, 84, 6)
        attack2 = load_and_scale_sheet(os.path.join(assets_path, "ATTACK 2.png"), 96, 84, 6)
        attack3 = load_and_scale_sheet(os.path.join(assets_path, "ATTACK 3.png"), 96, 84, 6)

        # Zincirleme saldırı için attack1, attack2 ve attack3'ü birleştir
        combo_attack = []
        combo_attack.extend(attack1)
        combo_attack.extend(attack2)
        combo_attack.extend(attack3)

        # Air attack animasyonu
        air_attack = load_and_scale_sheet(os.path.join(assets_path, "AIR ATTACK.png"), 96, 84, 6)

        throw = load_and_scale_sheet(os.path.join(assets_path, "THROW.png"), 96, 84, 7)

        # Animasyon listelerini oluştur
        # 0: idle, 1: walk, 2: run, 3: dash, 4: combo_attack, 5: throw, 6: air_attack
        animation_list = [charIdle, walkRight, runRight, dash, combo_attack, throw, air_attack]
        return animation_list

    @staticmethod
    def load_shuriken():
        assets_path = os.path.join("assets", "Player")
        shuriken = load_single_image(os.path.join(assets_path, "shuriken.png"), constants.scale)
        return shuriken


    def __init__(self, x, y, width, height, screenWidth, screenHeight, char_type=0):
        # Pozisyon ve boyutlar
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.center = (self.x + self.width / 2, self.y + self.height / 2)
        # Hareket ve hız
        self.vel = constants.CHAR_SPEED
        self.dashMultiplier = constants.CHAR_DASH_MULTIPLIER
        self.dashVel = constants.CHAR_DASH_SPEED * self.dashMultiplier
        self.isDashing = False
        self.running = False  # Koşma durumu
        self.dash_start_time = 0
        self.last_dash_time = 0
        self.dash_cooldown = constants.CHAR_DASH_COOLDOWN
        self.can_dash = True
        # Can ve sağlık
        self.health = constants.CHAR_HEALTH
        self.maxHealth = constants.CHAR_MAX_HEALTH
        # Saldırı
        self.is_attacking = False
        self.last_attack_time = 0
        self.attack_cooldown = constants.CHAR_ATTACK_COOLDOWN
        self.attack_frame_duration = constants.CHAR_ATTACK_FRAME_DURATION
        self.attack_damage = constants.CHAR_ATTACK_DAMAGE
        self.attack_frame = constants.CHAR_ATTACK_FRAME
        self.has_dealt_damage = False

        # Zincirleme saldırı
        self.combo_count = 0  # Kaç saldırı yapıldığını takip eder (0, 1, 2)
        self.combo_max = 3  # Maksimum zincirleme saldırı sayısı
        self.combo_window = 1000  # ms cinsinden zincirleme saldırı penceresi
        self.last_combo_time = 0  # Son zincirleme saldırı zamanı

        # Air attack
        self.is_air_attacking = False
        self.can_air_attack = False  # Dash sonrası air attack yapılabilir mi?
        self.air_attack_window = 500  # ms cinsinden dash sonrası air attack penceresi
        self.air_attack_damage = constants.CHAR_ATTACK_DAMAGE * 1.5  # Air attack daha güçlü
        self.air_attack_frame = 3  # Hangi frame'de hasar verilecek

        # Shuriken fırlatma
        self.is_throwing = False
        self.last_throw_time = 0
        self.throw_cooldown = 0  # 0.5 saniye cooldown
        self.throw_frame_duration = 70  # ms cinsinden fırlatma süresi
        self.throw_frame = 3  # Hangi frame'de shuriken fırlatılacak
        # Atak için çarpışma dikdörtgeni
        self.attack_rect = pygame.Rect(0, 0, 80, 80)  # Saldırı hitbox'ı - daha büyük yapıldı
        # Animasyon kontrol
        self.last_update = pygame.time.get_ticks()
        self.frame_index = 0
        self.flip = False

        # Yönelim
        self.horizontal = 0
        self.vertical = 0
        self.left = False

        # Ekran sınırları
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        # Karakter tipi (render offset vs.)
        self.char_type = char_type

        # Animasyonları yükle
        self.animation_list = self.load_animations()  # idle, walk, run, dash, attack, throw
        self.action = 0  # 0: idle, 1: walk, 2: run, 3: dash, 4: attack , 5: throw
        self.walking = False
        self.image = self.animation_list[self.action][self.frame_index]  # charIdle

        self.leftIdle = False

        # SFX yöneticisi (opsiyonel)
        self.sfx_manager = None

        # Shuriken referansını sakla
        self.shuriken = self.load_shuriken()[0]


    def set_sfx_manager(self, sfx_manager):
        self.sfx_manager = sfx_manager

    def throw_shuriken(self, bullets, Projectile):
        current_time = pygame.time.get_ticks()
        if self.is_throwing or current_time - self.last_throw_time < self.throw_cooldown:
            return False

        if len(bullets) >= 1:
            return False
        self.is_throwing = True
        self.last_throw_time = current_time
        self.frame_index = 0  # Animasyonu baştan başlat

        facing = -1 if self.leftIdle or self.left else 1

        if self.shuriken:
            w = self.shuriken.get_width()
            h = self.shuriken.get_height()
            bx = self.x + self.width if facing == 1 else self.x - w
            by = self.y + self.height // 2 - h // 2

            bullets.append(Projectile(bx, by, w, h, facing, 10, self.shuriken))
            return True
        else:
            print("Warning: shuriken sprite is not available.")
            return False

    def move(self, keys, clicks):
        self.walking = False

        self.horizontal = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.vertical   = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        if abs(self.horizontal) or abs(self.vertical): # if moving
            self.walking = True
        if abs(self.horizontal) and abs(self.vertical): # if moving diagonally
            self.x += self.horizontal * self.vel/math.sqrt(2)
            self.y += self.vertical * self.vel /math.sqrt(2)
        else:
            self.x += self.horizontal * self.vel
            self.y += self.vertical * self.vel

        # Character'in yönü
        if self.horizontal < 0:
            self.left = True
            self.flip = True
        elif self.horizontal > 0:
            self.left = False
            self.flip = False

        if keys[pygame.K_LSHIFT]:
            self.running = True
        else:
            self.running = False

        # Dash cooldown kontrolü
        current_time = pygame.time.get_ticks()
        if current_time - self.last_dash_time >= self.dash_cooldown:
            self.can_dash = True

        # Dash movement
        if keys[pygame.K_SPACE] and self.can_dash and not self.isDashing:
            self.isDashing = True
            self.can_dash = False
            self.last_dash_time = current_time # Cooldown için kullanılıyor
            self.dash_start_time = current_time # Dash süresi için kullanılıyor

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
            # Dash süresi kontrolü (dash_delay kadar sürer)
            if current_time - self.dash_start_time > constants.CHAR_DASH_DELAY:
                self.isDashing = False
                # Dash bittikten sonra air attack yapılabilir
                self.can_air_attack = True
                print("Air attack yapılabilir!")

        # Air attack penceresi kontrolü
        if self.can_air_attack and current_time - self.dash_start_time > self.air_attack_window:
            self.can_air_attack = False
            print("Air attack penceresi kapandı!")

        # Air attack (F tuşu ile)
        if clicks[2] and self.can_air_attack and not self.is_air_attacking and not self.is_attacking:
            self.is_air_attacking = True
            self.can_air_attack = False  # Bir kez kullanılabilir
            self.last_attack_time = current_time
            self.frame_index = 0  # Animasyonu baştan başlat
            self.has_dealt_damage = False
            print("Air attack başladı!")
            # Ses efekti
            if self.sfx_manager:
                self.sfx_manager.play_sound("attack1")

        # Normal saldırı (sol tık ile)
        if clicks[0]: # left mouse click
            current_time = pygame.time.get_ticks()

            # Eğer saldırı yapılmıyorsa ve cooldown geçtiyse
            if not self.is_attacking and not self.is_air_attacking and current_time - self.last_attack_time > self.attack_cooldown:
                self.is_attacking = True
                self.last_attack_time = current_time

                # Zincirleme saldırı kontrolü
                if current_time - self.last_combo_time < self.combo_window:
                    # Combo penceresi içinde, combo sayacını artır
                    self.combo_count = (self.combo_count + 1) % self.combo_max
                else:
                    # Combo penceresi dışında, combo sayacını sıfırla
                    self.combo_count = 0

                self.last_combo_time = current_time
                self.frame_index = 0  # Animasyonu baştan başlat
                self.has_dealt_damage = False




    def update(self):
        self.rect.center = (self.x + self.width / 2 , self.y + self.height / 2)
        # checking action
        if self.is_throwing:
            self.update_action(5)  # 5: throw animasyonu
        elif self.is_air_attacking:
            self.update_action(6)  # 6: air_attack animasyonu
        elif self.is_attacking:
            self.update_action(4)  # 4: combo_attack animasyonu
        elif self.isDashing:
            self.update_action(3)  # 3: dash animasyonu
        elif self.running:
            self.update_action(2)  # 2: run animasyonu
        elif self.walking:
            self.update_action(1)  # 1: walk animasyonu
        else:
            self.update_action(0)  # 0: idle animasyonu

        # Saldırı hitbox'ını karakterin yönüne göre güncelle
        if self.flip:
            # Sol tarafa saldırı
            self.attack_rect.midright = (self.rect.left - 10, self.rect.centery)
        else:
            # Sağ tarafa saldırı
            self.attack_rect.midleft = (self.rect.right + 10, self.rect.centery)

        # animation delay
        animation_cooldown = constants.CHAR_ANIM_COOLDOWN_MS

        if self.is_throwing:  # throw animation
            self.image = self.animation_list[5][self.frame_index]
            if pygame.time.get_ticks() - self.last_update >= self.throw_frame_duration:
                self.last_update = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.animation_list[5])

                if self.frame_index == 0:
                    self.is_throwing = False

        elif self.is_air_attacking:  # air attack animation
            self.image = self.animation_list[6][self.frame_index]
            if pygame.time.get_ticks() - self.last_update >= self.attack_frame_duration:
                self.last_update = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.animation_list[6])

                # Air attack hasar kontrolü
                if self.frame_index == self.air_attack_frame and not self.has_dealt_damage:
                    # has_dealt_damage değişkenini firstGame.py'de güncelleyeceğiz
                    # Burada sadece log mesajı yazdırıyoruz
                    print(f"Air attack hasar verme frame'i! Frame: {self.frame_index}")

                # Animasyon tamamlandığında
                if self.frame_index == 0:
                    self.is_air_attacking = False
                    print("Air attack tamamlandı!")

        elif self.is_attacking: # combo attack animation
            # Combo animasyonları için frame offset hesapla
            # Her bir saldırı animasyonu 7 frame, toplam 21 frame
            combo_offset = self.combo_count * 7

            # Toplam frame sayısı
            total_frames = len(self.animation_list[4])

            # Mevcut frame'i hesapla (combo offset + frame index)
            current_frame = (combo_offset + self.frame_index) % total_frames

            self.image = self.animation_list[4][current_frame]

            if pygame.time.get_ticks() - self.last_update >= self.attack_frame_duration:
                print(f"Combo {self.combo_count+1}, frame: {self.frame_index}, total: {current_frame}")
                self.last_update = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % 6  # Her bir saldırı 6 frame

                # Hasar verme frame'i kontrolü
                if self.frame_index == self.attack_frame and not self.has_dealt_damage:
                    # has_dealt_damage değişkenini firstGame.py'de güncelleyeceğiz
                    # Burada sadece log mesajı yazdırıyoruz
                    print(f"Combo {self.combo_count+1} hasar verme frame'i! Frame: {self.frame_index}")

                # Animasyon tamamlandığında
                if self.frame_index == 0:
                    self.is_attacking = False
                    print(f"Combo {self.combo_count} tamamlandı!")

        elif abs(self.horizontal) or abs(self.vertical): # walking/dashing animation
            if self.isDashing:
                # print("dashing")
                self.image = self.animation_list[3][self.frame_index]
                if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
                    self.last_update = pygame.time.get_ticks()
                    self.frame_index = (self.frame_index + 1) % len(self.animation_list[3])
            elif self.running:
                self.image = self.animation_list[2][self.frame_index]
                if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
                    self.last_update = pygame.time.get_ticks()
                    self.frame_index = (self.frame_index + 1) % len(self.animation_list[2])

            else:
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
        else: # idle animation
            #print("idle")
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

        # Saldırı süresi kontrolü
        if self.is_attacking and self.last_update - self.last_attack_time > self.attack_cooldown:
            self.is_attacking = False

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

        # Dash cooldown göstergesi
        current_time = pygame.time.get_ticks()
        if not self.can_dash:
            cooldown_remaining = self.dash_cooldown - (current_time - self.last_dash_time)
            if cooldown_remaining > 0:
                bar_x = self.x
                bar_y = self.y + self.height + 20
                bar_width = 100
                bar_height = 5
                fill_ratio = cooldown_remaining / self.dash_cooldown
                fill_width = bar_width * (1 - fill_ratio)  # Tersine çevrilmiş - cooldown azaldıkça bar dolar
                pygame.draw.rect(win, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))  # Gri arka plan
                pygame.draw.rect(win, (0, 150, 255), (bar_x, bar_y, fill_width, bar_height))  # Mavi doluluk


        # Game over text kaldırıldı - menu.py içinde yapılıyor

        # Saldırı hitbox'ını her zaman göster (debug için)
        if self.is_attacking or self.is_air_attacking:
            pygame.draw.rect(win, constants.RED, self.attack_rect, 2)