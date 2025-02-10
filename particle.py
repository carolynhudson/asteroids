import pygame
import random
from constants import *
from circleshape import *

class Particle(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, random.uniform(*PARTICLE_SIZE_RANGE))
        self.lifeleft = PARTICLE_LIFE
        self.velocity = pygame.Vector2(0,random.uniform(200.0, 600.0)).rotate(random.randrange(0, 360))
    
    def draw(self, screen):
        pygame.draw.circle(screen, pygame.Color(int(255 * self.lifeleft), int(200 * self.lifeleft), int(200 * self.lifeleft), int(255 * self.lifeleft)), self.position, self.radius, 2)
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