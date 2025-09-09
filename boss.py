import pygame
import math
import os
import random
import constants
from functions import load_and_scale_sheet, draw_health_bar
from menu import Menu




class Boss:
    def __init__(self, x, y, player, sfx_manager=None):
        self.scale = constants.BOSS_SCALE
        self.original_width = constants.BOSS_FRAME_WIDTH
        self.original_height = constants.BOSS_FRAME_HEIGHT

        # Hitbox için offset de, self.scaleerleri


        # Hitbox boyutlarını daha küçük ayarla - sadece karakterin çiziminin bulundu, self.scaleu kısmı kapsa

        # Pozisyon ayarları
        self.x = x
        self.y = y

        # Hitbox'u karakterin gövdesine hizala
        self.rect = pygame.Rect(
            self.x  + (self.original_width // 2),  # Yatay olarak ortala
            self.y + (self.original_height // 3),  # Biraz daha yukarıda olsun
            self.original_width*1.125,
            self.original_height*(124/108)
        )

        # Atak için çarpışma dikdörtgeni
        self.attack_width = 60  # Saldırı genişli, self.scalei
        self.attack_height = 100  # Saldırı yüksekli, self.scalei
        self.attack_rect = pygame.Rect(0, 0, self.attack_width, self.attack_height)  # Saldırı hitbox'ı

        # Saldırı frame'leri - her saldırı tipi için hangi frame'lerde hasar verilece, self.scalei
        self.attack_frames = {
            "attack1": [3, 4],  # attack1 animasyonunda 3. ve 4. frame'lerde hasar ver
            "attack2": [2, 3],  # attack2 animasyonunda 2. ve 3. frame'lerde hasar ver
            "attack3": [3, 4, 5],  # attack3 animasyonunda 3., 4. ve 5. frame'lerde hasar ver
            "jump_attack": [6, 7, 8]  # jump_attack animasyonunda 6., 7. ve 8. frame'lerde hasar ver
        }

        # Hasar verme kontrolü için
        self.has_dealt_damage = False

        # Ses yöneticisi
        self.sfx_manager = sfx_manager


        self.idleCount = 0
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.flip = False

        self.phase = 1
        self.action = "idle"
        self.health = constants.BOSS_HEALTH
        self.maxHealth = constants.BOSS_HEALTH
        self.invincible = False
        self.phase_transition = False

        # Boss'un karaktere yaklaşabilece, self.scalei minimum mesafe - daha yakına gelmez
        self.min_follow_distance = 100  # Sabit 50 piksel mesafe
        self.follow_distance = constants.BOSS_FOLLOW_DISTANCE

        self.phase2_speed_multiplier = 1.8
        self.phase2_damage_multiplier = 1.8
        self.dash_cooldown = 3000
        self.last_dash_time = 0
        self.is_dashing = False
        self.dash_duration = 300
        self.dash_start_time = 0
        self.dash_direction = (0, 0)
        self.dash_speed = 15
        self.attack_cooldown = 2000
        self.last_attack_time = pygame.time.get_ticks()

        # Blade Rift Projectile mekanikleri
        self.blade_rift_cooldown = constants.BLADE_RIFT_COOLDOWN
        self.last_blade_rift_time = pygame.time.get_ticks()
        self.blade_rift_projectiles = []  # Aktif projectile'lar

        self.key = 3
        self.old_key = 3
        assets = os.path.join("assets", "Boss")
        self.animations = {
            "attack1": load_and_scale_sheet(os.path.join(assets, "ATTACK 1.png"), self.original_width, self.original_height, 7,self.key, self.scale),
            "attack1_flame": load_and_scale_sheet(os.path.join(assets, "ATTACK 1 (FLAMING SWORD).png"), self.original_width, self.original_height, 7,self.key, self.scale),
            "attack2": load_and_scale_sheet(os.path.join(assets, "ATTACK 2.png"), self.original_width, self.original_height, 5,self.key, self.scale),
            "attack2_flame": load_and_scale_sheet(os.path.join(assets, "ATTACK 2 (FLAMING SWORD).png"), self.original_width, self.original_height, 6,self.key, self.scale),
            "attack3": load_and_scale_sheet(os.path.join(assets, "ATTACK 3.png"), self.original_width, self.original_height, 7,self.key, self.scale),
            "attack3_flame": load_and_scale_sheet(os.path.join(assets, "ATTACK 3 (FLAMING SWORD).png"), self.original_width, self.original_height, 7,self.key, self.scale),
            "jump_attack": load_and_scale_sheet(os.path.join(assets, "JUMP ATTACK.png"), self.original_width, self.original_height, 12,self.key, self.scale),
            "jump_attack_flame": load_and_scale_sheet(os.path.join(assets, "JUMP ATTACK (FLAMING SWORD).png"), self.original_width, self.original_height, 11,self.key, self.scale),
            "idle": load_and_scale_sheet(os.path.join(assets, "IDLE.png"), self.original_width, self.original_height, 6,self.key, self.scale),
            "idle_flame": load_and_scale_sheet(os.path.join(assets, "IDLE (FLAMING SWORD).png"), self.original_width, self.original_height, 6,self.key, self.scale),
            "run": load_and_scale_sheet(os.path.join(assets, "RUN.png"), self.original_width, self.original_height, 8,self.key, self.scale),
            "run_flame": load_and_scale_sheet(os.path.join(assets, "RUN (FLAMING SWORD).png"), self.original_width, self.original_height, 8,self.key, self.scale),
            "dash": load_and_scale_sheet(os.path.join(assets, "RUN.png"), self.original_width, self.original_height, 8,self.key, self.scale),
            "dash_flame": load_and_scale_sheet(os.path.join(assets, "RUN (FLAMING SWORD).png"), self.original_width, self.original_height, 8,self.key, self.scale),
            "hurt": load_and_scale_sheet(os.path.join(assets, "HURT.png"), self.original_width, self.original_height, 4,self.key, self.scale),
            "hurt_flame": load_and_scale_sheet(os.path.join(assets, "HURT (FLAMING SWORD).png"), self.original_width, self.original_height, 4,self.key, self.scale),
            "death": load_and_scale_sheet(os.path.join(assets, "DEATH.png"), self.original_width, self.original_height, 26,self.key, self.scale),
            "shout": load_and_scale_sheet(os.path.join(assets, "SHOUT.png"), self.original_width, self.original_height, 17,self.key, self.scale),
            "blade_rift": load_and_scale_sheet(os.path.join(assets, "spin_blade.png"), 64, 64, 7,self.key, self.scale),
        }

    def reload(self):
        assets = os.path.join("assets", "Boss")
        self.animations = {
            "attack1": load_and_scale_sheet(os.path.join(assets, "ATTACK 1.png"), self.original_width, self.original_height, 7,self.key, self.scale),
            "attack1_flame": load_and_scale_sheet(os.path.join(assets, "ATTACK 1 (FLAMING SWORD).png"), self.original_width, self.original_height, 7,self.key, self.scale),
            "attack2": load_and_scale_sheet(os.path.join(assets, "ATTACK 2.png"), self.original_width, self.original_height, 5,self.key, self.scale),
            "attack2_flame": load_and_scale_sheet(os.path.join(assets, "ATTACK 2 (FLAMING SWORD).png"), self.original_width, self.original_height, 6,self.key, self.scale),
            "attack3": load_and_scale_sheet(os.path.join(assets, "ATTACK 3.png"), self.original_width, self.original_height, 7,self.key, self.scale),
            "attack3_flame": load_and_scale_sheet(os.path.join(assets, "ATTACK 3 (FLAMING SWORD).png"), self.original_width, self.original_height, 7,self.key, self.scale),
            "jump_attack": load_and_scale_sheet(os.path.join(assets, "JUMP ATTACK.png"), self.original_width, self.original_height, 12,self.key, self.scale),
            "jump_attack_flame": load_and_scale_sheet(os.path.join(assets, "JUMP ATTACK (FLAMING SWORD).png"), self.original_width, self.original_height, 11,self.key, self.scale),
            "idle": load_and_scale_sheet(os.path.join(assets, "IDLE.png"), self.original_width, self.original_height, 6,self.key, self.scale),
            "idle_flame": load_and_scale_sheet(os.path.join(assets, "IDLE (FLAMING SWORD).png"), self.original_width, self.original_height, 6,self.key, self.scale),
            "run": load_and_scale_sheet(os.path.join(assets, "RUN.png"), self.original_width, self.original_height, 8,self.key, self.scale),
            "run_flame": load_and_scale_sheet(os.path.join(assets, "RUN (FLAMING SWORD).png"), self.original_width, self.original_height, 8,self.key, self.scale),
            "dash": load_and_scale_sheet(os.path.join(assets, "RUN.png"), self.original_width, self.original_height, 8,self.key, self.scale),
            "dash_flame": load_and_scale_sheet(os.path.join(assets, "RUN (FLAMING SWORD).png"), self.original_width, self.original_height, 8,self.key, self.scale),
            "hurt": load_and_scale_sheet(os.path.join(assets, "HURT.png"), self.original_width, self.original_height, 4,self.key, self.scale),
            "hurt_flame": load_and_scale_sheet(os.path.join(assets, "HURT (FLAMING SWORD).png"), self.original_width, self.original_height, 4,self.key, self.scale),
            "death": load_and_scale_sheet(os.path.join(assets, "DEATH.png"), self.original_width, self.original_height, 26,self.key, self.scale),
            "shout": load_and_scale_sheet(os.path.join(assets, "SHOUT.png"), self.original_width, self.original_height, 17,self.key, self.scale),
        }


    def get_animation(self):
        anim_key = self.action
        if self.phase == 2 and self.action in ["idle", "run", "hurt", "attack1", "attack2", "attack3", "jump_attack", "dash"]:
            anim_key += "_flame"
        return self.animations.get(anim_key, self.animations["idle"])

    def take_damage(self, amount):
        if not self.invincible and self.action != "death":
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.action = "death"
            else:
                self.action = "hurt_flame" if self.phase == 2 else "hurt"

            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()

            if self.phase == 1 and self.health <= self.maxHealth // 2:
                self.phase_transition = True
                self.invincible = True
                self.action = "shout"
                self.frame_index = 0
                self.last_update = pygame.time.get_ticks()

                # Shout animasyonu başladı, self.scaleında ses çal
                if self.sfx_manager:
                    self.sfx_manager.play_sound("shout")

    def dash_to_player(self, player):
        if self.is_dashing:
            return

        # Yatay mesafeyi hesapla - player'in sol kenarı ile boss'un sa, self.scale kenarı arasındaki mesafe
        dx = player.rect.centerx - self.rect.centerx

        # Dikey mesafeyi hesapla - player'in tabanı ile boss'un tabanı arasındaki mesafe
        # Tabanları hizalamak için
        dy = player.rect.bottom - self.rect.bottom

        dist = math.hypot(dx, dy)

        if dist <= self.min_follow_distance:
            return

        # Dash yönünü belirle - a, self.scaleırlıklı olarak yatay hareket, az dikey hareket
        dash_x = dx / dist
        dash_y = dy / dist * 0.5  # Dikey hareketi sınırla

        self.dash_direction = (dash_x, dash_y)
        self.is_dashing = True
        self.dash_start_time = pygame.time.get_ticks()
        self.action = "dash_flame" if self.phase == 2 else "dash"
        self.frame_index = 0
        self.last_dash_time = pygame.time.get_ticks()

    def update(self, player):
        now = pygame.time.get_ticks()
        
        self.key = Menu.current_resolution_index
        if self.key != self.old_key:
            self.reload()
            self.old_key = self.key


        # Saldırı hitbox'ını güncelle - self.rect'in bitişinden itibaren
        if not self.flip:  # Sağa bakma durumu
            self.attack_rect.x = self.rect.right  # self.rect'in sa, self.scale kenarından başla
            self.attack_rect.y = self.rect.centery - self.attack_height // 2  # Dikey olarak ortala
        else:  # Sola bakma durumu
            self.attack_rect.x = self.rect.left - self.attack_width  # self.rect'in sol kenarından başla
            self.attack_rect.y = self.rect.centery - self.attack_height // 2  # Dikey olarak ortala

        self.attack_rect.width = self.attack_width
        self.attack_rect.height = self.attack_height

        # Saldırı durumunda ve belirli frame'lerde hasar verme kontrolü
        if self.action.startswith("attack") or self.action == "jump_attack" or self.action == "jump_attack_flame":
            # Flame ekini kaldır
            attack_key = self.action
            if "_flame" in attack_key:
                attack_key = attack_key.replace("_flame", "")

        if self.health <= 0:
            self.action = "death"
            return

        if self.phase_transition:
            if self.frame_index >= len(self.get_animation()):
                self.phase_transition = False
                self.invincible = False
                self.phase = 2
                self.action = "idle"
                self.attack_cooldown = int(self.attack_cooldown / self.phase2_speed_multiplier)
                self.dash_speed *= 1.5
            return

        if self.action in ["shout", "death"]:
            if self.frame_index >= len(self.get_animation()):
                self.action = "idle"
            return

        if self.is_dashing:
            if now - self.dash_start_time < self.dash_duration:
                self.x += self.dash_direction[0] * self.dash_speed
                self.y += self.dash_direction[1] * self.dash_speed
                self.x = max(0, min(self.x, constants.screenWidth - (self.rect.width)))
                self.y = max(0, min(self.y, constants.screenHeight - (self.rect.height)))
            else:
                self.is_dashing = False
                self.action = "idle"
                self.x = max(0, min(self.x, constants.screenWidth - (self.rect.width)))
                self.y = max(0, min(self.y, constants.screenHeight - (self.rect.height)))
            return

        if self.action.startswith("attack") or self.action == "jump_attack":
            if self.frame_index < len(self.get_animation()):
                # Saldırı sırasında hitbox'ı aktif et
                if not self.flip:  # Sa, self.scalea bakma durumu
                    self.attack_rect.x = self.rect.right  # self.rect'in sa, self.scale kenarından başla
                    self.attack_rect.y = self.rect.centery - self.attack_height // 2  # Dikey olarak ortala
                else:  # Sola bakma durumu
                    self.attack_rect.x = self.rect.left - self.attack_width  # self.rect'in sol kenarından başla
                    self.attack_rect.y = self.rect.centery - self.attack_height // 2  # Dikey olarak ortala

                # Yeni frame'e geçti, self.scaleimizde hasar verme durumunu sıfırla
                attack_key = self.action
                if "_flame" in attack_key:
                    attack_key = attack_key.replace("_flame", "")

                if attack_key in self.attack_frames and self.frame_index in self.attack_frames[attack_key]:
                    self.has_dealt_damage = False
                return
            else:
                self.action = "idle"
                self.has_dealt_damage = False

        if self.action in ["hurt", "hurt_flame"]:
            if self.frame_index < len(self.get_animation()):
                return
            else:
                self.action = "idle"

        if self.phase == 2 and now - self.last_dash_time > self.dash_cooldown:
            if random.random() < 0.3:
                self.dash_to_player(player)
                return

        # Player'a göre konumu hesapla
        # Player'in merkezi ile boss'un merkezi arasındaki mesafe
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)


        # Player'in solunda mı sa, self.scaleında mı oldu, self.scaleunu belirle
        self.flip = dx < 0  # Player solda ise sola dön

        should_move = False

        # Belirli bir mesafede saldırı yap
        if dist < 150 and now - self.last_attack_time > self.attack_cooldown:
            self.choose_attack()
            self.last_attack_time = now
            self.frame_index = 0
            self.last_update = now
            return

        if (self.phase == 2) or (self.phase == 1 and dist < constants.BOSS_FOLLOW_DISTANCE):
            if dist > self.min_follow_distance:  # Çok yakına gelmesin
                speed = constants.BOSS_SPEED * (self.phase2_speed_multiplier if self.phase == 2 else 1)

                # Sadece yatay hareket et - player'in sa, self.scaleına veya soluna git
                self.x += speed * (dx / dist)

                # Dikey olarak player ile aynı taban seviyesinde ol
                # Player ve boss'un rect'lerinin tabanını hizala
                target_y = player.rect.bottom - self.rect.height  # Player'in tabanı ile boss'un tabanını hizala
                if abs(self.rect.bottom - player.rect.bottom) > 5:  # Belirli bir tolerans ile
                    if self.rect.bottom < player.rect.bottom:
                        self.y += speed
                    else:
                        self.y -= speed
                # Boss'u ekran sınırları içinde tut
                # Sprite'ın gerçek render pozisyonunu dikkate al
                # X koordinatı için kontrol
                sprite_right = self.x + 20 + self.original_width * self.scale
                sprite_left = self.x + 20
                
                if sprite_right > constants.screenWidth:
                    self.x = constants.screenWidth - (self.original_width * self.scale) - 20
                elif sprite_left < 0:
                    self.x = -20
                    
                # Y koordinatı için kontrol
                sprite_bottom = self.y - 35 + self.original_height * self.scale
                sprite_top = self.y - 35
                
                if sprite_bottom > constants.screenHeight:
                    self.y = constants.screenHeight - (self.original_height * self.scale) + 35
                elif sprite_top < 0:
                    self.y = 35

                # Hitbox'u karakterin gövdesine hizala
                self.rect.x = self.x + self.original_width   // 2
                self.rect.y = self.y + self.original_height // 3  # Biraz daha yukarıda olsun


                should_move = True
            elif now - self.last_dash_time > self.dash_cooldown:
                self.dash_to_player(player)
                return

        if self.is_dashing:
            self.action = "dash_flame" if self.phase == 2 else "dash"
        elif should_move:
            self.action = "run_flame" if self.phase == 2 else "run"
        else:
            self.action = "idle_flame" if self.phase == 2 else "idle"

        # Blade Rift Projectile mekanikleri
        # Phase 2'de blade rift projectile fırlat
        if self.phase == 2 and now - self.last_blade_rift_time >= self.blade_rift_cooldown:
            self.launch_blade_rift(player)

        # Aktif blade rift projectile'ları güncelle
        self.update_blade_rifts(player)

    def choose_attack(self):
        options = ["attack1", "attack2", "attack3", "jump_attack"] * (2 if self.phase == 2 else 1)
        self.action = random.choice(options)
        self.has_dealt_damage = False  # Yeni saldırı başladı, self.scaleında hasar verme durumunu sıfırla

        # E, self.scaleer attack1 seçildiyse ve ses yöneticisi varsa bossAttack1 sesini çal
        if self.action == "attack1" and self.sfx_manager:
            self.sfx_manager.play_sound("bossAttack1")

    def check_parry(self, player):
        """Player'in parry durumunu kontrol eder ve başarılı parry durumunda boss'u durdurur"""
        # E, self.scaleer boss saldırı durumundaysa ve player parry yapıyorsa
        if (self.action.startswith("attack") or self.action == "jump_attack" or
            self.action.startswith("attack_flame") or self.action == "jump_attack_flame") and player.is_parrying:

            # Saldırı frame'lerinde mi kontrol et
            attack_key = self.action
            if "_flame" in attack_key:
                attack_key = attack_key.replace("_flame", "")

            if attack_key in self.attack_frames and self.frame_index in self.attack_frames[attack_key]:
                # Saldırı hitbox'ları çarpışıyor mu kontrol et
                if self.attack_rect.colliderect(player.rect):
                    # Başarılı parry
                    player.successful_parry()

                    # Boss'u idle durumuna getir
                    self.action = "idle_flame" if self.phase == 2 else "idle"
                    self.frame_index = 0
                    self.has_dealt_damage = False

                    # Ses efekti çal
                    if self.sfx_manager:
                        self.sfx_manager.play_sound("parry")

                    return True
        return False

    def collision_with_player(self, player):
        # Boss ve player hitbox'ları çarpışıyorsa
        if self.rect.colliderect(player.rect):
            # Çarpışma yönünü belirle
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            # Mesafeyi normalize et
            dist = math.hypot(dx, dy) # hipotenüs
            if dist == 0:  # Sıfıra bölme hatasını önle
                dx, dy = 1, 0
            else:
                dx, dy = dx/dist, dy/dist

            # Player'ı dışarı it - boss'un hareket hızından daha hızlı
            push_strength = constants.BOSS_SPEED * 2

            # Player'ın pozisyonunu güncelle
            player.x += dx * push_strength
            player.y += dy * push_strength

            # Ekran sınırlarını kontrol et
            player.x = max(0, min(player.x, constants.screenWidth - player.width))
            player.y = max(0, min(player.y, constants.screenHeight - player.height))

            # Player'ın rect'ini güncelle
            player.rect.x = player.x
            player.rect.y = player.y

            return True  # Çarpışma var

        return False  # Çarpışma yok

    def draw(self, win):
        self.win = win
        animation_cooldown = constants.BOSS_ANIMATION_COOLDOWN
        if self.phase == 2:
            animation_cooldown = int(animation_cooldown / self.phase2_speed_multiplier)

        frames = self.get_animation()
        if self.frame_index >= len(frames):
            if self.action in ["death", "shout"]:
                self.frame_index = len(frames) - 1
            else:
                self.frame_index = 0

        sprite = frames[self.frame_index]
        flipped_sprite = pygame.transform.flip(sprite, self.flip, False)

        # Sprite'ı çiz - frame boyutları de, self.scaleişmeden
        win.blit(flipped_sprite, (self.x+20 , self.y-35))
        #pygame.draw.rect(win, constants.BLUE, self.rect, 2)

        draw_health_bar(win, self.x + 55, self.y + 25, self.health, self.maxHealth)

        if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
            self.last_update = pygame.time.get_ticks()
            self.frame_index += 1
        #pygame.draw.rect(win, constants.RED, self.rect, 2)
        # Saldırı hitbox'ını göster

        # Blade rift projectile'larını çiz
        self.draw_blade_rifts(win)

    def launch_blade_rift(self, player):
        """Blade rift projectile'ını fırlat"""
        current_time = pygame.time.get_ticks()

        # Cooldown kontrolü
        if current_time - self.last_blade_rift_time < self.blade_rift_cooldown:
            return

        # Yeni blade rift projectile oluştur
        blade_rift = BladeRiftProjectile(
            self.rect.centerx - 30,  # Boss'un merkezinden başlat
            self.rect.centery - 30,
            player.rect.centerx,     # Player'ı hedef al
            player.rect.centery,
            self.animations["blade_rift"],
            self.scale
        )

        self.blade_rift_projectiles.append(blade_rift)
        self.last_blade_rift_time = current_time

    def update_blade_rifts(self, player):
        """Blade rift projectile'larını güncelle"""
        for projectile in self.blade_rift_projectiles[:]:
            projectile.update(player)

            # Ölü projectile'ları kaldır
            if not projectile.alive:
                self.blade_rift_projectiles.remove(projectile)
                continue

            # Player ile çarpışma kontrolü
            projectile.check_collision_with_player(player)

    def draw_blade_rifts(self, win):
        """Blade rift projectile'larını çiz"""
        for projectile in self.blade_rift_projectiles:
            projectile.draw(win)


class BladeRiftProjectile:
    def __init__(self, x, y, target_x, target_y, animations, scale=1.0):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = constants.BLADE_RIFT_SPEED
        self.animations = animations
        self.scale = scale

        # Animasyon kontrolü
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100

        # Hitbox
        self.width = 60 * scale
        self.height = 60 * scale
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Yaşam süresi
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = constants.BLADE_RIFT_LIFETIME
        self.alive = False

        # Hasar verme
        self.damage_per_second = constants.BLADE_RIFT_DAMAGE_PER_SECOND
        self.last_damage_time = 0
        self.damage_interval = constants.BLADE_RIFT_DAMAGE_INTERVAL

        # Hedef takip etme
        self.tracking = True

    def update(self, player):
        if not self.alive:
            return

        current_time = pygame.time.get_ticks()

        # Yaşam süresi kontrolü
        if current_time - self.creation_time > self.lifetime:
            self.alive = False
            return

        # Hedefi takip et
        if self.tracking:
            # Player'ın mevcut pozisyonunu hedef olarak güncelle
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            # Mesafeyi normalize et
            distance = math.hypot(dx, dy)
            if distance > 0:
                # Hareket yönünü hesapla
                move_x = (dx / distance) * self.speed
                move_y = (dy / distance) * self.speed

                # Pozisyonu güncelle
                self.x += move_x
                self.y += move_y
                self.rect.x = self.x
                self.rect.y = self.y

        # Animasyon güncelleme
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame_index = (self.frame_index + 1) % len(self.animations)
            self.last_update = current_time

    def check_collision_with_player(self, player):
        if not self.alive:
            return False

        if self.rect.colliderect(player.rect):
            current_time = pygame.time.get_ticks()

            # Hasar verme zamanı geldi mi?
            if current_time - self.last_damage_time >= self.damage_interval:
                player.health -= self.damage_per_second
                self.last_damage_time = current_time

                # Player'ın hurt animasyonunu çal
                if hasattr(player, 'play_hurt_animation'):
                    player.play_hurt_animation()

                return True
        return False

    def draw(self, win):
        if not self.alive or not self.animations:
            return

        if self.frame_index < len(self.animations):
            sprite = self.animations[self.frame_index]
            win.blit(sprite, (self.x, self.y))

        # Debug için hitbox çiz (isteğe bağlı)
        # pygame.draw.rect(win, (255, 0, 0), self.rect, 2)
