import pygame
import random

pygame.init()

WIDTH = 600
HEIGHT = 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 - Snake")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
RED = (220, 0, 0)

font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

snake = [(100, 100), (80, 100), (60, 100)]
dx = CELL
dy = 0

score = 0
speed = 8

def new_food():
    weight = random.choice([1, 2, 3])

    if weight == 1:
        color = YELLOW
    elif weight == 2:
        color = ORANGE
    else:
        color = RED

    while True:
        x = random.randint(1, (WIDTH // CELL) - 2) * CELL
        y = random.randint(1, (HEIGHT // CELL) - 2) * CELL
        if (x, y) not in snake:
            return {"x": x, "y": y, "weight": weight, "color": color, "time": pygame.time.get_ticks()}

food = new_food()
food_life = 5000
grow = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and dx == 0:
                dx = -CELL
                dy = 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx = CELL
                dy = 0
            elif event.key == pygame.K_UP and dy == 0:
                dx = 0
                dy = -CELL
            elif event.key == pygame.K_DOWN and dy == 0:
                dx = 0
                dy = CELL

    # Еда исчезает через время
    if pygame.time.get_ticks() - food["time"] > food_life:
        food = new_food()

    head_x = snake[0][0] + dx
    head_y = snake[0][1] + dy
    new_head = (head_x, head_y)

    if head_x < 20 or head_x > WIDTH - 40 or head_y < 20 or head_y > HEIGHT - 40:
        running = False

    if new_head in snake:
        running = False

    if not running:
        break

    snake.insert(0, new_head)

    if new_head == (food["x"], food["y"]):
        score += food["weight"]
        grow += food["weight"]
        food = new_food()
    else:
        if grow > 0:
            grow -= 1
        else:
            snake.pop()

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), 20)

    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], CELL, CELL))

    pygame.draw.rect(screen, food["color"], (food["x"], food["y"], CELL, CELL))

    left_time = max(0, (food_life - (pygame.time.get_ticks() - food["time"])) // 1000)

    text1 = font.render("Score: " + str(score), True, BLACK)
    text2 = font.render("Food time: " + str(left_time), True, BLACK)

    screen.blit(text1, (20, 10))
    screen.blit(text2, (20, 40))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()