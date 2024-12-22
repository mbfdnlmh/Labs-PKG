import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


# Алгоритм Сазерленда-Коэна для отсечения отрезков
def sutherland_cohen_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    def compute_code(x, y):
        code = 0
        if x < xmin:
            code |= 1  # левая граница
        elif x > xmax:
            code |= 2  # правая граница
        if y < ymin:
            code |= 4  # нижняя граница
        elif y > ymax:
            code |= 8  # верхняя граница
        return code

    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)

    while True:
        # Полностью внутри окна
        if code1 == 0 and code2 == 0:
            return [(x1, y1), (x2, y2)]
        
        # Полностью снаружи
        elif code1 & code2 != 0:
            return None
        
        # Частично внутри
        else:
            # Выбираем точку за пределами окна
            outside_code = code1 if code1 != 0 else code2
            
            # Вычисляем точку пересечения
            if outside_code & 1:  # левая граница
                x = xmin
                y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
            elif outside_code & 2:  # правая граница
                x = xmax
                y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
            elif outside_code & 4:  # нижняя граница
                y = ymin
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            else:  # верхняя граница
                y = ymax
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            
            # Обновляем точку и код
            if outside_code == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2)


# Алгоритм Сазерленда-Ходжмана для отсечения выпуклых многоугольников
def sutherland_hodgman_clip(polygon, clip_window):
    xmin, ymin, xmax, ymax = clip_window

    def inside(x, y, edge):
        if edge == 'left':
            return x >= xmin
        elif edge == 'right':
            return x <= xmax
        elif edge == 'bottom':
            return y >= ymin
        elif edge == 'top':
            return y <= ymax

    def intersection(x1, y1, x2, y2, edge):
        if edge == 'left':
            x = xmin
            y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
        elif edge == 'right':
            x = xmax
            y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
        elif edge == 'bottom':
            y = ymin
            x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
        elif edge == 'top':
            y = ymax
            x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
        return x, y

    # Последовательно отсекаем по каждой границе
    output_polygon = polygon
    for edge in ['left', 'right', 'bottom', 'top']:
        input_polygon = output_polygon
        output_polygon = []

        if not input_polygon:
            break

        for i in range(len(input_polygon)):
            current = input_polygon[i]
            previous = input_polygon[(i - 1) % len(input_polygon)]

            # Текущая точка внутри
            if inside(current[0], current[1], edge):
                # Предыдущая снаружи
                if not inside(previous[0], previous[1], edge):
                    intersect = intersection(previous[0], previous[1], current[0], current[1], edge)
                    output_polygon.append(intersect)
                output_polygon.append(current)
            # Текущая точка снаружи
            elif inside(previous[0], previous[1], edge):
                intersect = intersection(previous[0], previous[1], current[0], current[1], edge)
                output_polygon.append(intersect)

    return output_polygon if output_polygon else None


# Функция для рисования отрезков и многоугольников
def plot_segments(segments, clip_window, ax, title, is_polygon=False):
    xmin, ymin, xmax, ymax = clip_window
    ax.clear()
    ax.set_title(title)
    ax.set_xlim(xmin - 1, xmax + 1)
    ax.set_ylim(ymin - 1, ymax + 1)

    # Рисуем отсекающее окно
    rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, 
                         linewidth=2, edgecolor='red', facecolor='none')
    ax.add_patch(rect)

    # Рисуем отрезки или многоугольники
    if is_polygon:
        # Для многоугольников замыкаем контур
        for polygon in segments:
            if polygon:
                polygon_coords = polygon + [polygon[0]]
                x_coords, y_coords = zip(*polygon_coords)
                ax.fill(x_coords, y_coords, alpha=0.3, color='blue', edgecolor='blue')
    else:
        # Для отрезков
        for segment in segments:
            if len(segment) == 4:  # Исходные отрезки
                x1, y1, x2, y2 = segment
                ax.plot([x1, x2], [y1, y2], color="blue")
            else:  # Результат отсечения
                x1, y1, x2, y2 = segment[0][0], segment[0][1], segment[1][0], segment[1][1]
                ax.plot([x1, x2], [y1, y2], color="blue")

    ax.set_aspect('equal')


