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
        hurt = load_and_scale_sheet(os.path.join(assets_path, "HURT.png"), 96, 84, 4)
        healing = load_and_scale_sheet(os.path.join(assets_path, "HEALING.png"), 96, 84, 15)
        defend = load_and_scale_sheet(os.path.join(assets_path, "DEFEND.png"), 96, 84, 6)
        combo_attack = []
        combo_attack.extend(attack1)
        combo_attack.extend(attack2)
        combo_attack.extend(attack3)
        air_attack = load_and_scale_sheet(os.path.join(assets_path, "AIR ATTACK.png"), 96, 84, 6)

        throw = load_and_scale_sheet(os.path.join(assets_path, "THROW.png"), 96, 84, 7)
        # 0: idle, 1: walk, 2: run, 3: dash, 4: combo_attack, 5: throw, 6: air_attack, 7: hurt, 8: healing, 9: defend
        animation_list = [charIdle, walkRight, runRight, dash, combo_attack, throw, air_attack, hurt, healing, defend]
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
        # Hurt ve healing animasyonları
        self.is_hurt = False
        self.hurt_duration = 500  # ms cinsinden hurt animasyonu süresi
        self.hurt_start_time = 0
        self.is_healing = False
        self.last_healing_time = 0
        self.healing_cooldown = constants.CHAR_HEALING_COOLDOWN
        self.healing_amount = constants.CHAR_HEALING_AMOUNT
        self.healing_frame_duration = 70  # ms cinsinden healing animasyonu süresi

        # Parry (savunma) mekanizması
        self.is_parrying = False
        self.parry_duration = 500  # 0.5 saniye parry süresi
        self.parry_cooldown = 1000  # 1 saniye cooldown
        self.last_parry_time = 0
        self.parry_start_time = 0
        self.parry_successful = False  # Başarılı parry durumu
        # Saldırı için hitbox
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

    def play_hurt_animation(self):
        if not self.is_hurt:
            self.is_hurt = True
            self.hurt_start_time = pygame.time.get_ticks()
            self.frame_index = 0

    def successful_parry(self):
        """Parry başarılı olduğunda çağrılır"""
        if self.is_parrying and self.frame_index == 0:  # Sadece parry'nin ilk frame'inde başarılı olabilir
            self.parry_successful = True
            if self.sfx_manager:
                self.sfx_manager.play_sound("parry")

    def parry_hit(self):
        """Parry sırasında hasar alındığında çağrılır"""
        if self.is_parrying:
            # Parry sırasında hasar alındığında tüm animasyonu oynat
            self.parry_successful = True
            if self.sfx_manager:
                self.sfx_manager.play_sound("parry")

    def start_healing(self):
        current_time = pygame.time.get_ticks()
        # Eğer healing cooldown süresi geçtiyse, healing animasyonu aktif değilse ve can maksimumdan düşükse
        if not self.is_healing and current_time - self.last_healing_time > self.healing_cooldown and self.health < self.maxHealth:
            self.is_healing = True
            self.last_healing_time = current_time
            self.frame_index = 0
            print("Healing started!")

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

        # Parry sırasında hareket etmeyi engelle
        if self.is_parrying:
            return

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

        # E tuşu ile healing
        if keys[pygame.K_e]:
            self.start_healing()


        # Dash cooldown kontrolü
        current_time = pygame.time.get_ticks()
        if current_time - self.last_dash_time >= self.dash_cooldown:
            self.can_dash = True

        # Dash movement (parry sırasında dash yapamaz)
        if keys[pygame.K_SPACE] and self.can_dash and not self.isDashing and not self.is_parrying:
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

        # Air attack penceresi kontrolü
        if self.can_air_attack and current_time - self.dash_start_time > self.air_attack_window:
            self.can_air_attack = False

        # Air attack (F tuşu ile) - parry sırasında air attack yapamaz
        if clicks[2] and self.can_air_attack and not self.is_air_attacking and not self.is_attacking and not self.is_parrying:
            self.is_air_attacking = True
            self.can_air_attack = False  # Bir kez kullanılabilir
            self.last_attack_time = current_time
            self.frame_index = 0  # Animasyonu baştan başlat
            self.has_dealt_damage = False
            if self.sfx_manager:
                self.sfx_manager.play_sound("attack1")

        # Parry (sağ tık ile)
        if clicks[2]:  # right mouse click
            current_time = pygame.time.get_ticks()

            # Eğer parry cooldown süresi geçtiyse ve başka bir aksiyon yoksa
            if not self.is_parrying and not self.is_attacking and not self.is_air_attacking and not self.is_throwing and not self.is_hurt and current_time - self.last_parry_time > self.parry_cooldown:
                self.is_parrying = True
                self.parry_start_time = current_time
                self.last_parry_time = current_time
                self.frame_index = 0  # Animasyonu baştan başlat
                self.parry_successful = False  # Başlangıçta başarısız

        # Normal saldırı (sol tık ile) - parry sırasında saldırı yapamaz
        if clicks[0] and not self.is_parrying: # left mouse click
            current_time = pygame.time.get_ticks()

            # Eğer saldırı yapılmıyorsa ve cooldown geçtiyse
            if not self.is_attacking and not self.is_air_attacking and not self.is_parrying and current_time - self.last_attack_time > self.attack_cooldown:
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
        current_time = pygame.time.get_ticks()


        # checking action
        if self.is_hurt:
            self.update_action(7)  # 7: hurt animasyonu
        elif self.is_healing:
            self.update_action(8)  # 8: healing animasyonu
        elif self.is_parrying:
            self.update_action(9)  # 9: defend (parry) animasyonu
        elif self.is_throwing:
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

        if self.flip:
            self.attack_rect.midright = (self.rect.left - 10, self.rect.centery)
        else:
            self.attack_rect.midleft = (self.rect.right + 10, self.rect.centery)

        animation_cooldown = constants.CHAR_ANIM_COOLDOWN_MS

        if self.is_hurt:
            self.image = self.animation_list[7][self.frame_index]
            if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
                self.last_update = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.animation_list[7])

                if self.frame_index == 0:
                    self.is_hurt = False

        elif self.is_healing:
            self.image = self.animation_list[8][self.frame_index]
            if pygame.time.get_ticks() - self.last_update >= self.healing_frame_duration:
                #print(f"Healing frame: {self.frame_index}")
                self.last_update = pygame.time.get_ticks()

                if self.frame_index >= len(self.animation_list[8]) - 1:
                    self.health = min(self.health + self.healing_amount, self.maxHealth)
                    self.is_healing = False
                else:
                    self.frame_index += 1

        elif self.is_parrying:
            self.image = self.animation_list[9][self.frame_index]
            if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
                self.last_update = pygame.time.get_ticks()

                # Eğer başarılı parry olduysa tüm animasyonu oynat
                if self.parry_successful:
                    if self.frame_index < len(self.animation_list[9]) - 1:
                        self.frame_index += 1
                    else:
                        self.is_parrying = False
                # Başarısız parry durumunda sadece ilk frame'i göster ve idle'a dön
                elif self.frame_index == 0:
                    # Sadece ilk frame'i göster ve orada kal
                    pass  # Parry süresi dolana kadar bekle, sonra update metodu içindeki kontrol ile idle'a dönecek

        elif self.is_throwing:
            self.image = self.animation_list[5][self.frame_index]
            if pygame.time.get_ticks() - self.last_update >= self.throw_frame_duration:
                self.last_update = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.animation_list[5])

                if self.frame_index == 0:
                    self.is_throwing = False

        elif self.is_air_attacking:
            self.image = self.animation_list[6][self.frame_index]
            if pygame.time.get_ticks() - self.last_update >= self.attack_frame_duration:
                self.last_update = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.animation_list[6])

                if self.frame_index == 0:
                    self.is_air_attacking = False

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
                self.last_update = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % 6


                if self.frame_index == 0:
                    self.is_attacking = False

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

        # Hurt animasyonu süresi kontrolü
        if self.is_hurt and current_time - self.hurt_start_time > self.hurt_duration:
            self.is_hurt = False

        # Parry süresi kontrolü
        if self.is_parrying and current_time - self.parry_start_time > self.parry_duration:
            self.is_parrying = False
            # Başarılı parry olmadıysa ve ilk frame'den sonra idle'a dön
            if not self.parry_successful and self.frame_index > 0:
                self.frame_index = 0




    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()

    def draw(self, win, font=None):  # font parametresi opsiyonel
        #pygame.draw.rect(win, constants.RED, self.rect, 1)
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if(self.char_type == 0):
            win.blit(flipped_image, (self.rect.x - constants.scale *constants.OFFSET_X, self.rect.y - constants.scale *constants.OFFSET_Y))
        else:
            win.blit(flipped_image, self.rect)
        # health bar
        draw_health_bar(win, self.x + 10, self.y, self.health, self.maxHealth)

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


