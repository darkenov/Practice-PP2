import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)


def draw_button(screen, rect, text, font):
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    txt = font.render(text, True, BLACK)
    screen.blit(txt, txt.get_rect(center=rect.center))


def menu_screen(screen, font):
    buttons = {
        "play": pygame.Rect(350, 180, 200, 50),
        "leaderboard": pygame.Rect(350, 250, 200, 50),
        "settings": pygame.Rect(350, 320, 200, 50),
        "exit": pygame.Rect(350, 390, 200, 50),
    }

    while True:
        screen.fill(WHITE)
        title = font.render("TSIS3 Racer", True, BLACK)
        screen.blit(title, (350, 100))

        for name, rect in buttons.items():
            draw_button(screen, rect, name.capitalize(), font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        return name


def leaderboard_screen(screen, font, data):
    back = pygame.Rect(20, 20, 100, 40)

    while True:
        screen.fill(WHITE)
        title = font.render("Top 10", True, BLACK)
        screen.blit(title, (400, 40))

        y = 100
        for i, item in enumerate(data, 1):
            txt = font.render(f"{i}. {item['name']} | score: {item['score']} | dist: {item['distance']}", True, BLACK)
            screen.blit(txt, (120, y))
            y += 40

        draw_button(screen, back, "Back", font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and back.collidepoint(event.pos):
                return


def settings_screen(screen, font, settings):
    back = pygame.Rect(20, 20, 180, 40)

    while True:
        screen.fill(WHITE)
        screen.blit(font.render("Settings", True, BLACK), (380, 50))
        screen.blit(font.render(f"Sound: {settings['sound']} (press S)", True, BLACK), (200, 150))
        screen.blit(font.render(f"Difficulty: {settings['difficulty']} (press D)", True, BLACK), (200, 220))
        screen.blit(font.render("Car color: B=blue, R=red, G=green", True, BLACK), (200, 290))
        draw_button(screen, back, "Save and Back", font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return settings
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]
                elif event.key == pygame.K_d:
                    if settings["difficulty"] == "easy":
                        settings["difficulty"] = "normal"
                    elif settings["difficulty"] == "normal":
                        settings["difficulty"] = "hard"
                    else:
                        settings["difficulty"] = "easy"
                elif event.key == pygame.K_b:
                    settings["car_color"] = [0, 100, 255]
                elif event.key == pygame.K_r:
                    settings["car_color"] = [220, 0, 0]
                elif event.key == pygame.K_g:
                    settings["car_color"] = [0, 180, 0]
            if event.type == pygame.MOUSEBUTTONDOWN and back.collidepoint(event.pos):
                return settings