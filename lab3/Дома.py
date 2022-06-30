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
rect(screen, (128, 166, 255), (0, 0, 455, 130))
rect(screen, (31, 204, 66), (0, 130, 455, 170))

# Дом и крыша
create_house(20, 174.8, 90, 70, 25, 40)
create_house(280, 119.6, 60, 50, 10, 20)

coordinate_of_home = (20, 174.8, 90, 70)


# Деревья
create_tree(170, 179.52, 10, 60, 15)
create_tree(374, 125, 7, 40, 13)

# Облака
# Первая группа
center_of_first_cloud = (87.5, 45.5)

create_clouds(center_of_first_cloud, 15)
create_clouds((center_of_first_cloud[0] + 13, center_of_first_cloud[1]), 15)
create_clouds((center_of_first_cloud[0] + 2 * 13, center_of_first_cloud[1]), 15)
create_clouds((center_of_first_cloud[0] + 3 * 13, center_of_first_cloud[1]), 15)
create_clouds((center_of_first_cloud[0] + 27, center_of_first_cloud[1] - 10.4), 15)
create_clouds((center_of_first_cloud[0] + 7, center_of_first_cloud[1] - 10.4), 15)

# Вторая группа
center_of_first_cloud = (200, 60)

create_clouds(center_of_first_cloud, 10)
create_clouds((center_of_first_cloud[0] + 13, center_of_first_cloud[1]), 10)
create_clouds((center_of_first_cloud[0] + 2 * 13, center_of_first_cloud[1]), 10)
create_clouds((center_of_first_cloud[0] + 3 * 13, center_of_first_cloud[1]), 10)
create_clouds((center_of_first_cloud[0] + 25, center_of_first_cloud[1] - 10.4), 10)
create_clouds((center_of_first_cloud[0] + 10, center_of_first_cloud[1] - 10.4), 10)

# Третья группа
center_of_first_cloud = (394, 37)

create_clouds(center_of_first_cloud, 15)
create_clouds((center_of_first_cloud[0] + 13, center_of_first_cloud[1]), 15)
create_clouds((center_of_first_cloud[0] + 2 * 13, center_of_first_cloud[1]), 15)
create_clouds((center_of_first_cloud[0] + 3 * 13, center_of_first_cloud[1]), 15)
create_clouds((center_of_first_cloud[0] + 25, center_of_first_cloud[1] - 10.4), 15)
create_clouds((center_of_first_cloud[0] + 10, center_of_first_cloud[1] - 10.4), 15)

# Солнце
center_of_sun = (30, 30)
circle(screen, (150, 149, 104), (30, 30), 15)

for angle in range(0, 360, 15):
    polygon(screen, (150, 149, 104),
            [(center_of_sun[0] + 15 * np.cos(np.deg2rad(angle)), center_of_sun[1] + 15 * np.sin(np.deg2rad(angle))),
             (center_of_sun[0] + 20 * np.cos(np.deg2rad(angle + 7.5)),
              center_of_sun[1] + 20 * np.sin(np.deg2rad(angle + 7.5))),
             (center_of_sun[0] + 15 * np.cos(np.deg2rad(angle + 15)),
              center_of_sun[1] + 15 * np.sin(np.deg2rad(angle + 15))),
             (center_of_sun[0] + 15 * np.cos(np.deg2rad(angle)), center_of_sun[1] + 15 * np.sin(np.deg2rad(angle)))])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
