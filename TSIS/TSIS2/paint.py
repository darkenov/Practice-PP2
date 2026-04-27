import pygame
import datetime
from tools import flood_fill

pygame.init()

WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 220)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont("Arial", 22)
text_font = pygame.font.SysFont("Arial", 28)
clock = pygame.time.Clock()

tool = "pencil"
color = BLACK
size = 2

drawing = False
start_pos = None
last_pos = None

typing = False
text_pos = (0, 0)
text_value = ""

running = True
while running:
    screen.blit(canvas, (0, 0))

    info = "P-pencil L-line R-rect C-circle Q-square F-fill T-text | 1/2/3 size | B-black G-green U-blue D-red"
    screen.blit(font.render(info, True, BLACK), (10, 10))

    if drawing and tool in ["line", "rect", "circle", "square"]:
        now = pygame.mouse.get_pos()

        if tool == "line":
            pygame.draw.line(screen, color, start_pos, now, size)

        elif tool == "rect":
            x = min(start_pos[0], now[0])
            y = min(start_pos[1], now[1])
            w = abs(start_pos[0] - now[0])
            h = abs(start_pos[1] - now[1])
            pygame.draw.rect(screen, color, (x, y, w, h), size)

        elif tool == "circle":
            radius = int(((now[0] - start_pos[0]) ** 2 + (now[1] - start_pos[1]) ** 2) ** 0.5)
            pygame.draw.circle(screen, color, start_pos, radius, size)

        elif tool == "square":
            side = min(abs(now[0] - start_pos[0]), abs(now[1] - start_pos[1]))
            x = start_pos[0] if now[0] >= start_pos[0] else start_pos[0] - side
            y = start_pos[1] if now[1] >= start_pos[1] else start_pos[1] - side
            pygame.draw.rect(screen, color, (x, y, side, side), size)

    if typing:
        text_surface = text_font.render(text_value, True, color)
        screen.blit(text_surface, text_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()

            if mods & pygame.KMOD_CTRL and event.key == pygame.K_s:
                filename = datetime.datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, filename)
                print("Saved:", filename)

            elif typing:
                if event.key == pygame.K_RETURN:
                    text_surface = text_font.render(text_value, True, color)
                    canvas.blit(text_surface, text_pos)
                    typing = False
                    text_value = ""
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text_value = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]
                else:
                    text_value += event.unicode

            else:
                if event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_l:
                    tool = "line"
                elif event.key == pygame.K_r:
                    tool = "rect"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_q:
                    tool = "square"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_t:
                    tool = "text"

                elif event.key == pygame.K_1:
                    size = 2
                elif event.key == pygame.K_2:
                    size = 5
                elif event.key == pygame.K_3:
                    size = 10

                elif event.key == pygame.K_b:
                    color = BLACK
                elif event.key == pygame.K_g:
                    color = GREEN
                elif event.key == pygame.K_u:
                    color = BLUE
                elif event.key == pygame.K_d:
                    color = RED

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if tool == "fill":
                flood_fill(canvas, event.pos[0], event.pos[1], color)
            elif tool == "text":
                typing = True
                text_pos = event.pos
                text_value = ""
            else:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos

                if tool == "line":
                    pygame.draw.line(canvas, color, start_pos, end_pos, size)

                elif tool == "rect":
                    x = min(start_pos[0], end_pos[0])
                    y = min(start_pos[1], end_pos[1])
                    w = abs(start_pos[0] - end_pos[0])
                    h = abs(start_pos[1] - end_pos[1])
                    pygame.draw.rect(canvas, color, (x, y, w, h), size)

                elif tool == "circle":
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, color, start_pos, radius, size)

                elif tool == "square":
                    side = min(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    x = start_pos[0] if end_pos[0] >= start_pos[0] else start_pos[0] - side
                    y = start_pos[1] if end_pos[1] >= start_pos[1] else start_pos[1] - side
                    pygame.draw.rect(canvas, color, (x, y, side, side), size)

            drawing = False

        elif event.type == pygame.MOUSEMOTION and drawing:
            if tool == "pencil":
                pygame.draw.line(canvas, color, last_pos, event.pos, size)
                last_pos = event.pos

    pygame.display.flip()
    clock.tick(60)

pygame.quit()