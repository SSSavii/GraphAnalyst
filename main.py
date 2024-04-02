from PIL import Image, ImageTk
import tkinter as tk
import sys
import os

# Функция для определения пути к ресурсам
def resource_path(relative_path):
    try:
        # PyInstaller создает временную папку и хранит путь в переменной _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Создание основного окна приложения
def create_app():
    app = tk.Tk()
    app.title('Desktop Application')
    app.geometry('800x600')  # Установка размера окна

    # Установка фона окна
    background_image_path = resource_path('tools/background_image.png')
    img = Image.open(background_image_path)
    img = img.convert('RGBA')
    tk_img = ImageTk.PhotoImage(img)
    background_label = tk.Label(app, image=tk_img)
    background_label.place(relwidth=1, relheight=1)

    # Создание фрейма для центрирования элементов
    center_frame = tk.Frame(app)
    center_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Поле для ввода текста
    entry = tk.Entry(center_frame)
    entry.pack()

    # Создание кнопок и размещение их под полем ввода
    button1 = tk.Button(center_frame, text='Button 1')
    button1.pack(fill='x')

    button2 = tk.Button(center_frame, text='Button 2')
    button2.pack(fill='x')

    button3 = tk.Button(center_frame, text='Button 3')
    button3.pack(fill='x')

    button4 = tk.Button(center_frame, text='Button 4')
    button4.pack(fill='x')

    app.background_image = tk_img

    return app

if __name__ == '__main__':
    app = create_app()
    app.mainloop()
