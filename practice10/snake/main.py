import pygame
import random

pygame.init()

WIDTH = 600
HEIGHT = 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 8 - Snake")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (220, 0, 0)

font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

# Змея
snake = [(100, 100), (80, 100), (60, 100)]

# Направление
dx = CELL
dy = 0

score = 0
level = 1
speed = 8

# Еда
def new_food():
    while True:
        x = random.randint(1, (WIDTH // CELL) - 2) * CELL
        y = random.randint(1, (HEIGHT // CELL) - 2) * CELL
        if (x, y) not in snake:
            return (x, y)

food = new_food()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Стрелки
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

    # Новая голова
    head_x = snake[0][0] + dx
    head_y = snake[0][1] + dy
    new_head = (head_x, head_y)

    # Столкновение со стеной
    if head_x < 20 or head_x > WIDTH - 40 or head_y < 20 or head_y > HEIGHT - 40:
        running = False

    # Столкновение с собой
    if new_head in snake:
        running = False

    if not running:
        break

    snake.insert(0, new_head)

    # Если съели еду
    if new_head == food:
        score += 1
        food = new_food()

        # Новый уровень каждые 4 очка
        if score % 4 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    # Рисование
    screen.fill(WHITE)

    # Рамка
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), 20)

    # Змея
    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], CELL, CELL))

    # Еда
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

    # Текст
    score_text = font.render("Score: " + str(score), True, BLACK)
    level_text = font.render("Level: " + str(level), True, BLACK)

    screen.blit(score_text, (20, 10))
    screen.blit(level_text, (20, 40))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()