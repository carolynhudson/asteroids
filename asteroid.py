import pygame
import random
from constants import *
from circleshape import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        #randomize asteroid rotation rate
        self.rotation = 0
        self.rotation_rate = random.uniform(-30,30)

        # make the randomized asteroid polygon from 10 to 15 vector points degrees is the base spacing +/- between 0.49 of degrees and the distance from the center 0.8 to 1.1 times the radius.
        degrees = 360 // random.randrange(10,15)
        self.shape = [pygame.Vector2(0,self.radius * random.uniform(0.8,1.1)).rotate(angle + random.uniform(degrees * -0.49, degrees * 0.49)) for angle in range(0, 360, degrees)]
             
    def draw(self, screen):
        # Update the asteroid's base polygon to match the new position and rotation
        rockpoly = [self.position + vector.rotate(self.rotation) for vector in self.shape]
        # Drawn the polygon
        pygame.draw.polygon(screen, pygame.Color(200, 200, 200), rockpoly, 2)
        return super().draw(screen)
    
    def update(self, dt):
        # Update asteroid position and rotation
        self.position += self.velocity * dt
        self.rotation += self.rotation_rate * dt
        
        # Wrap the asteroids to the other side of the screen if they cross over the spawn boundry just outside the screen
        self.position.x = ((self.position.x + ASTEROID_MAX_RADIUS + BOUNDRY_WIDTH * 2) % BOUNDRY_WIDTH) - ASTEROID_MAX_RADIUS
        self.position.y = ((self.position.y + ASTEROID_MAX_RADIUS + BOUNDRY_HEIGHT * 2) % BOUNDRY_HEIGHT) - ASTEROID_MAX_RADIUS
        return super().update(dt)
    
    def split(self, shot_velocity: pygame.Vector2):
        self.kill()
        if self.radius > ASTEROID_MIN_RADIUS:
            # Determine shot travel angle
            split_root_angle = shot_velocity.as_polar()[1]

            # Offset split spawn locations to the left and right of the orginal asteroid's center perpendicular to the shot angle
            new_size = self.radius - ASTEROID_MIN_RADIUS
            position_offset = pygame.Vector2(0,1).rotate(split_root_angle) * new_size * 1.1
            first_pos = self.position + position_offset
            second_pos = self.position - position_offset

            # Spawn new asteroids
            first_rock = Asteroid(first_pos.x, first_pos.y, new_size)
            second_rock = Asteroid(second_pos.x, second_pos.y, new_size)

            # Set new asteroid velocities based on the former asteroid's velocity
            split_angle =  random.uniform(20, 50)
            first_rock.velocity = self.velocity.rotate(split_angle) * 1.2
            second_rock.velocity = self.velocity.rotate(-split_angle) * 1.2
        return ASTEROID_MAX_RADIUS - self.radius + ASTEROID_MIN_RADIUS

            