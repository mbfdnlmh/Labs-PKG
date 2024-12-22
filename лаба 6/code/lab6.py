import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import math

class Letter3DVisualization:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Visualization of Letter X")

        # Координаты для правильной буквы "X"
        self.original_points = np.array([
            # Первая диагональ
            [-1, -0.5, 0], [1, 0.5, 0],
            [-1, -0.5, 5], [1, 0.5, 5],

            # Вторая диагональ
            [-1, 0.5, 0], [1, -0.5, 0],
            [-1, 0.5, 5], [1, -0.5, 5]
        ])

        self.faces = [
            # Первая диагональ
            [0, 1, 3, 2],
            # Вторая диагональ
            [4, 5, 7, 6]
        ]

        self.current_points = self.original_points.copy()

        # Создаем интерфейс
        self.create_interface()

    def create_interface(self):
        # Frame для параметров преобразований
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Кнопки преобразований
        transformations = [
            ("Масштабирование", self.scale),
            ("Перенос", self.translate),
            ("Вращение X", lambda: self.rotate('x')),
            ("Вращение Y", lambda: self.rotate('y')),
            ("Вращение Z", lambda: self.rotate('z')),
            ("Проекция XoY", lambda: self.create_projection('xy')),
            ("Проекция XoZ", lambda: self.create_projection('xz')),
            ("Проекция YoZ", lambda: self.create_projection('yz')),
            ("Сброс", self.reset)
        ]

        for label, command in transformations:
            ttk.Button(control_frame, text=label, command=command).pack(side=tk.LEFT, padx=5)

        # Frame для графика
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Первоначальная визуализация
        self.visualize_3d()

    def visualize_3d(self, points=None):
        # Очистка предыдущего графика
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Используем текущие точки, если не переданы другие
        if points is None:
            points = self.current_points

        # Создание 3D графика
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        # Построение системы координат
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([0, 6])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Закрашиваем плоскости
        for face in self.faces:
            verts = [points[face[i]] for i in range(4)]
            ax.add_collection3d(Poly3DCollection([verts], color="cyan", alpha=0.6))

        # Рисуем рёбра
        edges = [
            (0, 1), (1, 3), (3, 2), (2, 0),  # Первая диагональ
            (4, 5), (5, 7), (7, 6), (6, 4)   # Вторая диагональ
        ]
        for edge in edges:
            p1, p2 = points[edge[0]], points[edge[1]]
            ax.plot3D([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color="blue")

        # Оси координат
        ax.plot3D([0, 2], [0, 0], [0, 0], color='red', linewidth=1)  # Ось X
        ax.plot3D([0, 0], [0, 2], [0, 0], color='green', linewidth=1)  # Ось Y
        ax.plot3D([0, 0], [0, 0], [0, 6], color='blue', linewidth=1)  # Ось Z

        # Отображение графика
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def scale(self):
        try:
            scale_factor = float(tk.simpledialog.askfloat("Масштабирование", "Введите коэффициент масштабирования:"))

            # Матрица масштабирования
            scale_matrix = np.eye(3) * scale_factor
            scale_matrix = np.column_stack([scale_matrix, np.zeros(3)])
            scale_matrix = np.vstack([scale_matrix, [0, 0, 0, 1]])

            # Применяем преобразование
            homogeneous_points = np.column_stack([self.current_points, np.ones(len(self.current_points))])
            self.current_points = (homogeneous_points @ scale_matrix)[:, :3]

            # Визуализация
            self.visualize_3d()

            # Вывод матрицы преобразования
            print("Матрица масштабирования:")
            print(scale_matrix)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def translate(self):
        try:
            dx = float(tk.simpledialog.askfloat("Перенос", "Введите смещение по X:"))
            dy = float(tk.simpledialog.askfloat("Перенос", "Введите смещение по Y:"))
            dz = float(tk.simpledialog.askfloat("Перенос", "Введите смещение по Z:"))

            # Матрица переноса
            translate_matrix = np.eye(4)
            translate_matrix[:3, 3] = [dx, dy, dz]

            # Применяем преобразование
            homogeneous_points = np.column_stack([self.current_points, np.ones(len(self.current_points))])
            self.current_points = (homogeneous_points @ translate_matrix)[:, :3]

            # Визуализация
            self.visualize_3d()

            # Вывод матрицы преобразования
            print("Матрица переноса:")
            print(translate_matrix)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def rotate(self, axis):
        try:
            angle = float(tk.simpledialog.askfloat("Вращение", f"Введите угол вращения вокруг оси {axis} (градусы):"))
            angle_rad = np.deg2rad(angle)

            # Матрицы вращения
            if axis == 'x':
                rotate_matrix = np.array([
                    [1, 0, 0, 0],
                    [0, np.cos(angle_rad), -np.sin(angle_rad), 0],
                    [0, np.sin(angle_rad), np.cos(angle_rad), 0],
                    [0, 0, 0, 1]
                ])
            elif axis == 'y':
                rotate_matrix = np.array([
                    [np.cos(angle_rad), 0, np.sin(angle_rad), 0],
                    [0, 1, 0, 0],
                    [-np.sin(angle_rad), 0, np.cos(angle_rad), 0],
                    [0, 0, 0, 1]
                ])
            else:  # z
                rotate_matrix = np.array([
                    [np.cos(angle_rad), -np.sin(angle_rad), 0, 0],
                    [np.sin(angle_rad), np.cos(angle_rad), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]
                ])

            # Применяем преобразование
            homogeneous_points = np.column_stack([self.current_points, np.ones(len(self.current_points))])
            self.current_points = (homogeneous_points @ rotate_matrix)[:, :3]

            # Визуализация
            self.visualize_3d()

            # Вывод матрицы преобразования
            print(f"Матрица вращения вокруг оси {axis}:")
            print(rotate_matrix)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def create_projection(self, plane):
        # Проекции на координатные плоскости
        projection_points = self.current_points.copy()

        if plane == 'xy':
            projection_points[:, 2] = 0  # Проекция на плоскость XoY (Z = 0)
        elif plane == 'xz':
            projection_points[:, 1] = 0  # Проекция на плоскость XoZ (Y = 0)
        else:  # yz
            projection_points[:, 0] = 0  # Проекция на плоскость YoZ (X = 0)

        # Визуализация проекции
        self.visualize_3d(projection_points)

    def reset(self):
        # Возврат к исходным координатам
        self.current_points = self.original_points.copy()
        self.visualize_3d()

def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = Letter3DVisualization(root)
    root.mainloop()

if __name__ == "__main__":
    main()
