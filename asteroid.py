import pygame
import random
from constants import *
from circleshape import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
       
    def draw(self, screen):
        pygame.draw.circle(screen, pygame.Color(0xFFFFFF), self.position, self.radius, 2)
        return super().draw(screen)
    
    def update(self, dt):
        self.position += self.velocity * dt
        return super().update(dt)
    
    def split(self):
        self.kill()
        if self.radius > ASTEROID_MIN_RADIUS:
            split_angle = random.uniform(20, 50)
            first_rock = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
            second_rock = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
            first_rock.velocity = self.velocity.rotate(split_angle) * 1.2
            second_rock.velocity = self.velocity.rotate(-split_angle) * 1.2

            