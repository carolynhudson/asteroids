import pygame
from constants import *
from vectorlibrary import *

class VectorText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, scale, color):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
    
        self.position = pygame.Vector2(x, y)
        self.__generated = False
        self.generate_text(text, scale)
        self.color = color
        
    def generate_text(self, text, scale):
        self.__text = text
        self.__scale = scale
        self.__generated = True
        offset = pygame.Vector2(VECTOR_TEXT_OFFSET, 0)
        self.text_vectors = [[self.position + (pygame.Vector2(*coord) + (offset * pos)) * scale for coord in VECTOR_TEXT_LOOKUP[char]] for pos, char in enumerate([c if c in VECTOR_TEXT_LOOKUP else " " for c in str.upper(text)])]
        self.text_vectors = [tv for tv in self.text_vectors if len(tv) > 0]

    def update_text(self, text):
        if text != self.__text:
            self.__text = text
            self.__generated = False

    def draw(self, screen):
        for char_vect in self.text_vectors:
            pygame.draw.lines(screen, self.color, False, char_vect, 2)
    
    def update(self, dt):
        if not self.__generated:
            self.generate_text(self.__text, self.__scale)
        
        
