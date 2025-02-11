import pygame
import random
from constants import *
from circleshape import *
from randompolygon import RandomPolygon

class Particle(CircleShape):
    def __init__(self, x, y, size: float = random.uniform(*PARTICLE_SIZE_RANGE)):
        super().__init__(x, y, size)
        self.lifeleft = PARTICLE_LIFE
        
        # Randomize the particle speed and direction
        self.velocity = pygame.Vector2(0,random.uniform(200.0, 600.0)).rotate(random.randrange(0, 360))
        self.shape = RandomPolygon(3, 5, self.radius * 0.5, self.radius * 2.0)
        self.rotation_rate = random.uniform(-300, 300)
        self.rotation = 0

    def draw(self, screen):
        poly = self.shape.translate(self.position, self.rotation)
        pygame.draw.polygon(screen, pygame.Color(int(255 * self.lifeleft), int(200 * self.lifeleft), int(200 * self.lifeleft), int(255 * self.lifeleft)), poly, 1)
        return super().draw(screen)
    
    def update(self, dt):
        self.lifeleft -= dt
        if self.lifeleft > 0:
            self.position += self.velocity * dt
            self.rotation += self.rotation_rate * dt
            self.position.x = (self.position.x + SCREEN_WIDTH * 4) % SCREEN_WIDTH
            self.position.y = (self.position.y + SCREEN_HEIGHT * 4) % SCREEN_HEIGHT
        else:
            self.kill()

        return super().update(dt)