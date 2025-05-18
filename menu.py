import pygame
import os
import random

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_menu = "main"  # main, options, controls, video, audio
        self.previous_menu = "main"  # Önceki menüyü takip etmek için

        # Pixel font yükleme
        try:
            # Pixel font dosyasını bul
            font_path = os.path.join("assets", "fonts", "pixel.ttf")
            # Eğer pixel.ttf bulunamazsa, klasördeki herhangi bir .ttf dosyasını kullan
            if not os.path.exists(font_path):
                font_dir = os.path.join("assets", "fonts")
                if os.path.exists(font_dir):
                    for file in os.listdir(font_dir):
                        if file.endswith(".ttf"):
                            font_path = os.path.join(font_dir, file)
                            break

            # Font dosyası bulunduysa yükle
            if os.path.exists(font_path):
                self.font_large = pygame.font.Font(font_path, 72)
                self.font_medium = pygame.font.Font(font_path, 48)
                self.font_small = pygame.font.Font(font_path, 24)
                print(f"Pixel font yüklendi: {font_path}")
            else:
                # Fallback font
                self.font_large = pygame.font.Font(None, 72)
                self.font_medium = pygame.font.Font(None, 48)
                self.font_small = pygame.font.Font(None, 24)
                print("Pixel font bulunamadı, varsayılan font kullanılıyor.")
        except Exception as e:
            print(f"Font yüklenirken hata oluştu: {e}")
            # Fallback font
            self.font_large = pygame.font.Font(None, 72)
            self.font_medium = pygame.font.Font(None, 48)
            self.font_small = pygame.font.Font(None, 24)

        # Menü öğeleri
        self.main_menu_items = ["PLAY", "OPTIONS", "QUIT"]
        self.pause_menu_items = ["RESUME", "OPTIONS", "QUIT"]
        self.options_menu_items = ["CONTROLS", "VIDEO", "AUDIO", "BACK"]
        self.video_menu_items = ["800x600", "1000x800", "1280x720", "1920x1080", "BACK"]
        self.audio_menu_items = ["SFX", "MUSIC", "BACK"]
        self.selected_item = 0

        # Ses ayarları
        self.sfx_volume = 0.5
        self.music_volume = 0.5

        # Video ayarları
        self.resolutions = [(800, 600), (1000, 800), (1280, 720), (1920, 1080)]
        self.current_resolution_index = 1  # Varsayılan 1000x800

        # Kontroller
        self.controls = {
            "Movement": "WASD",
            "Attack": "LMB",
            "Shuriken": "V",
            "Dash": "L-SHIFT"
        }

        # Menü için renkler
        self.text_color = (200, 200, 200)  # Normal beyaz
        self.selected_color = (255, 255, 255)  # Parlak beyaz (seçili öğe için)
        self.hover_color = (255, 255, 255)  # Parlak beyaz (hover için)
        self.title_color = (255, 255, 255)  # Parlak beyaz (başlık için)

        # Ses ayarı için çubuklar
        self.bar_width = 200
        self.bar_height = 20
        self.sfx_bar_rect = pygame.Rect(0, 0, self.bar_width, self.bar_height)
        self.music_bar_rect = pygame.Rect(0, 0, self.bar_width, self.bar_height)
        self.dragging_sfx = False
        self.dragging_music = False

    def draw(self, win, constants, sfx_manager=None):
        # Tamamen siyah arkaplan
        win.fill(constants.BLACK)

        # Menü durumuna göre çizim yap
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
        # Başlık
        title_text = self.font_large.render("SHURA REBIRTH", True, self.title_color)
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

        # Menü öğeleri
        menu_rects = []
        y_pos = self.screen_height // 2
        mouse_pos = pygame.mouse.get_pos()

        # Önceki seçili öğeyi takip etmek için
        last_selected = getattr(self, 'last_selected_main', -1)

        for i, item in enumerate(self.main_menu_items):
            # Fare imleci üzerinde mi kontrol et
            text = self.font_medium.render(item, True, self.text_color)
            text_rect = text.get_rect(center=(self.screen_width // 2, y_pos))
            hover = text_rect.collidepoint(mouse_pos)

            # Renk ve parlaklık ayarla
            if i == self.selected_item:
                color = self.selected_color  # Seçili öğe için parlak beyaz
            elif hover:
                color = self.hover_color  # Fare üzerindeyse parlak beyaz
                # Eğer yeni bir öğe üzerinde hover yapılıyorsa ses çal
                if sfx_manager and i != last_selected:
                    sfx_manager.play_sound("button_highlight")
                    self.last_selected_main = i
            else:
                color = self.text_color  # Normal beyaz

            # Sallantı efekti ekle (rastgele hafif hareket)
            offset_x = random.randint(-1, 1)
            offset_y = random.randint(-1, 1)

            text = self.font_medium.render(item, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2 + offset_x, y_pos + offset_y))
            win.blit(text, text_rect)
            menu_rects.append(text_rect)
            y_pos += 70

        return menu_rects

    def draw_pause_menu(self, win, sfx_manager=None):
        # Başlık
        title_text = self.font_large.render("PAUSED", True, self.title_color)
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

        # Menü öğeleri
        menu_rects = []
        y_pos = self.screen_height // 2
        mouse_pos = pygame.mouse.get_pos()

        # Önceki seçili öğeyi takip etmek için
        last_selected = getattr(self, 'last_selected_pause', -1)

        for i, item in enumerate(self.pause_menu_items):
            # Fare imleci üzerinde mi kontrol et
            text = self.font_medium.render(item, True, self.text_color)
            text_rect = text.get_rect(center=(self.screen_width // 2, y_pos))
            hover = text_rect.collidepoint(mouse_pos)

            # Renk ve parlaklık ayarla
            if i == self.selected_item:
                color = self.selected_color  # Seçili öğe için parlak beyaz
            elif hover:
                color = self.hover_color  # Fare üzerindeyse parlak beyaz
                # Eğer yeni bir öğe üzerinde hover yapılıyorsa ses çal
                if sfx_manager and i != last_selected:
                    sfx_manager.play_sound("button_highlight")
                    self.last_selected_pause = i
            else:
                color = self.text_color  # Normal beyaz

            # Sallantı efekti ekle (rastgele hafif hareket)
            offset_x = random.randint(-1, 1)
            offset_y = random.randint(-1, 1)

            text = self.font_medium.render(item, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2 + offset_x, y_pos + offset_y))
            win.blit(text, text_rect)
            menu_rects.append(text_rect)
            y_pos += 70

        return menu_rects

    def draw_options_menu(self, win, sfx_manager=None):
        # Başlık
        title_text = self.font_large.render("OPTIONS", True, self.title_color)
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

        # Menü öğeleri
        menu_rects = []
        y_pos = self.screen_height // 2
        mouse_pos = pygame.mouse.get_pos()

        # Önceki seçili öğeyi takip etmek için
        last_selected = getattr(self, 'last_selected_options', -1)

        for i, item in enumerate(self.options_menu_items):
            # Fare imleci üzerinde mi kontrol et
            text = self.font_medium.render(item, True, self.text_color)
            text_rect = text.get_rect(center=(self.screen_width // 2, y_pos))
            hover = text_rect.collidepoint(mouse_pos)

            # Renk ve parlaklık ayarla
            if i == self.selected_item:
                color = self.selected_color  # Seçili öğe için parlak beyaz
            elif hover:
                color = self.hover_color  # Fare üzerindeyse parlak beyaz
                # Eğer yeni bir öğe üzerinde hover yapılıyorsa ses çal
                if sfx_manager and i != last_selected:
                    sfx_manager.play_sound("button_highlight")
                    self.last_selected_options = i
            else:
                color = self.text_color  # Normal beyaz

            # Sallantı efekti ekle (rastgele hafif hareket)
            offset_x = random.randint(-1, 1)
            offset_y = random.randint(-1, 1)

            text = self.font_medium.render(item, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2 + offset_x, y_pos + offset_y))
            win.blit(text, text_rect)
            menu_rects.append(text_rect)
            y_pos += 70

        return menu_rects

    def draw_controls_menu(self, win, sfx_manager=None):
        # Başlık
        title_text = self.font_large.render("CONTROLS", True, self.title_color)
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

        # Kontrol listesi
        y_pos = self.screen_height // 3
        mouse_pos = pygame.mouse.get_pos()

        for i, (control, key) in enumerate(self.controls.items()):
            # Sallantı efekti ekle (rastgele hafif hareket)
            offset_x = random.randint(-1, 1)
            offset_y = random.randint(-1, 1)

            control_text = self.font_medium.render(f"{control}: {key}", True, self.text_color)
            text_pos = (self.screen_width // 2 - control_text.get_width() // 2 + offset_x, y_pos + offset_y)
            win.blit(control_text, text_pos)
            y_pos += 60

        # Geri butonu
        # Sallantı efekti ekle
        offset_x = random.randint(-1, 1)
        offset_y = random.randint(-1, 1)

        # Fare imleci üzerinde mi kontrol et
        temp_rect = pygame.Rect(0, 0, 100, 40)
        temp_rect.center = (self.screen_width // 2, y_pos + 40)
        hover = temp_rect.collidepoint(mouse_pos)

        # Önceki seçili öğeyi takip etmek için
        last_hover = getattr(self, 'last_hover_controls', False)

        # Renk seçimi
        color = self.hover_color if hover else self.selected_color

        # Eğer yeni hover durumu varsa ses çal
        if sfx_manager and hover and not last_hover:
            sfx_manager.play_sound("button_highlight")

        # Hover durumunu güncelle
        self.last_hover_controls = hover

        back_text = self.font_medium.render("BACK", True, color)
        back_rect = back_text.get_rect(center=(self.screen_width // 2 + offset_x, y_pos + 40 + offset_y))
        win.blit(back_text, back_rect)

        return [back_rect]

    def draw_video_menu(self, win, sfx_manager=None):
        # Başlık
        title_text = self.font_large.render("VIDEO", True, self.title_color)
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

        # Çözünürlük seçenekleri
        menu_rects = []
        y_pos = self.screen_height // 3
        mouse_pos = pygame.mouse.get_pos()

        # Önceki seçili öğeyi takip etmek için
        last_selected = getattr(self, 'last_selected_video', -1)

        for i, res in enumerate(self.video_menu_items):
            # Fare imleci üzerinde mi kontrol et
            temp_text = self.font_medium.render(res, True, self.text_color)
            text_rect = temp_text.get_rect(center=(self.screen_width // 2, y_pos))
            hover = text_rect.collidepoint(mouse_pos)

            # Renk ve parlaklık ayarla
            if i == self.selected_item:
                color = self.selected_color  # Seçili öğe için parlak beyaz
            elif hover:
                color = self.hover_color  # Fare üzerindeyse parlak beyaz
                # Eğer yeni bir öğe üzerinde hover yapılıyorsa ses çal
                if sfx_manager and i != last_selected:
                    sfx_manager.play_sound("button_highlight")
                    self.last_selected_video = i
            else:
                color = self.text_color  # Normal beyaz

            # Sallantı efekti ekle (rastgele hafif hareket)
            offset_x = random.randint(-1, 1)
            offset_y = random.randint(-1, 1)

            # Mevcut çözünürlüğü işaretle
            if i < len(self.resolutions) and i == self.current_resolution_index:
                text = self.font_medium.render(f"{res} *", True, color)
            else:
                text = self.font_medium.render(res, True, color)

            text_rect = text.get_rect(center=(self.screen_width // 2 + offset_x, y_pos + offset_y))
            win.blit(text, text_rect)
            menu_rects.append(text_rect)
            y_pos += 60

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

        # Geri butonu
        # Sallantı efekti ekle
        offset_x = random.randint(-1, 1)
        offset_y = random.randint(-1, 1)

        # Fare imleci üzerinde mi kontrol et
        temp_rect = pygame.Rect(0, 0, 100, 40)
        temp_rect.center = (self.screen_width // 2, y_pos)
        hover = temp_rect.collidepoint(mouse_pos)

        # Önceki hover durumunu kontrol et
        last_hover = getattr(self, 'last_hover_audio_back', False)

        # Renk seçimi
        if self.selected_item == 2:
            color = self.selected_color
        elif hover:
            color = self.hover_color
            # Eğer yeni hover durumu varsa ses çal
            if sfx_manager and not last_hover:
                sfx_manager.play_sound("button_highlight")
        else:
            color = self.text_color

        # Hover durumunu güncelle
        self.last_hover_audio_back = hover

        back_text = self.font_medium.render("BACK", True, color)
        back_rect = back_text.get_rect(center=(self.screen_width // 2 + offset_x, y_pos + offset_y))
        win.blit(back_text, back_rect)

        # Ses ayarlarını uygula
        if sfx_manager:
            sfx_manager.set_sfx_volume(self.sfx_volume)
            sfx_manager.set_music_volume(self.music_volume)

        return [self.sfx_bar_rect, self.music_bar_rect, back_rect]

    def draw_death_menu(self, win, sfx_manager=None):
        # Başlık
        title_text = self.font_large.render("GAME OVER", True, (255, 0, 0))  # Kırmızı renk
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

        # Menü öğeleri
        menu_rects = []
        y_pos = self.screen_height // 2
        mouse_pos = pygame.mouse.get_pos()

        # Ölüm menüsü öğeleri
        death_menu_items = ["TRY AGAIN", "QUIT"]

        # Önceki seçili öğeyi takip etmek için
        last_selected = getattr(self, 'last_selected_death', -1)

        for i, item in enumerate(death_menu_items):
            # Fare imleci üzerinde mi kontrol et
            text = self.font_medium.render(item, True, self.text_color)
            text_rect = text.get_rect(center=(self.screen_width // 2, y_pos))
            hover = text_rect.collidepoint(mouse_pos)

            # Renk ve parlaklık ayarla
            if hover:
                color = self.hover_color  # Fare üzerindeyse parlak beyaz
                # Eğer yeni bir öğe üzerinde hover yapılıyorsa ses çal
                if sfx_manager and i != last_selected:
                    sfx_manager.play_sound("button_highlight")
                    self.last_selected_death = i
            else:
                color = self.text_color  # Normal beyaz

            # Sallantı efekti ekle (rastgele hafif hareket)
            offset_x = random.randint(-1, 1)
            offset_y = random.randint(-1, 1)

            text = self.font_medium.render(item, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2 + offset_x, y_pos + offset_y))
            win.blit(text, text_rect)
            menu_rects.append(text_rect)
            y_pos += 70

        return menu_rects

    def draw_win_menu(self, win, sfx_manager=None):
        # Başlık
        title_text = self.font_large.render("YOU'VE DEFEATED THE ONI", True, (0, 255, 0))  # Yeşil renk
        win.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

        # Menü öğeleri
        menu_rects = []
        y_pos = self.screen_height // 2
        mouse_pos = pygame.mouse.get_pos()

        # Zafer menüsü öğeleri
        win_menu_items = ["TRY AGAIN", "QUIT"]

        # Önceki seçili öğeyi takip etmek için
        last_selected = getattr(self, 'last_selected_win', -1)

        for i, item in enumerate(win_menu_items):
            # Fare imleci üzerinde mi kontrol et
            text = self.font_medium.render(item, True, self.text_color)
            text_rect = text.get_rect(center=(self.screen_width // 2, y_pos))
            hover = text_rect.collidepoint(mouse_pos)

            # Renk ve parlaklık ayarla
            if hover:
                color = self.hover_color  # Fare üzerindeyse parlak beyaz
                # Eğer yeni bir öğe üzerinde hover yapılıyorsa ses çal
                if sfx_manager and i != last_selected:
                    sfx_manager.play_sound("button_highlight")
                    self.last_selected_win = i
            else:
                color = self.text_color  # Normal beyaz

            # Sallantı efekti ekle (rastgele hafif hareket)
            offset_x = random.randint(-1, 1)
            offset_y = random.randint(-1, 1)

            text = self.font_medium.render(item, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2 + offset_x, y_pos + offset_y))
            win.blit(text, text_rect)
            menu_rects.append(text_rect)
            y_pos += 70

        return menu_rects

    def handle_event(self, event, win_size=None, sfx_manager=None):
        # Menü öğelerinin dikdörtgenlerini al
        menu_rects = self.get_current_menu_rects(sfx_manager)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % self.get_current_menu_length()
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % self.get_current_menu_length()
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Seçim sesi çal
                if sfx_manager:
                    sfx_manager.play_sound("button_select")
                return self.select_current_item(win_size)
            elif event.key == pygame.K_ESCAPE:
                # Geri dönme sesi çal
                if sfx_manager:
                    sfx_manager.play_sound("button_select")

                # Pause menüsünde ESC tuşu RESUME gibi davransın
                if self.current_menu == "pause":
                    return "resume"
                # Diğer menülerde ESC tuşu bir önceki menüye dönsün
                elif self.current_menu != "main":
                    # Alt menülerden options menüsüne dönüş
                    if self.current_menu in ["controls", "video", "audio"]:
                        self.current_menu = "options"
                        self.selected_item = 0
                        return "back"
                    # Options menüsünden önceki menüye dönüş
                    elif self.current_menu == "options":
                        # Önceki menüye dön
                        temp_menu = self.current_menu  # Geçici olarak mevcut menüyü sakla
                        self.current_menu = self.previous_menu
                        self.previous_menu = temp_menu  # Önceki menü artık options oldu
                        self.selected_item = 0
                        return "back"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Sol tık
                mouse_pos = pygame.mouse.get_pos()

                # Ses çubukları için kontrol
                if self.current_menu == "audio":
                    if self.sfx_bar_rect.collidepoint(mouse_pos):
                        self.dragging_sfx = True
                        self.update_volume(mouse_pos[0], "sfx")
                        return None
                    elif self.music_bar_rect.collidepoint(mouse_pos):
                        self.dragging_music = True
                        self.update_volume(mouse_pos[0], "music")
                        return None

                # Menü öğelerine tıklama kontrolü
                for i, rect in enumerate(menu_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_item = i
                        # Seçim sesi çal
                        if sfx_manager:
                            sfx_manager.play_sound("button_select")
                        return self.select_current_item(win_size)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Sol tık bırakıldı
                self.dragging_sfx = False
                self.dragging_music = False

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()

            # Sürüklenme işlemleri
            if self.dragging_sfx:
                self.update_volume(mouse_pos[0], "sfx")
            elif self.dragging_music:
                self.update_volume(mouse_pos[0], "music")

            # Fare imlecinin üzerinde olduğu menü öğesini vurgula
            for i, rect in enumerate(menu_rects):
                if rect.collidepoint(mouse_pos):
                    self.selected_item = i
                    break

        return None

    def get_current_menu_rects(self, sfx_manager=None):
        """Mevcut menünün dikdörtgenlerini döndür"""
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

    def update_volume(self, x_pos, volume_type):
        if volume_type == "sfx":
            bar_rect = self.sfx_bar_rect
            relative_x = max(0, min(x_pos - bar_rect.left, bar_rect.width))
            self.sfx_volume = relative_x / bar_rect.width
            print(f"SFX ses seviyesi güncellendi: {self.sfx_volume}")
        elif volume_type == "music":
            bar_rect = self.music_bar_rect
            relative_x = max(0, min(x_pos - bar_rect.left, bar_rect.width))
            self.music_volume = relative_x / bar_rect.width
            print(f"MUSIC ses seviyesi güncellendi: {self.music_volume}")

    def get_current_menu_length(self):
        if self.current_menu == "main":
            return len(self.main_menu_items)
        elif self.current_menu == "options":
            return len(self.options_menu_items)
        elif self.current_menu == "video":
            return len(self.video_menu_items)
        elif self.current_menu == "audio":
            return 3  # SFX, MUSIC, BACK
        elif self.current_menu == "controls":
            return 1  # Sadece BACK butonu
        elif self.current_menu == "death":
            return 2  # TRY AGAIN, QUIT
        elif self.current_menu == "win":
            return 2  # TRY AGAIN, QUIT
        return 0

    def select_current_item(self, win_size=None):
        if self.current_menu == "main":
            if self.selected_item == 0:  # PLAY
                return "play"
            elif self.selected_item == 1:  # OPTIONS
                self.previous_menu = "main"
                self.current_menu = "options"
                self.selected_item = 0
                return "options"
            elif self.selected_item == 2:  # QUIT
                return "quit"

        elif self.current_menu == "pause":
            if self.selected_item == 0:  # RESUME
                return "resume"
            elif self.selected_item == 1:  # OPTIONS
                self.previous_menu = "pause"  # Pause menüsünden geldiğimizi kaydet
                self.current_menu = "options"
                self.selected_item = 0
                return "options"
            elif self.selected_item == 2:  # QUIT
                return "quit"

        elif self.current_menu == "options":
            if self.selected_item == 0:  # CONTROLS
                # previous_menu değişkenini güncelleme, options'tan geldiğimizi hatırlayalım
                self.current_menu = "controls"
                self.selected_item = 0
                return "controls"
            elif self.selected_item == 1:  # VIDEO
                # previous_menu değişkenini güncelleme, options'tan geldiğimizi hatırlayalım
                self.current_menu = "video"
                self.selected_item = 0
                return "video"
            elif self.selected_item == 2:  # AUDIO
                # previous_menu değişkenini güncelleme, options'tan geldiğimizi hatırlayalım
                self.current_menu = "audio"
                self.selected_item = 0
                return "audio"
            elif self.selected_item == 3:  # BACK
                # Önceki menüye dön
                self.current_menu = self.previous_menu
                self.selected_item = 0
                return "back"

        elif self.current_menu == "controls":
            # Kontroller menüsünde sadece BACK butonu var
            self.current_menu = "options"
            self.selected_item = 0
            return "back"

        elif self.current_menu == "video":
            if self.selected_item < len(self.resolutions):  # Bir çözünürlük seçildi
                self.current_resolution_index = self.selected_item
                if win_size:
                    return ("resolution", self.resolutions[self.selected_item])
            elif self.selected_item == len(self.video_menu_items) - 1:  # BACK
                self.current_menu = "options"
                self.selected_item = 0
                return "back"

        elif self.current_menu == "audio":
            if self.selected_item == 2:  # BACK
                self.current_menu = "options"
                self.selected_item = 0
                return "back"

        elif self.current_menu == "death" or self.current_menu == "win":
            if self.selected_item == 0:  # TRY AGAIN
                return "try_again"
            elif self.selected_item == 1:  # QUIT
                return "quit"

        return None