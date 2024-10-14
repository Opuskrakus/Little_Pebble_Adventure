import pygame
pygame.init()
class Obstacle():
    def __init__(self, x: int, y: int, xSize: int, ySize: int, color: tuple, dangerous: bool = False):
        self.x = x
        self.y = y
        self.xSize = xSize
        self.ySize = ySize
        self.color = color
        self.dangerous = dangerous
        self.obstacle_n = y*ySize
        self.obstacle_e = (x+1) * xSize
        self.obstacle_s = (y+1) * ySize
        self.obstacle_w = x*xSize

    def get_x(self):
        return self.x * self.xSize
    
    def get_y(self):
        return self.y * self.ySize

    def get_side(self, direction: str):
        if direction == "n":
            return self.obstacle_n
        if direction == "e":
            return self.obstacle_e
        if direction == "s":
            return self.obstacle_s
        if direction == "w":
            return self.obstacle_w

    def is_dangerous(self) -> bool:
        return self.dangerous