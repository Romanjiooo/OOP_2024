import math
from random import choice, randint as rnd

import pygame
from datetime import datetime


class GameSettings:
    """
    Класс с настройками игры
    Позволяет легко изменять любые настройки
    """
    SCREEN_SIZE = (800, 600)

    GRAVITY_X = 0
    GRAVITY_Y = 9.8

    FPS = 30

    DIFFICULTY = 1


# Глобальная переменная
timestep = 0


class Color():
    """
    Класс, содержащий информацию о цвете
    """

    # Константы для преобразования цветов в HEX-значение
    HEX_R = (16 ** 4)
    HEX_G = (16 ** 2)

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def value(self):
        """
        Выводит HEX-значение цвета
        """
        return self.r * Color.HEX_R + self.g * Color.HEX_G + self.b

    @staticmethod
    def from_hex(value):
        """
        Создаёт объект класса Color из HEX-значения цвета
        """
        r = value // Color.HEX_R
        value %= Color.HEX_R
        g = value // Color.HEX_G
        value %= Color.HEX_G
        b = value
        return Color(r, g, b)


class GameColors():
    """
    Класс, содержащий все цвета, используемые в игре
    Содержит все функции, связанные с выбором цвета
    """
    # внутри класса можно обозначить постоянные цвета, которые не будут
    # использоваться для рисования кругов
    black = Color(0, 0, 0)
    white = Color(255, 255, 255)
    gray = Color.from_hex(0x7D7D7D)
    light_gray = Color.from_hex(0xADADAD)

    def __init__(self):
        # Сначала создаём список, который будет находится внутри класса
        self.__colors = dict()

    def add(self, name, color):
        self.__colors[name] = color

    def get(self, name=None):
        return (
            choice([*self.__colors.values()]) if name is None
            else self.__colors[name]
        )


colors = GameColors()

