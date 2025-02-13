import pygame
from constants import *

class Audio(pygame.sprite.Sprite):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Audio, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.__audio_enabled = False
        self.__sounds = {}
        self.__thrust_channel = None
        self.__saucer_channel = None
        self.__beat_channel = None
        self.thrust_sound = None
        self.saucer_sounds = None
        self.beats = None
        self.thrust_playing = False
        self.saucer_playing = False
        self.bangs = None
        self.shot_sound = None
        self.extra_life_sound = None

        if USE_AUDIO:
            try:
                pygame.mixer.init(channels=16)
                self.__audio_enabled = True
                    
            except Exception as e:
                print("Unable to initialize pygame audio system...")
                print(e)
            
            if self.__audio_enabled:
                for name, file in SOUND_FILES:
                    try:
                        self.__sounds[name] = pygame.mixer.Sound(file=f"{SOUND_FILES_PATH}{file}")
                    except Exception as e:
                        print(f"Error unable to load sound {name} from '{SOUND_FILES_PATH}{file}':")
                        print(e)
                
                pygame.mixer.set_reserved(3)

                self.__thrust_channel = pygame.mixer.Channel(0)
                self.__saucer_channel = pygame.mixer.Channel(1)
                self.__beat_channel = pygame.mixer.Channel(3)
                self.thrust_sound = self.__sounds.get("thrust", None)
                self.saucer_sounds = (self.__sounds.get("saucer_small", self.__sounds.get("saucer_big", None)), 
                                      self.__sounds.get("saucer_big", self.__sounds.get("saucer_small", None)))
                self.beats = (self.__sounds.get("beat1", self.__sounds.get("beat2", None)), self.__sounds.get("beat2", self.__sounds.get("beat1", None)))
                self.bangs = (self.__sounds.get("bang_small", self.__sounds.get("bang_medium", self.__sounds.get("bang_large", None))),
                              self.__sounds.get("bang_medium", self.__sounds.get("bang_small", self.__sounds.get("bang_large", None))),
                              self.__sounds.get("bang_large", self.__sounds.get("bang_medium", self.__sounds.get("bang_small", None))))
                self.shot_sound = self.__sounds.get("shoot", None)
                self.extra_life_sound = self.__sounds.get("extra_ship", None)
    
    def start_thrust(self):
        if self.__audio_enabled and self.thrust_sound is not None:
            if not self.__thrust_channel.get_busy():
                self.__thrust_channel.play(self.thrust_sound, -1)
                self.thrust_playing = True

    def stop_thrust(self):
        if self.__audio_enabled and self.thrust_sound is not None:
            if self.__thrust_channel.get_busy():
                self.__thrust_channel.stop()
                self.thrust_playing = False

    def start_saucer(self, small: bool):
        if self.__audio_enabled and self.saucer_sounds is not None:
            sound = self.saucer_sounds[0] if small else self.saucer_sounds[1]
            if not self.__saucer_channel.get_busy():
                self.__saucer_channel.play(sound, -1)
                self.saucer_playing = True

    def stop_saucer(self):
        if self.__audio_enabled and self.saucer_sounds is not None:
            if self.__saucer_channel.get_busy():
                self.__saucer_channel.stop()
                self.saucer_playing = False

    def play_sound(self, sound_name: str):
        if self.__audio_enabled:
            sound = self.__sounds.get(sound_name, None)
            channel = pygame.mixer.find_channel()
            if sound is not None and channel is not None:
                channel.play(sound)

    def shoot(self):
        if self.__audio_enabled:
            channel = pygame.mixer.find_channel()
            if self.shot_sound is not None and channel is not None:
                channel.play(self.shot_sound)

    def extra_life(self):
        if self.__audio_enabled:
            channel = pygame.mixer.find_channel()
            if self.extra_life_sound is not None and channel is not None:
                channel.play(self.extra_life_sound)

    def bang(self, size: int):
        if self.__audio_enabled and self.bangs is not None:
            sound = self.bangs[size]
            channel = pygame.mixer.find_channel()
            if sound is not None and channel is not None:
                channel.play(sound)
