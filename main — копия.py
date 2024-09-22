import pygame
import random
import time

pygame.init()

# Constants
WIDTH = 720
HEIGHT = 480

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
DarkGreen = (0, 100, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)

# Set up the display
sr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')
icon = pygame.image.load('favicon.png')
pygame.display.set_icon(icon)

# Frames per second
fps = 10
clock = pygame.time.Clock()

# Snake settings
speed = 15
size = 15

# Fonts
f1 = pygame.font.Font(None, 36)
game_over_text = f1.render("Game Over", True, Red)

# Main Menu
def main_menu():
    menu = True
    selected = 'start'
    while menu:
        sr.fill(DarkGreen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                if event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        return True
                    else:
                        return False

        f1 = pygame.font.SysFont("Comic Sans MS", 90)
        title = f1.render("Snake game", True, Yellow)
        f2 = pygame.font.SysFont("Comic Sans MS", 75)
        if selected == 'start':
            start = f2.render("START", True, Black)
        else:
            start = f2.render("START", True, Yellow)
        if selected == 'quit':
            quit_text = f2.render("QUIT", True, Black)
        else:
            quit_text = f2.render("QUIT", True, Yellow)

        sr.blit(title, (WIDTH / 2 - 300, 80))
        sr.blit(start, (WIDTH / 2, 200))
        sr.blit(quit_text, (WIDTH / 2, 300))

        pygame.display.update()
        clock.tick(fps)

class Snake:
    def __init__(self, x, y, color, speed, size):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.size = size
        self.dir_x = 0
        self.dir_y = 0
        self.count = 1
        self.heads = []
        self.add_head()

    def add_head(self):
        self.heads.append(Snake_head(self.x, self.y, self.color, self.speed, self.size))

    def remove_head(self):
        if len(self.heads) > self.count:
            self.heads.pop(0)

    def draw(self, screen):
        for head in self.heads:
            head.draw(screen)

    def move(self):
        if self.dir_x == 1:
            self.x += self.speed
        if self.dir_x == -1:
            self.x -= self.speed
        if self.dir_y == 1:
            self.y += self.speed
        if self.dir_y == -1:
            self.y -= self.speed
        self.add_head()
        self.remove_head()

    def move_right(self):
        if self.count == 1 or self.dir_y != 0:
            self.dir_x = 1
            self.dir_y = 0

    def move_left(self):
        if self.count == 1 or self.dir_y != 0:
            self.dir_x = -1
            self.dir_y = 0

    def move_down(self):
        if self.count == 1 or self.dir_x != 0:
            self.dir_x = 0
            self.dir_y = 1

    def move_up(self):
        if self.count == 1 or self.dir_x != 0:
            self.dir_x = 0
            self.dir_y = -1

    def check_walls(self):
        if self.x < 0 or self.y < 0 or self.y >= HEIGHT or self.x >= WIDTH:
            return False
        return True

    def check_snake(self):
        for i in range(len(self.heads) - 1):
            if self.x == self.heads[i].x and self.y == self.heads[i].y:
                return False
        return True

    def check_food(self, food_x, food_y):
        if self.x == food_x and self.y == food_y:
            self.count += 1
            return True
        return False

class Snake_head:
    def __init__(self, x, y, color, speed, size):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.size = size

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

# Game initialization
is_key_right = False
is_key_left = False
is_key_down = False
is_key_top = False

food_x = 150
food_y = 150

snake = Snake(3 * speed, 3 * speed, Red, speed, size)

is_game_active = main_menu()

# Main game loop
while is_game_active:
    sr.fill(DarkGreen)

    f2 = pygame.font.Font(None, 36)
    score_text = f2.render(str(snake.count), True, Green)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                is_key_right = True
            if event.key == pygame.K_LEFT:
                is_key_left = True
            if event.key == pygame.K_UP:
                is_key_top = True
            if event.key == pygame.K_DOWN:
                is_key_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                is_key_right = False
            if event.key == pygame.K_LEFT:
                is_key_left = False
            if event.key == pygame.K_UP:
                is_key_top = False
            if event.key == pygame.K_DOWN:
                is_key_down = False

    if is_key_right:
        snake.move_right()
    if is_key_left:
        snake.move_left()
    if is_key_top:
        snake.move_up()
    if is_key_down:
        snake.move_down()

    snake.move()
    is_game_active = snake.check_walls() and snake.check_snake()
    is_eat = snake.check_food(food_x, food_y)
    snake.draw(sr)
    if is_eat:
        is_repeat = True
        while is_repeat:
            is_repeat = False
            food_x = random.randint(0, (WIDTH - size) // size) * size
            food_y = random.randint(0, (HEIGHT - size) // size) * size
            for snake_head in snake.heads:
                if food_x == snake_head.x and food_y == snake_head.y:
                    is_repeat = True

    sr.blit(score_text, (0, 0))
    pygame.draw.rect(sr, Blue, (food_x, food_y, size, size))
    pygame.display.update()
    clock.tick(fps)

# Game over screen
sr.blit(game_over_text, (250, 200))
pygame.display.update()
time.sleep(2)
pygame.quit()
