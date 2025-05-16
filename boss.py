#boss.py
import pygame
import math
import os
import random
import constants
from functions import load_and_scale_sheet, draw_health_bar


class Boss:
    def __init__(self, x, y,player):
        self.scale = constants.BOSS_SCALE
        self.original_width = constants.BOSS_FRAME_WIDTH
        self.original_height = constants.BOSS_FRAME_HEIGHT
        self.width = int(self.original_width * self.scale)
        self.height = int(self.original_height * self.scale)

        # Hitbox için offset değerleri
        self.hitbox_offset_x = constants.BOSS_HITBOX_OFFSET_X * self.scale
        self.hitbox_offset_y = constants.BOSS_HITBOX_OFFSET_Y * self.scale

        # Hitbox boyutlarını daha küçük ayarla - sadece karakterin çiziminin bulunduğu kısmı kapsa
        self.hitbox_width = int(self.width * 0.4)  # Frame genişliğinin %40'ı
        self.hitbox_height = int(self.height * 0.5)  # Frame yüksekliğinin %50'si

        # Pozisyon ayarları
        self.x = x - self.width // 2
        self.y = y - self.height // 2

        # Hitbox'u karakterin gövdesine hizala
        self.rect = pygame.Rect(
            self.x + (self.width - self.hitbox_width) // 2,  # Yatay olarak ortala
            self.y + (self.height - self.hitbox_height) // 3,  # Biraz daha yukarıda olsun
            self.hitbox_width,
            self.hitbox_height
        )

        # Atak için çarpışma dikdörtgeni
        self.attack_width = 60  # Saldırı genişliği
        self.attack_height = 100  # Saldırı yüksekliği
        self.attack_rect = pygame.Rect(0, 0, self.attack_width, self.attack_height)  # Saldırı hitbox'ı

        # Saldırı frame'leri - her saldırı tipi için hangi frame'lerde hasar verileceği
        self.attack_frames = {
            "attack1": [3, 4],  # attack1 animasyonunda 3. ve 4. frame'lerde hasar ver
            "attack2": [2, 3],  # attack2 animasyonunda 2. ve 3. frame'lerde hasar ver
            "attack3": [3, 4, 5],  # attack3 animasyonunda 3., 4. ve 5. frame'lerde hasar ver
            "jump_attack": [6, 7, 8]  # jump_attack animasyonunda 6., 7. ve 8. frame'lerde hasar ver
        }

        # Hasar verme kontrolü için
        self.has_dealt_damage = False

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

        self.min_follow_distance = self.rect.width * 1.1 - player.rect.width
        self.follow_distance = constants.BOSS_FOLLOW_DISTANCE


        self.phase2_speed_multiplier = 3
        self.phase2_damage_multiplier = 2
        self.dash_cooldown = 3000
        self.last_dash_time = 0
        self.is_dashing = False
        self.dash_duration = 300
        self.dash_start_time = 0
        self.dash_direction = (0, 0)
        self.dash_speed = 15
        self.attack_cooldown = 2000
        self.last_attack_time = pygame.time.get_ticks()

        assets = os.path.join("assets", "Boss")
        self.animations = {
            "attack1": load_and_scale_sheet(os.path.join(assets, "ATTACK 1.png"), self.original_width, self.original_height, 7, self.scale),
            "attack1_flame": load_and_scale_sheet(os.path.join(assets, "ATTACK 1 (FLAMING SWORD).png"), self.original_width, self.original_height, 7, self.scale),
            "attack2": load_and_scale_sheet(os.path.join(assets, "ATTACK 2.png"), self.original_width, self.original_height, 5, self.scale),
            "attack2_flame": load_and_scale_sheet(os.path.join(assets, "ATTACK 2 (FLAMING SWORD).png"), self.original_width, self.original_height, 6, self.scale),
            "attack3": load_and_scale_sheet(os.path.join(assets, "ATTACK 3.png"), self.original_width, self.original_height, 7, self.scale),
            "attack3_flame": load_and_scale_sheet(os.path.join(assets, "ATTACK 3 (FLAMING SWORD).png"), self.original_width, self.original_height, 7, self.scale),
            "jump_attack": load_and_scale_sheet(os.path.join(assets, "JUMP ATTACK.png"), self.original_width, self.original_height, 12, self.scale),
            "jump_attack_flame": load_and_scale_sheet(os.path.join(assets, "JUMP ATTACK (FLAMING SWORD).png"), self.original_width, self.original_height, 11, self.scale),
            "idle": load_and_scale_sheet(os.path.join(assets, "IDLE.png"), self.original_width, self.original_height, 6, self.scale),
            "idle_flame": load_and_scale_sheet(os.path.join(assets, "IDLE (FLAMING SWORD).png"), self.original_width, self.original_height, 6, self.scale),
            "run": load_and_scale_sheet(os.path.join(assets, "RUN.png"), self.original_width, self.original_height, 8, self.scale),
            "run_flame": load_and_scale_sheet(os.path.join(assets, "RUN (FLAMING SWORD).png"), self.original_width, self.original_height, 8, self.scale),
            "dash": load_and_scale_sheet(os.path.join(assets, "RUN.png"), self.original_width, self.original_height, 8, self.scale),
            "dash_flame": load_and_scale_sheet(os.path.join(assets, "RUN (FLAMING SWORD).png"), self.original_width, self.original_height, 8, self.scale),
            "hurt": load_and_scale_sheet(os.path.join(assets, "HURT.png"), self.original_width, self.original_height, 4, self.scale),
            "hurt_flame": load_and_scale_sheet(os.path.join(assets, "HURT (FLAMING SWORD).png"), self.original_width, self.original_height, 4, self.scale),
            "death": load_and_scale_sheet(os.path.join(assets, "DEATH.png"), self.original_width, self.original_height, 26, self.scale),
            "shout": load_and_scale_sheet(os.path.join(assets, "SHOUT.png"), self.original_width, self.original_height, 17, self.scale),
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

    def dash_to_player(self, player):
        if self.is_dashing:
            return

        # Yatay mesafeyi hesapla - player'in sol kenarı ile boss'un sağ kenarı arasındaki mesafe
        dx = player.rect.left - self.rect.right

        # Dikey mesafeyi hesapla - player'in tabanı ile boss'un tabanı arasındaki mesafe
        # Tabanları hizalamak için
        dy = player.rect.bottom - self.rect.bottom

        dist = math.hypot(dx, dy)

        if dist <= self.min_follow_distance:
            return

        # Dash yönünü belirle - ağırlıklı olarak yatay hareket, az dikey hareket
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
        # Hitbox'u karakterin gövdesine hizala
        self.rect.x = self.x + (self.width - self.hitbox_width) // 2
        self.rect.y = self.y + (self.height - self.hitbox_height) // 3  # Biraz daha yukarıda olsun

        # Saldırı hitbox'ını güncelle - self.rect'in bitişinden itibaren
        if not self.flip:  # Sağa bakma durumu
            self.attack_rect.x = self.rect.right  # self.rect'in sağ kenarından başla
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

            # Frame değiştiğinde hasar verme durumunu kontrol et
            if attack_key in self.attack_frames:
                # Debug için frame bilgisini yazdır
                if self.frame_index in self.attack_frames[attack_key]:
                    print(f"Boss attack frame: {self.frame_index} in {attack_key} (Action: {self.action})")

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
                self.x = max(0, min(self.x, constants.screenWidth - self.width))
                self.y = max(0, min(self.y, constants.screenHeight - self.height))
            else:
                self.is_dashing = False
                self.action = "idle"
            return

        if self.action.startswith("attack") or self.action == "jump_attack":
            if self.frame_index < len(self.get_animation()):
                # Saldırı sırasında hitbox'ı aktif et
                if not self.flip:  # Sağa bakma durumu
                    self.attack_rect.x = self.rect.right  # self.rect'in sağ kenarından başla
                    self.attack_rect.y = self.rect.centery - self.attack_height // 2  # Dikey olarak ortala
                else:  # Sola bakma durumu
                    self.attack_rect.x = self.rect.left - self.attack_width  # self.rect'in sol kenarından başla
                    self.attack_rect.y = self.rect.centery - self.attack_height // 2  # Dikey olarak ortala

                # Yeni frame'e geçtiğimizde hasar verme durumunu sıfırla
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


        # Player'in solunda mı sağında mı olduğunu belirle
        self.flip = dx < 0  # Player solda ise sola dön

        should_move = False

        if dist < 100 and now - self.last_attack_time > self.attack_cooldown:
            self.choose_attack()
            self.last_attack_time = now
            self.frame_index = 0
            self.last_update = now
            return

        if (self.phase == 2) or (self.phase == 1 and dist < constants.BOSS_FOLLOW_DISTANCE):
            if dist > self.min_follow_distance:  # Çok yakına gelmesin
                speed = constants.BOSS_SPEED * (self.phase2_speed_multiplier if self.phase == 2 else 1)

                # Sadece yatay hareket et - player'in sağına veya soluna git
                self.x += speed * (dx / dist)

                # Dikey olarak player ile aynı taban seviyesinde ol
                # Player ve boss'un rect'lerinin tabanını hizala
                target_y = player.rect.bottom - self.rect.height  # Player'in tabanı ile boss'un tabanını hizala
                if abs(self.rect.bottom - player.rect.bottom) > 5:  # Belirli bir tolerans ile
                    if self.rect.bottom < player.rect.bottom:
                        self.y += speed
                    else:
                        self.y -= speed

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

    def choose_attack(self):
        options = ["attack1", "attack2", "attack3", "jump_attack"] * (2 if self.phase == 2 else 1)
        self.action = random.choice(options)
        self.has_dealt_damage = False  # Yeni saldırı başladığında hasar verme durumunu sıfırla

    def collision_with_player(self, player):
        """
        Player'ın boss içerisine girmesini engeller.
        Eğer çarpışma varsa, player'ı dışarı iter.
        """
        # Boss ve player hitbox'ları çarpışıyorsa
        if self.rect.colliderect(player.rect):
            # Çarpışma yönünü belirle
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            # Mesafeyi normalize et
            dist = math.hypot(dx, dy)
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

        # Sprite'ı çiz - frame boyutları değişmeden
        win.blit(flipped_sprite, (self.x - constants.BOSS_HITBOX_OFFSET_X * self.scale, self.y - constants.BOSS_HITBOX_OFFSET_Y * self.scale))
        pygame.draw.rect(win, constants.BLUE, self.rect, 2)

        draw_health_bar(win, self.x - 10, self.y - 10, self.health, self.maxHealth)

        if pygame.time.get_ticks() - self.last_update >= animation_cooldown:
            self.last_update = pygame.time.get_ticks()
            self.frame_index += 1
        pygame.draw.rect(win, constants.RED, self.rect, 2)
        # Saldırı hitbox'ını göster
        if self.action.startswith("attack") or self.action == "jump_attack":
            pygame.draw.rect(win, constants.RED, self.attack_rect, 2)