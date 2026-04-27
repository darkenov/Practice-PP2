import pygame
import datetime
from tools import flood_fill

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 220)
YELLOW = (255, 255, 0)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont("Arial", 24)
text_font = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()

tool = "pencil"
color = BLACK
brush_size = 2

drawing = False
start_pos = None
last_pos = None

typing_mode = False
text_pos = (0, 0)
text_buffer = ""

def draw_preview():
    screen.blit(canvas, (0, 0))
    info = f"Tool: {tool} | Size: {brush_size} | Keys: P pencil, L line, R rect, C circle, S square, F fill, T text, 1/2/3 size, Ctrl+S save"
    txt = font.render(info, True, BLACK)
    screen.blit(txt, (10, 10))

    if drawing and tool in ["line", "rect", "circle", "square"] and start_pos:
        current_pos = pygame.mouse.get_pos()

        if tool == "line":
            pygame.draw.line(screen, color, start_pos, current_pos, brush_size)

        elif tool == "rect":
            x = min(start_pos[0], current_pos[0])
            y = min(start_pos[1], current_pos[1])
            w = abs(start_pos[0] - current_pos[0])
            h = abs(start_pos[1] - current_pos[1])
            pygame.draw.rect(screen, color, (x, y, w, h), brush_size)

        elif tool == "circle":
            radius = int(((current_pos[0] - start_pos[0]) ** 2 + (current_pos[1] - start_pos[1]) ** 2) ** 0.5)
            pygame.draw.circle(screen, color, start_pos, radius, brush_size)

        elif tool == "square":
            side = min(abs(current_pos[0] - start_pos[0]), abs(current_pos[1] - start_pos[1]))
            x = start_pos[0] if current_pos[0] >= start_pos[0] else start_pos[0] - side
            y = start_pos[1] if current_pos[1] >= start_pos[1] else start_pos[1] - side
            pygame.draw.rect(screen, color, (x, y, side, side), brush_size)

    if typing_mode:
        preview = text_font.render(text_buffer, True, color)
        screen.blit(preview, text_pos)


running = True
while running:
    draw_preview()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()

            if mods & pygame.KMOD_CTRL and event.key == pygame.K_s:
                filename = datetime.datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, filename)
                print("Saved:", filename)

            elif typing_mode:
                if event.key == pygame.K_RETURN:
                    text_surface = text_font.render(text_buffer, True, color)
                    canvas.blit(text_surface, text_pos)
                    typing_mode = False
                    text_buffer = ""
                elif event.key == pygame.K_ESCAPE:
                    typing_mode = False
                    text_buffer = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                else:
                    text_buffer += event.unicode

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
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10

                elif event.key == pygame.K_b:
                    color = BLACK
                elif event.key == pygame.K_g:
                    color = GREEN
                elif event.key == pygame.K_r:
                    color = RED
                elif event.key == pygame.K_y:
                    color = YELLOW
                elif event.key == pygame.K_u:
                    color = BLUE

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if tool == "fill":
                flood_fill(canvas, event.pos[0], event.pos[1], color)
            elif tool == "text":
                typing_mode = True
                text_pos = event.pos
                text_buffer = ""
            else:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos

                if tool == "line":
                    pygame.draw.line(canvas, color, start_pos, end_pos, brush_size)

                elif tool == "rect":
                    x = min(start_pos[0], end_pos[0])
                    y = min(start_pos[1], end_pos[1])
                    w = abs(start_pos[0] - end_pos[0])
                    h = abs(start_pos[1] - end_pos[1])
                    pygame.draw.rect(canvas, color, (x, y, w, h), brush_size)

                elif tool == "circle":
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, color, start_pos, radius, brush_size)

                elif tool == "square":
                    side = min(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    x = start_pos[0] if end_pos[0] >= start_pos[0] else start_pos[0] - side
                    y = start_pos[1] if end_pos[1] >= start_pos[1] else start_pos[1] - side
                    pygame.draw.rect(canvas, color, (x, y, side, side), brush_size)

            drawing = False
            start_pos = None
            last_pos = None

        elif event.type == pygame.MOUSEMOTION and drawing:
            if tool == "pencil":
                pygame.draw.line(canvas, color, last_pos, event.pos, brush_size)
                last_pos = event.pos

    pygame.display.flip()
    clock.tick(60)

pygame.quit()