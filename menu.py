import pygame
import os
import random
import constants

class Button:
    def __init__(self, text, font, position=None, center_position=None, text_color=(200, 200, 200), hover_color=(255, 255, 255), selected_color=(255, 255, 255)):
        self.text = text
        self.font = font
        self.position = position  # Sol üst köşe koordinatı
        self.center_position = center_position  # Merkez koordinatı
        self.text_color = text_color
        self.hover_color = hover_color
        self.selected_color = selected_color
        self.is_hovered = False
        self.is_selected = False
        self.last_hover = False

        # Buton metnini render et ve rect'ini al
        self.render_text()

    def render_text(self):
        # Metin rengi seçimi
        if self.is_selected:
            color = self.selected_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.text_color

        # Sallanma efekti için rastgele offset
        self.offset_x = random.randint(-1, 1)
        self.offset_y = random.randint(-1, 1)

        # Metni render et
        self.rendered_text = self.font.render(self.text, True, color)

        # Rect'i oluştur
        if self.center_position:
            self.rect = self.rendered_text.get_rect(center=(self.center_position[0] + self.offset_x,
                                                           self.center_position[1] + self.offset_y))
        elif self.position:
            self.rect = self.rendered_text.get_rect(topleft=(self.position[0] + self.offset_x,
                                                           self.position[1] + self.offset_y))

    def update(self, mouse_pos, sfx_manager=None):
        # Mouse butonun üzerinde mi kontrol et
        hover = self.rect.collidepoint(mouse_pos)

        # Hover durumu değişti mi?
        if hover and not self.last_hover and sfx_manager:
            sfx_manager.play_sound("button_highlight")

        # Hover durumunu güncelle
        self.is_hovered = hover
        self.last_hover = hover

        # Metni yeniden render et (sallanma efekti ve renk güncellemesi için)
        self.render_text()

        return hover

    def draw(self, surface):
        # Butonu çiz
        surface.blit(self.rendered_text, self.rect)

