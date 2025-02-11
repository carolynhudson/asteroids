import pygame
import random
import math
from constants import *
from circleshape import *
from randompolygon import RandomPolygon

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        self.mass = math.pi * self.radius * self.radius * random.uniform(0.4, 1.0)

        #randomize asteroid rotation rate
        self.rotation = 0
        self.rotation_rate = random.uniform(-30,30)

        # make the randomized asteroid polygon from 10 to 15 vector points degrees is the base spacing +/- between 0.49 of degrees and the distance from the center 0.8 to 1.1 times the radius.
        self.shape = RandomPolygon(10, 15, self.radius * 0.8, self.radius * 1.1)
             
    def draw(self, screen):
        # Update the asteroid's base polygon to match the new position and rotation
        rockpoly = self.shape.translate(self.position, self.rotation)

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
            position_offset = pygame.Vector2(0,1).rotate(split_root_angle) * (new_size + 2)
            first_pos = self.position + position_offset
            second_pos = self.position - position_offset

            # Spawn new asteroids
            first_rock = Asteroid(first_pos.x, first_pos.y, new_size)
            second_rock = Asteroid(second_pos.x, second_pos.y, new_size)
            

            # Set new asteroid velocities based on the former asteroid's velocity
            split_angle =  random.uniform(20, 50)
            v_mult = (4 - new_size // ASTEROID_MIN_RADIUS) / 2
            first_rock.velocity = self.velocity + pygame.Vector2(0,random.uniform(30.0, 60.0) * v_mult).rotate(split_root_angle + random.uniform(-10.0, 10.0))
            second_rock.velocity = self.velocity - pygame.Vector2(0,random.uniform(30.0, 60.0) * v_mult).rotate(split_root_angle + random.uniform(-10.0, 10.0))
        return ASTEROID_MAX_RADIUS - self.radius + ASTEROID_MIN_RADIUS
    
    def collide(self, other: CircleShape):
        #Compute new velocities for both objects
        self.velocity = (self.velocity - (2 * other.mass / (self.mass + other.mass)) * pygame.math.Vector2.project((self.velocity - other.velocity), (self.position - other.position))) * random.uniform(0.85, 0.99)
        other.velocity = (other.velocity - (2 * self.mass / (self.mass + other.mass)) * pygame.math.Vector2.project((other.velocity - self.velocity), (other.position - self.position))) * random.uniform(0.85, 0.99)

        #Check if objects are "inside" each other and reposition them outside with a little saftey margin along the line formed between their centers.
        distance = self.position.distance_to(other.position)
        pos_correction = (self.radius + other.radius + 4) - distance
        if pos_correction > 0:
            correction_vec = (self.position - other.position) * (pos_correction / distance)
            self.position += correction_vec
            other.position -= correction_vec
        


            