# Чтение данных из файла
def read_data(file_path):
    segments = []
    clip_window = None
    with open(file_path, 'r') as file:
        # Читаем тип данных первой строкой
        data_type = file.readline().strip().lower()
        
        # Читаем количество сегментов/многоугольников
        n = int(file.readline())
        
        # Читаем сегменты или многоугольники
        if data_type == 'lines':
            for _ in range(n):
                x1, y1, x2, y2 = map(float, file.readline().split())
                segments.append((x1, y1, x2, y2))
        elif data_type == 'polygons':
            for _ in range(n):
                # Читаем многоугольник (набор точек)
                m = int(file.readline())  # Количество точек в многоугольнике
                polygon = []
                for _ in range(m):
                    x, y = map(float, file.readline().split())
                    polygon.append((x, y))
                segments.append(polygon)
        
        # Читаем координаты отсекающего окна
        clip_window = tuple(map(float, file.readline().split()))
    
    return segments, clip_window, data_type


class LineClippingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритм отсечения отрезков и многоугольников")
        
        # Переменные для хранения данных
        self.file_path = None
        self.segments = None
        self.clip_window = None
        self.data_type = None
        
        # Создаем frame для кнопок
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Кнопка для выбора файла
        self.file_select_button = tk.Button(
            self.button_frame, 
            text="Выбрать файл с данными", 
            command=self.on_file_select
        )
        self.file_select_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Кнопка для алгоритма Сазерленда-Коэна
        self.sutherland_button = tk.Button(
            self.button_frame, 
            text="Отсечение отрезков (Сазерленд-Коэна)", 
            command=self.on_sutherland_cohen_button_click,
            state=tk.DISABLED  # изначально неактивна
        )
        self.sutherland_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Кнопка для отсечения многоугольников
        self.polygon_button = tk.Button(
            self.button_frame, 
            text="Отсечение многоугольников", 
            command=self.on_polygon_clip_button_click,
            state=tk.DISABLED  # изначально неактивна
        )
        self.polygon_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Создаем место для графика
        self.figure, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def on_file_select(self):
        """Выбор файла с данными"""
        self.file_path = filedialog.askopenfilename(
            title="Выберите файл", 
            filetypes=[("Text files", "*.txt")]
        )
        if self.file_path:
            try:
                self.segments, self.clip_window, self.data_type = read_data(self.file_path)
                
                # Очищаем график
                self.ax.clear()
                self.canvas.draw()
                
                # Активируем кнопки в зависимости от типа данных
                if self.data_type == 'lines':
                    self.sutherland_button.config(state=tk.NORMAL)
                    self.polygon_button.config(state=tk.DISABLED)
                elif self.data_type == 'polygons':
                    self.sutherland_button.config(state=tk.DISABLED)
                    self.polygon_button.config(state=tk.NORMAL)
                
                messagebox.showinfo("Файл выбран", f"Выбран файл: {self.file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {str(e)}")

    def on_sutherland_cohen_button_click(self):
        """Применение алгоритма Сазерленда-Коэна"""
        # Проверка, что файл выбран и это линии
        if not self.file_path or self.data_type != 'lines':
            messagebox.showwarning("Ошибка", "Выберите файл с отрезками!")
            return
        
        # Применяем алгоритм отсечения
        clipped_segments = []
        for segment in self.segments:
            x1, y1, x2, y2 = segment
            clipped = sutherland_cohen_clip(x1, y1, x2, y2, *self.clip_window)
            if clipped:
                clipped_segments.append(clipped)
        
        # Рисуем отсеченные отрезки
        plot_segments(clipped_segments, self.clip_window, self.ax, "Отсеченные отрезки (Сазерленд-Коэна)")
        self.canvas.draw()

    def on_polygon_clip_button_click(self):
        """Применение алгоритма отсечения многоугольников"""
        # Проверка, что файл выбран и это многоугольники
        if not self.file_path or self.data_type != 'polygons':
            messagebox.showwarning("Ошибка", "Выберите файл с многоугольниками!")
            return
        
        # Применяем алгоритм отсечения многоугольников
        clipped_polygons = []
        for polygon in self.segments:
            clipped = sutherland_hodgman_clip(polygon, self.clip_window)
            if clipped:
                clipped_polygons.append(clipped)
        
        # Рисуем отсеченные многоугольники
        plot_segments(clipped_polygons, self.clip_window, self.ax, "Отсеченные многоугольники", is_polygon=True)
        self.canvas.draw()


def create_gui():
    root = tk.Tk()
    app = LineClippingApp(root)
    root.mainloop()


if __name__ == "__main__":
    create_gui()