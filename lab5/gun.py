import math
import random
from random import choice, randint, sample
from time import sleep
import traceback

import pygame

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
BOMBS = 10

WIDTH = 800
HEIGHT = 600

FPS = 30


def collision(rleft, rtop, width, height,  # rectangle definition
              center_x, center_y, radius):  # circle definition
    """ Detect collision between a rectangle and circle. """

    # complete boundbox of the rectangle
    rright, rbottom = rleft + width / 2, rtop + height / 2

    # bounding box of the circle
    cleft, ctop = center_x - radius, center_y - radius
    cright, cbottom = center_x + radius, center_y + radius

    # trivial reject if bounding boxes do not intersect
    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False  # no collision possible

    # check whether any point of rectangle is inside circle's radius
    for x in (rleft, rleft + width):
        for y in (rtop, rtop + height):
            # compare distance between circle's center point and each point of
            # the rectangle with the circle's radius
            if math.hypot(x - center_x, y - center_y) <= radius:
                return True  # collision detected

    # check if center of circle is inside rectangle
    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True  # overlaid

    return False  # no collision detected


def main():
    global FPS

    global BLACK, YELLOW, GREY, RED
    global screen

    global GAME_COLORS

    GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

    global WIDTH
    global HEIGHT

    global angry_balls, balls, bullet_for_target_1, bullet_for_target_2

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bullet_for_target_1 = 0
    bullet_for_target_2 = 0
    points = 0
    balls = []
    bombs = []
    missiles = []

    start_ticks = pygame.time.get_ticks()
    time_for_angry_gun = 5
    step_for_update_angry_gun = 5

    for i in range(BOMBS):
        new_bomb = Bomb()
        bombs.append(new_bomb)

    clock = pygame.time.Clock()
    gun = Gun(screen)
    angry_gun = AngryGun(screen)
    target = Target()
    target2 = TargetRect()
    finished = False
    not_fire = False
    power_of_angry_gun = randint(90, 99)

    pygame.font.init()
    font = pygame.font.Font(None, 25)
    font_fail = pygame.font.Font(None, 40)
    success1 = font.render('', True,
                           (0, 0, 0))
    success2 = font.render('', True,
                           (0, 0, 0))

    fail = font.render('', True,
                       (0, 0, 0))

    angry_gun.update_characteristics(power_of_angry_gun)

    while not finished:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds
        screen.fill(WHITE)
        points_of_gamer = font.render(f'{points}', True,
                                      (0, 0, 0))
        screen.blit(points_of_gamer, (10, 10))
        screen.blit(success1, (WIDTH // 3.5, HEIGHT // 3))
        screen.blit(success2, (WIDTH // 3.5, HEIGHT // 2))
        screen.blit(fail, (WIDTH // 2.5, HEIGHT // 2))
        gun.draw()

        if angry_gun.live != 0:
            angry_gun.draw()

        for bomb in bombs:
            if bomb.live == 1:
                bomb.draw()

        for missile in missiles:
            if missile.live == 1:
                missile.draw()

        if target.live == 1:
            target.draw()
        if target2.live == 1:
            target2.draw()
        for b in balls:
            if b.live == 0:
                balls.pop(balls.index(b))
                success1 = font.render('', True,
                                       (0, 0, 0))
                success2 = font.render('', True,
                                       (0, 0, 0))
                fail = font.render('', True,
                                   (255, 0, 0))
                if target.live == 0:
                    target.update()
                if target2.live == 0:
                    target2.update()
                not_fire = False
            b.draw()
        pygame.display.update()

        if int(seconds) == time_for_angry_gun and angry_gun.live == 1:
            power_of_angry_gun = randint(1, 99)
            angry_gun.update_characteristics(power_of_angry_gun)
            angry_gun.fire_end()
            time_for_angry_gun += step_for_update_angry_gun

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN and not not_fire:
                gun.fire2_start()
            elif event.type == pygame.MOUSEBUTTONUP and not not_fire:
                gun.fire2_end(event)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                gun.make_gun_up()
                angry_gun.targetting(gun)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                gun.make_gun_down()
                angry_gun.targetting(gun)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                gun.make_gun_forward()
                angry_gun.targetting(gun)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                gun.make_gun_back()
                angry_gun.targetting(gun)
            elif event.type == pygame.KEYUP:
                gun.stop_moving()

        target.move()
        target2.move()

        for missile in missiles:
            missile.move()

        for bomb in bombs:
            x = bomb.hittest(gun)
            if x and bomb.live:
                bomb.live = 0
                missiles.append(TargetDown(x))

        for b in balls:
            b.move()
            if type(b).__name__ != 'ShellAngryBall' and b.hittest(target) and target.live:
                success1 = font.render(f'Вы уничтожили цель 1 за {bullet_for_target_1} выстрелов', True,
                                       (0, 0, 0))
                points += 1
                not_fire = True
                bullet_for_target_1 = 0
                target.live = 0
                target.hit()
            if type(b).__name__ != 'ShellAngryBall' and b.hittest(target2) and target2.live:
                success2 = font.render(f'Вы уничтожили цель 2 за {bullet_for_target_2} выстрелов', True,
                                       (0, 0, 0))
                points += 1
                not_fire = True
                bullet_for_target_2 = 0
                target2.live = 0
                target2.hit()

            if type(b).__name__ == 'ShellAngryBall' and b.hittest(gun):
                screen.fill(WHITE)
                fail = font_fail.render('Вы проиграли', True,
                                   (255, 0, 0))
                points = 0
                del gun
                bombs = []
                balls = []
                for i in range(BOMBS):
                    new_bomb = Bomb()
                    bombs.append(new_bomb)

                gun = Gun(screen)




            if type(b).__name__ != 'ShellAngryBall' and b.hittest(angry_gun):
                angry_gun.live = 0

            for missile in missiles:
                if type(b).__name__ != 'ShellAngryBall' and b.hittest(missile) and missile.live:
                    points += 1
                    not_fire = True
                    missile.live = 0
                    missile.hit()
        gun.power_up()

    pygame.quit()


class Bomb:
    def __init__(self):
        self.screen = screen
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.r = 10
        self.live = 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            RED,
            (self.x, self.y),
            self.r
        )

    def hittest(self, gun):
        '''Проверка того, что пушка заехала на бомбу

        Args:
            gun: пушка
        Returns:
            Возвращает True в случае наезда пушки на бомбу. В противном случае возвращает False.
        '''
        if gun.x_right_caterpillar <= self.x <= gun.x_right_caterpillar + gun.width and \
                gun.y_right_caterpillar <= self.y <= gun.y_right_caterpillar + gun.height \
                or gun.x_left_caterpillar <= self.x <= gun.x_left_caterpillar + gun.width and \
                gun.y_left_caterpillar <= self.y <= gun.y_left_caterpillar + gun.height:

            return self.x
        else:
            return False


class ShellBall:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ShellBall

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

        self.vy_initial = 0
        self.t = 0.8
        self.ay = 2
        self.coefficient_of_y = 0.3
        self.coefficient_of_x = 0.8
        self.stop_speed = 0.4

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        self.x += self.vx * self.t
        self.y = self.y + (self.vy * self.t + self.ay * self.t ** 2 / 2)
        if self.x + self.r > WIDTH or self.x - self.r <= 0:
            # self.vx = self.vx * self.coefficient_of_x
            self.vx = -self.vx
        self.vy += self.ay * self.t
        if self.y >= HEIGHT:
            self.y = HEIGHT
            self.vy = -self.vy * self.coefficient_of_y
            self.vx = self.vx * self.coefficient_of_x
        if abs(self.vx) < self.stop_speed:
            self.vx = 0
        if abs(self.vy) < self.stop_speed:
            self.vy = 0
        if self.vy == 0 and self.vx == 0:
            self.live = 0

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if type(obj).__name__ == 'Target' or type(obj).__name__ == 'TargetDown':
            if math.sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) <= (self.r + obj.r):
                return True
            else:
                return False
        elif type(obj).__name__ == 'TargetRect':
            if obj.x <= self.x <= obj.x + obj.width and obj.y <= self.y <= obj.y + obj.height:
                return True
            else:
                return False
        else:
            if collision(obj.x_right_caterpillar, obj.y_right_caterpillar, obj.width, obj.height,
                         self.x, self.y, self.r):
                return True
            elif collision(obj.x_left_caterpillar, obj.y_left_caterpillar, obj.width, obj.height,
                           self.x, self.y, self.r):
                return True
            else:
                return False


class ShellAngryBall(ShellBall):
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        super().__init__(screen, x, y)

    def hittest(self, obj):
        '''
        Проверка того, что злая пушка попала в пушку игрока

        @param obj: злая пушка
        @return: если снаряд попал в пушку - True, иначе False
        '''
        if collision(obj.x_right_caterpillar, obj.y_right_caterpillar, obj.width, obj.height,
                     self.x, self.y, self.r):
            return True
        elif collision(obj.x_left_caterpillar, obj.y_left_caterpillar, obj.width, obj.height,
                       self.x, self.y, self.r):
            return True
        else:
            return False


class ShellRect(ShellBall):
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ShellRect

        Args:
        x - начальное положение прямоугольника по горизонтали
        y - начальное положение прямоугольника по вертикали
        """
        super().__init__(screen, x, y)
        self.width = randint(10, WIDTH // 5)
        self.height = randint(10, HEIGHT // 5)

        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self):
        '''Рисуем снаряд'''
        self.rect = pygame.draw.rect(
            self.screen,
            self.color,
            (self.x, self.y, self.width, self.height)
        )

        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (self.x, self.y, self.width, self.height),
            2
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if type(obj).__name__ == 'Target' or type(obj).__name__ == 'TargetDown':
            if self.x <= obj.x <= self.x + self.width and self.y <= obj.y <= self.y + self.height:
                return True
            else:
                return False
        elif type(obj).__name__ == 'TargetRect':
            return pygame.Rect.colliderect(self.rect, obj.rect)
        else:
            return pygame.Rect.colliderect(self.rect, obj.right_rect) or pygame.Rect.colliderect(self.rect, obj.left_rect)


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = BLACK
        self.gun_down = False
        self.gun_up = False
        self.gun_forward = False
        self.gun_back = False
        self.step = 5

        self.color_caterpillar = GREEN

        self.x_trunk = 50
        self.y_trunk = 450
        self.x_trunk_end = 60
        self.y_trunk_end = 450
        self.len = 20
        self.width = 50
        self.height = 10
        self.x_right_caterpillar = 5
        self.y_right_caterpillar = 450
        self.x_left_caterpillar = 5
        self.y_left_caterpillar = 439
        self.live = 1

    def fire2_start(self):
        self.f2_on = 1

    def make_gun_down(self):
        self.gun_down = True

    def make_gun_up(self):
        self.gun_up = True

    def make_gun_forward(self):
        self.gun_forward = True

    def make_gun_back(self):
        self.gun_back = True

    def stop_moving(self):
        self.gun_down = False
        self.gun_up = False
        self.gun_back = False
        self.gun_forward = False

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global shell, bullet_for_target_1, bullet_for_target_2
        self.len = 20
        bullet_for_target_1 += 1
        bullet_for_target_2 += 1
        new_shell = sample([ShellRect, ShellBall], 1)[0](self.screen, x=self.x_trunk_end, y=self.y_trunk_end)
        # new_shell = ShellRect(self.screen)
        new_shell.r += 5
        try:
            self.an = math.atan2((event.pos[1] - new_shell.y), (event.pos[0] - new_shell.x))
        except ZeroDivisionError:
            print(traceback.format_exc())
        new_shell.vx = self.f2_power * math.cos(self.an)
        new_shell.vy = self.f2_power * math.sin(self.an)
        new_shell.vy_initial = new_shell.vy
        new_shell.vx_initial = new_shell.vx
        new_shell.an = self.an
        balls.append(new_shell)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            try:
                self.an = math.atan((event.pos[1] - self.y_trunk) / (event.pos[0] - self.x_trunk))
            except ZeroDivisionError:
                print(traceback.format_exc())
            # self.x_trunk = 40 + self.len * math.cos(self.an)
            # self.y_trunk = 450 + self.len * math.sin(self.an)
        if self.f2_on:
            self.color = YELLOW
        else:
            self.color = BLACK

    def draw(self):
        if self.f2_on == 1 and self.len < 150:
            self.len += 1
            self.x_trunk_end = self.x_trunk + self.len * math.cos(self.an)
            self.y_trunk_end = self.y_trunk + self.len * math.sin(self.an)
        else:
            self.x_trunk_end = self.x_trunk + self.len * math.cos(self.an)
            self.y_trunk_end = self.y_trunk + self.len * math.sin(self.an)
        pygame.draw.line(self.screen, self.color, (self.x_trunk, self.y_trunk), (self.x_trunk_end, self.y_trunk_end), 8)
        pygame.draw.rect(self.screen,
                         self.color_caterpillar,
                         (self.x_right_caterpillar, self.y_right_caterpillar, self.width, self.height))
        pygame.draw.rect(self.screen,
                         self.color_caterpillar,
                         (self.x_left_caterpillar, self.y_left_caterpillar, self.width, self.height))

        if self.gun_up:
            self.y_right_caterpillar -= self.step
            self.y_left_caterpillar -= self.step
            self.y_trunk -= self.step
        elif self.gun_down:
            self.y_right_caterpillar += self.step
            self.y_left_caterpillar += self.step
            self.y_trunk += self.step
        elif self.gun_forward:
            self.x_right_caterpillar += self.step
            self.x_left_caterpillar += self.step
            self.x_trunk += self.step
        elif self.gun_back:
            self.x_right_caterpillar -= self.step
            self.x_left_caterpillar -= self.step
            self.x_trunk -= self.step

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = YELLOW
        else:
            self.color = GREY


class AngryGun(Gun):
    def __init__(self, screen):
        super().__init__(screen)
        self.x_trunk = WIDTH - WIDTH / 10
        self.x_trunk_end = WIDTH - WIDTH / 8
        # self.y_trunk_end = 470
        # self.y_trunk = 470
        self.x_right_caterpillar = WIDTH - WIDTH / 10
        self.x_left_caterpillar = WIDTH - WIDTH / 10
        # self.y_right_caterpillar =
        self.right_rect = pygame.Rect(self.x_right_caterpillar, self.y_right_caterpillar, self.width, self.height)
        self.left_rect = pygame.Rect(self.x_left_caterpillar, self.y_left_caterpillar, self.width, self.height)


    def targetting(self, obj):
        try:
            if self.y_trunk >= obj.y_trunk:
                self.an = -(math.pi - math.atan(abs(self.y_trunk - obj.y_trunk) / abs(self.x_trunk - obj.x_trunk)))
            else:
                self.an = -(math.pi + math.atan(abs(self.y_trunk - obj.y_trunk) / abs(self.x_trunk - obj.x_trunk)))
        except ZeroDivisionError:
            print(traceback.format_exc())

    def update_characteristics(self, f2_power):
        '''
        Set new random value for characterisitics of gun

        @param f2_power: set random power
        @return: void
        '''
        self.f2_power = f2_power

    def fire_end(self):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global shell, bullet_for_target_1, bullet_for_target_2
        self.len = 20
        bullet_for_target_1 += 1
        bullet_for_target_2 += 1
        new_shell = ShellAngryBall(self.screen, x=int(self.x_trunk_end), y=self.y_trunk_end)
        # new_shell = ShellRect(self.screen)
        new_shell.r += 5
        new_shell.vx = self.f2_power * math.cos(self.an)
        new_shell.vy = self.f2_power * math.sin(self.an)
        new_shell.vy_initial = new_shell.vy
        new_shell.vx_initial = new_shell.vx
        new_shell.an = self.an
        balls.append(new_shell)
        self.f2_on = 0
        self.f2_power = 10


class Target:

    def __init__(self):
        """ Инициализация новой цели. """
        self.screen = screen
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(10, 50)
        self.color = RED
        self.points = 0
        self.live = 1

        self.vy = 5

    def update(self):
        '''Создаём новую цель'''
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(10, 50)
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def move(self):
        '''Движение целей'''
        self.y += self.vy
        if self.y > HEIGHT or self.y < 0:
            self.vy *= -1

    def draw(self):
        '''Рисуем цель'''
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

        pygame.draw.circle(
            self.screen,
            (0, 0, 0),
            (self.x, self.y),
            self.r, 2)


class TargetRect(Target):
    def __init__(self):
        """ Инициализация новой цели. """
        super().__init__()
        self.width = randint(10, WIDTH // 5)
        self.height = randint(10, HEIGHT // 5)
        self.angle = 0
        self.r = 50
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        '''Создаём новую цель'''
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.width = randint(10, WIDTH // 5)
        self.height = randint(10, HEIGHT // 5)
        self.live = 1

    def move(self):
        '''Движение целей'''
        self.angle += 0.1
        if self.angle >= 360:
            self.angle = 0
        self.y = self.r * math.sin(self.angle) + HEIGHT * 0.75
        self.x = self.r * math.cos(self.angle) + WIDTH * 0.75

    def draw(self):
        '''Рисуем цель'''
        self.rect = pygame.draw.rect(
            self.screen,
            self.color,
            (self.x, self.y, self.width, self.height)
        )

        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (self.x, self.y, self.width, self.height),
            2
        )


class TargetDown(Target):
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.y = 0

    def move(self):
        '''Падение цели на пушку'''
        self.y += self.vy


main()
