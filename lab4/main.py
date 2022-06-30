import pygame
from pygame.draw import *
from random import randint
import math


def new_rect():
    '''Рисует новый прямоугольник'''
    x = randint(100, 700)
    y = randint(100, 500)
    color = COLORS[randint(0, 5)]
    width = randint(100, 300)
    height = randint(100, 200)
    rect(screen, color, (x, y, width, height))
    return x, y, width, height, color


def new_ball():
    '''рисует новый шарик '''
    x = randint(100, 700)
    y = randint(100, 500)
    r = randint(30, 50)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    return x, y, r, color


def movement_of_rect(x, y, color, widht, height, coff_x, coff_y):
    '''Задаёт движение прямоугольника'''
    if coff_y == -1:
        velocity_y = randint(-highest_speed, -smallest_speed)
    else:
        velocity_y = randint(smallest_speed, highest_speed)
    if coff_x == -1:
        velocity_x = randint(-highest_speed, -smallest_speed)
    else:
        velocity_x = randint(smallest_speed, highest_speed)

    x += velocity_x
    y += velocity_y
    if x >= 1200:
        coff_x = -1
        velocity_x = randint(-highest_speed, -smallest_speed)
        x += velocity_x
        rect(screen, color, (x, y, widht, height))
    elif x <= 0:
        coff_x = 1
        velocity_x = randint(smallest_speed, highest_speed)
        x += velocity_x
        rect(screen, color, (x, y, widht, height))
    if y >= 900:
        coff_y = -1
        velocity_y = randint(-highest_speed, -smallest_speed)
        y += velocity_y
        rect(screen, color, (x, y, widht, height))
    elif y <= 0:
        coff_y = 1
        velocity_y = randint(smallest_speed, highest_speed)
        y += velocity_y
        rect(screen, color, (x, y, widht, height))
    rect(screen, color, (x, y, widht, height))
    return x, y, widht, height, color, coff_x, coff_y


def movement_of_ball(velocity_x, velocity_y, x, y, r, color):
    '''Задаёт движение шара'''
    x += velocity_x
    y += velocity_y
    if x >= 1200:
        velocity_x = randint(smallest_speed, highest_speed)
        velocity_x *= -1
        x += velocity_x
        circle(screen, color, (x, y), r)
    elif x <= 0:
        velocity_x = randint(smallest_speed, highest_speed)
        x += velocity_x
        circle(screen, color, (x, y), r)
    if y >= 900:
        velocity_y = randint(smallest_speed, highest_speed)
        velocity_y *= -1
        y += velocity_y
        circle(screen, color, (x, y), r)
    elif y <= 0:
        velocity_y = randint(smallest_speed, highest_speed)
        y += velocity_y
        circle(screen, color, (x, y), r)
    circle(screen, color, (x, y), r)
    return velocity_x, velocity_y, x, y


def click_ball(event, points, x, y, r):
    '''Проверяем, попал ли наш щелчёк на шарик'''
    if math.sqrt((event.pos[0] - x) ** 2 + (event.pos[1] - y) ** 2) <= r:
        points += 1
        print(f"Количество ваших очков: {points}")
    return points


def click_rect(event, points, x, y, width, height):
    '''Проверяем, попал ли наш щелчёк на прямоугольник'''
    if x <= event.pos[0] <= x + width and y <= event.pos[1] <= y + height:
        points += 0.5
        print(f"Количество ваших очков: {points}")
    return points


def check_and_write_name_of_gamer(name, points, list):
    '''Проверяет, есть ли текущий игрок в таблице
    Если нет, то заносит его'''
    index = 0
    for i in list:
        if name in i:
            list[index][1] = points
            return list
        index += 1
    new_gamer = [name, points]
    list.append(new_gamer)
    return list


def read_file(filename):
    '''Читаем файл лучших игроков'''
    f = open('best.txt')
    best_gamers = []
    count = 0

    for line in f:
        count += 1
        if count > 2:
            name, point_of_gamer = line.split('    ')
            point = float(point_of_gamer)
            list = [name, point]
            best_gamers.append(list)

    return best_gamers


pygame.init()

username = input('Введите свой ник: ')

best_gamers = read_file('best.txt')

FPS = 60
screen = pygame.display.set_mode((1200, 900))
points = 0
smallest_speed = 10
highest_speed = 20
coff_x = 1
coff_y = 1

velocity_of_rect_x = randint(smallest_speed, highest_speed)
velocity_of_rect_y = randint(smallest_speed, highest_speed)

velocity_of_ball_x_1 = randint(smallest_speed, highest_speed)
velocity_of_ball_y_1 = randint(smallest_speed, highest_speed)

velocity_of_ball_x_2 = randint(smallest_speed, highest_speed)
velocity_of_ball_y_2 = randint(smallest_speed, highest_speed)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

pygame.display.update()
clock = pygame.time.Clock()
finished = False

x1, y1, r1, color1 = new_ball()
x2, y2, r2, color2 = new_ball()

x3, y3, width, height, color3 = new_rect()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            points = click_ball(event, points, x1, y1, r1)
            points = click_ball(event, points, x2, y2, r2)
            points = click_rect(event, points, x3, y3, width, height)
    velocity_of_ball_x_1, velocity_of_ball_y_1, x1, y1 = movement_of_ball(velocity_of_ball_x_1, velocity_of_ball_y_1,
                                                                          x1, y1, r1, color1)
    velocity_of_ball_x_2, velocity_of_ball_y_2, x2, y2 = movement_of_ball(velocity_of_ball_x_2, velocity_of_ball_y_2,
                                                                          x2, y2, r2, color2)
    x3, y3, width, height, color3, coff_x, coff_y = movement_of_rect(x3, y3, color3, width, height, coff_x, coff_y)

    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()

with open('best.txt', 'w') as f:
    if not best_gamers:
        print('No data in file')
        f.write('Gamer    Points\n\n')
        f.write(f'{username}    {points}')
    else:
        list = [username, points]
        best_gamers = check_and_write_name_of_gamer(username, points, best_gamers)
        best_gamers = sorted(best_gamers, key=lambda i: i[1], reverse=True)
        f.write('Gamer    Points\n\n')

        if len(best_gamers) > 5:
            min = best_gamers[4][1]

            for line in best_gamers:
                if min <= line[1]:
                    f.write(str(line[0]) + '    ' + str(line[1]) + '\n')
                else:
                    break
        else:
            for line in best_gamers:
                f.write(str(line[0]) + '    ' + str(line[1]) + '\n')
