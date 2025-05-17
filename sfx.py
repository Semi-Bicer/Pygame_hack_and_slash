# sfx.py
import pygame
import os


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None

        self.music_files = {
            "menu": os.path.join("assets", "Sounds", "MUSIC", "menu_music.mp3"),
            "battle": os.path.join("assets", "Sounds", "MUSIC", "battle_music.mp3")
        }

        self.sfx_files = {
            "attack1": os.path.join("assets", "Sounds", "SFX", "attack1.mp3"),
            "bossAttack1": os.path.join("assets", "Sounds", "SFX", "bossAttack1.mp3"),
            "shout": os.path.join("assets", "Sounds", "SFX", "shout.mp3")
        }

        # Ayrı ses seviyeleri
        self.music_volume = 0.5
        self.sfx_volume = 0.5

        # SFX seslerini yükle
        self.sfx_sounds = {}
        self.load_sound_effects()



    def load_sound_effects(self):
        """Ses efektlerini yükle"""
        print("\n--- SES DOSYALARI YÜKLENİYOR ---")
        print(f"Toplam {len(self.sfx_files)} ses dosyası bulundu.")

        for name, path in self.sfx_files.items():
            try:
                self.sfx_sounds[name] = pygame.mixer.Sound(path)
                print(f"Ses dosyası başarıyla yüklendi: {name}")
            except Exception as e:
                print(f"Ses dosyası yüklenemedi: {path} - Hata: {e}")

        print(f"\nYüklenen ses dosyaları: {list(self.sfx_sounds.keys())}")
        print("--- SES DOSYALARI YÜKLEME TAMAMLANDI ---\n")

    def play_music(self, track_name, loops=-1, fade_ms=0):
        if track_name in self.music_files and os.path.exists(self.music_files[track_name]):
            # Önce müziği durdur
            pygame.mixer.music.stop()

            # Yeni müziği yükle
            pygame.mixer.music.load(self.music_files[track_name])

            # Müzik ses seviyesini ayarla (bu çok önemli!)
            # Eğer ses seviyesi 0 ise, müziği çalma
            if self.music_volume <= 0.01:
                print(f"Müzik ses seviyesi çok düşük, müzik çalınmayacak: {track_name}, Ses seviyesi: {self.music_volume}")
                return

            pygame.mixer.music.set_volume(self.music_volume)

            # Müziği çal
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            self.current_music = track_name
            print(f"Müzik çalınıyor: {track_name}, Ses seviyesi: {self.music_volume}")

    def stop_music(self, fade_ms=0):
        pygame.mixer.music.fadeout(fade_ms)
        self.current_music = None
        print(f"Müzik durduruldu, fade_ms: {fade_ms}")

    def set_volume(self, volume):
        """Genel ses seviyesini ayarla (geriye dönük uyumluluk için)"""
        self.music_volume = max(0.0, min(1.0, volume))
        self.sfx_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

        # Ses efektlerinin sesini de ayarla
        for sound in self.sfx_sounds.values():
            sound.set_volume(self.sfx_volume)

    def set_music_volume(self, volume):
        """Sadece müzik ses seviyesini ayarla"""
        self.music_volume = max(0.0, min(1.0, volume))
        # Şu anda çalan müziğin ses seviyesini ayarla
        pygame.mixer.music.set_volume(self.music_volume)
        print(f"Müzik ses seviyesi ayarlandı: {self.music_volume}")
        # Tüm müzik dosyalarının ses seviyesini güncelle
        # Not: Pygame'de müzik dosyaları için ses seviyesi global olarak ayarlanır
        # Bu yüzden sadece pygame.mixer.music.set_volume() yeterlidir

    def set_sfx_volume(self, volume):
        """Sadece ses efektlerinin ses seviyesini ayarla"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        print(f"SFX ses seviyesi ayarlandı: {self.sfx_volume}")

        # Tüm yüklenmiş ses efektlerinin ses seviyesini güncelle
        for sound_name, sound in self.sfx_sounds.items():
            sound.set_volume(self.sfx_volume)
            print(f"  - {sound_name} ses seviyesi: {self.sfx_volume}")

        # Henüz yüklenmemiş ses dosyaları için bir şey yapmamıza gerek yok
        # Çünkü yeni bir ses dosyası yüklendiğinde, play_sound metodu
        # otomatik olarak güncel sfx_volume değerini kullanacak

    def play_sound(self, sound_name):
        """Ses efektini çal"""
        # Eğer ses seviyesi 0 ise, sesi çalma
        if self.sfx_volume <= 0.01:
            print(f"SFX ses seviyesi çok düşük, ses çalınmayacak: {sound_name}, Ses seviyesi: {self.sfx_volume}")
            return

        # Animasyon adıyla eşleşen ses dosyasını çal
        if sound_name in self.sfx_sounds:
            # Önce ses seviyesini ayarla, sonra çal
            self.sfx_sounds[sound_name].set_volume(self.sfx_volume)
            print(f"SFX çalınıyor: {sound_name}, Ses seviyesi: {self.sfx_volume}")
            self.sfx_sounds[sound_name].play()
        else:
            # Ses dosyasını bulmayı ve yüklemeyi dene
            sfx_dir = os.path.join("assets", "Sounds", "SFX")
            potential_file = os.path.join(sfx_dir, f"{sound_name}.mp3")

            if os.path.exists(potential_file):
                # Dosyayı yükle ve çal
                self.sfx_files[sound_name] = potential_file
                sound = pygame.mixer.Sound(potential_file)
                sound.set_volume(self.sfx_volume)  # Ses seviyesini ayarla
                self.sfx_sounds[sound_name] = sound
                print(f"Yeni SFX yüklendi ve çalınıyor: {sound_name}, Ses seviyesi: {self.sfx_volume}")
                sound.play()

    def is_music_playing(self):
        return pygame.mixer.music.get_busy()