class Menu:
    current_resolution_index = 3  # Varsayılan 1920x1080
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_menu = "main"              # main, options, controls, video, audio
        self.previous_menu = "main"             # Önceki menüyü takip etmek için

        # Ana menü arka plan görseli kaldırıldı - siyah arkaplan kullanılacak                                👁️
        self.background_image = None

        # Ana menü animasyonları için
        self.menu_character = None
        self.menu_boss = None
        self.animation_timer = 0
        self.animation_cooldown = 100                                                                       #👁️

        # Ölüm ekranı arka plan görseli
        self.death_image = None
        death_path = os.path.join("assets", "pics", "Death.jpeg")
        if os.path.exists(death_path):
            self.death_image = pygame.image.load(death_path)

        # Kazanma ekranı arka plan görseli
        self.win_image = None
        win_path = os.path.join("assets", "pics", "Win.jpeg")
        if os.path.exists(win_path):
            self.win_image = pygame.image.load(win_path)

        font_path = os.path.join("assets", "fonts", "SchoonSquare-Regular.ttf")
        self.font_large = pygame.font.Font(font_path, 72)
        self.font_medium = pygame.font.Font(font_path, 48)
        self.font_small = pygame.font.Font(font_path, 24)

        #Skor Değişkeni
        self.skor = 0

        # Renk ayarları
        self.title_color = (255, 255, 255)  # Beyaz başlık rengi
        self.text_color = (200, 200, 200)   # Gri metin rengi
        self.hover_color = (255, 255, 255)  # Beyaz hover rengi
        self.selected_color = (255, 255, 255)  # Beyaz seçili rengi

        # Menü öğeleri
        self.main_menu_items = ["PLAY", "OPTIONS", "QUIT"]
        self.pause_menu_items = ["RESUME", "RETRY", "OPTIONS", "MAIN MENU", "QUIT"]
        self.options_menu_items = ["CONTROLS", "VIDEO", "AUDIO", "BACK"]
        self.video_menu_items = ["800x600", "1000x800", "1280x720", "Full Screen", "BACK"]
        self.audio_menu_items = ["SFX", "MUSIC", "BACK"]
        self.selected_item = 0

        # Ses ayarları
        self.sfx_volume = 0.5
        self.music_volume = 0.5

        # Video ayarları
        self.resolutions = [(800, 600), (1000, 800), (1280, 720), "fullscreen"]

        # Kontroller
        self.controls = {
            "Movement": "WASD",
            "Run": "L-SHIFT",
            "Dash": "SPACE",
            "Attack": "LMB",
            "Parry": "RMB",
            "Shuriken": "V",
            "Healing" : "E"
        }

        # Ses ayarı için çubuklar
        self.bar_width = 200
        self.bar_height = 20
        self.sfx_bar_rect = pygame.Rect(0, 0, self.bar_width, self.bar_height)
        self.music_bar_rect = pygame.Rect(0, 0, self.bar_width, self.bar_height)
        self.dragging_sfx = False
        self.dragging_music = False

    def getskor(self, skor):
        self.skor = skor
    def set_menu_characters(self, character, boss):
        """Ana menü için karakter ve boss referanslarını ayarla"""
        self.menu_character = character
        self.menu_boss = boss

    def draw(self, win, constants, sfx_manager=None):
        win.fill(constants.BLACK)

        if self.current_menu == "main":
            return self.draw_main_menu(win, sfx_manager)
        elif self.current_menu == "pause":
            return self.draw_pause_menu(win, sfx_manager)
        elif self.current_menu == "options":
            return self.draw_options_menu(win, sfx_manager)
        elif self.current_menu == "controls":
            return self.draw_controls_menu(win, sfx_manager)
        elif self.current_menu == "video":
            return self.draw_video_menu(win, sfx_manager)
        elif self.current_menu == "audio":
            return self.draw_audio_menu(win, sfx_manager)
        elif self.current_menu == "death":
            return self.draw_death_menu(win, sfx_manager)
        elif self.current_menu == "win":
            return self.draw_win_menu(win, sfx_manager)

    def draw_main_menu(self, win, sfx_manager=None):
        # Siyah arkaplan
        win.fill(constants.BLACK)

        # Karakter ve boss animasyonlarını çiz              👁️
        self.draw_menu_animations(win)

        # Başlık
        title_text = self.font_large.render("SHURA REBIRTH", True, self.title_color)
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

        # Menü butonlarını oluştur (eğer henüz oluşturulmadıysa)
        if not hasattr(self, 'main_menu_buttons') or len(self.main_menu_buttons) != len(self.main_menu_items):
            self.main_menu_buttons = []
            y_pos = self.screen_height // 2

            for item in self.main_menu_items:
                button = Button(
                    text=item,
                    font=self.font_medium,
                    center_position=(self.screen_width // 2, y_pos),
                    text_color=self.text_color,
                    hover_color=self.hover_color,
                    selected_color=self.selected_color
                )
                self.main_menu_buttons.append(button)
                y_pos += 70

        # Butonları güncelle ve çiz
        mouse_pos = pygame.mouse.get_pos()
        menu_rects = []

        for i, button in enumerate(self.main_menu_buttons):
            # Seçili buton durumunu güncelle
            button.is_selected = (i == self.selected_item)

            # Butonu güncelle ve çiz
            button.update(mouse_pos, sfx_manager)
            button.draw(win)

            # Rect'i listeye ekle
            menu_rects.append(button.rect)

        return menu_rects

    def draw_menu_animations(self, win):                                                            #👁️ tamamı
        """Ana menüde karakter ve boss animasyonlarını çiz"""
        if not self.menu_character or not self.menu_boss:
            return

        current_time = pygame.time.get_ticks()

        # Animasyon timer'ını güncelle
        if current_time - self.animation_timer >= self.animation_cooldown:
            self.animation_timer = current_time

            # Karakter idle animasyonu
            if hasattr(self.menu_character, 'animation_list') and len(self.menu_character.animation_list) > 0:
                idle_frames = self.menu_character.animation_list[0]  # 0: idle animasyonu
                if len(idle_frames) > 0:
                    self.menu_character.frame_index = (self.menu_character.frame_index + 1) % len(idle_frames)
                    self.menu_character.image = idle_frames[self.menu_character.frame_index]

            # Boss idle animasyonu
            if hasattr(self.menu_boss, 'animations') and 'idle' in self.menu_boss.animations:
                idle_frames = self.menu_boss.animations['idle']
                if len(idle_frames) > 0:
                    self.menu_boss.frame_index = (self.menu_boss.frame_index + 1) % len(idle_frames)

        # Basit konum ayarları - manuel değiştirilebilir
        char_scale = 4
        boss_scale = 4

        # Karakter konumu (sol taraf)
        char_x = 150
        char_y = 100

        # Boss konumu (sağ taraf)
        boss_x = 950
        boss_y = 0

        # Karakter çiz (boyutu artırılmış)
        if hasattr(self.menu_character, 'image') and self.menu_character.image:
            # Karakteri büyüt
            char_image = pygame.transform.scale(self.menu_character.image,
                                              (int(self.menu_character.image.get_width() * char_scale),
                                               int(self.menu_character.image.get_height() * char_scale)))
            win.blit(char_image, (char_x, char_y))

        # Boss çiz (boyutu artırılmış)
        if hasattr(self.menu_boss, 'animations') and 'idle' in self.menu_boss.animations:
            idle_frames = self.menu_boss.animations['idle']
            if len(idle_frames) > 0:
                boss_image = idle_frames[self.menu_boss.frame_index]
                # Boss'u sola çevir (karaktere bakacak şekilde)
                boss_image = pygame.transform.flip(boss_image, True, False)
                # Boss'u büyüt
                boss_image = pygame.transform.scale(boss_image,
                                                  (int(boss_image.get_width() * boss_scale),
                                                   int(boss_image.get_height() * boss_scale)))
                win.blit(boss_image, (boss_x, boss_y))

    def draw_pause_menu(self, win, sfx_manager=None):
        # Başlık
        title_text = self.font_large.render("PAUSED", True, self.title_color)
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

        # Menü butonlarını oluştur (eğer henüz oluşturulmadıysa)
        if not hasattr(self, 'pause_menu_buttons') or len(self.pause_menu_buttons) != len(self.pause_menu_items):
            self.pause_menu_buttons = []
            y_pos = self.screen_height // 2

            for item in self.pause_menu_items:
                button = Button(
                    text=item,
                    font=self.font_medium,
                    center_position=(self.screen_width // 2, y_pos),
                    text_color=self.text_color,
                    hover_color=self.hover_color,
                    selected_color=self.selected_color
                )
                self.pause_menu_buttons.append(button)
                y_pos += 70

        # Butonları güncelle ve çiz
        mouse_pos = pygame.mouse.get_pos()
        menu_rects = []

        for i, button in enumerate(self.pause_menu_buttons):
            # Seçili buton durumunu güncelle
            button.is_selected = (i == self.selected_item)

            # Butonu güncelle ve çiz
            button.update(mouse_pos, sfx_manager)
            button.draw(win)

            # Rect'i listeye ekle
            menu_rects.append(button.rect)

        return menu_rects

    def draw_options_menu(self, win, sfx_manager=None):
        # Başlık
        title_text = self.font_large.render("OPTIONS", True, self.title_color)
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

        # Menü butonlarını oluştur (eğer henüz oluşturulmadıysa)
        if not hasattr(self, 'options_menu_buttons') or len(self.options_menu_buttons) != len(self.options_menu_items):
            self.options_menu_buttons = []
            y_pos = self.screen_height // 2

            for item in self.options_menu_items:
                button = Button(
                    text=item,
                    font=self.font_medium,
                    center_position=(self.screen_width // 2, y_pos),
                    text_color=self.text_color,
                    hover_color=self.hover_color,
                    selected_color=self.selected_color
                )
                self.options_menu_buttons.append(button)
                y_pos += 70

        # Butonları güncelle ve çiz
        mouse_pos = pygame.mouse.get_pos()
        menu_rects = []

        for i, button in enumerate(self.options_menu_buttons):
            # Seçili buton durumunu güncelle
            button.is_selected = (i == self.selected_item)

            # Butonu güncelle ve çiz
            button.update(mouse_pos, sfx_manager)
            button.draw(win)

            # Rect'i listeye ekle
            menu_rects.append(button.rect)

        return menu_rects

    def draw_controls_menu(self, win, sfx_manager=None):
        # Başlık
        title_text = self.font_large.render("CONTROLS", True, self.title_color)
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

        # Kontrol listesi
        y_pos = self.screen_height // 3

        for i, (control, key) in enumerate(self.controls.items()):
            # Sallantı efekti ekle (rastgele hafif hareket)
            offset_x = random.randint(-1, 1)
            offset_y = random.randint(-1, 1)

            control_text = self.font_medium.render(f"{control}: {key}", True, self.text_color)
            text_pos = (self.screen_width // 2 - control_text.get_width() // 2 + offset_x, y_pos + offset_y)
            win.blit(control_text, text_pos)
            y_pos += 60

        # BACK butonu
        if not hasattr(self, 'controls_back_button'):
            self.controls_back_button = Button(
                text="BACK",
                font=self.font_medium,
                center_position=(self.screen_width // 2, y_pos + 40),
                text_color=self.text_color,
                hover_color=self.hover_color,
                selected_color=self.selected_color
            )

        # Butonu güncelle ve çiz
        mouse_pos = pygame.mouse.get_pos()
        self.controls_back_button.update(mouse_pos, sfx_manager)
        self.controls_back_button.draw(win)

        return [self.controls_back_button.rect]

    def draw_video_menu(self, win, sfx_manager=None):
        # Başlık
        title_text = self.font_large.render("VIDEO", True, self.title_color)
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

        # Menü butonlarını oluştur (eğer henüz oluşturulmadıysa)
        if not hasattr(self, 'video_menu_buttons') or len(self.video_menu_buttons) != len(self.video_menu_items):
            self.video_menu_buttons = []
            y_pos = self.screen_height // 3

            for i, res in enumerate(self.video_menu_items):
                # Mevcut çözünürlüğü işaretle
                if i < len(self.resolutions) and i == self.current_resolution_index:
                    button_text = f"{res} *"
                else:
                    button_text = res

                button = Button(
                    text=button_text,
                    font=self.font_medium,
                    center_position=(self.screen_width // 2, y_pos),
                    text_color=self.text_color,
                    hover_color=self.hover_color,
                    selected_color=self.selected_color
                )
                self.video_menu_buttons.append(button)
                y_pos += 60

        # Butonları güncelle ve çiz
        mouse_pos = pygame.mouse.get_pos()
        menu_rects = []

        for i, button in enumerate(self.video_menu_buttons):
            # Seçili buton durumunu güncelle
            button.is_selected = (i == self.selected_item)

            # Çözünürlük değiştiyse buton metnini güncelle
            if i < len(self.resolutions):
                if i == self.current_resolution_index and not button.text.endswith(" *"):
                    button.text = f"{self.video_menu_items[i]} *"
                elif i != self.current_resolution_index and button.text.endswith(" *"):
                    button.text = self.video_menu_items[i]

            # Butonu güncelle ve çiz
            button.update(mouse_pos, sfx_manager)
            button.draw(win)

            # Rect'i listeye ekle
            menu_rects.append(button.rect)

        return menu_rects

    def draw_audio_menu(self, win, sfx_manager=None):
        # Başlık
        title_text = self.font_large.render("AUDIO", True, self.title_color)
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

        # Ses ayarları
        y_pos = self.screen_height // 3
        mouse_pos = pygame.mouse.get_pos()

        # SFX ses seviyesi
        # Sallantı efekti ekle
        offset_x = random.randint(-1, 1)
        offset_y = random.randint(-1, 1)

        sfx_text = self.font_medium.render("SFX", True, self.text_color)
        win.blit(sfx_text, (self.screen_width // 4 + offset_x, y_pos + offset_y))

        # SFX çubuğu
        self.sfx_bar_rect.topleft = (self.screen_width // 2, y_pos + 10)
        pygame.draw.rect(win, (100, 100, 100), self.sfx_bar_rect)  # Arkaplan
        fill_width = int(self.sfx_bar_rect.width * self.sfx_volume)
        pygame.draw.rect(win, (0, 255, 0), (self.sfx_bar_rect.left, self.sfx_bar_rect.top, fill_width, self.sfx_bar_rect.height))
        pygame.draw.rect(win, (255, 255, 255), self.sfx_bar_rect, 2)  # Çerçeve

        y_pos += 80

        # Music ses seviyesi
        # Sallantı efekti ekle
        offset_x = random.randint(-1, 1)
        offset_y = random.randint(-1, 1)

        music_text = self.font_medium.render("MUSIC", True, self.text_color)
        win.blit(music_text, (self.screen_width // 4 + offset_x, y_pos + offset_y))

        # Music çubuğu
        self.music_bar_rect.topleft = (self.screen_width // 2, y_pos + 10)
        pygame.draw.rect(win, (100, 100, 100), self.music_bar_rect)  # Arkaplan
        fill_width = int(self.music_bar_rect.width * self.music_volume)
        pygame.draw.rect(win, (0, 255, 0), (self.music_bar_rect.left, self.music_bar_rect.top, fill_width, self.music_bar_rect.height))
        pygame.draw.rect(win, (255, 255, 255), self.music_bar_rect, 2)  # Çerçeve

        y_pos += 100

        # BACK butonu
        if not hasattr(self, 'audio_back_button'):
            self.audio_back_button = Button(
                text="BACK",
                font=self.font_medium,
                center_position=(self.screen_width // 2, y_pos),
                text_color=self.text_color,
                hover_color=self.hover_color,
                selected_color=self.selected_color
            )

        # Butonu güncelle ve çiz
        self.audio_back_button.is_selected = (self.selected_item == 2)
        self.audio_back_button.update(mouse_pos, sfx_manager)
        self.audio_back_button.draw(win)

        # Ses ayarlarını uygula
        if sfx_manager:
            sfx_manager.set_sfx_volume(self.sfx_volume)
            sfx_manager.set_music_volume(self.music_volume)

        return [self.sfx_bar_rect, self.music_bar_rect, self.audio_back_button.rect]

    def draw_death_menu(self, win, sfx_manager=None):
        # Arka planı siyah yap
        win.fill(constants.BLACK)

        # Ölüm görselini ortalayarak çiz
        if self.death_image:
            # Görselin boyutlarını al
            img_width, img_height = self.death_image.get_size()

            # Görseli ekranın ortasına yerleştir
            x_pos = (self.screen_width - img_width) // 2
            y_pos = (self.screen_height - img_height) // 2

            # Görseli çiz
            win.blit(self.death_image, (x_pos, y_pos))

        # Başlık
        title_text = self.font_large.render("GAME OVER", True, (255, 0, 0))  # Kırmızı renk
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))
        skor = self.font_large.render("SKOR: "+str(self.skor), True, (200, 200, 0))
        win.blit(skor, ((self.screen_width - skor.get_width()) // 2, 150 + skor.get_height()))
        # Ölüm menüsü butonlarını oluştur (eğer henüz oluşturulmadıysa)
        death_menu_items = ["TRY AGAIN", "QUIT"]

        if not hasattr(self, 'death_menu_buttons') or len(self.death_menu_buttons) != len(death_menu_items):
            self.death_menu_buttons = []
            y_pos = self.screen_height - 200  # Butonları daha aşağıya yerleştir

            for item in death_menu_items:
                button = Button(
                    text=item,
                    font=self.font_medium,
                    center_position=(self.screen_width // 2, y_pos),
                    text_color=self.text_color,
                    hover_color=self.hover_color,
                    selected_color=self.selected_color
                )
                self.death_menu_buttons.append(button)
                y_pos += 70

        # Butonları güncelle ve çiz
        mouse_pos = pygame.mouse.get_pos()
        menu_rects = []

        for i, button in enumerate(self.death_menu_buttons):
            # Butonu güncelle ve çiz
            button.update(mouse_pos, sfx_manager)
            button.draw(win)

            # Rect'i listeye ekle
            menu_rects.append(button.rect)

        return menu_rects

    def draw_win_menu(self, win, sfx_manager=None):
        # Arka planı siyah yap
        win.fill(constants.BLACK)

        # Kazanma görselini ortalayarak çiz
        if self.win_image:
            # Görselin boyutlarını al
            img_width, img_height = self.win_image.get_size()

            # Görseli ekranın ortasına yerleştir
            x_pos = (self.screen_width - img_width) // 2
            y_pos = (self.screen_height - img_height) // 2

            # Görseli çiz
            win.blit(self.win_image, (x_pos, y_pos))

        # Başlık
        title_text = self.font_large.render("YOU'VE DEFEATED THE ONI", True, (0, 255, 0))  # Yeşil renk
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))
        skor = self.font_large.render("SKOR: "+str(self.skor), True, (200, 200, 0))
        win.blit(skor, ((self.screen_width - skor.get_width()) // 2, 150 + skor.get_height()))

        # Zafer menüsü butonlarını oluştur (eğer henüz oluşturulmadıysa)
        win_menu_items = ["TRY AGAIN", "QUIT"]

        if not hasattr(self, 'win_menu_buttons') or len(self.win_menu_buttons) != len(win_menu_items):
            self.win_menu_buttons = []
            y_pos = self.screen_height - 200  # Butonları daha aşağıya yerleştir

            for item in win_menu_items:
                button = Button(
                    text=item,
                    font=self.font_medium,
                    center_position=(self.screen_width // 2, y_pos),
                    text_color=self.text_color,
                    hover_color=self.hover_color,
                    selected_color=self.selected_color
                )
                self.win_menu_buttons.append(button)
                y_pos += 70

        # Butonları güncelle ve çiz
        mouse_pos = pygame.mouse.get_pos()
        menu_rects = []

        for i, button in enumerate(self.win_menu_buttons):
            # Butonu güncelle ve çiz
            button.update(mouse_pos, sfx_manager)
            button.draw(win)

            # Rect'i listeye ekle
            menu_rects.append(button.rect)

        return menu_rects

    def get_current_menu_rects(self, sfx_manager=None):
        # Boş bir yüzey oluştur
        temp_surface = pygame.Surface((self.screen_width, self.screen_height))

        # Mevcut menüyü çiz ve dikdörtgenleri al
        if self.current_menu == "main":
            return self.draw_main_menu(temp_surface, sfx_manager)
        elif self.current_menu == "pause":
            return self.draw_pause_menu(temp_surface, sfx_manager)
        elif self.current_menu == "options":
            return self.draw_options_menu(temp_surface, sfx_manager)
        elif self.current_menu == "controls":
            return self.draw_controls_menu(temp_surface, sfx_manager)
        elif self.current_menu == "video":
            return self.draw_video_menu(temp_surface, sfx_manager)
        elif self.current_menu == "audio":
            return self.draw_audio_menu(temp_surface, sfx_manager)
        elif self.current_menu == "death":
            return self.draw_death_menu(temp_surface, sfx_manager)
        elif self.current_menu == "win":
            return self.draw_win_menu(temp_surface, sfx_manager)

        return []

    def handle_event(self, event, win_size=None, sfx_manager=None):
        menu_rects = self.get_current_menu_rects(sfx_manager)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % self.get_current_menu_length()
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % self.get_current_menu_length()
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if sfx_manager:
                    sfx_manager.play_sound("button_select")
                return self.select_current_item(win_size)
            elif event.key == pygame.K_ESCAPE:
                if sfx_manager:
                    sfx_manager.play_sound("button_select")

                if self.current_menu == "pause":
                    return "resume"

                elif self.current_menu != "main":
                    if self.current_menu in ["controls", "video", "audio"]:
                        self.current_menu = "options"
                        self.selected_item = 0
                        return "back"

                    elif self.current_menu == "options":
                        temp_menu = self.current_menu
                        self.current_menu = self.previous_menu
                        self.previous_menu = temp_menu
                        self.selected_item = 0
                        return "back"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if self.current_menu == "audio":
                    if self.sfx_bar_rect.collidepoint(mouse_pos):
                        self.dragging_sfx = True
                        self.update_volume(mouse_pos[0], "sfx")
                        return None
                    elif self.music_bar_rect.collidepoint(mouse_pos):
                        self.dragging_music = True
                        self.update_volume(mouse_pos[0], "music")
                        return None

                for i, rect in enumerate(menu_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_item = i
                        if sfx_manager:
                            sfx_manager.play_sound("button_select")
                        return self.select_current_item(win_size)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging_sfx = False
                self.dragging_music = False

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()

            if self.dragging_sfx:
                self.update_volume(mouse_pos[0], "sfx")
            elif self.dragging_music:
                self.update_volume(mouse_pos[0], "music")

            for i, rect in enumerate(menu_rects):
                if rect.collidepoint(mouse_pos):
                    self.selected_item = i
                    break

        return None

    def update_volume(self, x_pos, volume_type):
        if volume_type == "sfx":
            bar_rect = self.sfx_bar_rect
            relative_x = max(0, min(x_pos - bar_rect.left, bar_rect.width))
            self.sfx_volume = relative_x / bar_rect.width
        elif volume_type == "music":
            bar_rect = self.music_bar_rect
            relative_x = max(0, min(x_pos - bar_rect.left, bar_rect.width))
            self.music_volume = relative_x / bar_rect.width

    def get_current_menu_length(self):
        if self.current_menu == "main":
            return len(self.main_menu_items)
        elif self.current_menu == "options":
            return len(self.options_menu_items)
        elif self.current_menu == "video":
            return len(self.video_menu_items)
        elif self.current_menu == "audio":
            return 3                                    # SFX, MUSIC, BACK
        elif self.current_menu == "controls":
            return 1                                    # BACK
        elif self.current_menu == "death":
            return 2                                    # TRY AGAIN, QUIT
        elif self.current_menu == "win":
            return 2                                    # TRY AGAIN, QUIT
        return 0

    def select_current_item(self, win_size=None):
        if self.current_menu == "main":
            if self.selected_item == 0:                 # PLAY
                return "play"
            elif self.selected_item == 1:               # OPTIONS
                self.previous_menu = "main"
                self.current_menu = "options"
                self.selected_item = 0
                return "options"
            elif self.selected_item == 2:               # QUIT
                return "quit"

        elif self.current_menu == "pause":
            if self.selected_item == 0:                 # RESUME
                return "resume"
            elif self.selected_item == 1:               # RETRY
                return "try_again"
            elif self.selected_item == 2:               # OPTIONS
                self.previous_menu = "pause"            # Pause'dan geldiğimizi kaydet
                self.current_menu = "options"
                self.selected_item = 0
                return "options"
            elif self.selected_item == 3:               # MAIN MENU
                return "main_menu"
            elif self.selected_item == 4:               # QUIT
                return "quit"

        elif self.current_menu == "options":
            if self.selected_item == 0:                 # CONTROLS
                self.current_menu = "controls"
                self.selected_item = 0
                return "controls"
            elif self.selected_item == 1:  # VIDEO
                self.current_menu = "video"
                self.selected_item = 0
                return "video"
            elif self.selected_item == 2:  # AUDIO
                self.current_menu = "audio"
                self.selected_item = 0
                return "audio"
            elif self.selected_item == 3:  # BACK
                self.current_menu = self.previous_menu
                self.selected_item = 0
                return "back"

        elif self.current_menu == "controls":
            self.current_menu = "options"
            self.selected_item = 0
            return "back"

        elif self.current_menu == "video":
            if self.selected_item < len(self.resolutions):
                Menu.current_resolution_index = self.selected_item
                print(f"Selected resolution index: {self.current_resolution_index}")
                if win_size:
                    return ("resolution", self.resolutions[self.selected_item])
            elif self.selected_item == len(self.video_menu_items) - 1:
                self.current_menu = "options"
                self.selected_item = 0
                return "back"

        elif self.current_menu == "audio":
            if self.selected_item == 2:
                self.current_menu = "options"
                self.selected_item = 0
                return "back"

        elif self.current_menu == "death" or self.current_menu == "win":
            if self.selected_item == 0:
                return "try_again"
            elif self.selected_item == 1:
                return "quit"

        return None