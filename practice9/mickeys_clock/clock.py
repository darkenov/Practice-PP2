import pygame
import datetime
import os

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, "images")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Центр часов
CENTER = (600, 320)


def load_images():
    clock_img = pygame.image.load(os.path.join(IMAGES_DIR, "clock.png")).convert_alpha()
    mickey_img = pygame.image.load(os.path.join(IMAGES_DIR, "mUmrP.png")).convert_alpha()
    left_hand = pygame.image.load(os.path.join(IMAGES_DIR, "hand_left.png")).convert_alpha()
    right_hand = pygame.image.load(os.path.join(IMAGES_DIR, "hand_right.png")).convert_alpha()

    clock_img = pygame.transform.scale(clock_img, (800, 600))
    mickey_img = pygame.transform.scale(mickey_img, (350, 350))
    left_hand = pygame.transform.scale(left_hand, (120, 120))
    right_hand = pygame.transform.scale(right_hand, (120, 120))

    return clock_img, mickey_img, left_hand, right_hand


def draw_hand(screen, image, angle, pivot_x, pivot_y):
    x = CENTER[0] - pivot_x
    y = CENTER[1] - pivot_y

    rect = image.get_rect(topleft=(x, y))
    offset = pygame.math.Vector2(CENTER) - rect.center
    rotated_offset = offset.rotate(angle)

    new_center = (CENTER[0] - rotated_offset.x, CENTER[1] - rotated_offset.y)

    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=new_center)

    screen.blit(rotated_image, rotated_rect)


def draw_clock(screen, font, clock_img, mickey_img, left_hand, right_hand):
    now = datetime.datetime.now()
    minute = now.minute
    second = now.second

    minute_angle = -(minute * 6)
    second_angle = -(second * 6)

    screen.fill(WHITE)

    # фон часов
    screen.blit(clock_img, clock_img.get_rect(center=(600, 340)))

    # сам Микки
    screen.blit(mickey_img, mickey_img.get_rect(center=(600, 320)))

    # руки поверх Микки
    draw_hand(screen, left_hand, second_angle, 95, 60)   # левая рука = секунды
    draw_hand(screen, right_hand, minute_angle, 35, 65)  # правая рука = минуты

    # время внизу
    text = font.render(now.strftime("%M:%S"), True, BLACK)
    screen.blit(text, text.get_rect(center=(600, 640)))