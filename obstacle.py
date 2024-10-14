import pygame
pygame.init()
class Obstacle():
    def __init__(self, x: int, y: int, xSize: int, ySize: int, color: tuple):
        self.x = x
        self.y = y
        self.xSize = xSize
        self.ySize = ySize
        self.color = color

    def get_x(self):
        return self.x * self.xSize
    
    def get_y(self):
        return self.y * self.ySize    