# sfx.py
import pygame
import os
import constants


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None

        self.music_files = {
            "menu": os.path.join("assets", "Sounds", "menu_music.mp3"),
            "battle": os.path.join("assets", "Sounds", "battle_music.mp3")
        }

        self.volume = 0.5

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

    def is_music_playing(self):
        return pygame.mixer.music.get_busy()


