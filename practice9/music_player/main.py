import pygame
import os
from player import get_tracks, get_time

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 30)
small_font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

music_folder = os.path.join(os.path.dirname(__file__), "music")
tracks = get_tracks(music_folder)

current = 0
paused = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

            if len(tracks) > 0:
                if event.key == pygame.K_p:
                    if paused:
                        pygame.mixer.music.unpause()
                        paused = False
                    else:
                        pygame.mixer.music.load(tracks[current])
                        pygame.mixer.music.play()

                elif event.key == pygame.K_s:
                    pygame.mixer.music.pause()
                    paused = True

                elif event.key == pygame.K_n:
                    current = (current + 1) % len(tracks)
                    pygame.mixer.music.load(tracks[current])
                    pygame.mixer.music.play()
                    paused = False

                elif event.key == pygame.K_b:
                    current = (current - 1) % len(tracks)
                    pygame.mixer.music.load(tracks[current])
                    pygame.mixer.music.play()
                    paused = False

    screen.fill((240, 240, 240))

    title = font.render("Music Player", True, (0, 0, 0))
    screen.blit(title, (30, 30))

    if len(tracks) == 0:
        text = small_font.render("No music files", True, (200, 0, 0))
        screen.blit(text, (30, 90))
    else:
        track_name = os.path.basename(tracks[current])
        track_text = small_font.render("Track: " + track_name, True, (0, 0, 0))
        time_text = small_font.render("Position: " + get_time(), True, (0, 0, 0))

        screen.blit(track_text, (30, 90))
        screen.blit(time_text, (30, 130))

    screen.blit(small_font.render("P = Play", True, (0, 0, 0)), (30, 220))
    screen.blit(small_font.render("S = Pause", True, (0, 0, 0)), (30, 255))
    screen.blit(small_font.render("N = Next", True, (0, 0, 0)), (30, 290))
    screen.blit(small_font.render("B = Previous", True, (0, 0, 0)), (30, 325))
    screen.blit(small_font.render("Q = Quit", True, (0, 0, 0)), (30, 360))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()