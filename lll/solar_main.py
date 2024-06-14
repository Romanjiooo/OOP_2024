# coding: utf-8
# license: GPLv3

import tkinter
from tkinter import *
from tkinter.filedialog import *
from solar_vis import *
from solar_model import *
from solar_input import *

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

physical_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""

def toggle_orbits():
    if orbits_button['text'] == "orbits ON":
        orbits_button['text'] = "orbits OFF"
    else:
        orbits_button['text'] = "orbits:on"

def open_data_window():
    data_window = Toplevel()
    toplevel_width = 300
    toplevel_height = 300
    data_window.geometry(f"{toplevel_width}x{toplevel_height}")
    data_window.resizable( width=False ,height=False )
    
    # Создание текста
    label_text = Label(data_window, text="Enter cosmic bodie's paramets:")
    label_text.pack(side=TOP)

    label_type = Label(data_window, text="type:")
    label_type.place(x=20, y=40)

    label_radius = Label(data_window, text="R:")
    label_radius.place(x=20, y=70)

    label_color = Label(data_window, text="color:")
    label_color.place(x=20, y=100)

    label_x = Label(data_window, text="x:")
    label_x.place(x=20, y=130)

    label_y = Label(data_window, text="y:")
    label_y.place(x=20, y=160)

    label_V_tg = Label(data_window, text="V_tg:")
    label_V_tg.place(x=20, y=190)

    # Создание полей ввода и размещение их рядом с соответствующими метками
    entry_type = Entry(data_window)
    entry_type.place(x=100, y=50)

    entry_radius = Entry(data_window)
    entry_radius.place(x=100, y=70)

    entry_color = Entry(data_window)
    entry_color.place(x=100, y=100)

    entry_x = Entry(data_window)
    entry_x.place(x=100, y=130)

    entry_y = Entry(data_window)
    entry_y.place(x=100, y=160)

    entry_V_tg = Entry(data_window)
    entry_V_tg.place(x=100, y=190)

def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global physical_time
    global displayed_time
    recalculate_space_objects_positions(space_objects, time_step.get())
    for body in space_objects:
        update_object_position(space, body)     
    physical_time += time_step.get()
    displayed_time.set("%.1f" % physical_time + " seconds gone")

    if perform_execution:
        space.after(101 - int(time_speed.get()), execution)


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True
    start_button['text'] = "Pause"
    start_button['command'] = stop_execution

    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = False
    start_button['text'] = "Start"
    start_button['command'] = start_execution
    print('Paused execution.')


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global perform_execution
    perform_execution = False
    for obj in space_objects:
        space.delete(obj.image)  # удаление старых изображений планет
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    space_objects = read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space_objects])
    calculate_scale_factor(max_distance)

    
    for obj in space_objects:
        if obj.type == 'star':
            Star.create_cosmic_body_image(space, obj, scale_x, scale_y)
        elif obj.type == 'planet':
            Planet.create_cosmic_body_image(space, obj, scale_x, scale_y)
        elif obj.type == 'satelite':
            Satelite.create_cosmic_body_image(space, obj, scale_x, scale_y)
        else:
            raise AssertionError("Unknown cosmic body type")


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    write_space_objects_data_to_file(out_filename, space_objects)


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    global orbits_button

    print('Modelling started!')
    physical_time = 0

    root = tkinter.Tk()
    root.geometry("+450+50")
    # космическое пространство отображается на холсте типа Canvas
    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="black")
    space.pack(side=tkinter.TOP)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    orbits_button = Button(frame, text="orbits:on", command=toggle_orbits, width=10)
    orbits_button.pack(side=RIGHT)

    cosmic_bodies_data = tkinter.Button(frame, text="parametrs", command= open_data_window,width=12)
    cosmic_bodies_data.pack(side=tkinter.LEFT)

    start_button = tkinter.Button(frame, text="Start", command=start_execution, width=6)
    start_button.pack(side=tkinter.LEFT)

    time_step = tkinter.DoubleVar()
    time_step.set(1)
    time_step_entry = tkinter.Entry(frame, textvariable=time_step)
    time_step_entry.pack(side=tkinter.LEFT)

    time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(frame, variable=time_speed, orient=tkinter.HORIZONTAL)
    scale.pack(side=tkinter.LEFT)

    load_file_button = tkinter.Button(frame, text="Open file...", command=open_file_dialog)
    load_file_button.pack(side=tkinter.LEFT)
    save_file_button = tkinter.Button(frame, text="Save to file...", command=save_file_dialog)
    save_file_button.pack(side=tkinter.LEFT)

    displayed_time = tkinter.StringVar()
    displayed_time.set(str(physical_time) + " seconds gone")
    time_label = tkinter.Label(frame, textvariable=displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)

    root.mainloop()
    print('Modelling finished!')

if __name__ == "__main__":
    main()
