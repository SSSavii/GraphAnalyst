from PIL import Image, ImageTk
import tkinter as tk
import tkinter.messagebox
import sys
import os
from openpyxl import Workbook, load_workbook
import pandas as pd
from Analyst import read_data_from_file, count_glyphs, find_repeated_glyphs, find_all_repeated_patterns, count_glyphs_in_uni, output_to_excel

# Функция для определения пути к ресурсам
def resource_path(relative_path):
    try:
        # PyInstaller создает временную папку и хранит путь в переменной _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Измененная функция для вывода данных в Excel
def output_to_excel(data_dict, filename='output.xlsx'):
    try:
        # Проверяем, существует ли файл Excel
        if os.path.exists(filename):
            # Файл существует, открываем его и добавляем листы
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='error') as writer:
                for sheet_name, data in data_dict.items():
                    # Проверяем, существует ли лист с таким именем
                    if sheet_name in writer.book.sheetnames:
                        tk.messagebox.showinfo("Информация", f"Данные для листа '{sheet_name}' уже существуют в файле '{filename}'.")
                        return  # Выходим из функции, если лист уже существует
                    df = pd.DataFrame(list(data.items()), columns=['Key', 'Value'])
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            # Файл не существует, создаем новый файл и добавляем листы
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                for sheet_name, data in data_dict.items():
                    df = pd.DataFrame(list(data.items()), columns=['Key', 'Value'])
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        tk.messagebox.showinfo("Успех", f"Данные сохранены в файл '{filename}'.")
    except Exception as e:
        tk.messagebox.showerror("Ошибка", str(e))


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

    # Метка и поле для ввода имени файла Excel
    label_excel_name = tk.Label(center_frame, text="Введите имя выходного файла Excel:")
    label_excel_name.pack()
    entry_excel_name = tk.Entry(center_frame)
    entry_excel_name.pack()

    # Функция для запуска анализа и вывода данных
    def run_analysis(function):
        data_filename = "Data.txt"  # Получаем имя файла данных из поля ввода
        excel_filename = entry_excel_name.get()  # Получаем имя файла Excel из поля ввода
        if not excel_filename:  # Если имя файла Excel не введено, используем имя функции
            excel_filename = function.__name__
        if data_filename:  # Проверяем, что имя файла данных введено
            try:
                glyph_data = read_data_from_file(data_filename)
                result = function(glyph_data)
                output_to_excel({function.__name__: result}, f'{excel_filename}.xlsx')
            except FileNotFoundError:
                tk.messagebox.showerror("Ошибка", f"Файл '{data_filename}' не найден.")
        else:
            tk.messagebox.showerror("Ошибка", "Введите имя файла данных.")

    # Создание кнопок и размещение их под полями ввода
    button1 = tk.Button(center_frame, text='Вывод данных о кол-ве графем',
                        command=lambda: run_analysis(count_glyphs))
    button1.pack(fill='x')

    button2 = tk.Button(center_frame, text='Вывод данных о повторяющихся графемах',
                        command=lambda: run_analysis(find_repeated_glyphs))
    button2.pack(fill='x')

    button3 = tk.Button(center_frame, text='Вывод данных о часто используемых парах графем',
                        command=lambda: run_analysis(find_all_repeated_patterns))
    button3.pack(fill='x')

    button4 = tk.Button(center_frame, text='Вывод данных о длинах иероглифов',
                        command=lambda: run_analysis(count_glyphs_in_uni))
    button4.pack(fill='x')

    app.background_image = tk_img

    return app

if __name__ == '__main__':
    app = create_app()
    app.mainloop()