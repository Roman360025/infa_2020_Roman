import pygame
from pygame.draw import *
from pygame.color import THECOLORS

pygame.init()

FPS = 30
screen = pygame.display.set_mode((800, 800))
screen.fill(THECOLORS['gray'])

# rect(screen, (255, 0, 255), (100, 100, 200, 200))
# rect(screen, (0, 0, 255), (100, 100, 200, 200), 5)
# polygon(screen, (255, 255, 0), [(100,100), (200,50),
#                                (300,100), (100,100)])
# polygon(screen, (0, 0, 255), [(100,100), (200,50),
#                                (300,100), (100,100)], 5)
# circle(screen, (0, 255, 0), (200, 175), 50)

# Лицо
circle(screen, (0, 0, 0), (300, 300), 200, 3)
circle(screen, (255, 255, 0), (300, 300), 200)

# Рот
rect(screen, (0, 0, 0), (200, 400, 200, 50))

# Глаза
circle(screen, (255, 0, 0), (200, 250), 35)
circle(screen, (255, 0, 0), (400, 250), 30)

# Зрачки
circle(screen, (0, 0, 0), (200, 250), 15)
circle(screen, (0, 0, 0), (400, 250), 15)

# Брови
# polygon(screen, (0, 0, 0), [(266,250), (282, 234),
#                                (148, 100), (133, 116)])

polygon(screen, (0, 0, 0), [(266, 268), (280, 254),
                            (146, 120), (133, 134)])
polygon(screen, (0, 0, 0), [(332, 255), (325, 239),
                            (505, 132), (516, 146)])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
