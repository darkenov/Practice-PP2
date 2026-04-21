import pygame

pygame.init()

WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 8 - Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

font = pygame.font.SysFont("Arial", 20)
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

        # Клавиши режимов
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

            # Цвет
            elif event.key == pygame.K_1:
                color = BLACK
            elif event.key == pygame.K_2:
                color = RED
            elif event.key == pygame.K_3:
                color = GREEN
            elif event.key == pygame.K_4:
                color = BLUE

        # Нажали мышь
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos

        # Отпустили мышь
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

        # Движение мыши
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

    text = font.render("P-pen R-rect C-circle E-eraser H-highlight 1-black 2-red 3-green 4-blue", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()