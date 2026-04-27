import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 150, 0)
RED = (220, 0, 0)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
PURPLE = (150, 0, 200)

WIDTH = 900
HEIGHT = 700
ROAD_X = 250
ROAD_W = 400


def safe_x(player_x):
    while True:
        x = random.randint(ROAD_X + 20, ROAD_X + ROAD_W - 60)
        if abs(x - player_x) > 80:
            return x


def run_game(screen, font, username, settings):
    car_color = tuple(settings["car_color"])
    base_speed = 5 if settings["difficulty"] == "easy" else 7 if settings["difficulty"] == "normal" else 9

    player = pygame.Rect(430, 580, 40, 70)
    player_speed = 8

    enemy_speed = base_speed
    distance = 0
    coins = 0
    score = 0

    enemies = [pygame.Rect(safe_x(player.x), -200, 40, 70)]
    obstacles = []
    items = []

    active_power = None
    power_time = 0
    shield = False
    repair = 0

    line_y = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > ROAD_X + 5:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x + player.width < ROAD_X + ROAD_W - 5:
            player.x += player_speed

        if active_power == "nitro" and now > power_time:
            active_power = None
            player_speed = 8

        if random.randint(1, 100) == 1:
            obstacles.append({"rect": pygame.Rect(safe_x(player.x), -40, 50, 25), "type": random.choice(["oil", "slow", "barrier"])})

        if random.randint(1, 140) == 1 and len(items) < 2:
            kind = random.choice(["nitro", "shield", "repair"])
            items.append({"rect": pygame.Rect(safe_x(player.x), -40, 30, 30), "kind": kind})

        if random.randint(1, 80) == 1 and len(items) < 3:
            weight = random.choice([1, 2, 3])
            items.append({"rect": pygame.Rect(safe_x(player.x), -40, 24, 24), "kind": f"coin_{weight}"})

        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                enemy.y = -200
                enemy.x = safe_x(player.x)

        for ob in obstacles:
            ob["rect"].y += enemy_speed
        obstacles = [o for o in obstacles if o["rect"].y < HEIGHT + 50]

        for item in items:
            item["rect"].y += enemy_speed
        items = [i for i in items if i["rect"].y < HEIGHT + 50]

        if distance > 0 and distance % 400 == 0:
            enemy_speed += 1

        for enemy in enemies:
            if player.colliderect(enemy):
                if shield:
                    shield = False
                    enemy.y = -200
                elif repair > 0:
                    repair -= 1
                    enemy.y = -200
                else:
                    running = False

        for ob in obstacles:
            if player.colliderect(ob["rect"]):
                if ob["type"] == "oil":
                    if player.x > ROAD_X + 30:
                        player.x -= 40
                elif ob["type"] == "slow":
                    player_speed = 4
                elif ob["type"] == "barrier":
                    if shield:
                        shield = False
                    elif repair > 0:
                        repair -= 1
                    else:
                        running = False

        for item in items[:]:
            if player.colliderect(item["rect"]):
                kind = item["kind"]

                if kind == "nitro":
                    active_power = "nitro"
                    player_speed = 14
                    power_time = now + 4000
                elif kind == "shield":
                    shield = True
                    active_power = "shield"
                elif kind == "repair":
                    repair += 1
                    active_power = "repair"
                elif kind.startswith("coin_"):
                    w = int(kind.split("_")[1])
                    coins += w

                items.remove(item)

        distance += 1
        score = coins * 10 + distance

        screen.fill(GREEN)
        pygame.draw.rect(screen, GRAY, (ROAD_X, 0, ROAD_W, HEIGHT))
        pygame.draw.line(screen, WHITE, (ROAD_X, 0), (ROAD_X, HEIGHT), 5)
        pygame.draw.line(screen, WHITE, (ROAD_X + ROAD_W, 0), (ROAD_X + ROAD_W, HEIGHT), 5)

        line_y += 10
        if line_y > 60:
            line_y = 0
        for i in range(0, HEIGHT, 60):
            pygame.draw.rect(screen, WHITE, (ROAD_X + ROAD_W // 2 - 5, i + line_y, 10, 30))

        pygame.draw.rect(screen, car_color, player)

        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        for ob in obstacles:
            c = BLACK if ob["type"] == "oil" else ORANGE if ob["type"] == "slow" else WHITE
            pygame.draw.rect(screen, c, ob["rect"])

        for item in items:
            if item["kind"].startswith("coin_"):
                w = int(item["kind"].split("_")[1])
                c = YELLOW if w == 1 else ORANGE if w == 2 else PURPLE
                pygame.draw.circle(screen, c, item["rect"].center, 12)
            else:
                c = (0, 100, 255) if item["kind"] == "nitro" else (0, 255, 255) if item["kind"] == "shield" else (255, 0, 255)
                pygame.draw.rect(screen, c, item["rect"])

        screen.blit(font.render(f"Player: {username}", True, BLACK), (20, 20))
        screen.blit(font.render(f"Coins: {coins}", True, BLACK), (20, 60))
        screen.blit(font.render(f"Score: {score}", True, BLACK), (20, 100))
        screen.blit(font.render(f"Distance: {distance}", True, BLACK), (20, 140))
        screen.blit(font.render(f"Shield: {shield}", True, BLACK), (20, 180))
        screen.blit(font.render(f"Repair: {repair}", True, BLACK), (20, 220))
        screen.blit(font.render(f"Power: {active_power}", True, BLACK), (20, 260))

        pygame.display.flip()
        clock.tick(60)

    return {"score": score, "distance": distance, "coins": coins}