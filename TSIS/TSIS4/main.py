import pygame
from db import init_db, get_top10, save_result, get_best_score, load_settings, save_settings
from game import run_snake

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("TSIS4 Snake")
font = pygame.font.SysFont("Arial", 28)

init_db()
settings = load_settings()


def ask_username():
    text = ""
    while True:
        screen.fill((255, 255, 255))
        screen.blit(font.render("Enter username:", True, (0, 0, 0)), (280, 220))
        screen.blit(font.render(text, True, (0, 0, 255)), (280, 270))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and text.strip():
                    return text.strip()
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if event.unicode.isprintable():
                        text += event.unicode


def menu():
    while True:
        screen.fill((255, 255, 255))
        screen.blit(font.render("TSIS4 Snake", True, (0, 0, 0)), (320, 80))
        screen.blit(font.render("1 - Play", True, (0, 0, 0)), (320, 180))
        screen.blit(font.render("2 - Leaderboard", True, (0, 0, 0)), (320, 230))
        screen.blit(font.render("3 - Settings", True, (0, 0, 0)), (320, 280))
        screen.blit(font.render("4 - Exit", True, (0, 0, 0)), (320, 330))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "play"
                elif event.key == pygame.K_2:
                    return "leaderboard"
                elif event.key == pygame.K_3:
                    return "settings"
                elif event.key == pygame.K_4:
                    return "exit"


def leaderboard_screen():
    data = get_top10()
    waiting = True

    while waiting:
        screen.fill((255, 255, 255))
        screen.blit(font.render("Leaderboard", True, (0, 0, 0)), (300, 40))

        y = 100
        for i, row in enumerate(data, 1):
            text = f"{i}. {row[0]} | score: {row[1]} | level: {row[2]}"
            screen.blit(font.render(text, True, (0, 0, 0)), (100, y))
            y += 40

        screen.blit(font.render("Press ESC", True, (0, 0, 0)), (320, 540))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False


def settings_screen():
    global settings
    waiting = True

    while waiting:
        screen.fill((255, 255, 255))
        screen.blit(font.render("Settings", True, (0, 0, 0)), (340, 80))
        screen.blit(font.render(f"G - Grid: {settings['grid']}", True, (0, 0, 0)), (220, 180))
        screen.blit(font.render(f"S - Sound: {settings['sound']}", True, (0, 0, 0)), (220, 230))
        screen.blit(font.render("R - Red | B - Blue | N - Green snake", True, (0, 0, 0)), (220, 280))
        screen.blit(font.render("Enter - Save and Back", True, (0, 0, 0)), (220, 330))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    settings["grid"] = not settings["grid"]
                elif event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]
                elif event.key == pygame.K_r:
                    settings["snake_color"] = [220, 0, 0]
                elif event.key == pygame.K_b:
                    settings["snake_color"] = [0, 0, 220]
                elif event.key == pygame.K_n:
                    settings["snake_color"] = [0, 180, 0]
                elif event.key == pygame.K_RETURN:
                    save_settings(settings)
                    waiting = False


running = True
while running:
    choice = menu()

    if choice == "exit":
        running = False

    elif choice == "leaderboard":
        leaderboard_screen()

    elif choice == "settings":
        settings_screen()

    elif choice == "play":
        username = ask_username()
        if not username:
            running = False
            continue

        best = get_best_score(username)
        result = run_snake(screen, font, username, settings, best)

        if result:
            save_result(username, result["score"], result["level"])
            new_best = get_best_score(username)

            waiting = True
            while waiting:
                screen.fill((255, 255, 255))
                screen.blit(font.render("Game Over", True, (0, 0, 0)), (320, 140))
                screen.blit(font.render(f"Score: {result['score']}", True, (0, 0, 0)), (300, 220))
                screen.blit(font.render(f"Level: {result['level']}", True, (0, 0, 0)), (300, 260))
                screen.blit(font.render(f"Personal best: {new_best}", True, (0, 0, 0)), (240, 300))
                screen.blit(font.render("Press M for menu", True, (0, 0, 0)), (280, 380))
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                        waiting = False

pygame.quit()