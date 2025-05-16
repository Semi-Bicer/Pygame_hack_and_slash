# sfx.py
import pygame
import os
import constants
import glob


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None

        # Ses dosyalarının bulunduğu klasörleri kontrol et
        self.check_sound_directories()

        # Ses klasörünü oluştur (yoksa)
        self.ensure_sound_directories()

        self.music_files = {
            "menu": os.path.join("assets", "Sounds", "MUSIC", "menu_music.mp3"),
            "battle": os.path.join("assets", "Sounds", "MUSIC", "battle_music.mp3")
        }

        # Ses dosyalarını otomatik olarak bul
        self.sfx_files = self.find_sound_files()

        self.volume = 0.5

        # SFX seslerini yükle
        self.sfx_sounds = {}
        self.load_sound_effects()

    def ensure_sound_directories(self):
        """Ses klasörlerinin var olduğundan emin ol"""
        # Ana klasörler
        assets_dir = "assets"
        sounds_dir = os.path.join(assets_dir, "Sounds")
        sfx_dir = os.path.join(sounds_dir, "SFX")
        music_dir = os.path.join(sounds_dir, "MUSIC")

        # Klasörleri oluştur
        for directory in [assets_dir, sounds_dir, sfx_dir, music_dir]:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                    print(f"Klasör oluşturuldu: {directory}")
                except Exception as e:
                    print(f"Klasör oluşturulamadı: {directory} - Hata: {e}")

    def check_sound_directories(self):
        """Ses dosyalarının bulunduğu klasörleri kontrol et"""
        # Müzik klasörünü kontrol et
        music_dir = os.path.join("assets", "Sounds", "MUSIC")
        if os.path.exists(music_dir):
            print(f"Müzik klasörü bulundu: {music_dir}")
            music_files = glob.glob(os.path.join(music_dir, "*.*"))
            print(f"Müzik dosyaları: {music_files}")
        else:
            print(f"HATA: Müzik klasörü bulunamadı: {music_dir}")

        # SFX klasörünü kontrol et
        sfx_dir = os.path.join("assets", "Sounds", "SFX")
        if os.path.exists(sfx_dir):
            print(f"SFX klasörü bulundu: {sfx_dir}")
            sfx_files = glob.glob(os.path.join(sfx_dir, "*.*"))
            print(f"SFX dosyaları: {sfx_files}")
        else:
            print(f"HATA: SFX klasörü bulunamadı: {sfx_dir}")

    def find_sound_files(self):
        """SFX klasöründeki tüm ses dosyalarını bul"""
        sfx_files = {}
        sfx_dir = os.path.join("assets", "Sounds", "SFX")

        if not os.path.exists(sfx_dir):
            print(f"HATA: SFX klasörü bulunamadı: {sfx_dir}")
            # Varsayılan değerleri kullan
            return {
                "attack1": os.path.join("assets", "Sounds", "SFX", "attack1.wav"),
                "bossAttack1": os.path.join("assets", "Sounds", "SFX", "bossAttack1.wav")
            }

        # Tüm ses dosyalarını bul
        sound_extensions = [".wav", ".mp3", ".ogg"]
        for ext in sound_extensions:
            for sound_file in glob.glob(os.path.join(sfx_dir, f"*{ext}")):
                # Dosya adını al (uzantısız)
                base_name = os.path.basename(sound_file)
                sound_name = os.path.splitext(base_name)[0]
                sfx_files[sound_name] = sound_file
                print(f"Ses dosyası bulundu: {sound_name} -> {sound_file}")

        # Eğer hiç ses dosyası bulunamadıysa, varsayılan değerleri kullan
        if not sfx_files:
            print("UYARI: Hiçbir ses dosyası bulunamadı. Varsayılan değerler kullanılıyor.")
            return {
                "attack1": os.path.join("assets", "Sounds", "SFX", "attack1.wav"),
                "bossAttack1": os.path.join("assets", "Sounds", "SFX", "bossAttack1.wav")
            }

        return sfx_files

    def load_sound_effects(self):
        """Ses efektlerini yükle"""
        print("\n--- SES DOSYALARI YÜKLENİYOR ---")
        print(f"Toplam {len(self.sfx_files)} ses dosyası bulundu.")

        for name, path in self.sfx_files.items():
            try:
                print(f"\nSes dosyası yükleniyor: {name} -> {path}")

                if not os.path.exists(path):
                    print(f"HATA: Dosya bulunamadı: {path}")
                    # Farklı uzantıları dene
                    found = False
                    for ext in [".wav", ".mp3", ".ogg"]:
                        base_path = os.path.splitext(path)[0]
                        alt_path = f"{base_path}{ext}"
                        if os.path.exists(alt_path):
                            print(f"Alternatif dosya bulundu: {alt_path}")
                            path = alt_path
                            found = True
                            break

                    if not found:
                        print(f"Hiçbir alternatif dosya bulunamadı {name} için.")
                        continue

                print(f"Ses yükleniyor: {path}")
                self.sfx_sounds[name] = pygame.mixer.Sound(path)
                print(f"Ses dosyası başarıyla yüklendi: {name}")
            except Exception as e:
                print(f"Ses dosyası yüklenemedi: {path} - Hata: {e}")

        print(f"\nYüklenen ses dosyaları: {list(self.sfx_sounds.keys())}")
        print("--- SES DOSYALARI YÜKLEME TAMAMLANDI ---\n")

    def play_music(self, track_name, loops=-1, fade_ms=0):
        if track_name in self.music_files and os.path.exists(self.music_files[track_name]):
            pygame.mixer.music.load(self.music_files[track_name])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            self.current_music = track_name

    def stop_music(self, fade_ms=0):
        pygame.mixer.music.fadeout(fade_ms)
        self.current_music = None

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)

        # Ses efektlerinin sesini de ayarla
        for sound in self.sfx_sounds.values():
            sound.set_volume(self.volume)

    def play_sound(self, sound_name):
        """Ses efektini çal"""
        print(f"Ses çalma isteği: {sound_name}")
        if sound_name in self.sfx_sounds:
            try:
                print(f"{sound_name} sesi çalınıyor...")
                self.sfx_sounds[sound_name].play()
                print(f"{sound_name} sesi çalındı.")
            except Exception as e:
                print(f"Ses çalınamadı: {sound_name} - Hata: {e}")
                # Ses dosyasını yeniden yüklemeyi dene
                try:
                    print(f"Ses dosyası yeniden yükleniyor: {sound_name}")
                    if sound_name in self.sfx_files and os.path.exists(self.sfx_files[sound_name]):
                        self.sfx_sounds[sound_name] = pygame.mixer.Sound(self.sfx_files[sound_name])
                        self.sfx_sounds[sound_name].play()
                        print(f"Ses dosyası yeniden yüklendi ve çalındı: {sound_name}")
                except Exception as e2:
                    print(f"Ses dosyası yeniden yüklenemedi: {sound_name} - Hata: {e2}")
        else:
            print(f"HATA: {sound_name} isimli ses bulunamadı. Yüklenen sesler: {list(self.sfx_sounds.keys())}")
            # Ses dosyasını bulmayı ve yüklemeyi dene
            try:
                sfx_dir = os.path.join("assets", "Sounds", "SFX")
                for ext in [".wav", ".mp3", ".ogg"]:
                    potential_file = os.path.join(sfx_dir, f"{sound_name}{ext}")
                    if os.path.exists(potential_file):
                        print(f"Ses dosyası bulundu ve yükleniyor: {potential_file}")
                        self.sfx_files[sound_name] = potential_file
                        self.sfx_sounds[sound_name] = pygame.mixer.Sound(potential_file)
                        self.sfx_sounds[sound_name].play()
                        print(f"Ses dosyası yüklendi ve çalındı: {sound_name}")
                        return
                print(f"Hiçbir ses dosyası bulunamadı: {sound_name}")
            except Exception as e:
                print(f"Ses dosyası yüklenemedi: {sound_name} - Hata: {e}")

    def is_music_playing(self):
        return pygame.mixer.music.get_busy()


