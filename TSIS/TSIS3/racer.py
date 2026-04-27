import pygame
import random
import time

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


def spawn_safe_x(player_x):
    while True:
        x = random.randint(ROAD_X + 20, ROAD_X + ROAD_W - 60)
        if abs(x - player_x) > 80:
            return x


def run_game(screen, font, username, settings):
    car_color = tuple(settings["car_color"])

    difficulty_base = {"easy": 5, "normal": 7, "hard": 9}[settings["difficulty"]]

    player = pygame.Rect(430, 580, 40, 70)
    player_speed = 8

    enemy_speed = difficulty_base
    distance = 0
    coins = 0
    score = 0
    finish_distance = 2000

    enemies = []
    obstacles = []
    powerups = []

    active_power = None
    active_until = 0
    shield = False
    repairs = 0

    line_y = 0
    clock = pygame.time.Clock()

    for _ in range(2):
        enemies.append(pygame.Rect(spawn_safe_x(player.x), random.randint(-600, -100), 40, 70))

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

        # difficulty grows
        if distance % 400 == 0 and distance > 0:
            enemy_speed = difficulty_base + distance // 400

        # active bonus timer
        if active_power == "nitro" and now > active_until:
            active_power = None
            player_speed = 8

        # spawn powerups
        if len(powerups) == 0 and random.randint(1, 160) == 1:
            kind = random.choice(["nitro", "shield", "repair"])
            powerups.append({
                "rect": pygame.Rect(spawn_safe_x(player.x), -50, 30, 30),
                "kind": kind,
                "spawn": now
            })

        # spawn obstacles
        if random.randint(1, max(20, 90 - distance // 50)) == 1:
            kind = random.choice(["oil", "slow", "barrier"])
            obstacles.append({"rect": pygame.Rect(spawn_safe_x(player.x), -40, 50, 25), "kind": kind})

        # move enemies
        for e in enemies:
            e.y += enemy_speed
            if e.y > HEIGHT:
                e.y = random.randint(-500, -100)
                e.x = spawn_safe_x(player.x)

        # move obstacles
        for ob in obstacles:
            ob["rect"].y += enemy_speed

        obstacles = [o for o in obstacles if o["rect"].y < HEIGHT + 100]

        # move powerups
        for p in powerups:
            p["rect"].y += enemy_speed
        powerups = [p for p in powerups if p["rect"].y < HEIGHT and now - p["spawn"] < 8000]

        # collisions enemies
        for e in enemies:
            if player.colliderect(e):
                if shield:
                    shield = False
                    e.y = -200
                elif repairs > 0:
                    repairs -= 1
                    e.y = -200
                else:
                    running = False

        # collisions obstacles
        for ob in obstacles:
            if player.colliderect(ob["rect"]):
                if ob["kind"] == "oil":
                    if player.x > ROAD_X + 50:
                        player.x -= 40
                elif ob["kind"] == "slow":
                    player_speed = 4
                elif ob["kind"] == "barrier":
                    if shield:
                        shield = False
                    elif repairs > 0:
                        repairs -= 1
                    else:
                        running = False

        # collect powerups
        for p in powerups[:]:
            if player.colliderect(p["rect"]):
                kind = p["kind"]
                powerups.remove(p)
                active_power = kind

                if kind == "nitro":
                    player_speed = 14
                    active_until = now + 4000
                elif kind == "shield":
                    shield = True
                elif kind == "repair":
                    repairs += 1

        # weighted coins
        if random.randint(1, 60) == 1:
            weight = random.choice([1, 2, 3])
            color = YELLOW if weight == 1 else ORANGE if weight == 2 else PURPLE
            powerups.append({
                "rect": pygame.Rect(spawn_safe_x(player.x), -40, 24, 24),
                "kind": f"coin_{weight}",
                "spawn": now,
                "color": color
            })

        for p in powerups[:]:
            if p["kind"].startswith("coin_") and player.colliderect(p["rect"]):
                w = int(p["kind"].split("_")[1])
                coins += w
                score += 10 * w
                powerups.remove(p)

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

        for e in enemies:
            pygame.draw.rect(screen, RED, e)

        for ob in obstacles:
            color = BLACK if ob["kind"] == "oil" else ORANGE if ob["kind"] == "slow" else WHITE
            pygame.draw.rect(screen, color, ob["rect"])

        for p in powerups:
            if p["kind"].startswith("coin_"):
                color = p["color"]
                pygame.draw.circle(screen, color, p["rect"].center, 12)
            else:
                color = BLUE = (0, 100, 255) if p["kind"] == "nitro" else (0, 255, 255) if p["kind"] == "shield" else (255, 0, 255)
                pygame.draw.rect(screen, color, p["rect"])

        screen.blit(font.render(f"Player: {username}", True, BLACK), (20, 20))
        screen.blit(font.render(f"Coins: {coins}", True, BLACK), (20, 60))
        screen.blit(font.render(f"Score: {score}", True, BLACK), (20, 100))
        screen.blit(font.render(f"Distance: {distance}/{finish_distance}", True, BLACK), (20, 140))
        screen.blit(font.render(f"Repair: {repairs}", True, BLACK), (20, 180))

        bonus_text = "None"
        if shield:
            bonus_text = "shield"
        elif active_power:
            bonus_text = active_power

        if active_power == "nitro":
            left = max(0, (active_until - now) // 1000)
            bonus_text += f" {left}s"

        screen.blit(font.render(f"Bonus: {bonus_text}", True, BLACK), (20, 220))

        pygame.display.flip()
        clock.tick(60)

        if distance >= finish_distance:
            break

    return {"score": score, "distance": distance, "coins": coins}