import pygame
from map import Grid
import constants as const
import time
import sys


pygame.init()


class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH,const.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player_surface = pygame.Surface((200, 150))
        self.grid: Grid = Grid(40, 30)
        self.player = Player(200,200)
        self.player_y = self.player.velocity[0]
        self.grid.add_obstacles_from_list(self.grid.get_random_list(0.05))
        self.time_since_jump = 0
    
    def check_collisions(self):
        grid = self.grid.get_obstacle_grid()
        #self.player.on_ground = False
        for row in grid:
            for obstacle in row:
                if obstacle is not None:
                    if self.player.rect.colliderect(pygame.Rect(obstacle.get_x(), obstacle.get_y(), obstacle.xSize, obstacle.ySize)):
                        if self.player.velocity[1] > 0:  # Falling
                            self.player.rect.bottom = obstacle.get_y()
                            self.player.velocity[1] = 0
                            self.player.on_ground = True
                        elif self.player.velocity[1] < 0:  # Jumping
                            self.player.rect.top = obstacle.get_y() + obstacle.ySize
                            self.player.velocity[1] = 0
                        # Horizontal collision
                        if self.player.velocity[0] > 0:  # Moving right
                            self.player.rect.right = obstacle.get_x()
                        elif self.player.velocity[0] < 0:  # Moving left
                            self.player.rect.left = obstacle.get_x() + obstacle.xSize

    def draw_player(self):
        pygame.draw.circle(self.screen, const.CYAN, self.player.rect.center, 10)
    
    
    def draw_obstacles(self):
        grid = self.grid.get_obstacle_grid()
        for row in grid:
            for obstacle in row:
                if obstacle is not None:
                    pygame.draw.rect(self.screen, obstacle.color, pygame.Rect(obstacle.get_x(), obstacle.get_y(), obstacle.xSize, obstacle.ySize))
    def update(self):
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.velocity[0] = -5
            elif keys[pygame.K_RIGHT]:
                self.player.velocity[0] = 5
            else:
                self.player.velocity[0] = 0

            if keys[pygame.K_UP]:
                self.player.velocity[1] = -5
                self.player.jump_strength = 0


            elif keys[pygame.K_DOWN]:
                self.player.velocity[1] = 5
            else:
                self.player.velocity[1] = 5
                self.player.velocity[0] = 0

            self.player.rect.move_ip(self.player.velocity)

    def Run(self):
        while self.running:
            
            self.screen.fill(const.BLACK)
            self.draw_player()
            self.draw_obstacles()
            self.update()
            self.player_y += self.player.gravity # "y pretty sure"
            self.check_collisions()
            current_time = pygame.time.get_ticks()
            self.player.jump_strength 
            if self.time_since_jump >= 10:
                self.player.jump_strength += 1
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                        
                        
            pygame.display.flip()
            self.clock.tick(60)
        
    



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(const.CYAN)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = [0, 0]
        self.jump_strength = 30
        self.gravity = 0.3
        

    
       
        

if __name__ == "__main__":
    game = Game()
    game.Run()