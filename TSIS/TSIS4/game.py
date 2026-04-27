import pygame
import random

WIDTH = 800
HEIGHT = 600
CELL = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (220, 0, 0)
DARK_RED = (120, 0, 0)
YELLOW = (255, 215, 0)
BLUE = (0, 100, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 140, 0)


def free_cell(snake, obstacles, reserved=None):
    if reserved is None:
        reserved = []

    while True:
        x = random.randint(1, (WIDTH // CELL) - 2) * CELL
        y = random.randint(1, (HEIGHT // CELL) - 2) * CELL

        if (x, y) not in snake and (x, y) not in obstacles and (x, y) not in reserved:
            return (x, y)


def new_food(snake, obstacles):
    weight = random.choice([1, 2, 3])

    if weight == 1:
        color = YELLOW
    elif weight == 2:
        color = ORANGE
    else:
        color = RED

    pos = free_cell(snake, obstacles)

    return {
        "pos": pos,
        "weight": weight,
        "color": color,
        "born": pygame.time.get_ticks()
    }


def new_poison(snake, obstacles, food_pos):
    pos = free_cell(snake, obstacles, [food_pos])
    return {"pos": pos}


def new_bonus(snake, obstacles, food_pos, poison_pos):
    kind = random.choice(["speed_up", "slow_down", "shield"])

    if kind == "speed_up":
        color = BLUE
    elif kind == "slow_down":
        color = CYAN
    else:
        color = YELLOW

    pos = free_cell(snake, obstacles, [food_pos, poison_pos])

    return {
        "pos": pos,
        "kind": kind,
        "color": color,
        "born": pygame.time.get_ticks()
    }


def generate_obstacles(level, snake):
    obstacles = []

    if level < 3:
        return obstacles

    count = level

    while len(obstacles) < count:
        pos = free_cell(snake, obstacles)

        # не ставим слишком близко к голове
        if abs(pos[0] - snake[0][0]) > 60 or abs(pos[1] - snake[0][1]) > 60:
            obstacles.append(pos)

    return obstacles


def run_snake(screen, font, username, settings, personal_best):
    snake = [(100, 100), (80, 100), (60, 100)]
    dx = CELL
    dy = 0

    score = 0
    level = 1
    base_speed = 8
    speed = base_speed
    grow = 0

    snake_color = tuple(settings["snake_color"])
    show_grid = settings["grid"]

    shield = False
    active_bonus = None
    bonus_until = 0

    obstacles = generate_obstacles(level, snake)
    food = new_food(snake, obstacles)
    poison = new_poison(snake, obstacles, food["pos"])
    bonus = None

    food_life = 5000
    bonus_life = 8000

    clock = pygame.time.Clock()
    running = True

    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

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

        # еда исчезает
        if now - food["born"] > food_life:
            food = new_food(snake, obstacles)

        # бонус исчезает
        if bonus and now - bonus["born"] > bonus_life:
            bonus = None

        # иногда создаём бонус
        if bonus is None and random.randint(1, 150) == 1:
            bonus = new_bonus(snake, obstacles, food["pos"], poison["pos"])

        # если временный бонус закончился
        if active_bonus in ["speed_up", "slow_down"] and now > bonus_until:
            active_bonus = None
            speed = base_speed + (level - 1) * 2

        head_x = snake[0][0] + dx
        head_y = snake[0][1] + dy
        new_head = (head_x, head_y)

        wall_collision = head_x < CELL or head_x > WIDTH - 2 * CELL or head_y < CELL or head_y > HEIGHT - 2 * CELL
        self_collision = new_head in snake
        obstacle_collision = new_head in obstacles

        if wall_collision or self_collision or obstacle_collision:
            if shield:
                shield = False
            else:
                break

        snake.insert(0, new_head)

        # обычная еда
        if new_head == food["pos"]:
            score += food["weight"]
            grow += food["weight"]

            food = new_food(snake, obstacles)
            poison = new_poison(snake, obstacles, food["pos"])

            level = score // 5 + 1
            speed = base_speed + (level - 1) * 2

            obstacles = generate_obstacles(level, snake)

        # ядовитая еда
        elif new_head == poison["pos"]:
            if len(snake) <= 3:
                break

            if len(snake) > 1:
                snake.pop()
            if len(snake) > 1:
                snake.pop()

            poison = new_poison(snake, obstacles, food["pos"])

        # бонус
        elif bonus and new_head == bonus["pos"]:
            if bonus["kind"] == "speed_up":
                active_bonus = "speed_up"
                speed += 5
                bonus_until = now + 5000
            elif bonus["kind"] == "slow_down":
                active_bonus = "slow_down"
                speed = max(4, speed - 3)
                bonus_until = now + 5000
            elif bonus["kind"] == "shield":
                active_bonus = "shield"
                shield = True

            bonus = None

        else:
            if grow > 0:
                grow -= 1
            else:
                snake.pop()

        screen.fill(WHITE)

        if show_grid:
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(screen, (230, 230, 230), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL):
                pygame.draw.line(screen, (230, 230, 230), (0, y), (WIDTH, y))

        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), 20)

        for ob in obstacles:
            pygame.draw.rect(screen, BLACK, (ob[0], ob[1], CELL, CELL))

        for part in snake:
            pygame.draw.rect(screen, snake_color, (part[0], part[1], CELL, CELL))

        pygame.draw.rect(screen, food["color"], (food["pos"][0], food["pos"][1], CELL, CELL))
        pygame.draw.rect(screen, DARK_RED, (poison["pos"][0], poison["pos"][1], CELL, CELL))

        if bonus:
            pygame.draw.rect(screen, bonus["color"], (bonus["pos"][0], bonus["pos"][1], CELL, CELL))

        left_food = max(0, (food_life - (now - food["born"])) // 1000)
        left_bonus = 0
        if bonus:
            left_bonus = max(0, (bonus_life - (now - bonus["born"])) // 1000)

        screen.blit(font.render(f"Player: {username}", True, BLACK), (20, 10))
        screen.blit(font.render(f"Score: {score}", True, BLACK), (20, 40))
        screen.blit(font.render(f"Level: {level}", True, BLACK), (20, 70))
        screen.blit(font.render(f"Best: {personal_best}", True, BLACK), (20, 100))
        screen.blit(font.render(f"Food time: {left_food}", True, BLACK), (20, 130))
        screen.blit(font.render(f"Shield: {shield}", True, BLACK), (20, 160))

        if bonus:
            screen.blit(font.render(f"Bonus on field: {bonus['kind']} ({left_bonus})", True, BLACK), (20, 190))
        else:
            screen.blit(font.render(f"Active bonus: {active_bonus}", True, BLACK), (20, 190))

        pygame.display.flip()
        clock.tick(speed)

    return {"score": score, "level": level}