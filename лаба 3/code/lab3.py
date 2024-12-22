import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# Функции обработки изображений
def apply_highpass_filter(image):
    kernel = np.array([[-1, -1, -1], [-1,  9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(image, -1, kernel)
    return sharpened

def apply_local_threshold(image, method="mean"):
    if method == "mean":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    elif method == "gaussian":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return thresh

def apply_global_threshold(image, threshold_value=128):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    return thresh

def apply_adaptive_threshold(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    return adaptive_thresh

def open_image():
    global img
    file_path = filedialog.askopenfilename(title="Открыть изображение", filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if file_path:
        img = cv2.imread(file_path)
        display_image(img)

def display_image(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_tk = ImageTk.PhotoImage(image_pil)
    
    label.config(image=image_tk)
    label.image = image_tk

def process_highpass():
    global img
    img = apply_highpass_filter(img)
    display_image(img)

def process_local_threshold_mean():
    global img
    img = apply_local_threshold(img, method="mean")
    display_image(img)

def process_local_threshold_gaussian():
    global img
    img = apply_local_threshold(img, method="gaussian")
    display_image(img)

def process_global_threshold():
    global img
    img = apply_global_threshold(img)
    display_image(img)

def process_adaptive_threshold():
    global img
    img = apply_adaptive_threshold(img)
    display_image(img)

def save_image():
    global img
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        cv2.imwrite(file_path, img)

# Настройка графического интерфейса с использованием Tkinter
root = Tk()
root.title("Image Processing App")

# Главное окно
label = Label(root)
label.pack(padx=10, pady=10)

# Кнопки
open_button = Button(root, text="Открыть изображение", command=open_image)
open_button.pack(padx=10, pady=5)

# Кнопки для обработки изображений
highpass_button = Button(root, text="High-pass Filter", command=process_highpass)
highpass_button.pack(padx=10, pady=5)

local_mean_button = Button(root, text="Local Threshold (Mean)", command=process_local_threshold_mean)
local_mean_button.pack(padx=10, pady=5)

local_gaussian_button = Button(root, text="Local Threshold (Gaussian)", command=process_local_threshold_gaussian)
local_gaussian_button.pack(padx=10, pady=5)

global_button = Button(root, text="Global Threshold", command=process_global_threshold)
global_button.pack(padx=10, pady=5)

adaptive_button = Button(root, text="Adaptive Threshold", command=process_adaptive_threshold)
adaptive_button.pack(padx=10, pady=5)

# Кнопка сохранения изображения
save_button = Button(root, text="Сохранить изображение", command=save_image)
save_button.pack(padx=10, pady=5)

# Главный цикл приложения
root.mainloop()
