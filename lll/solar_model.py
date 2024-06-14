# coding: utf-8
# license: GPLv3

from solar_objects import *
G = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список объектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени
    
    star_body - это centre_body, вокруг готорого вращается planet и т.д
    """

    for star_body in space_objects:
        if isinstance(star_body, Star):
            star_ID = star_body.ID
            for planet_body in space_objects:
                if isinstance(planet_body, Planet) and planet_body.ID /11 == star_ID:
                    planet_body.rotate_planet_around(star_body, dt)
                    planet_ID = planet_body.ID
                    for satelite_body in space_objects:
                        if isinstance(satelite_body, Satelite) and satelite_body.ID / 11== planet_ID:
                            satelite_body.rotate_satelite_around(planet_body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")
