import pygame
import random

class RandomPolygon:
    def __init__(self, min_point_count: int = 3, max_point_count : int = 15, min_vertex_dist: float = 0.8, max_vertex_dist: float = 1.1):
        degrees = 360 // random.randrange(min_point_count, max_point_count)
        self.__shape = [pygame.Vector2(0,random.uniform(min_vertex_dist, max_vertex_dist)).rotate(angle + random.uniform(-degrees / 2.1, degrees / 2.1)) for angle in range(0, 360, degrees)]
    
    def translate(self, position : pygame.Vector2, rotation_angle: float, scale: float = 1.0):
        return [position + (vector.rotate(rotation_angle) * scale) for vector in self.__shape]