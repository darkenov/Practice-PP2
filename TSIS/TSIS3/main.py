import pygame
from persistence import load_settings, save_settings, load_leaderboard, save_score
from ui import menu_screen, leaderboard_screen, settings_screen
from racer import run_game

pygame.init()
screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption("TSIS3 Racer")
font = pygame.font.SysFont("Arial", 28)

settings = load_settings()

def ask_name():
    username = ""
    while True:
        screen.fill((255, 255, 255))
        screen.blit(font.render("Enter name and press Enter:", True, (0, 0, 0)), (250, 250))
        screen.blit(font.render(username, True, (0, 0, 255)), (250, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    return username.strip()
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

while True:
    choice = menu_screen(screen, font)

    if choice == "exit":
        break

    elif choice == "leaderboard":
        leaderboard_screen(screen, font, load_leaderboard())

    elif choice == "settings":
        settings = settings_screen(screen, font, settings)
        save_settings(settings)

    elif choice == "play":
        name = ask_name()
        if not name:
            break

        result = run_game(screen, font, name, settings)
        if result:
            save_score(name, result["score"], result["distance"])

            waiting = True
            while waiting:
                screen.fill((255, 255, 255))
                screen.blit(font.render("Game Over", True, (0, 0, 0)), (380, 150))
                screen.blit(font.render(f"Score: {result['score']}", True, (0, 0, 0)), (350, 220))
                screen.blit(font.render(f"Distance: {result['distance']}", True, (0, 0, 0)), (350, 260))
                screen.blit(font.render(f"Coins: {result['coins']}", True, (0, 0, 0)), (350, 300))
                screen.blit(font.render("R - Retry | M - Menu", True, (0, 0, 0)), (320, 380))
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        choice = "exit"
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            waiting = False
                            choice = "play"
                        elif event.key == pygame.K_m:
                            waiting = False

pygame.quit()