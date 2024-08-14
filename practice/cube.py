import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import networkx as nx
import itertools

# Инициализация вершин куба
vertices = [(x, y, z) for x in range(2) for y in range(2) for z in range(2)]

# Определение рёбер куба
edges = [
    (v1, v2)
    for v1, v2 in itertools.combinations(vertices, 2)
    if sum([abs(a - b) for a, b in zip(v1, v2)]) == 1
]


def generate_unfolding(start_vertex):
    # Начинаем с фиксированной грани и разворачиваем
    unfolding = [start_vertex]
    stack = [start_vertex]
    visited = set(unfolding)

    # Делаем развёртку до тех пор, пока не получим 6 граней
    while len(unfolding) < 6:
        current = stack.pop()

        # Поиск соседних граней
        for edge in edges:
            if current in edge:
                neighbor = edge[0] if edge[1] == current else edge[1]

                # Добавляем только новые грани
                if neighbor not in visited:
                    unfolding.append(neighbor)
                    stack.append(neighbor)
                    visited.add(neighbor)
                    break

    return unfolding


def visualize_unfolding(unfolding):
    # Создаем граф для визуализации
    G = nx.Graph()
    G.add_edges_from(edges)

    # Позиции вершин для развёртки
    pos = {
        (0, 0, 0): (0, 0),
        (1, 0, 0): (1, 0),
        (0, 1, 0): (0, 1),
        (1, 1, 0): (1, 1),
        (0, 0, 1): (0, 2),
        (1, 0, 1): (1, 2),
        (0, 1, 1): (0, 3),
        (1, 1, 1): (1, 3),
    }

    # Визуализация
    plt.figure(figsize=(6, 6))
    nx.draw(G, pos=pos, with_labels=True, node_color='lightblue', node_size=500)
    plt.title("Развёртка куба")
    plt.show()


# Функция для обновления развёртки
def update_unfolding():
    start_vertex = (int(x_var.get()), int(y_var.get()), int(z_var.get()))
    unfolding = generate_unfolding(start_vertex)
    visualize_unfolding(unfolding)


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

# Кнопка для построения развёртки
build_button = ttk.Button(frame, text="Построить развёртку", command=update_unfolding)
build_button.grid(column=0, row=4, columnspan=2, pady=10)

# Настройки для расширяемости интерфейса
for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
