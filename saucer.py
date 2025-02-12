import pygame
import random
import math
from constants import *
from circleshape import *
from polygon import Polygon
from particle import Particle
from shot import Shot

class Saucer(CircleShape):

    def __init__(self, x, y, radius, player_group):
        super().__init__(x, y, radius)

        self.rotation = 0
        self.gun_cooldown = SAUCER_INITIAL_SHOOT_COOLDOWN
        self.player_group = player_group
        self.hurts_player = True

        # make the randomized asteroid polygon from 10 to 15 vector points degrees is the base spacing +/- between 0.49 of degrees and the distance from the center 0.8 to 1.1 times the radius.
        self.shape = Polygon(SAUCER_POLYGON, radius)
             
    def shoot(self):
        player = random.choice(list(self.player_group))
        player_distance = self.position.distance_to(player.position)
        if player_distance < SAUCER_SHOOT_MAX_DISTANCE:
            self.gun_cooldown = SAUCER_SHOOT_COOLDOWN
            angle_to_player = ((player.position + player.velocity * (player_distance / SAUCER_SHOT_SPEED)) - self.position).as_polar()[1] + random.uniform(-SAUCER_SHOT_ANGLE_VARIANCE, SAUCER_SHOT_ANGLE_VARIANCE)
            new_shot = Shot(self.position, self.radius, angle_to_player, True)            
            new_shot.velocity = pygame.Vector2(1, 0).rotate(angle_to_player) * SAUCER_SHOT_SPEED #
            #self.gun_sound.play()

    def got_shot(self, shot_velocity: pygame.Vector2):
        # Generate a spray of temporary particles
        for i in range(random.randrange(*PARTICLE_COUNT_RANGE)):
            Particle(self.position.x, self.position.y, random.uniform(2.0, 10.0))

        self.kill()
        return 1000 if self.radius == min(SAUCER_RADIUS_SIZES) else 500

    def draw(self, screen):
        # Update the asteroid's base polygon to match the new position and rotation
        poly = self.shape.translate(self.position, self.rotation)

        # Drawn the polygon
        pygame.draw.polygon(screen, pygame.Color(200, 200, 200), poly, 2)
        return super().draw(screen, SAUCER_SHOW_HITBOX)
    
    def update(self, dt):
        if self.gun_cooldown > 0:
            self.gun_cooldown -= dt
        elif len(self.player_group) > 0 and random.uniform(0.0, 100.0) <= SAUCER_SHOT_CHANCE:
            self.shoot()

        # Update asteroid position and rotation
        self.position += self.velocity * dt
        
        # Wrap the asteroids to the other side of the screen if they cross over the spawn boundry just outside the screen
        self.position.x = ((self.position.x + ASTEROID_MAX_RADIUS + BOUNDRY_WIDTH * 2) % BOUNDRY_WIDTH) - ASTEROID_MAX_RADIUS
        self.position.y = ((self.position.y + ASTEROID_MAX_RADIUS + BOUNDRY_HEIGHT * 2) % BOUNDRY_HEIGHT) - ASTEROID_MAX_RADIUS
        return super().update(dt)
    