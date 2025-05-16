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

        self.volume = 0.5

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
        # Animasyon adıyla eşleşen ses dosyasını çal
        if sound_name in self.sfx_sounds:
            self.sfx_sounds[sound_name].play()
        else:
            # Ses dosyasını bulmayı ve yüklemeyi dene
            sfx_dir = os.path.join("assets", "Sounds", "SFX")
            potential_file = os.path.join(sfx_dir, f"{sound_name}.mp3")

            if os.path.exists(potential_file):
                # Dosyayı yükle ve çal
                self.sfx_files[sound_name] = potential_file
                self.sfx_sounds[sound_name] = pygame.mixer.Sound(potential_file)
                self.sfx_sounds[sound_name].play()

    def is_music_playing(self):
        return pygame.mixer.music.get_busy()