colors.add("red", Color.from_hex(0xFF0000))
colors.add("blue", Color.from_hex(0x0000FF))
colors.add("yellow", Color.from_hex(0xFFC91F))
colors.add("green", Color.from_hex(0x00FF00))
colors.add("magenta", Color.from_hex(0xFF03B8))
colors.add("cyan", Color.from_hex(0x00FFCC))


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

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

        self.color = colors.get().value()

        self.live = 30

        self.bounces = 4

    def move(self):
        """Переместить мяч

        Метод описывает перемещение мяча за один кадр перерисовки.
        То есть, обновляет значения self.x и self.y
        с учетом скоростей self.vx и self.vy,
        силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # timestep - разница времени между текущим и предыдущим кадром
        # (в секундах)
        # т.к значение слишком маленькое, умножим его на 10
        lTimestep = timestep * 10

        self.vx += GameSettings.GRAVITY_X * lTimestep
        self.vy -= GameSettings.GRAVITY_Y * lTimestep

        if self.y + self.r >= GameSettings.SCREEN_SIZE[1]:
            if self.bounces <= 0:
                return False
            self.bounces -= 1
            self.vy /= -math.sqrt(2)
        if self.y - self.r <= 0:
            if self.bounces <= 0:
                return False
            self.bounces -= 1
            self.vy /= -math.sqrt(2)

        if self.x + self.r >= GameSettings.SCREEN_SIZE[0]:
            if self.bounces <= 0:
                return False
            self.bounces -= 1
            self.vx /= -math.sqrt(2)
        if self.x - self.r <= 0:
            if self.bounces <= 0:
                return False
            self.bounces -= 1
            self.vx /= -math.sqrt(2)

        self.x = max(
            0, min(GameSettings.SCREEN_SIZE[0], self.x + self.vx * lTimestep))
        self.y = max(
            0, min(GameSettings.SCREEN_SIZE[1], self.y - self.vy * lTimestep))

        return True

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """
        Функция проверяет, сталкивалкивается ли данный обьект с целью,
        описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели.
            В противном случае возвращает False.
        """
        if self.live <= 0:
            return False
        # Вычисляем расстояние между центрами объектов
        distance = math.sqrt((obj.x - self.x)**2+(obj.y - self.y)**2)
        # Проверяем, находятся ли объекты на необходимом расстоянии,
        # чтобы считаться столкнувшимися
        if distance <= self.r + obj.r:
            return True
        return False


class BouncyBall(Ball):
    """
    Прыгучий шар
    """
    def __init__(self, screen, x=40, y=450):
        # super() позволяет вызывать методы, реализованные в базовом классе
        super().__init__(screen, x, y)
        self.bounces = 15

    def move(self):
        lTimestep = timestep * 10

        self.vx += GameSettings.GRAVITY_X * lTimestep
        self.vy -= GameSettings.GRAVITY_Y * lTimestep

        if self.y + self.r >= GameSettings.SCREEN_SIZE[1]:
            if self.bounces <= 0:
                return False
            self.bounces -= 1
            self.vy /= -math.sqrt(1.25)
        if self.y - self.r <= 0:
            if self.bounces <= 0:
                return False
            self.bounces -= 1
            self.vy /= -math.sqrt(1.25)

        if self.x + self.r >= GameSettings.SCREEN_SIZE[0]:
            if self.bounces <= 0:
                return False
            self.bounces -= 1
            self.vx /= -math.sqrt(1.25)
        if self.x - self.r <= 0:
            if self.bounces <= 0:
                return False
            self.bounces -= 1
            self.vx /= -math.sqrt(1.25)

        self.x = max(
            0, min(GameSettings.SCREEN_SIZE[0], self.x + self.vx * lTimestep))
        self.y = max(
            0, min(GameSettings.SCREEN_SIZE[1], self.y - self.vy * lTimestep))

        return True


class FlyingBall(Ball):
    def __init__(self, screen, x=40, y=450):
        super().__init__(screen, x, y)
        self.color = Color(40, 147, 255).value()

    def move(self):
        lTimestep = timestep * 10

        if self.y + self.r >= GameSettings.SCREEN_SIZE[1]:
            if self.bounces <= 0:
                return False
            self.bounces -= 1
            self.vy /= -math.sqrt(1.25)
        if self.y - self.r <= 0:
            if self.bounces <= 0:
                return False
            self.bounces -= 1
            self.vy /= -math.sqrt(1.25)

        if self.x + self.r >= GameSettings.SCREEN_SIZE[0]:
            if self.bounces <= 0:
                return False
            self.bounces -= 1
            self.vx /= -math.sqrt(1.25)
        if self.x - self.r <= 0:
            if self.bounces <= 0:
                return False
            self.bounces -= 1
            self.vx /= -math.sqrt(1.25)

        self.x = max(
            0, min(GameSettings.SCREEN_SIZE[0], self.x + self.vx * lTimestep))
        self.y = max(
            0, min(GameSettings.SCREEN_SIZE[1], self.y - self.vy * lTimestep))

        return True


AVAILABLE_BALL_TYPES = [
    Ball,
    BouncyBall,
    FlyingBall
]


class BallHandler:
    """
    Выделенный в отдельный класс список шаров, запущенных пушкой
    Содержит функции для работы с шарами
    """
    def __init__(self):
        self.__balls = list()
        self.__balls_queue = list()
        self.shot_count = 0

    def add_ball(self, ball):
        """
        Добавляет шар в список
        Args:
            ball - Шар, который нужно добавить в список
        """
        self.__balls.append(ball)

    def remove_ball(self, ball):
        """
        Удаляет шар из списка
        Args:
            ball - Шар, который нужно удалить из списка
        """
        self.__balls.remove(ball)

    def move(self):
        """
        Двигает все шары по игровому полю
        Если шар "умирает", удаляет его из списка
        """
        for ball in self.__balls:
            if not ball.move():
                self.remove_ball(ball)

    def get_next_ball(self):
        """
        Получает следующий шар из списка
        """
        # т.к мы получаем шар только при выстреле, мы можем считать их
        # количество здесь
        self.shot_count += 1

        if len(self.__balls_queue) <= 0:
            self.refill()
        ball = self.__balls_queue.pop(0)
        return ball

    def get_queue(self):
        """
        Возвращает список шаров, которые будут запущены следующими
        """
        return self.__balls_queue

    def refill(self):
        """
        Восполняет список шаров, которые будут запущены
        """
        for i in range(15):
            self.__balls_queue.append(
                choice(AVAILABLE_BALL_TYPES)
            )

    def hittest(self, obj):
        """
        Проверяет каждый шар на столкновения с объектов
        Args:
            obj - объект, с которым проверяется столкновение шаров
        Return:
            Возвращает шар, который столкнулся с объектом первым
            Если ни один шар не столкнулся, возвращает None
        """
        for ball in self.__balls:
            if ball.hittest(obj):
                return ball
        return None

    def draw(self):
        """
        Отвечает за отрисовку всех шаров
        """
        for ball in self.__balls:
            ball.draw()


class Gun:
    def __init__(self, screen, balls):
        self.screen = screen

        self.f2_power = 20
        self.f2_on = 0

        self.angle = 1

        self.color = colors.gray.value()

        self.balls = balls
        self.shots_done = 0

        self.active = False

        self.r = 10

        self.x = 20
        self.y = 450

    def fire2_start(self, event):
        if not self.active:
            return
        self.f2_on = 1

    def fire2_end(self, event):
        """
        Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от
        положения мыши.
        """
        if not self.active or not self.f2_on:
            return
        new_ball = self.balls.get_next_ball()(
            self.screen,
            self.x,
            self.y)
        self.angle = math.atan2(
            (event.pos[1]-new_ball.y),
            (event.pos[0]-new_ball.x)
        )
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = -self.f2_power * math.sin(self.angle)
        self.balls.add_ball(new_ball)
        self.f2_on = 0
        self.f2_power = 20

    def update_position(self, x, y):
        """
        Изменяет корневую позицию пушки
        """
        self.x = x
        self.y = y

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if not self.active:
            return
        if event:
            self.angle = math.atan2(
                (event.pos[1]-self.y), (event.pos[0]-self.x))
        if self.f2_on:
            self.color = colors.get("red").value()
        else:
            self.color = colors.gray.value()

    # Для исключения ошибок, сделаем пустую функцию move()
    def move(self):
        """
        Двигает пушку согласно заданным правилам
        """
        pass

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color if self.active else colors.light_gray.value(),
            (
                self.x,
                self.y
            ),
            10
        )
        if not self.active:
            return
        direction = (
            math.cos(self.angle),
            math.sin(self.angle)
        )
        direction = [x * self.f2_power for x in direction]
        pygame.draw.line(
            self.screen,
            self.color,
            (self.x, self.y),
            (self.x + direction[0], self.y + direction[1]),
            5
        )

    def power_up(self):
        if self.active and self.f2_on:
            if self.f2_power < 100:
                self.f2_power += timestep * 100
            self.color = colors.get("red").value()
        else:
            self.color = colors.gray.value()


class MoveableGun(Gun):
    """
    Пушка, двигающаяся туда-обратно в заданном направлении
    """
    def __init__(self, screen, balls):
        super().__init__(screen, balls)
        self.from_x = self.x
        self.from_y = self.y
        self.to_x = self.from_x + rnd(-40, 40)
        self.to_y = self.from_y + rnd(-40, 40)

    def update_position(self, x, y):
        """
        Обновляет корневую позицию с учётом цели перемещения
        """
        # Вычисляем разницу между положениями
        diff_x = x - self.x
        diff_y = y - self.y

        # Обновляем цель перемещения
        self.to_x += diff_x
        self.to_y += diff_y

        # Обновляем положения пушки
        super().update_position(x, y)
        self.from_x = self.x
        self.from_y = self.y

    def move(self):
        """
        Двигает пушку
        """
        def swap_positions(from_x, to_x, from_y, to_y):
            """
            Меняет позиции местами
            """
            tmp_x = to_x
            tmp_y = to_y
            self.to_x = from_x
            self.from_x = tmp_x
            self.to_y = from_y
            self.from_y = tmp_y
        lTimestep = timestep
        self.x = self.x + (self.to_x - self.x) * lTimestep
        self.y = self.y + (self.to_y - self.y) * lTimestep
        distance = math.sqrt((self.to_x - self.x)**2 + (self.to_y - self.y)**2)
        if distance <= 1:
            swap_positions(self.from_x, self.to_x, self.from_y, self.to_y)


GUN_TYPES = [
    Gun,
    MoveableGun
]


class Target:
    def __init__(self, screen, difficulty):
        """
        Инициализирует цель
        """
        self.screen = screen

        self.x = rnd(600, 780)
        self.y = rnd(300, 550)

        self.origin_x = self.x
        self.origin_y = self.y

        self.r = rnd(*difficulty.targets_size_range)
        self.color = colors.get("red").value()

    def move(self):
        """
        Двигает цель по заданному правилу
        """
        pass  # т.к стандартная цель неподвижна, мы ничего не делаем

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (
                self.x,
                self.y
            ),
            self.r
        )


class CircularTarget(Target):
    """
    Представляет собой цель, движущуюся по кругу
    """
    def move(self):
        angle = datetime.now().timestamp() % 360
        self.x = self.origin_x + (math.cos(angle) * 20)
        self.y = self.origin_y - (math.sin(angle) * 20)


class MovingTarget(Target):
    """
    Цель, движущаяся туда-орбатно
    """
    def __init__(self, screen, difficulty):
        super().__init__(screen, difficulty)
        self.from_x = self.origin_x
        self.from_y = self.origin_y

        self.to_x = self.from_x + rnd(-40, 40)
        self.to_y = self.from_y + rnd(-40, 40)

    def move(self):
        def swap_positions(from_x, to_x, from_y, to_y):
            tmp_x = to_x
            tmp_y = to_y
            self.to_x = from_x
            self.from_x = tmp_x
            self.to_y = from_y
            self.from_y = tmp_y
        lTimestep = timestep * 0.5
        self.x = self.x + (self.to_x - self.x) * lTimestep
        self.y = self.y + (self.to_y - self.y) * lTimestep
        distance = math.sqrt((self.to_x - self.x)**2 + (self.to_y - self.y)**2)
        if distance <= 1:
            swap_positions(self.from_x, self.to_x, self.from_y, self.to_y)


class FallingTarget(Target):
    """
        Цель, падающая вниз
    """
    def __init__(self, screen, difficulty):
        super().__init__(screen, difficulty)
        self.r = 40
        self.vy = 9.8

    def move(self):
        lTimestep = timestep * 10
        self.vy -= GameSettings.GRAVITY_Y * lTimestep
        self.y -= self.vy * lTimestep

        # Чтобы не удалять цель, помещяем её вверх экрана
        if self.y > GameSettings.SCREEN_SIZE[1] + 40:
            self.y = -40
            self.vy = 0

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (
                self.x,
                self.y
            ),
            self.r
        )


class Bombs:
    """
    Класс, представляющий бомбу
    """
    def __init__(self, screen, x, y, state):
        self.x = x
        self.y = y
        self.screen = screen
        self.color = colors.black.value()
        self.state = state

    def drop(self):
        """
        Сбрасываем падающую цель
        """
        # Создадим объект цели
        target = FallingTarget(self.screen, self.state.difficulty)
        target.x = self.x + 20
        target.y = self.y + 35
        # Добавим цель к остальным
        self.state.targets.append(
            target
        )

    def draw(self):
        """
        Отрисовываем "бомбу"
        """
        pygame.draw.rect(
            self.screen,
            self.color,
            (self.x, self.y, 40, 15)
        )


class GameDifficulty:
    """
    Класс, содержащий значения, которые можно менять со сложностью
    """
    def __init__(
                 self, targets=4,
                 targets_size_range=(30, 50), allowed_targets=[Target]):
        self.targets = targets
        self.targets_size_range = targets_size_range
        self.allowed_targets = allowed_targets


DIFFICULTIES = [
    GameDifficulty(1, (30, 40), [Target]),
    GameDifficulty(2, (20, 40), [Target, MovingTarget]),
    GameDifficulty(3, (20, 30), [Target, MovingTarget, CircularTarget])
]


class GameState:
    """
    Класс, содержащий информацию о текущей игре
    Очки, очередь шаров, цели
    """
    def __init__(self, screen, difficulty):
        """
        Инициализирует объект класса, содержащий данные о состоянии игры
        Args:
            screen - экран
            difficulty - сложность
        """
        self.points = 0
        self.targets = list()
        self.balls = BallHandler()

        self.bomb = Bombs(screen, GameSettings.SCREEN_SIZE[0] - 400, 10, self)

        self.active_gun = choice(GUN_TYPES)(screen, self.balls)
        self.guns = [choice(GUN_TYPES)(screen, self.balls) for i in range(2)]
        for i in self.guns:
            x = rnd(
                0,
                GameSettings.SCREEN_SIZE[0] / 2)
            y = rnd(
                GameSettings.SCREEN_SIZE[1]//2,
                GameSettings.SCREEN_SIZE[1] - 15)
            i.update_position(x, y)

        self.guns += [self.active_gun]

        self.screen = screen
        self.difficulty = difficulty

    def hit_target(self, target):
        """
        Вызывается при попадании по цели
        """
        self.points += 1
        self.balls.shot_count = 0
        self.targets.remove(target)

    def new_round(self):
        """
        Начинает новый раунд
        """
        self.balls.shot_count = 0
        self.targets = [
            choice(self.difficulty.allowed_targets)(
                self.screen, self.difficulty) for i in range(
                    self.difficulty.targets)
        ]


pygame.init()
screen = pygame.display.set_mode(GameSettings.SCREEN_SIZE)
# Для отображения текста на экране объявим стандартный шрифт размером 14
font = pygame.font.Font(pygame.font.get_default_font(), 14)

# Создадим объект класса GameState, содержащий информацию о текущей игре
state = GameState(screen, DIFFICULTIES[GameSettings.DIFFICULTY])

# Переменная-счётчик для сброса целей с бомбы
lastdrop = 0

clock = pygame.time.Clock()
finished = False

while not finished:
    # Сначала отобразим счёт в игре
    screen.fill(colors.white.value())
    text = font.render(
        f"Ваш счёт: {state.points}",
        True,
        colors.black.value())
    screen.blit(text, (10, 10))

    # Пока в игре существуют цели
    if len(state.targets) > 0:
        # Выключаем и рисуем все пушки
        for gun in state.guns:
            gun.active = False
            gun.draw()

        # Включаем "активную" пушку
        gun = state.active_gun
        gun.active = True

        # Выводим количество оставшихся целей
        text = font.render(
            f"Осталось целей: {len(state.targets)}",
            True,
            colors.black.value())
        screen.blit(text, (10, 20))

        # Выводим количество использованных шаров
        text = font.render(
            f"Потрачено шаров на цель: {state.balls.shot_count}",
            True,
            colors.black.value()
        )
        screen.blit(text, (10, 30))

        # Выводим список шаров, которые будут следующими
        count_ball = 0
        for i in state.balls.get_queue():
            text = font.render(
                f"{str(i).split('.')[-1][:-2]}", True, colors.black.value())
            screen.blit(text, (10, 60 + (count_ball * 10)))
            count_ball += 1

        # Рисуем все цели
        for target in state.targets:
            target.draw()
        # Рисуем все шары
        state.balls.draw()
        # Рисуем бомбу
        state.bomb.draw()

        pygame.display.update()

        # Используем timestep для вычисления передвижения,
        # чтобы не привязывать скорость шара к количеству FPS
        # clock.tick() возвращает количество миллисекунд,
        # прошедших с последнего кадра
        timestep = clock.tick(GameSettings.FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gun.fire2_start(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                gun.fire2_end(event)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)

        # Двигаем все шары
        state.balls.move()

        # Отсчитываем время для сброса целей с бомбы
        if lastdrop >= 5:
            lastdrop = 0
            state.bomb.drop()
        else:
            lastdrop += timestep

        # Для переключения между пушками проверяем, попал ли шарик в пушку
        for gun_test in state.guns:
            gun_test.move()
            if gun_test == state.active_gun:
                continue
            htest = state.balls.hittest(gun_test)
            if htest is not None:
                state.balls.remove_ball(htest)
                state.balls.get_queue().insert(0, type(htest))
                state.active_gun = gun_test

        # Для уничтожения целей проверяем, попал ли какой-либо шарик в цель
        for target in state.targets:
            target.move()
            htest = state.balls.hittest(target)
            if htest is not None:
                state.hit_target(target)
                state.balls.remove_ball(htest)

        # Увеличение силы выстрела в конце
        gun.power_up()
    else:
        # Начинаем новый раунд
        state.new_round()

pygame.quit()
