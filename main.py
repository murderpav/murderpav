import pygame
import random
import time

pygame.init()

# Constants
WIDTH, HEIGHT = 720, 480
COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "dark_green": (0, 100, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0)
}
FPS = 10
SPEED = 15
SIZE = 30  # Increase size to scale the head image

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')
icon = pygame.image.load('favicon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Load images
head_img = pygame.image.load('head.png').convert_alpha()
head_img = pygame.transform.scale(head_img, (SIZE, SIZE))
food_img = pygame.image.load('food.png').convert_alpha()
food_img = pygame.transform.scale(food_img, (SIZE, SIZE))

# Fonts
font_large = pygame.font.SysFont("Comic Sans MS", 90)
font_medium = pygame.font.SysFont("Comic Sans MS", 75)
font_small = pygame.font.Font(None, 36)

# Load sounds
eat_sound = pygame.mixer.Sound('eat.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')

class Snake:
    def __init__(self, x, y, color, speed, size):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.size = size
        self.direction = (0, 0)
        self.length = 1
        self.body = [SnakeSegment(x, y, color, size, is_head=True)]

    def add_segment(self):
        self.body.append(SnakeSegment(self.x, self.y, self.color, self.size))

    def remove_tail(self):
        if len(self.body) > self.length:
            self.body.pop(0)

    def draw(self, surface):
        for segment in self.body:
            segment.draw(surface)

    def move(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        self.add_segment()
        self.remove_tail()
        self.body[-1].is_head = True
        if len(self.body) > 1:
            self.body[-2].is_head = False

    def change_direction(self, x, y):
        if self.direction == (0, 0) or (self.direction[0] != x and self.direction[1] != y):
            self.direction = (x, y)

    def check_boundaries(self):
        return 0 <= self.x < WIDTH and 0 <= self.y < HEIGHT

    def check_self_collision(self):
        return all(self.x != segment.x or self.y != segment.y for segment in self.body[:-1])

    def check_food_collision(self, food_x, food_y):
        if self.x == food_x and self.y == food_y:
            self.length += 1
            eat_sound.play()
            return True
        return False

class SnakeSegment:
    def __init__(self, x, y, color, size, is_head=False):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.is_head = is_head

    def draw(self, surface):
        if self.is_head:
            surface.blit(head_img, (self.x, self.y))
        else:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

def main_menu():
    menu_active = True
    selected_option = 'start'
    while menu_active:
        screen.fill(COLORS["dark_green"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = "start"
                elif event.key == pygame.K_DOWN:
                    selected_option = "quit"
                elif event.key == pygame.K_RETURN:
                    return selected_option == "start"

        render_text(screen, font_large, "Snake game", COLORS["yellow"], WIDTH / 2 - 300, 80)
        render_text(screen, font_medium, "START", COLORS["black"] if selected_option == 'start' else COLORS["yellow"], WIDTH / 2 - 50, 200)
        render_text(screen, font_medium, "QUIT", COLORS["black"] if selected_option == 'quit' else COLORS["yellow"], WIDTH / 2 - 50, 300)

        pygame.display.update()
        clock.tick(FPS)

def render_text(surface, font, text, color, x, y):
    rendered_text = font.render(text, True, color)
    surface.blit(rendered_text, (x, y))

def generate_food(snake):
    while True:
        food_x = random.randint(0, (WIDTH - SIZE) // SIZE) * SIZE
        food_y = random.randint(0, (HEIGHT - SIZE) // SIZE) * SIZE
        if not any(food_x == segment.x and food_y == segment.y for segment in snake.body):
            return food_x, food_y

def main_game():
    snake = Snake(3 * SPEED, 3 * SPEED, COLORS["red"], SPEED, SIZE)
    food_x, food_y = generate_food(snake)
    game_active = True

    while game_active:
        screen.fill(COLORS["dark_green"])
        score_text = font_small.render(str(snake.length), True, COLORS["green"])
        screen.blit(score_text, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.change_direction(1, 0)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(-1, 0)
                elif event.key == pygame.K_UP:
                    snake.change_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(0, 1)

        snake.move()
        game_active = snake.check_boundaries() and snake.check_self_collision()
        if snake.check_food_collision(food_x, food_y):
            food_x, food_y = generate_food(snake)

        snake.draw(screen)
        screen.blit(food_img, (food_x, food_y))
        pygame.display.update()
        clock.tick(FPS)

    game_over_sound.play()
    render_text(screen, font_small, "Game Over", COLORS["red"], WIDTH // 2 - 50, HEIGHT // 2 - 20)
    pygame.display.update()
    time.sleep(2)

if __name__ == "__main__":
    if main_menu():
        main_game()
    pygame.quit()
