import pygame
from constants import *
from circleshape import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
    
    def draw(self, screen):
        pygame.draw.circle(screen, pygame.Color(0xFFFFFF), self.position, self.radius, 2)
        return super().draw(screen)
    
    def update(self, dt):
        self.position += self.velocity * dt
        return super().update(dt)