import pygame
import random
from constants import *
from circleshape import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.rotation_rate = random.uniform(-30,30)
        degrees = 360 // random.randrange(10,15)
        self.shape = [pygame.Vector2(0,self.radius * random.uniform(0.8,1.1)).rotate(angle + random.uniform(degrees * -0.49, degrees * 0.49)) for angle in range(0, 360, degrees)]
             
    def draw(self, screen):
        rockpoly = [self.position + vector.rotate(self.rotation) for vector in self.shape]
        pygame.draw.polygon(screen, pygame.Color(200, 200, 200), rockpoly, 2)
        return super().draw(screen)
    
    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.rotation_rate * dt
        
        self.position.x = ((self.position.x + ASTEROID_MAX_RADIUS + BOUNDRY_WIDTH * 2) % BOUNDRY_WIDTH) - ASTEROID_MAX_RADIUS
        self.position.y = ((self.position.y + ASTEROID_MAX_RADIUS + BOUNDRY_HEIGHT * 2) % BOUNDRY_HEIGHT) - ASTEROID_MAX_RADIUS
        return super().update(dt)
    
    def split(self, shot_velocity: pygame.Vector2):
        self.kill()
        if self.radius > ASTEROID_MIN_RADIUS:
            split_root_angle = shot_velocity.as_polar()[1]
            new_size = self.radius - ASTEROID_MIN_RADIUS
            position_offset = pygame.Vector2(0,1).rotate(split_root_angle + 90) * new_size * 1.1
            first_pos = self.position + position_offset
            second_pos = self.position - position_offset
            first_rock = Asteroid(first_pos.x, first_pos.y, new_size)
            second_rock = Asteroid(second_pos.x, second_pos.y, new_size)
            split_angle =  random.uniform(20, 50)
            first_rock.velocity = self.velocity.rotate(split_root_angle + split_angle) * 1.2
            second_rock.velocity = self.velocity.rotate(split_root_angle - split_angle) * 1.2
        return ASTEROID_MAX_RADIUS - self.radius + ASTEROID_MIN_RADIUS

            