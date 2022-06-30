import math
from random import choice, randint
from time import sleep
import traceback
import sys

import pygame

import pygame
from pygame.draw import *
import numpy as np


def create_leafs(coordinates, radius):
    circle(screen, (28, 99, 63), coordinates, radius)
    circle(screen, (0, 0, 0), coordinates, radius, 1)


def create_clouds(coordinates, radius):
    circle(screen, (255, 255, 255), coordinates, radius)
    circle(screen, (0, 0, 0), coordinates, radius, 1)


def create_tree(x, y, width, height, radius):
    rect(screen, (99, 54, 28), (x, y, width, height))
    coordinate_of_first_leafs = (x + radius - 12, y - 3 * radius + 3.8)
    create_leafs(coordinate_of_first_leafs, radius)
    # create_leafs((coordinate_of_first_leafs[0], coordinate_of_first_leafs[1] + radius - 2), radius)
    create_leafs((coordinate_of_first_leafs[0], coordinate_of_first_leafs[1] + 2 * radius - 2), radius)
    create_leafs((coordinate_of_first_leafs[0] - radius, coordinate_of_first_leafs[1] + 2 * radius + 6), radius)
    create_leafs((coordinate_of_first_leafs[0] + radius + 5, coordinate_of_first_leafs[1] + 2 * radius + 6), radius)
    create_leafs((coordinate_of_first_leafs[0] - radius - 5, coordinate_of_first_leafs[1] + radius + 1), radius)
    create_leafs((coordinate_of_first_leafs[0] + radius + 2, coordinate_of_first_leafs[1] + radius - 8), radius)

def create_house(x, y, width, height, width_of_window, height_of_roof):
    # Дом и крыша
    coordinate_of_home = (x, y, width, height)
    rect(screen, (150, 75, 0), coordinate_of_home)
    rect(screen, (0, 0, 0), coordinate_of_home, width=1)
    polygon(screen, (255, 0, 0),
            [coordinate_of_home[0:2], (coordinate_of_home[0] + coordinate_of_home[2] / 2, coordinate_of_home[1] - height_of_roof),
             (coordinate_of_home[0] + coordinate_of_home[2], coordinate_of_home[1]), coordinate_of_home[0:2]])
    polygon(screen, (255, 0, 0),
            [coordinate_of_home[0:2], (coordinate_of_home[0] + coordinate_of_home[2] / 2, coordinate_of_home[1] - height_of_roof),
             (coordinate_of_home[0] + coordinate_of_home[2], coordinate_of_home[1]), coordinate_of_home[0:2]], width=1)

    # Окно
    rect(screen, (19, 100, 128),
         (coordinate_of_home[0] + (coordinate_of_home[2] - width_of_window) / 2,
          coordinate_of_home[1] + (coordinate_of_home[3] - width_of_window) / 2, width_of_window, width_of_window))
    rect(screen, (19, 100, 128),
         (coordinate_of_home[0] + (coordinate_of_home[2] - width_of_window) / 2,
          coordinate_of_home[1] + (coordinate_of_home[3] - width_of_window) / 2, width_of_window, width_of_window),
         width=1)


pygame.init()

FPS = 30
screen = pygame.display.set_mode([455, 300])

# Фон
rect1  = rect(screen, (128, 166, 255), (0, 0, 455, 130))

rect1.right = 100
rect1.bottom = 100

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
