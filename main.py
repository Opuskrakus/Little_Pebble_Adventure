import pygame
from map import Grid
import constants as const
import random


pygame.init()


class Game():
    def __init__(self):
        self.startpoint = 200,550
        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH,const.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid: Grid = Grid(40, 30, [7, 14, 21])
        self.player = Player(200, 550)
        #self.player_y = self.player.velocity[0]
        self.new_map()
        self.time_since_jump = 0
        self.value = random.choice([100, 700])
        self.goal = Goal(self.value,100)
        self.time_score = pygame.time.get_ticks()
        self.font = pygame.font.SysFont(None, 48)  # Set font and size
        self.button_font = pygame.font.SysFont(None, 36)
        self.velocity_right = 2
        self.velocity_left = -2
        
        
    
    def new_map(self):
        self.grid.new_map()
        self.grid.add_random_platform(0, 4, color=const.RED, dangerous=True)
        self.grid.add_random_platform(0, 4)
        self.grid.add_random_platform(0, 4)
        self.grid.add_random_platform(1, 4, color=const.RED, dangerous=True)
        self.grid.add_random_platform(1, 4)
        self.grid.add_random_platform(1, 4)
        self.grid.add_random_platform(2, 4, color=const.RED, dangerous=True)
        self.grid.add_random_platform(2, 4)
        self.grid.add_random_platform(2, 4)


    def dangerous_collision(self):
        self.player.health -= 1
        if self.player.health > 0:
            self.player.rect.x, self.player.rect.y = self.startpoint
            self.player.velocity[0] = 0
            self.player.velocity[1] = 0
        else:
            pass

    
    def check_collisions(self):
        grid = self.grid.get_obstacle_grid()
        self.player.on_ground = False

        # Check horizontal collisions
        self.player.rect.x += self.player.velocity[0]
        for row in grid:
            for obstacle in row:
                if obstacle is not None:
                    if self.player.rect.colliderect(pygame.Rect(obstacle.get_x(), obstacle.get_y(), obstacle.xSize, obstacle.ySize)):
                        if obstacle.is_dangerous():
                            self.dangerous_collision()
                        if self.player.velocity[0] > 0:  # Moving right
                            self.player.rect.right = obstacle.get_x()
                        elif self.player.velocity[0] < 0:  # Moving left
                            self.player.rect.left = obstacle.get_x() + obstacle.xSize
                        self.player.velocity[0] = 0

        # Check vertical collisions
        self.player.rect.y += self.player.velocity[1]
        for row in grid:
            for obstacle in row:
                if obstacle is not None:
                    if self.player.rect.colliderect(pygame.Rect(obstacle.get_x(), obstacle.get_y(), obstacle.xSize, obstacle.ySize)):
                        if obstacle.is_dangerous():
                            self.dangerous_collision()
                    if self.player.rect.colliderect(pygame.Rect(obstacle.get_x(), obstacle.get_y(), obstacle.xSize, obstacle.ySize)):
                        if self.player.velocity[1] > 0:  # Falling
                            self.player.rect.bottom = obstacle.get_y()
                            self.player.on_ground = True
                        elif self.player.velocity[1] < 0:  # Jumping
                            self.player.rect.top = obstacle.get_y() + obstacle.ySize
                        self.player.velocity[1] = 0

    def draw_player(self):
        pygame.draw.circle(self.screen, const.CYAN, self.player.rect.center, 10)

    # def draw_player(self):
    #     stone = pygame.image.load("geodude.png")
    #     pygame.draw.stone(self.screen, "geodude.png", self.player.rect.center, 10)    
    
    def draw_goal(self):
        pygame.draw.circle(self.screen,const.GOLD,self.goal.rect.center,10)
    
    def check_goal_collision(self):
        if pygame.sprite.collide_rect(self.player, self.goal):
            print("Goal reached!")
            self.score()
            self.running = False
    
    def draw_button(self, text, x, y, width, height, text_color, bg_color):
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, bg_color, button_rect)
        text_surface = self.button_font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)
        return button_rect

    def score(self):
        self.screen.fill(const.DARK_GRAY)
        score_screen = True
        # Display "You Win!!" text
        text_surface = self.font.render("You Win!!", True, const.GOLD)
        text_rect = text_surface.get_rect(center=(const.SCREEN_WIDTH // 2, const.SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(text_surface, text_rect)

        # Draw buttons
        next_button = self.draw_button("Next Level", const.SCREEN_WIDTH // 2 - 75, const.SCREEN_HEIGHT // 2 + 20, 150, 50, const.WHITE, const.GREEN)
        quit_button = self.draw_button("Quit Game", const.SCREEN_WIDTH // 2 - 75, const.SCREEN_HEIGHT // 2 + 100, 150, 50, const.WHITE, const.RED)
        pygame.display.flip()
        # Handle events
        while score_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    score_screen = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if next_button.collidepoint(event.pos):
                        self.next_level()  # Call method to go to next level
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()  # Quit the game


    def next_level(self):
        # Reinitialize player position
        self.player.rect.x, self.player.rect.y = self.startpoint
        self.player.velocity = [0, 0]  # Reset player velocity
        self.velocity_left -= 0.5
        self.velocity_right += 0.5
        # Randomize new goal position
        self.value = random.choice([100, 700])  # Randomize X-coordinate of the goal
        self.goal.rect.center = (self.value, 100)

        self.new_map()
        self.Run()

    def game_over(self):
        self.screen.fill(const.DARK_GRAY)
        game_over_screen = True
        text_surface = self.font.render("YOU LOSE", True, const.RED)
        text_rect = text_surface.get_rect(center=(const.SCREEN_WIDTH // 2, const.SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(text_surface, text_rect)

        # Draw buttons
        next_button = self.draw_button("Try Again", const.SCREEN_WIDTH // 2 - 75, const.SCREEN_HEIGHT // 2 + 20, 150, 50, const.WHITE, const.GREEN)
        quit_button = self.draw_button("Quit Game", const.SCREEN_WIDTH // 2 - 75, const.SCREEN_HEIGHT // 2 + 100, 150, 50, const.WHITE, const.RED)
        pygame.display.flip()
        # Handle events
        while game_over_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over_screen = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if next_button.collidepoint(event.pos):
                        self.next_level()  # Call method to go to next level
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()  # Quit the game


    def draw_obstacles(self):
        grid = self.grid.get_obstacle_grid()
        for row in grid:
            for obstacle in row:
                if obstacle is not None:
                    pygame.draw.rect(self.screen, obstacle.color, pygame.Rect(obstacle.get_x(), obstacle.get_y(), obstacle.xSize, obstacle.ySize))
    def update(self):
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.velocity[0] = self.velocity_left
            elif keys[pygame.K_RIGHT]:
                self.player.velocity[0] = self.velocity_right
            elif not self.player.on_ground:
                self.player.velocity[1] += self.player.gravity
            else:
                self.player.velocity[0] = 0
            
                

            if keys[pygame.K_UP] and self.player.on_ground:
                self.player.velocity[1] = -self.player.jump_strength  # Apply upward force
                self.player.on_ground = False  # Player is no longer on the ground

            elif not self.player.on_ground:
                self.player.velocity[1] += self.player.gravity  # Gravity pulls the player down
            else:
                self.player.velocity[1] = 0


            self.player.rect.move_ip(self.player.velocity)

    def Run(self):
        self.running = True
        while self.running:
            
            self.screen.fill(const.BLACK)
            self.draw_player()
            self.draw_goal()
            self.draw_obstacles()
            self.update()
            self.check_collisions()
            self.check_goal_collision()
            
            if self.player.health == 0:
                self.game_over()
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
        self.jump_strength = 10
        self.gravity = 0.3
        self.on_ground = False
        self.health = 3

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(const.GOLD)
        self.rect = self.image.get_rect(center=(x, y))
        

# class Stone(pygame.sprite.Sprite):
#     def __innit__(self, color, width, height):
#         pygame.sprite.Sprite.__innit__(self)

#         self.image = pygame.surface([width, height])    
        
       
        

if __name__ == "__main__":
    game = Game()
    game.Run()