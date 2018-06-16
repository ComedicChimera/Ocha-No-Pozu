import pygame
from collections import OrderedDict


AUDIO_END = pygame.USEREVENT + 1


class Sound:
    def __init__(self, sound, channel, paused):
        self.sound = sound
        self.channel = channel
        self.paused = paused


class AudioManager:
    def __init__(self):
        pygame.mixer.init(44100)
        self.pause = False
        self.sounds = OrderedDict()

    @staticmethod
    def play_music(name, volume=1, loop=False):
        if pygame.mixer.music.get_busy():
            return

        pygame.mixer.music.load('assets/sounds/' + name)

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
        if name in self.sounds:
            return

        loaded_sound = pygame.mixer.Sound('assets/sounds/' + name)

        loaded_sound.set_volume(volume)
        chan = loaded_sound.play()
        chan.set_endevent(AUDIO_END)

        self.sounds[name] = Sound(loaded_sound, chan, False)

    def stop_sound(self, name):
        if name in self.sounds:
            self.sounds[name].sound.stop()
            self._remove_sound(name)

    def _remove_sound(self, name):
        # no check necessary; called internally
        self.sounds.pop(name)

    def remove_bottom(self):
        if len(self.sounds) > 0:
            self.sounds.pop(list(self.sounds.keys())[0])

    def set_sound_pause(self, name):
        if name in self.sounds:
            self.sounds[name].paused = not self.sounds[name].paused
            if self.sounds[name].paused:
                self.sounds[name].sound.unpause()
            else:
                self.sounds[name].sound.pause()


am = AudioManager()



