# coding: utf-8
# license: GPLv3

from solar_objects import *


def read_space_objects_data_from_file(input_filename):
    """Считывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла

    ID сичтается по формуле: self.id += self.id * 10 , только записывать в файле надо по следующему правилу:
    star : id
    planet : id
    satelite : id * 11 
    
    """
    
    objects = []
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            parts = line.split()
            object_type = parts[0].lower()
            ID = int(parts[-1]) * 10  # Увеличиваем ID на 10 для планет и на 100 для спутников
            if object_type == "star":
                star = Star()
                star.parse_star_parameters(line)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                planet.parse_planet_parameters(line)
                planet.ID += ID  # Добавляем вложенность к ID планеты
                objects.append(planet)
            elif object_type == "satelite":
                satelite = Satelite()
                satelite.parse_satelite_parameters(line)
                satelite.ID += ID  # Добавляем вложенность к ID спутника
                objects.append(satelite)
            else:
                print("Unknown space object")

    return objects

def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.
    Строки должны иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:
    
    **output_filename** — имя выходного файла
    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        for obj in space_objects:
            if isinstance(obj, Planet):
                out_file.write(f"Planet {obj.R} {obj.color} {obj.m} {obj.x} {obj.y} {obj.Vx} {obj.Vy}\n")
            elif isinstance(obj, Star):
                out_file.write(f"Star {obj.R} {obj.color} {obj.m} {obj.x} {obj.y}\n")
            elif obj.type == "satelite":
                out_file.write(f"Satelite {obj.R} {obj.color} {obj.x} {obj.y} {obj.V_tg} {obj.ID}\n")
# FIXME: хорошо бы ещё сделать функцию, сохраняющую статистику в заданный файл...




if __name__ == "__main__":
    print("This module is not for direct call!")