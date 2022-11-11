# coding: utf-8
# license: GPLv3

import pygame as pg

"""
Модуль визуализации.
Нигде, кроме этого модуля, не используются экранные координаты объектов.
Функции, создающие гaрафические объекты и перемещающие их на экране, принимают физические координаты
"""

header_font = "Arial-16"
"""Шрифт в заголовке"""

window_width = 900
"""Ширина окна"""

window_height = 900
"""Высота окна"""

scale_factor = 1
"""
Масштабирование экранных координат по отношению к физическим.

Тип: float

Мера: количество пикселей на один метр.
"""


def calculate_scale_factor(max_distance):
    """
    Вычисляет значение глобальной переменной **scale_factor** по данной характерной длине

    Args:
        max_distance - максимальное расстояние
    """

    global scale_factor
    scale_factor = 0.5 * min(window_height, window_width) / max_distance
    print('Scale factor:', scale_factor)


def scale_x(x):
    """
    Возвращает экранную **x** координату по **x** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **x** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.

    Args:
        x — иксовая координата модели.

    Returns:
        x_screen - экранная иксовая координата
    """

    x_screen = int(x * scale_factor) + window_width // 2
    return x_screen


def scale_y(y):
    """
    Возвращает экранную **y** координату по **y** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **y** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.
    Направление оси развёрнуто, чтобы у модели ось **y** смотрела вверх.

    Args:
        y - игрековая координата модели

    Returns:
        y_screen - игрековая экранная координата
    """

    y_screen = window_height - (int(y * scale_factor) + window_width // 2)
    return y_screen


if __name__ == "__main__":
    print("This module is not for direct call!")


class Drawer:
    def __init__(self, screen):
        """
        Конструктор класса Drawer

        Args:
            screen - экран
        """
        self.screen = screen

    def update(self, figures, ui):
        """
        Обновляет экран, рисуе объекты, печатает текст

        Args:
            figures - набор объектов для отрисовки
            ui - ?????
        """
        self.screen.fill((0, 0, 0))
        for figure in figures:
            figure.drawing(self.screen)

        ui.blit()
        ui.update()
        pg.display.update()


class DrawableObject:
    def __init__(self, obj):
        """
        Конструктор класса DrawableObject

        Args:
            obj - объект
        """

        self.obj = obj

    def drawing(self, surface):
        """
        Рисует DrawableObject на поверхности surface

        Args:
             surface - поверхность для отрисовки
        """
        pg.draw.circle(surface, self.obj.color, (self.obj.x, self.obj.y), self.obj.R)
