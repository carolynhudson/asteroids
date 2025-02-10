import pygame
from constants import *
from circleshape import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.lifeleft = SHOT_LIFESPAN
    
    def draw(self, screen):
        pygame.draw.circle(screen, pygame.Color(255,255,0), self.position, self.radius, 2)
        return super().draw(screen)
    
    def update(self, dt):
        self.lifeleft -= dt
        if self.lifeleft > 0:
            self.position += self.velocity * dt
            self.position.x = (self.position.x + SCREEN_WIDTH * 4) % SCREEN_WIDTH
            self.position.y = (self.position.y + SCREEN_HEIGHT * 4) % SCREEN_HEIGHT
        else:
            self.kill()

        return super().update(dt)