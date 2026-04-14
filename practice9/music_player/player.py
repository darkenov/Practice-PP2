import os
import pygame


def get_tracks(folder):
    tracks = []

    for file in os.listdir(folder):
        if file.endswith(".wav") or file.endswith(".mp3") or file.endswith(".ogg"):
            tracks.append(os.path.join(folder, file))

    tracks.sort()
    return tracks


def get_time():
    ms = pygame.mixer.music.get_pos()

    if ms < 0:
        ms = 0

    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes:02}:{seconds:02}"