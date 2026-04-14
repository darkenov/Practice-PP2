import pygame
import datetime
import os

WHITE = (255, 255, 255)

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# Центры объектов на экране
CLOCK_BG_CENTER = (600, 340)
MICKEY_CENTER = (600, 320)

# Точки вращения рук
# левая рука = секунды
# правая рука = минуты
LEFT_HAND_CENTER = (575, 300)
RIGHT_HAND_CENTER = (640, 300)


def load_assets():
    image_surface = pygame.image.load(os.path.join(IMAGES_DIR, "clock.png")).convert_alpha()
    mickey = pygame.image.load(os.path.join(IMAGES_DIR, "mUmrP.png")).convert_alpha()
    hand_l = pygame.image.load(os.path.join(IMAGES_DIR, "hand_left.png")).convert_alpha()
    hand_r = pygame.image.load(os.path.join(IMAGES_DIR, "hand_right.png")).convert_alpha()

    resized_image = pygame.transform.scale(image_surface, (800, 600))
    res_mickey = pygame.transform.scale(mickey, (350, 350))

    # Средний размер рук
    hand_l_base = pygame.transform.scale(hand_l, (140, 140))
    hand_r_base = pygame.transform.scale(hand_r, (160, 160))

    return {
        "clock_bg": resized_image,
        "mickey": res_mickey,
        "hand_left": hand_l_base,
        "hand_right": hand_r_base
    }


def draw_clock(screen, assets):
    now = datetime.datetime.now()
    m = now.minute
    s = now.second

    # По заданию:
    # правая рука = минуты
    # левая рука = секунды
    minutes_angle = -(m * 6 + s * 0.1)
    seconds_angle = -(s * 6)

    rotated_minutes = pygame.transform.rotate(assets["hand_right"], minutes_angle)
    rotated_seconds = pygame.transform.rotate(assets["hand_left"], seconds_angle)

    minutes_rect = rotated_minutes.get_rect(center=RIGHT_HAND_CENTER)
    seconds_rect = rotated_seconds.get_rect(center=LEFT_HAND_CENTER)

    screen.fill(WHITE)

    image_rect = assets["clock_bg"].get_rect(center=CLOCK_BG_CENTER)
    screen.blit(assets["clock_bg"], image_rect)

    mic_rect = assets["mickey"].get_rect(center=MICKEY_CENTER)
    screen.blit(assets["mickey"], mic_rect)

    screen.blit(rotated_minutes, minutes_rect)
    screen.blit(rotated_seconds, seconds_rect)