from PIL import Image, ImageTk
import tkinter as tk

# Создание основного окна приложения
def create_app():
    app = tk.Tk()
    app.title('Desktop Application')
    app.geometry('800x600')  # Установка размера окна

    # Установка фона окна
    img = Image.open('background_image.png')
    img = img.convert('RGBA')
    tk_img = ImageTk.PhotoImage(img)
    background_label = tk.Label(app, image=tk_img)
    background_label.place(relwidth=1, relheight=1)

    # Поле для ввода текста
    entry = tk.Entry(app)
    entry.pack()

    # Создание кнопок
    button1 = tk.Button(app, text='Button 1')
    button1.pack()

    button2 = tk.Button(app, text='Button 2')
    button2.pack()

    button3 = tk.Button(app, text='Button 3')
    button3.pack()

    button4 = tk.Button(app, text='Button 4')
    button4.pack()

    # Не забудьте сохранить ссылку на изображение фона
    app.background_image = tk_img

    return app

if __name__ == '__main__':
    app = create_app()
    app.mainloop()
