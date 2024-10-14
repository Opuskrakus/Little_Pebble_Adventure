from obstacle import Obstacle
import constants
import random

class Grid():
    def __init__(self, xSize: int, ySize: int, line_placements: list[int],
                 cellWidth: int = 20, cellHeight: int = 20, platform_length: int = 4):
        """Creates a grid"""
        self.obstacle_grid: list[list[Obstacle]] = []
        self.xSize = xSize
        self.ySize = ySize
        self.line_placements = line_placements
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.platform_length = platform_length
        self.obstacle_n = 0
        self.obstacle_e = 0
        self.obstacle_s = 0
        self.obstacle_w = 0
        self.new_map()

    def get_obstacle(self, x, y) -> Obstacle:
        return self.obstacle_grid[y][x]
    
    def get_obstacle_grid(self):
        """Get a grid"""
        return self.obstacle_grid

    def get_obstacle_at(self, x: int, y: int) -> Obstacle:
        grid_x = int(x / self.cellWidth)
        grid_y = int(y / self.cellHeight)
        obstacle = self.obstacle_grid[grid_y][grid_x]
        return obstacle

    def new_map(self):
        self.obstacle_grid = []

        for y in range(self.ySize):
            row = []
            for x in range(self.xSize):
                if y == self.ySize - 1:
                    row.append(Obstacle(x, y, self.cellHeight, self.cellWidth, constants.DARK_GREEN))
                # elif y == 0:
                #     row.append(Obstacle(x, y, self.cellHeight, self.cellWidth, constants.DARK_GREEN))
                elif x == 0:
                    row.append(Obstacle(x, y, self.cellHeight, self.cellWidth, constants.DARK_GREEN))
                elif x == self.xSize - 1:
                    row.append(Obstacle(x, y, self.cellHeight, self.cellWidth, constants.DARK_GREEN))
                else:
                    row.append(None)
            self.obstacle_grid.append(row)

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
    
    def add_random_platform(self, line: int, platform_length: int,
                            color: tuple = constants.DARK_GREEN, dangerous: bool = False):
        row = self.line_placements[line]
        obstacle_row = self.obstacle_grid[row]
        success = False

        while success == False:
            start_x = random.randrange(0, self.xSize - platform_length)
            end_x = start_x + platform_length
            success = True

            for index in range(start_x - 1, end_x + 1):
                if index < 0 or index == self.xSize:
                    continue
                elif obstacle_row[index] is not None:
                    success = False
                    break
            
            if success:
                for index in range(start_x, end_x):
                    obstacle_row[index] = Obstacle(
                        index, row, self.cellHeight, self.cellWidth, color, dangerous)
