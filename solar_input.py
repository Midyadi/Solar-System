# coding: utf-8
# license: GPLv3

from solar_objects import SpaceObject
from solar_vis import DrawableObject


def read_space_objects_data_from_file(input_filename):
    """
    Считывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Args:
        input_filename — имя входного файла

    Returns:
        список DrawableObject объектов
    """

    objects = []
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            else:
                obj = SpaceObject()
                parse_object_parameters(line, obj)
                objects.append(obj)

    return [DrawableObject(obj) for obj in objects]


def parse_object_parameters(line, obj):
    """
    Считывает данные об объекте из строки.
    Входная строка должна иметь следующий формат:
    <тип объекта> <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Здесь (x, y) — координаты, (Vx, Vy) — скорость.

    Пример строки:
    Star 10 red 1000 1 2 3 4

    Параметры:
    **line** — строка с описанием объекта.
    **obj** — объект.
    """
    line = line.split()
    obj.type = line[0].lower()
    obj.orbit = []
    obj.R = float(line[1])
    obj.color = line[2]
    obj.m, obj.x, obj.y, obj.Vx, obj.Vy = [float(param) for param in line[3:]]


def write_space_objects_data_to_file(output_filename, space_objects):
    """
    Сохраняет данные о космических объектах в файл.
    Строки должны иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Параметры:
    **output_filename** — имя входного файла
    **space_objects** — список объектов планет и звёзд
    """

    with open(output_filename, 'w') as out_file:
        for obj in space_objects:
            print(*obj, file=out_file)


if __name__ == "__main__":
    print("This module is not for direct call!")
