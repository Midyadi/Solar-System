# coding: utf-8
# license: GPLv3

import pygame
from Engine import graphs, solar_input, solar_model, solar_vis
import thorpy
import time
import numpy as np

timer = None

alive = True

stopper = False

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

model_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

time_scale = 1000.0
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""


def execution(delta, t):

    """
    Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру
    через время от 1 мс до 100 мс.

    Args:
        delta - промежуток времени между отрисовками

        t - текущий момент времени
    """

    global model_time
    global displayed_time
    solar_model.recalculate_space_objects_positions([dr.obj for dr in space_objects], delta, t)
    model_time += delta


def start_execution():

    """
    Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """

    global perform_execution
    perform_execution = True


def pause_execution():

    """
    Обработчик события нажатия на кнопку Pause.
    Останавливает циклическое исполнение функции execution.
    """

    global perform_execution
    perform_execution = False


def stop_execution():

    """
    Обработчик события нажатия на кнопку Quit.
    Останавливает циклическое исполнение функции execution
    для дальнейшего вывода графиков на экран.
    """

    global stopper
    stopper = True


def open_file():

    """
    Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """

    global space_objects
    global browser
    global model_time

    model_time = 0.0
    in_filename = "Systems Data/one_satellite.txt"
    space_objects = solar_input.read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.obj.x), abs(obj.obj.y)) for obj in space_objects])
    solar_vis.calculate_scale_factor(max_distance)


def handle_events(events, menu):
    global alive
    for event in events:
        menu.react(event)
        if event.type == pygame.QUIT:
            alive = False


def slider_to_real(val):
    return np.exp(5 + val)


def slider_reaction(event):
    global time_scale
    time_scale = slider_to_real(event.el.get_value())


def init_ui(screen):

    """
    Создаёт интерфейс взаимодействия пользователя с симуляцией

    Args:
        screen - экран для отрисовки интерфейса

    Returns:
        menu - сам интерфейс
        box - набор элементов интерфейса
        in-timer - время
    """

    global browser
    slider = thorpy.SliderX(100, (-10, 10), "Simulation speed")
    slider.user_func = slider_reaction
    button_stop = thorpy.make_button("Quit", func=stop_execution)
    button_pause = thorpy.make_button("Pause", func=pause_execution)
    button_play = thorpy.make_button("Play", func=start_execution)
    in_timer = thorpy.OneLineText("Days passed")

    button_load = thorpy.make_button(text="Load a file", func=open_file)

    box = thorpy.Box(elements=[
        slider,
        button_pause,
        button_stop,
        button_play,
        button_load,
        in_timer])
    reaction1 = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=slider_reaction,
                                event_args={"id": thorpy.constants.EVENT_SLIDE},
                                params={},
                                reac_name="slider reaction")
    box.add_reaction(reaction1)

    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen

    box.set_topleft((0, 0))
    box.blit()
    box.update()
    return menu, box, in_timer


def main():

    """
    Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter:
    окно, холст, фрейм с кнопками, кнопки.
    """

    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    global perform_execution
    global timer

    print('Modelling started!')
    physical_time = 0

    pygame.init()

    width = 700
    height = 700
    screen = pygame.display.set_mode((width, height))
    last_time = time.perf_counter()
    drawer = solar_vis.Drawer(screen)
    menu, box, timer = init_ui(screen)
    perform_execution = True

    while alive:
        handle_events(pygame.event.get(), menu)
        cur_time = time.perf_counter()
        if perform_execution:
            execution((cur_time - last_time) * time_scale, model_time)
            text = "%d days passed" % (int(model_time / 3600 / 24))
            timer.set_text(text)

        last_time = cur_time
        drawer.updating(space_objects, box)
        time.sleep(1.0 / 60)

    with open('Output/Data/out_file.txt', 'w', encoding='utf-8') as out_file:
        for body in space_objects:
            if body.obj.type != 'star':
                for data in (body.obj.speed, body.obj.x_speed, body.obj.y_speed, body.obj.dst, body.obj.t):
                    print(*data[:-5], file=out_file)

    data = graphs.reading('Output/Data/out_file.txt')

    graphs.plotting(data[-1], data[0], "../Output/Graphs/V(t).jpg", "t, days", "V, kps")
    graphs.plotting(data[-1], data[1], '../Output/Graphs/Vx(t).jpg', 't, days', 'Vx, kps')
    graphs.plotting(data[-1], data[2], '../Output/Graphs/Vy(t).jpg', 't, days', 'Vy, kps')
    graphs.plotting(data[-1], data[3], '../Output/Graphs/Dst(t).jpg', 't, days', 'dst, mln km')
    graphs.plotting(data[3], data[0], '../Output/Graphs/V(dst).jpg', 'dst, mln km', "V, kps")
    graphs.plotting(data[3], data[1], '../Output/Graphs/Vx(dst).jpg', 'dst, mln km', "Vx, kps")
    graphs.plotting(data[3], data[2], '../Output/Graphs/Vy(dst).jpg', 'dst, mln km', "Vy, kps")

    print('Modelling finished!')


if __name__ == "__main__":
    main()
