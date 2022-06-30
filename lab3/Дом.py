import pygame
from pygame.draw import *
import numpy as np


def create_leafs(coordinates):
    circle(screen, (28, 99, 63), coordinates, 15)
    circle(screen, (0, 0, 0), coordinates, 15, 1)


def create_clouds(coordinates):
    circle(screen, (255, 255, 255), coordinates, 15)
    circle(screen, (0, 0, 0), coordinates, 15, 1)


def create_sunray():
    pass


pygame.init()

FPS = 30
screen = pygame.display.set_mode([455, 300])

# Фон
rect(screen, (128, 166, 255), (0, 0, 455, 130))
rect(screen, (31, 204, 66), (0, 130, 455, 170))

# Дом и крыша
rect(screen, (150, 75, 0), (60, 110, 90, 70))
rect(screen, (0, 0, 0), (60, 110, 90, 70), width=1)
polygon(screen, (255, 0, 0), [(60, 110), (105, 70),
                              (150, 110), (60, 110)])
polygon(screen, (0, 0, 0), [(60, 110), (105, 70),
                            (150, 110), (60, 110)], width=1)

# Окно
rect(screen, (19, 100, 128), (92.5, 132.5, 25, 25))
rect(screen, (234, 97, 19), (92.5, 132.5, 25, 25), width=1)

# Дерево
rect(screen, (99, 54, 28), (330, 110, 10, 60))
create_leafs((333, 68.8))
create_leafs((333, 96.8))
create_leafs((318, 104.8))
create_leafs((353, 104.8))
create_leafs((313, 84.8))
create_leafs((350, 75.8))

# Облака
create_clouds((153, 30))
create_clouds((166, 30))
create_clouds((179, 30))
create_clouds((192, 30))
create_clouds((180, 20.6))
create_clouds((160, 20.6))

# Солнце
circle(screen, (150, 149, 104), (384, 25.38), 15)

for angle in range(0, 360, 15):
    polygon(screen, (150, 149, 104), [(384 + 15 * np.cos(np.deg2rad(angle)), 25.38+15 * np.sin(np.deg2rad(angle))),
                                      (384+20 * np.cos(np.deg2rad(angle + 7.5)), 25.38+20 * np.sin(np.deg2rad(angle + 7.5))),
                                      (384+15 * np.cos(np.deg2rad(angle + 15)), 25.38+15 * np.sin(np.deg2rad(angle + 15))),
                                      (384+15 * np.cos(np.deg2rad(angle)), 25.38+15 * np.sin(np.deg2rad(angle)))])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
