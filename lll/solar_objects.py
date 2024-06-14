# coding: utf-8
# license: GPLv3

class CosmicBody:
    """Тип данных, описывающий звезду.
    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселах и её цвет.
    """
    type: str
    """Признак объекта звезды"""
    R: int
    """Радиус звезды"""
    color: str
    """Цвет звезды"""
    x: float
    """Координата по оси **x**"""
    y: float
    """Координата по оси **y**"""
    m: float
    """Масса звезды"""
    ID: int
    """Идентификатор тела"""
    image = None
    """Изображение звезды"""

    def parse_cosmic_body_parameters(self, line):
        """Считывает данные о звезде из строки.

        Входная строка должна иметь следующий формат:
        Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

        Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
        Пример строки:
        Star 50 yellow 1.0 100.0 200.0 0.0 0.0

        Параметры:
        **line** — строка с описанием звезды.
        **star** — объект звезды.
        """
        line = line.strip()
        if line and not line.startswith('#'):
            parts = line.split()
            self.R = int(parts[1])
            self.color = parts[2]
            self.m = float(parts[3])  # Добавлено для массы
            self.x = float(parts[4])
            self.y = float(parts[5])
            self.ID = int(parts[-1])

    @staticmethod
    def create_cosmic_body_image(space, obj, scale_x, scale_y):
        """Создаёт отображаемый объект.

        Параметры:

        **space** — холст для рисования.
        **star** — объект звезды.
        """
        x = scale_x(obj.x)
        y = scale_y(obj.y)
        r = obj.R
        obj.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=obj.color)


class Star(CosmicBody):
    type = 'star'

    def __init__(self):
        super().__init__()
        self.satellites = []

    def parse_star_parameters(self, line):
        super().parse_cosmic_body_parameters(line)


class Planet(CosmicBody):
    type = 'planet'

    V_tg: float
    """Тангенциальная скорость"""

    def parse_planet_parameters(self, line):
        super().parse_cosmic_body_parameters(line)
        line = line.strip()
        if line and not line.startswith('#'):
            parts = line.split()
            self.V_tg = float(parts[6])

    def rotate_planet_around(self, center_body, dt):
        import math
        """Вращает тело вокруг другого тела.

        Параметры:
        - center_body: Тело, вокруг которого нужно вращаться.
        - dt: Временной шаг.
        """
        r = ((self.x - center_body.x) ** 2 + (self.y - center_body.y) ** 2) ** 0.5
        if r == 0:
            return
        G = 6.67408E-11
        # Calculate the tangential velocity for circular orbit
        self.V_tg = (G * center_body.m / r) ** 0.5
        omega = self.V_tg / r
        phi = omega * dt
        print(f"Planet rotation debug: r={r}, V_tg={self.V_tg}, omega={omega}, phi={phi}")
        cos_phi = math.cos(phi)
        sin_phi = math.sin(phi)
        new_x = (self.x - center_body.x) * cos_phi - (self.y - center_body.y) * sin_phi + center_body.x
        new_y = (self.x - center_body.x) * sin_phi + (self.y - center_body.y) * cos_phi + center_body.y
        self.x = new_x
        self.y = new_y


class Satelite(Planet):
    type = 'satelite'

    def parse_satelite_parameters(self, line):
        super().parse_planet_parameters(line)

    def rotate_satelite_around(self, center_body, dt):
        import math
        r = ((self.x - center_body.x) ** 2 + (self.y - center_body.y) ** 2) ** 0.5
        if r == 0:
            return
        G = 6.67408E-11
        # Calculate the tangential velocity for circular orbit
        V_tg = (G * center_body.m / r) ** 0.5
        omega = V_tg / r
        phi = omega * dt
        print(f"Satelite rotation debug: r={r}, V_tg={V_tg}, omega={omega}, phi={phi}")
        cos_phi = math.cos(phi)
        sin_phi = math.sin(phi)
        new_x = (self.x - center_body.x) * cos_phi - (self.y - center_body.y) * sin_phi + center_body.x
        new_y = (self.x - center_body.x) * sin_phi + (self.y - center_body.y) * cos_phi + center_body.y
        self.x = new_x
        self.y = new_y
