import tkinter as tk
import math

# Константы
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2
STAR_RADIUS = 10
PLANET_RADIUS = 5
SATELLITE_RADIUS = 3
ORBIT_SPACING = 30  # увеличено для предотвращения столкновений
PLANET_STEP_ANGLE = 1
SATELLITE_STEP_ANGLE = 5

# Класс для звезды
class Star:
    def __init__(self, canvas, x, y, num_planets, star_index):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.num_planets = num_planets
        self.star_index = star_index
        self.planets = []
        self.draw_star()
        self.create_planets()

    def draw_star(self):
        self.canvas.create_oval(self.x - STAR_RADIUS, self.y - STAR_RADIUS,
                                self.x + STAR_RADIUS, self.y + STAR_RADIUS,
                                fill="yellow")

    def create_planets(self):
        for i in range(self.num_planets):
            angle = i * (360 / self.num_planets)
            orbit_radius = ORBIT_SPACING * (i + 1)
            clockwise = (i + 1) % 2 == 0
            has_satellite = False

            # Проверка условия для спутников
            if self.star_index in [0, 2] and (i + 1) % 2 == 0:
                has_satellite = True

            # Проверка условия для минимального количества планет на четных орбитах
            if (i + 1) % 2 == 0 and len(self.planets) < 3:
                for _ in range(3 - len(self.planets)):
                    self.planets.append(Planet(self.canvas, self.x, self.y, orbit_radius, angle, clockwise, has_satellite))
            else:
                planet = Planet(self.canvas, self.x, self.y, orbit_radius, angle, clockwise, has_satellite)
                self.planets.append(planet)

# Класс для планеты
class Planet:
    def __init__(self, canvas, star_x, star_y, orbit_radius, angle, clockwise, has_satellite):
        self.canvas = canvas
        self.star_x = star_x
        self.star_y = star_y
        self.orbit_radius = orbit_radius
        self.angle = angle
        self.clockwise = clockwise
        self.has_satellite = has_satellite
        self.planet = None
        self.orbit = None
        self.satellite = None
        self.create_planet()
        self.create_orbit()

    def create_planet(self):
        x = self.star_x + self.orbit_radius * math.cos(math.radians(self.angle))
        y = self.star_y + self.orbit_radius * math.sin(math.radians(self.angle))
        self.planet = self.canvas.create_oval(x - PLANET_RADIUS, y - PLANET_RADIUS,
                                              x + PLANET_RADIUS, y + PLANET_RADIUS,
                                              fill="Orange")

        if self.has_satellite:
            self.satellite = Satellite(self.canvas, x, y, SATELLITE_RADIUS, self.orbit_radius / 4)

    def create_orbit(self):
        self.orbit = self.canvas.create_oval(self.star_x - self.orbit_radius, self.star_y - self.orbit_radius,
                                             self.star_x + self.orbit_radius, self.star_y + self.orbit_radius,
                                             outline="white")

    def move(self):
        if self.clockwise:
            self.angle -= PLANET_STEP_ANGLE
        else:
            self.angle += PLANET_STEP_ANGLE

        x = self.star_x + self.orbit_radius * math.cos(math.radians(self.angle))
        y = self.star_y + self.orbit_radius * math.sin(math.radians(self.angle))
        self.canvas.coords(self.planet, x - PLANET_RADIUS, y - PLANET_RADIUS,
                           x + PLANET_RADIUS, y + PLANET_RADIUS)
        if self.satellite:
            self.satellite.move(x, y)

# Класс для спутника
class Satellite:
    def __init__(self, canvas, planet_x, planet_y, radius, orbit_radius):
        self.canvas = canvas
        self.planet_x = planet_x
        self.planet_y = planet_y
        self.radius = radius
        self.orbit_radius = orbit_radius
        self.angle = 0
        self.create_satellite()

    def create_satellite(self):
        x = self.planet_x + self.orbit_radius * math.cos(math.radians(self.angle))
        y = self.planet_y + self.orbit_radius * math.sin(math.radians(self.angle))
        self.satellite = self.canvas.create_oval(x - SATELLITE_RADIUS, y - SATELLITE_RADIUS,
                                                 x + SATELLITE_RADIUS, y + SATELLITE_RADIUS,
                                                 fill="red")

    def move(self, planet_x, planet_y):
        self.planet_x = planet_x
        self.planet_y = planet_y
        self.angle += SATELLITE_STEP_ANGLE
        x = self.planet_x + self.orbit_radius * math.cos(math.radians(self.angle))
        y = self.planet_y + self.orbit_radius * math.sin(math.radians(self.angle))
        self.canvas.coords(self.satellite, x - SATELLITE_RADIUS, y - SATELLITE_RADIUS,
                           x + SATELLITE_RADIUS, y + SATELLITE_RADIUS)

# Главный класс для интерфейса и анимации
class SolarSystemApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
        self.canvas.pack()
        self.show_orbits = tk.BooleanVar()
        self.show_orbits.set(True)
        self.create_ui()
        self.stars = []
        self.create_stars()
        self.animate()

    def create_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack()
        orbit_checkbox = tk.Checkbutton(control_frame, text="Show Orbits", variable=self.show_orbits, command=self.toggle_orbits)
        orbit_checkbox.pack(side=tk.LEFT)

    def create_stars(self):
        self.stars.append(Star(self.canvas, CENTER_X - 300, CENTER_Y - 200, 20, 0))
        self.stars.append(Star(self.canvas, CENTER_X + 300, CENTER_Y - 200, 30, 1))
        self.stars.append(Star(self.canvas, CENTER_X - 300, CENTER_Y + 200, 20, 2))
        self.stars.append(Star(self.canvas, CENTER_X + 300, CENTER_Y + 200, 30, 3))

    def toggle_orbits(self):
        for star in self.stars:
            for planet in star.planets:
                if self.show_orbits.get():
                    self.canvas.itemconfigure(planet.orbit, state='normal')
                else:
                    self.canvas.itemconfigure(planet.orbit, state='hidden')

    def animate(self):
        for star in self.stars:
            for planet in star.planets:
                planet.move()
        self.root.after(50, self.animate)

def main():
    root = tk.Tk()
    app = SolarSystemApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
