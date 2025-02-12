import pygame
from constants import *
from circleshape import *

class Shot(CircleShape):
    def __init__(self, shooter_pos, shooter_size, shot_angle, hurts_player: bool = False):
        self.hurts_player = hurts_player
        self.lifeleft = SHOT_LIFESPAN
        shot_dist = shooter_size + SHOT_RADIUS + 1
        shot_pos = shooter_pos + pygame.Vector2(shot_dist if hurts_player else 0, 0 if hurts_player else shot_dist).rotate(shot_angle)
        super().__init__(shot_pos.x, shot_pos.y, SHOT_RADIUS)
    
    def draw(self, screen):
        pygame.draw.circle(screen, pygame.Color(0 ,255,0) if self.hurts_player else pygame.Color(255, 255, 0), self.position, self.radius, 2)
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