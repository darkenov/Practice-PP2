import pygame
import math

pygame.init()

WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 - Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

font = pygame.font.SysFont("Arial", 18)
clock = pygame.time.Clock()

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

mode = "pen"
color = BLACK
drawing = False
start_pos = (0, 0)
last_pos = (0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                mode = "pen"
            elif event.key == pygame.K_r:
                mode = "rect"
            elif event.key == pygame.K_c:
                mode = "circle"
            elif event.key == pygame.K_e:
                mode = "eraser"
            elif event.key == pygame.K_h:
                mode = "highlight"
            elif event.key == pygame.K_s:
                mode = "square"
            elif event.key == pygame.K_t:
                mode = "right_triangle"
            elif event.key == pygame.K_y:
                mode = "equal_triangle"
            elif event.key == pygame.K_d:
                mode = "rhombus"

            elif event.key == pygame.K_1:
                color = BLACK
            elif event.key == pygame.K_2:
                color = RED
            elif event.key == pygame.K_3:
                color = GREEN
            elif event.key == pygame.K_4:
                color = BLUE

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if mode == "rect":
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                w = abs(start_pos[0] - end_pos[0])
                h = abs(start_pos[1] - end_pos[1])
                pygame.draw.rect(canvas, color, (x, y, w, h), 2)

            elif mode == "circle":
                radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                pygame.draw.circle(canvas, color, start_pos, radius, 2)

            elif mode == "square":
                side = min(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                x = start_pos[0]
                y = start_pos[1]
                if end_pos[0] < start_pos[0]:
                    x = start_pos[0] - side
                if end_pos[1] < start_pos[1]:
                    y = start_pos[1] - side
                pygame.draw.rect(canvas, color, (x, y, side, side), 2)

            elif mode == "right_triangle":
                points = [start_pos, (start_pos[0], end_pos[1]), end_pos]
                pygame.draw.polygon(canvas, color, points, 2)

            elif mode == "equal_triangle":
                side = abs(end_pos[0] - start_pos[0])
                h = int(side * math.sqrt(3) / 2)
                points = [
                    (start_pos[0], end_pos[1]),
                    (start_pos[0] + side, end_pos[1]),
                    (start_pos[0] + side // 2, end_pos[1] - h)
                ]
                pygame.draw.polygon(canvas, color, points, 2)

            elif mode == "rhombus":
                x1, y1 = start_pos
                x2, y2 = end_pos
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
                pygame.draw.polygon(canvas, color, points, 2)

        if event.type == pygame.MOUSEMOTION and drawing:
            now = event.pos

            if mode == "pen":
                pygame.draw.line(canvas, color, last_pos, now, 4)
            elif mode == "eraser":
                pygame.draw.line(canvas, WHITE, last_pos, now, 20)
            elif mode == "highlight":
                pygame.draw.line(canvas, YELLOW, last_pos, now, 12)

            last_pos = now

    screen.blit(canvas, (0, 0))

    text = font.render("P pen R rect C circle E eraser H highlight S square T right-triangle Y equal-triangle D rhombus", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()