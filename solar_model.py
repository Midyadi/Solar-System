# coding: utf-8
# license: GPLv3
import math

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """
    Вычисляет силу, действующую на тело.

    Args:
        body — тело, для которого нужно вычислить дейстующую силу

        space_objects — список объектов, которые воздействуют на тело
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if body != obj:
            r = ((body.x - obj.x) ** 2 + (body.y - obj.y) ** 2) ** 0.5
            r = max(r, body.R)  # FIXME: обработка аномалий при прохождении одного тела сквозь другое
            f = gravitational_constant * obj.m * body.m / r ** 2
            alpha = math.atan2((body.y - obj.y), (body.x - obj.x))
            body.Fx -= f * math.cos(alpha)
            body.Fy -= f * math.sin(alpha)


def move_space_object(body, dt):
    """
    Перемещает тело в соответствии с действующей на него силой.

    Args:
        body — тело, которое нужно переместить
        dt - шаг по времени
    """

    ax = body.Fx / body.m
    ay = body.Fy / body.m
    body.Vx += ax * dt
    body.Vy += ay * dt
    body.x += body.Vx * dt
    body.y += body.Vy * dt
    body.orbit.append([body.x, body.y])


def recalculate_space_objects_positions(space_objects, dt):
    """
    Пересчитывает координаты объектов.

    Args:
        space_objects — список объектов, для которых нужно пересчитать координаты
        dt — шаг по времени
    """

    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        move_space_object(body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")
