import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # Используем ttk для Treeview
from PIL import Image
from PIL.PngImagePlugin import PngImageFile
from PIL.JpegImagePlugin import JpegImageFile
from PIL.BmpImagePlugin import BmpImageFile
from PIL.GifImagePlugin import GifImageFile
from PIL.TiffImagePlugin import TiffImageFile
import os
import concurrent.futures
import logging

# Настройка логирования
logging.basicConfig(
    filename="image_processing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Функция для получения информации о изображении
def get_image_info(image_path):
    try:
        info = {}
        data = Image.open(image_path)
        with Image.open(image_path) as img:
            info['filename'] = os.path.basename(image_path)
            info['size'] = f"{img.width} x {img.height} px"
            info['color_depth'] = img.mode
            if isinstance(img, JpegImageFile):
                info['compression'] = 'Lossy'
            elif isinstance(img, PngImageFile):
                info['compression'] = 'Deflate'
            elif isinstance(img, GifImageFile):
                info['compression'] = 'LZW'
            elif isinstance(img, BmpImageFile):
                info['compression'] = 'RLE or None'
            elif isinstance(img, TiffImageFile):
                info['compression'] = img.info.get('compression', 'N/A')
            else:
                info['compression'] = 'N/A'

        logging.info(f"Processed file: {image_path}")
        return info

    except Exception as e:
        logging.error(f"Error processing file {image_path}: {e}")
        return {'error': str(e)}

# Асинхронная обработка файлов
def process_file(file_path):
    try:
        return get_image_info(file_path)
    except Exception as e:
        logging.error(f"Error in process_file for {file_path}: {e}")
        return {'filename': os.path.basename(file_path), 'error': str(e)}

def process_directory():
    folder = filedialog.askdirectory(title="Выберите папку с изображениями")
    if not folder:
        logging.warning("No folder selected.")
        return

    logging.info(f"Selected folder: {folder}")

    try:
        all_files = os.scandir(folder)
        files = [entry.path for entry in all_files if entry.is_file() and entry.name.lower().endswith(('jpg', 'jpeg', 'gif', 'tif', 'bmp', 'png', 'pcx'))]
        
        logging.info(f"Total files found: {len(files)}")

        for row in tree.get_children():
            tree.delete(row)

        # Асинхронная обработка файлов
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(process_file, files)

        for result in results:
            if 'error' in result:
                logging.warning(f"Failed to process file: {result['filename']} - {result['error']}")
            else:
                tree.insert("", "end", values=(
                    result['filename'], result.get('size', 'N/A'), result.get('color_depth', 'N/A'), result.get('compression', 'N/A')
                ))

    except Exception as e:
        logging.error(f"Error processing directory {folder}: {e}")
        messagebox.showerror("Ошибка", f"Не удалось обработать папку: {e}")

# Создаем окно приложения
root = tk.Tk()
root.title("Информация об изображениях")
root.geometry("800x500")  # Задаем фиксированный размер окна
root.resizable(False, False)

# Стилизация
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", rowheight=25, font=("Arial", 10))
style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
style.configure("TButton", font=("Arial", 10), padding=5)

# Верхняя панель с кнопкой
frame_top = tk.Frame(root, bg="#f0f0f0")
frame_top.pack(side="top", fill="x", padx=10, pady=10)

btn_load_folder = ttk.Button(frame_top, text="Загрузить папку с изображениями", command=process_directory)
btn_load_folder.pack(pady=5)

# Центр с таблицей и прокруткой
frame_center = tk.Frame(root, bg="#ffffff")
frame_center.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("Имя файла", "Размер (px)", "Глубина цвета", "Сжатие")
tree = ttk.Treeview(frame_center, columns=columns, show="headings")
tree.pack(side="left", fill="both", expand=True)

# Прокрутка для таблицы
scroll_y = ttk.Scrollbar(frame_center, orient="vertical", command=tree.yview)
scroll_y.pack(side="right", fill="y")
tree.configure(yscrollcommand=scroll_y.set)

# Заголовки и ширина колонок
for col in columns:
    tree.heading(col, text=col, anchor="center")
    tree.column(col, anchor="center", width=150)

# Запуск приложения
root.mainloop()
