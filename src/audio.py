import os
import pygame

from src.settings import ASSETS_DIR


class AudioManager:
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        self.music_path = os.path.join(ASSETS_DIR, "audio", "background.mp3")

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            print("Audio disabled: mixer could not be initialized")

        if self.enabled:
            self._load_sounds()

    def _load_sounds(self):
        sound_files = {
            "dot": "eat_dot.mp3",
            "death": "death.mp3",
            "game_over": "game_over.mp3",
            "level_complete": "level_complete.mp3",
        }

        for name, filename in sound_files.items():
            path = os.path.join(ASSETS_DIR, "audio", filename)
            if os.path.exists(path):
                self.sounds[name] = pygame.mixer.Sound(path)

    def play_sound(self, name):
        if not self.enabled:
            return

        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def play_music(self):
        if not self.enabled or not os.path.exists(self.music_path):
            return

        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.play(-1)

    def stop_music(self):
        if self.enabled:
            pygame.mixer.music.stop()