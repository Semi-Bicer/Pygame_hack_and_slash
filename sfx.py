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
            "shout": os.path.join("assets", "Sounds", "SFX", "shout.mp3"),
            "button_select": os.path.join("assets", "Sounds", "SFX", "button_select.mp3"),
            "button_highlight": os.path.join("assets", "Sounds", "SFX", "button_highlight.mp3")
        }

        self.music_volume = 0.5
        self.sfx_volume = 0.5

        self.sfx_sounds = {}
        self.load_sound_effects()

    def load_sound_effects(self):
        for name, path in self.sfx_files.items():
            self.sfx_sounds[name] = pygame.mixer.Sound(path)

    def play_music(self, track_name, loops=-1, fade_ms=0):
        if track_name in self.music_files and os.path.exists(self.music_files[track_name]):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.music_files[track_name])

            if self.music_volume <= 0.01:
                return

            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            self.current_music = track_name

    def stop_music(self, fade_ms=0):
        pygame.mixer.music.fadeout(fade_ms)
        self.current_music = None

    def set_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        self.sfx_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

        for sound in self.sfx_sounds.values():
            sound.set_volume(self.sfx_volume)

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))

        for sound_name, sound in self.sfx_sounds.items():
            sound.set_volume(self.sfx_volume)

    def play_sound(self, sound_name):
        if self.sfx_volume <= 0.01:
            return

        if sound_name in self.sfx_sounds:
            self.sfx_sounds[sound_name].set_volume(self.sfx_volume)
            self.sfx_sounds[sound_name].play()
        else:
            sfx_dir = os.path.join("assets", "Sounds", "SFX")
            potential_file = os.path.join(sfx_dir, f"{sound_name}.mp3")

            if os.path.exists(potential_file):
                self.sfx_files[sound_name] = potential_file
                sound = pygame.mixer.Sound(potential_file)
                sound.set_volume(self.sfx_volume)
                self.sfx_sounds[sound_name] = sound
                sound.play()

    def is_music_playing(self):
        return pygame.mixer.music.get_busy()
