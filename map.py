from obstacle import Obstacle
import constants
import pygame
import random

class Grid():
    def __init__(self, xSize: int, ySize: int, cellWidth: int = 20, cellHeight: int = 20):
        """Creates a grid"""
        self.obstacle_grid: list[list[Obstacle]] = []
        self.xSize = xSize
        self.ySize = ySize
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.obstacle_n = 0
        self.obstacle_e = 0
        self.obstacle_s = 0
        self.obstacle_w = 0

        for y in range(ySize):
            row = []
            for x in range(xSize):
                if y == ySize - 1:
                    row.append(Obstacle(x, y, cellHeight, cellWidth, constants.DARK_GREEN))
                else:
                    row.append(None)
            self.obstacle_grid.append(row)

    def get_obstacle(self, x, y) -> Obstacle:
        return self.obstacle_grid[y][x]
    
    def get_obstacle_grid(self):
        """Get a grid"""
        return self.obstacle_grid

    def has_obstacle_at(self, x: int, y: int) -> bool:
        grid_x = int(x*self.cellWidth)
        grid_y = int(y*self.cellHeight)
        obstacle = self.obstacle_grid[grid_y][grid_x]
        self.obstacle_n = grid_y
        self.obstacle_e = grid_x + self.cellWidth
        self.obstacle_s = grid_y + self.cellHeight
        self.obstacle_w = grid_x
        return obstacle is not None

    def get_obstacle_side(self, direction: str) -> int:
        """For direction n,s,e,w get beginning of obstacle. Call has_obstacle_at first"""
        if direction == "n":
            return self.obstacle_n
        elif direction == "s":
            return self.obstacle_s
        elif direction == "e":
            return self.obstacle_e
        elif direction == "w":
            return self.obstacle_w
    

    def add_obstacles_from_list(self, double_list: list[list[int]]):
        for y in range(self.ySize):
            for x in range(self.xSize):
                if double_list[y][x] > 0:
                    self.obstacle_grid[y][x] = Obstacle(x, y, self.cellHeight, self.cellWidth, constants.DARK_GREEN)
                
    def get_random_list(self, frequency: float):
        double_list = []

        for y in range(self.ySize):
            row = []
            for x in range(self.xSize):
                if random.random() < frequency:
                    row.append(1)
                else:
                    row.append(0)
            double_list.append(row)
        return double_list