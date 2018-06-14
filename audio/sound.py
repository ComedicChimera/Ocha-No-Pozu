import pygame
from functools import partial


class Sound:
    def __init__(self, sound, paused):
        self.sound = sound
        self.paused = paused


class AudioManager:
    def __init__(self):
        pygame.mixer.init(44100)
        self.pause = False
        self.sounds = {}

    @staticmethod
    def play_music(name, volume=1, loop=False):
        if pygame.mixer.music.get_busy():
            return

        pygame.mixer.music.load(name)

        pygame.mixer.music.set_volume(volume)

        if loop:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.play()

    def set_pause(self):
        self.pause = not self.pause
        if self.pause:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    @staticmethod
    def stop_music():
        pygame.mixer.music.stop()

    def play_sound(self, name, volume=1):
        loaded_sound = pygame.mixer.Sound(name)

        loaded_sound.set_volume(volume)
        loaded_sound.play().set_endevent(partial(self._remove_sound, name))

        self.sounds[name] = Sound(loaded_sound, False)

    def stop_sound(self, name):
        if name in self.sounds:
            self.sounds[name].sound.stop()
            self._remove_sound(name)

    def _remove_sound(self, name):
        # no check necessary; called internally
        self.sounds.pop(name)

    def set_sound_pause(self, name):
        if name in self.sounds:
            self.sounds[name].paused = not self.sounds[name].paused
            if self.sounds[name].paused:
                self.sounds[name].sound.unpause()
            else:
                self.sounds[name].sound.pause()






