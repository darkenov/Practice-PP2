import pygame
import random

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 - Racer")

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 150, 0)
BLUE = (0, 100, 255)
RED = (220, 0, 0)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Arial", 22)
clock = pygame.time.Clock()

road_x = 100
road_w = 200

player_x = 180
player_y = 500
player_w = 40
player_h = 70
player_speed = 7

enemy_x = random.randint(110, 250)
enemy_y = -100
enemy_w = 40
enemy_h = 70
enemy_speed = 5

coins = 0
line_y = 0

def new_coin():
    weight = random.choice([1, 2, 3])

    if weight == 1:
        color = YELLOW
        radius = 10
    elif weight == 2:
        color = ORANGE
        radius = 12
    else:
        color = RED
        radius = 14

    x = random.randint(120, 280)
    y = -50
    return x, y, weight, color, radius

coin_x, coin_y, coin_weight, coin_color, coin_radius = new_coin()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > road_x:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x + player_w < road_x + road_w:
        player_x += player_speed

    # Скорость врага растёт каждые 5 монет
    enemy_speed = 5 + coins // 5

    enemy_y += enemy_speed
    if enemy_y > HEIGHT:
        enemy_y = -100
        enemy_x = random.randint(110, 250)

    coin_y += enemy_speed
    if coin_y > HEIGHT:
        coin_x, coin_y, coin_weight, coin_color, coin_radius = new_coin()

    player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_w, enemy_h)
    coin_rect = pygame.Rect(coin_x - coin_radius, coin_y - coin_radius, coin_radius * 2, coin_radius * 2)

    if player_rect.colliderect(enemy_rect):
        running = False

    if player_rect.colliderect(coin_rect):
        coins += coin_weight
        coin_x, coin_y, coin_weight, coin_color, coin_radius = new_coin()

    line_y += 8
    if line_y > 60:
        line_y = 0

    screen.fill(GREEN)
    pygame.draw.rect(screen, GRAY, (road_x, 0, road_w, HEIGHT))

    pygame.draw.line(screen, WHITE, (road_x, 0), (road_x, HEIGHT), 5)
    pygame.draw.line(screen, WHITE, (road_x + road_w, 0), (road_x + road_w, HEIGHT), 5)

    for i in range(0, HEIGHT, 60):
        pygame.draw.rect(screen, WHITE, (195, i + line_y, 10, 30))

    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_w, player_h))
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_w, enemy_h))
    pygame.draw.circle(screen, coin_color, (coin_x, coin_y), coin_radius)

    text1 = font.render("Coins: " + str(coins), True, BLACK)
    text2 = font.render("Speed: " + str(enemy_speed), True, BLACK)

    screen.blit(text1, (260, 20))
    screen.blit(text2, (260, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()