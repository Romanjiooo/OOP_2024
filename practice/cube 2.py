import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
import networkx as nx
import itertools
import matplotlib.image as mpimg

# Инициализация вершин куба
vertices = [(x, y, z) for x in range(2) for y in range(2) for z in range(2)]

# Определение рёбер куба
edges = [
    (v1, v2)
    for v1, v2 in itertools.combinations(vertices, 2)
    if sum([abs(a - b) for a, b in zip(v1, v2)]) == 1
]

# Заранее заданные координаты для визуализации в 2D
# Используем координаты, которые ты предоставил (например, для карты)
predefined_positions = [
    (0, 0),  # 010
    (0, 1),  # 110
    (1, 0),  # 000
    (3, 0),  # 100
    (3, 1),  # 001
    (2, 0),  # 101
    (2, 1),  # 011
    (1, 1)   # 111
]

current_map_image = None  # Переменная для хранения пути к карте
map_scale = 1.0  # Масштаб карты
map_offset = [0, 0]  # Смещение карты

def generate_unfolding(start_vertex):
    # Начинаем с фиксированной грани и разворачиваем куб, начиная с выбранной вершины
    unfolding = [start_vertex]
    stack = [start_vertex]
    visited = set(unfolding)

    # Делаем развёртку, охватывая все вершины куба
    while len(visited) < 8:
        current = stack.pop()

        # Поиск соседних вершин
        for edge in edges:
            if current in edge:
                neighbor = edge[0] if edge[1] == current else edge[1]

                # Добавляем только новые вершины
                if neighbor not in visited:
                    unfolding.append(neighbor)
                    stack.append(neighbor)
                    visited.add(neighbor)

    return unfolding

def visualize_unfolding(unfolding):
    global map_scale, map_offset

    # Создаем граф для визуализации
    G = nx.Graph()
    G.add_edges_from(edges)

    # Назначаем заранее заданные координаты вершинам
    pos = {}
    for i, vertex in enumerate(unfolding):
        pos[vertex] = (predefined_positions[i][0] * map_scale + map_offset[0],
                       predefined_positions[i][1] * map_scale + map_offset[1])

    # Визуализация с наложением на карту
    plt.figure(figsize=(10, 6))

    if current_map_image:
        # Отображение карты
        img = mpimg.imread(current_map_image)
        plt.imshow(img, extent=[0, 3 * map_scale, 0, 2 * map_scale])

    # Наложение графа
    nx.draw(G, pos=pos, with_labels=True, node_color='blue', node_size=500, edge_color='red')

    plt.title("Развёртка куба на карте")
    plt.show()

def update_unfolding():
    start_vertex = (int(x_var.get()), int(y_var.get()), int(z_var.get()))
    unfolding = generate_unfolding(start_vertex)
    visualize_unfolding(unfolding)

def load_map():
    global current_map_image
    map_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if map_path:
        current_map_image = map_path

def zoom_in():
    global map_scale
    map_scale *= 1.25  # Увеличение масштаба карты на 25%
    update_unfolding()

def zoom_out():
    global map_scale
    map_scale /= 1.25  # Уменьшение масштаба карты на 25%
    update_unfolding()

def move_map(dx, dy):
    global map_offset
    map_offset[0] += dx
    map_offset[1] += dy
    update_unfolding()

# Создание графического интерфейса
root = tk.Tk()
root.title("Построение развёрток куба")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Выбор начальной вершины
ttk.Label(frame, text="Выберите начальную вершину куба:").grid(column=0, row=0, columnspan=2, pady=5)

ttk.Label(frame, text="x:").grid(column=0, row=1, sticky=tk.E)
x_var = tk.StringVar(value='0')
x_entry = ttk.Entry(frame, width=5, textvariable=x_var)
x_entry.grid(column=1, row=1)

ttk.Label(frame, text="y:").grid(column=0, row=2, sticky=tk.E)
y_var = tk.StringVar(value='0')
y_entry = ttk.Entry(frame, width=5, textvariable=y_var)
y_entry.grid(column=1, row=2)

ttk.Label(frame, text="z:").grid(column=0, row=3, sticky=tk.E)
z_var = tk.StringVar(value='0')
z_entry = ttk.Entry(frame, width=5, textvariable=z_var)
z_entry.grid(column=1, row=3)

# Кнопка для загрузки карты
load_map_button = ttk.Button(frame, text="Загрузить карту", command=load_map)
load_map_button.grid(column=0, row=4, columnspan=2, pady=10)

# Кнопка для построения развёртки
build_button = ttk.Button(frame, text="Построить развёртку", command=update_unfolding)
build_button.grid(column=0, row=5, columnspan=2, pady=10)

# Кнопки для управления картой
zoom_in_button = ttk.Button(frame, text="Увеличить", command=zoom_in)
zoom_in_button.grid(column=0, row=6, padx=5, pady=5)

zoom_out_button = ttk.Button(frame, text="Уменьшить", command=zoom_out)
zoom_out_button.grid(column=1, row=6, padx=5, pady=5)

move_left_button = ttk.Button(frame, text="Влево", command=lambda: move_map(-0.3, 0))  # Увеличено на 3x
move_left_button.grid(column=0, row=7, padx=5, pady=5)

move_right_button = ttk.Button(frame, text="Вправо", command=lambda: move_map(0.3, 0))  # Увеличено на 3x
move_right_button.grid(column=1, row=7, padx=5, pady=5)

move_up_button = ttk.Button(frame, text="Вверх", command=lambda: move_map(0, 0.3))  # Увеличено на 3x
move_up_button.grid(column=0, row=8, padx=5, pady=5)

move_down_button = ttk.Button(frame, text="Вниз", command=lambda: move_map(0, -0.3))  # Увеличено на 3x
move_down_button.grid(column=1, row=8, padx=5, pady=5)

# Настройки для расширяемости интерфейса
for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
