import pygame

class Polygon:
    def __init__(self, points: list, scale: float):
        if len(points) > 0:
            if type(points[0]) is tuple:
                self.__shape = [pygame.Vector2(x,y) * scale for x,y in points]
            else:
                self.__shape = [v * scale for v in points]
        else:
            self.__shape = []

    
    def translate(self, position : pygame.Vector2, rotation_angle: float, scale: float = 1.0):
        return [position + (vector.rotate(rotation_angle) * scale) for vector in self.__shape]