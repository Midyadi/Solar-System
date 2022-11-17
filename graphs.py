import matplotlib
from matplotlib import pyplot as plt


def reading(file_name):

    """
    Считывает и обрабатывает информацию из входного файла

    Args:
        file_name - название входного файла

    Returns:
        speed - скорость в разные моменты времени

        x_speed, y_speed - иксовая и игрековая компоненты скорости в разные моменты времени

        dst - расстояние до звезды в разные моменты времени

        t - моменты времени
    """

    with open(file_name, 'rt', encoding='utf-8') as file:
        speed, x_speed, y_speed, dst, t = [[float(i) for i in line.split()] for line in file.readlines()]
        speed = [i / 1000 for i in speed]
        x_speed = [i / 1000 for i in x_speed]
        y_speed = [i / 1000 for i in y_speed]
        dst = [i / 1000000000 for i in dst]
        t = [i / 3600 / 24 for i in t]
    return speed, x_speed, y_speed, dst, t


def plotting(x_data, y_data, name, x_label, y_label):

    """
    Создаёт картинку с графиком

    Args:
        x_data - данные по оси x

        y_data - данные по оси y

        name - имя картинки с графиком

        x_label - подпись оси x

        y_label - подпис оси y
    """

    matplotlib.rcParams['font.size'] = 19
    plt.figure(figsize=(11, 7))

    plt.grid(visible=True, which='major', axis='both', alpha=1)
    plt.grid(visible=True, which='minor', axis='both', alpha=0.5)
    plt.minorticks_on()

    plt.title(name[:-4])
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.plot(x_data, y_data)
    plt.savefig(name)


def show_graph():

    """
    Выводит заранее изготовленную картинку с графиком на экран
    """

    pass
