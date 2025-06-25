import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "hatch": pygame.mixer.Sound("sfx/hatching.wav"),
            "attention": pygame.mixer.Sound("sfx/attention.wav"),
            "start": pygame.mixer.Sound("sfx/game-start.wav"),
            "death": pygame.mixer.Sound("sfx/death.wav")
        }

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    