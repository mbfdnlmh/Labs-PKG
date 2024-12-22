import tkinter as tk
from tkinter import messagebox
import time

class RasterizationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Rasterization Algorithms")
        self.master.geometry("900x700")
        self.scale = 20  # Масштаб для работы с координатами (начальный масштаб)
        
        # Coordinates inputs
        tk.Label(master, text="X1 (start point):").grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.x1_entry = tk.Entry(master)
        self.x1_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(master, text="Y1 (start point):").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        self.y1_entry = tk.Entry(master)
        self.y1_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(master, text="X2 (end point/radius):").grid(row=2, column=0, sticky='e', padx=5, pady=2)
        self.x2_entry = tk.Entry(master)
        self.x2_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(master, text="Y2 (end point, empty for circle):").grid(row=3, column=0, sticky='e', padx=5, pady=2)
        self.y2_entry = tk.Entry(master)
        self.y2_entry.grid(row=3, column=1, padx=5, pady=2)

        # Buttons
        self.step_button = tk.Button(master, text="Step Algorithm", command=self.draw_step_algorithm)
        self.step_button.grid(row=0, column=2, padx=5, pady=2)

        self.cda_button = tk.Button(master, text="CDA Algorithm", command=self.draw_cda_algorithm)
        self.cda_button.grid(row=1, column=2, padx=5, pady=2)

        self.bresenham_button = tk.Button(master, text="Bresenham Line", command=self.draw_bresenham_algorithm)
        self.bresenham_button.grid(row=2, column=2, padx=5, pady=2)

        self.bresenham_circle_button = tk.Button(master, text="Bresenham Circle", command=self.draw_bresenham_circle)
        self.bresenham_circle_button.grid(row=3, column=2, padx=5, pady=2)

        # Create a canvas to draw the results
        self.canvas = tk.Canvas(master, width=800, height=500, bg="white")
        self.canvas.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        # Field to show time taken for algorithms
        tk.Label(master, text="Time taken for algorithm (in seconds):").grid(row=5, column=0, columnspan=2, sticky='e', padx=5)
        self.time_display = tk.Label(master, text="")
        self.time_display.grid(row=5, column=2, sticky='w', padx=5)

        # Scale adjustment (Slider)
        tk.Label(master, text="Scale:").grid(row=6, column=0, sticky='e', padx=5, pady=5)
        self.scale_slider = tk.Scale(master, from_=5, to=50, orient="horizontal", command=self.update_scale)
        self.scale_slider.set(self.scale)
        self.scale_slider.grid(row=6, column=1, columnspan=2, padx=5, pady=5)

    def clear_canvas(self):
        self.canvas.delete("all")

    def draw_grid(self):
        """ Drawing the grid with axes centered, so that we can see everything """
        # Draw grid lines and axes:
        for i in range(0, 800, self.scale):
            self.canvas.create_line(i, 0, i, 500, fill="lightgray")
            self.canvas.create_line(0, i, 800, i, fill="lightgray")

        # Draw X and Y axes at calculated center positions
        center_x = 400
        center_y = 250
        self.canvas.create_line(center_x, 0, center_x, 500, fill="black", width=2)  # Y axis
        self.canvas.create_line(0, center_y, 800, center_y, fill="black", width=2)  # X axis

        # Drawing coordinate labels
        for i in range(-20, 21, 5):
            # X axis labels
            self.canvas.create_text(center_x + i * self.scale, center_y + 15, text=str(i), fill="black")
            # Y axis labels
            self.canvas.create_text(center_x + 15, center_y - i * self.scale, text=str(i), fill="black")

    def scale_coordinates(self, x, y):
        """ Функция для масштабирования координат в пикселях относительно центра окна """
        # Преобразуем координаты в пиксели с учетом масштаба
        center_x = 400
        center_y = 250
        return center_x + x * self.scale, center_y - y * self.scale

    def update_scale(self, value):
        """ Обновить масштаб и перерисовать сетку """
        self.scale = int(value)
        self.clear_canvas()
        self.draw_grid()

    def draw_step_algorithm(self):
        """Draw using Step Algorithm"""
        if not self.x1_entry.get() or not self.y1_entry.get() or not self.x2_entry.get():
            messagebox.showerror("Ошибка", "Пожалуйста, введите все координаты.")
            return

        try:
            x1 = float(self.x1_entry.get())
            y1 = float(self.y1_entry.get())
            x2 = float(self.x2_entry.get())
            y2 = float(self.y2_entry.get()) if self.y2_entry.get() else y1  # If no Y2, use Y1 for horizontal line
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные координаты.")
            return

        # Start time
        start_time = time.time()

        self.clear_canvas()
        self.draw_grid()

        # Step Algorithm logic (example for drawing a line)
        x1_scaled, y1_scaled = self.scale_coordinates(x1, y1)
        x2_scaled, y2_scaled = self.scale_coordinates(x2, y2)
        self.canvas.create_line(x1_scaled, y1_scaled, x2_scaled, y2_scaled, fill="red", width=2)

        # End time
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.time_display.config(text=f"{elapsed_time:.6f} секунд")

    def draw_cda_algorithm(self):
        """Draw using CDA Algorithm"""
        if not self.x1_entry.get() or not self.y1_entry.get() or not self.x2_entry.get() or not self.y2_entry.get():
            messagebox.showerror("Ошибка", "Пожалуйста, введите все координаты.")
            return

        try:
            x1 = float(self.x1_entry.get())
            y1 = float(self.y1_entry.get())
            x2 = float(self.x2_entry.get())
            y2 = float(self.y2_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные координаты.")
            return

        # Start time
        start_time = time.time()

        self.clear_canvas()
        self.draw_grid()

        # CDA Algorithm logic (example for drawing a line)
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))

        Xinc = dx / steps
        Yinc = dy / steps

        x = x1
        y = y1

        # Draw lines between points
        for i in range(int(steps)):
            x_scaled, y_scaled = self.scale_coordinates(x, y)
            next_x_scaled, next_y_scaled = self.scale_coordinates(x + Xinc, y + Yinc)
            self.canvas.create_line(x_scaled, y_scaled, next_x_scaled, next_y_scaled, fill="blue")
            x += Xinc
            y += Yinc

        # End time
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.time_display.config(text=f"{elapsed_time:.6f} секунд")

    def draw_bresenham_algorithm(self):
        """Draw using Bresenham's Algorithm"""
        if not self.x1_entry.get() or not self.y1_entry.get() or not self.x2_entry.get() or not self.y2_entry.get():
            messagebox.showerror("Ошибка", "Пожалуйста, введите все координаты.")
            return

        try:
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
            x2 = int(self.x2_entry.get())
            y2 = int(self.y2_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные координаты.")
            return

        # Bresenham Line Drawing Algorithm
        start_time = time.time()

        self.clear_canvas()
        self.draw_grid()

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            x_scaled, y_scaled = self.scale_coordinates(x1, y1)
            self.canvas.create_oval(x_scaled, y_scaled, x_scaled + 2, y_scaled + 2, fill="green", width=1)

            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        # End time
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.time_display.config(text=f"{elapsed_time:.6f} секунд")

    def draw_bresenham_circle(self):
        """Draw using Bresenham's Circle Algorithm"""
        if not self.x1_entry.get() or not self.y1_entry.get() or not self.x2_entry.get():
            messagebox.showerror("Ошибка", "Пожалуйста, введите все координаты.")
            return

        try:
            xc = int(self.x1_entry.get())
            yc = int(self.y1_entry.get())
            r = int(self.x2_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные координаты.")
            return

        # Bresenham Circle Drawing Algorithm
        start_time = time.time()

        self.clear_canvas()
        self.draw_grid()

        x = 0
        y = r
        p = 3 - 2 * r

        def plot_circle_points(xc, yc, x, y):
            """Plot circle points in all octants"""
            points = [
                (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
                (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
            ]
            for px, py in points:
                px_scaled, py_scaled = self.scale_coordinates(px, py)
                self.canvas.create_oval(px_scaled, py_scaled, px_scaled + 2, py_scaled + 2, fill="purple", width=1)

        # Initial circle drawing
        while x <= y:
            plot_circle_points(xc, yc, x, y)
            x += 1
            if p < 0:
                p += 4 * x + 6
            else:
                y -= 1
                p += 4 * (x - y) + 10

        # End time
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.time_display.config(text=f"{elapsed_time:.6f} секунд")


if __name__ == "__main__":
    root = tk.Tk()
    app = RasterizationApp(root)
    root.mainloop()
