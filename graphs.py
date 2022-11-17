import matplotlib
from matplotlib import pyplot as plt


def reading(file_name):
    with open(file_name, 'rt', encoding='utf-8') as file:
        speed, x_speed, y_speed, dst, t = [[float(i) for i in line.split()] for line in file.readlines()]
        speed = [i / 1000 for i in speed]
        x_speed = [i / 1000 for i in x_speed]
        y_speed = [i / 1000 for i in y_speed]
        dst = [i / 1000000000 for i in dst]
        t = [i / 3600 / 24 for i in t]
    return speed, x_speed, y_speed, dst, t


def plotting(x_data, y_data, name, x_label, y_label):
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
    pass
