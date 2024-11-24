from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from datetime import datetime
from calendar_full import CalendarApp, QuarterCalendar
from table_quarter import TableQuarter
from holiday_fetcher import country_names
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_resized_image(image_path, size):
    img = Image.open(image_path)
    img = img.resize(size)
    return ImageTk.PhotoImage(img)

# Инициализация глобальных переменных
main_color='#e6f2fc'
current_year = datetime.now().year
current_start_month = 1  # Начинаем с января
current_country = 'Russia'  # Инициализируем переменную страны


def update_year(year):
    global current_year
    current_year = year
    default_home()


def default_home():
    clear_content()
    CalendarApp(content_frame, current_year, update_year, current_country)


# Функция для отображения календаря по кварталам
def show_quartiles():
    clear_content()
    content_frame.pack_propagate(True)
    content_frame.config(height=screen_height)
    special_days = {2016: {20: 2}, 2017: {}, 2018: {28: 4, 9: 6}, 2019: {}, 2020: {}, 2021: {20: 2},
                         2022: {5: 3}, 2023: {}, 2024: {27: 4, 2: 11, 28: 12}, 2025: {1: 11}}  # {day: month}
    def update_quarter():
        clear_content()

        QuarterCalendar(content_frame, current_start_month, current_year, current_country)

        # Создаем фрейм для таблицы квартала и размещаем его в контенте
        quarter_calendar_frame = Frame(content_frame)
        quarter_calendar_frame.pack(padx=180, fill='both', expand=True)

        # Создаем объект таблицы для квартала
        TableQuarter(quarter_calendar_frame, current_country, current_year, current_start_month, special_days[current_year])

        # Добавляем кнопки навигации по кварталам
        next_arrow_image = load_resized_image(resource_path('image/next_arrow.png'), (55, 55))
        prev_arrow_image = load_resized_image(resource_path('image/prev_arrow.png'), (65, 65))
        next_button = Button(content_frame, image=next_arrow_image, command=next_quarter, borderwidth=0, bg=main_color,
                             activebackground=main_color)
        next_button.image = next_arrow_image  # Сохраняем ссылку для избежания сборки мусора
        next_button.pack(side=RIGHT, padx=20, pady=40)

        prev_button = Button(content_frame, image=prev_arrow_image, command=prev_quarter, borderwidth=0, bg=main_color,
                             activebackground=main_color)
        prev_button.image = prev_arrow_image  # Сохраняем ссылку для избежания сборки мусора
        prev_button.pack(side=LEFT, padx=20, pady=40)

    def next_quarter():
        global current_start_month
        if current_start_month < 10:
            current_start_month += 3
        else:
            current_start_month = 1
        update_quarter()

    def prev_quarter():
        global current_start_month
        if current_start_month > 1:
            current_start_month -= 3
        else:
            current_start_month = 10
        update_quarter()

    # Инициализация отображения квартала
    update_quarter()


# Функция для отображения годового календаря
def show_year():
    clear_content()

    # Создаем заголовок с названием страны и года
    label_year = Label(content_frame, text=f'Страна: {country_names[current_country].capitalize()}  Год: {current_year}',
                       font=("Verdana", 13, 'bold'), fg='#08224a', bg=main_color)
    label_year.pack(padx=20, anchor='ne')

    year_label = Label(content_frame, text=f"Нормы рабочего времени в {current_year} году",
                       font=("Verdana", 20, 'bold'), fg='#08224a', bg=main_color)
    year_label.pack(pady=20)

    # Создаем фрейм для таблицы годового календаря с фиксированной высотой
    quarter_calendar_frame = Frame(content_frame, width=700, height=300)  # Устанавливаем фиксированную высоту
    quarter_calendar_frame.pack_propagate(False)  # Предотвращаем изменение размера в зависимости от содержимого
    quarter_calendar_frame.pack(padx=100, pady=90, fill='both', expand=False)  # Не расширяем

    # Создаем объект таблицы для годового календаря
    TableQuarter(quarter_calendar_frame, current_country, current_year, 1, {27: 4, 2: 11, 28: 12}, full=True)

    # Обеспечиваем поддержание размера контент-фрейма
    content_frame.pack_propagate(False)  # Предотвращаем изменение размера контент-фрейма
    content_frame.configure(width=screen_width)


# Функция настроек приложения
def settings():
    clear_content()

    countries = list(country_names.values())

    # Заголовок
    header = Label(content_frame, text="Настройки", font=("Verdana", 20, 'bold'), fg='#08224a', bg=main_color)
    header.pack(pady=20, padx=500)

    # Выбор страны
    country_label = Label(content_frame, text="Выбрать страну", bg=main_color, font=("Verdana", 14), fg='#08224a')
    country_label.pack(padx=340, pady=(10, 0), anchor='w')  # Выравниваем по западу

    # Создаем выпадающий список для выбора страны
    country_var = StringVar(value=country_names[current_country])  # Set default to Russian name
    country_dropdown = ttk.Combobox(content_frame, textvariable=country_var, values=countries,
                                    state='normal', font=("Arial", 12), width=20)
    country_dropdown.pack(padx=20, pady=10)

    # Выбор года
    year_label = Label(content_frame, text="Выбрать год", font=("Verdana", 14), bg=main_color, fg='#08224a')
    year_label.pack(padx=365, pady=(10, 0), anchor='w')  # Выравниваем по западу

    # Создаем выпадающий список для выбора года
    selected_year_var = StringVar(value=str(current_year))
    year_dropdown = ttk.Combobox(content_frame, textvariable=selected_year_var,
                                 values=[str(year) for year in range(2018, datetime.now().year + 2)],
                                 state="readonly", font=("Arial", 12), width=20)
    year_dropdown.pack(padx=20, pady=10)

    # Функция применения настроек при нажатии кнопки
    def apply_settings():
        global current_country
        selected_country = country_var.get()

        for eng, rus in country_names.items():
            if rus == selected_country:
                current_country = eng
                break

        # Обработка ошибок
        if current_country not in country_names:
            messagebox.showerror("Ошибка", f"Страна '{selected_country}' не найдена в списке праздников.")
            return

        update_year(int(selected_year_var.get()))  # Применяем выбранный год
        clear_content()
        default_home()

    # Кнопка применения настроек
    select_button = Button(content_frame, text="Применить", command=apply_settings, width=18, height=2,
                           background='#e83a3a', activebackground='#e36666', activeforeground='white', fg='white',
                           font=('Arial', 14))
    select_button.pack(pady=30)

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

# Основная настройка приложения
w = Tk()
screen_width = 1280
screen_height = 720
img = PhotoImage(file=resource_path("image/calendar_icon_main.png"))
w.iconphoto(False, img)
w.config(bg=main_color)
w.resizable(False, False)
w.geometry(f"{screen_width}x{screen_height}+0+0")  # Устанавливаем геометрию окна
w.title('Производственный календарь')

# Создаем контент-фрейм, который будет содержать всю видимую информацию
content_frame = Frame(w, width=screen_width, height=screen_height, bg=main_color)
content_frame.place(x=5, y=0)

# Функция для переключения окна (создает боковую панель с кнопками)
def toggle_win():
    global f1
    f1 = Frame(w, width=screen_width * 0.2, height=800, bg='#2b7ecc')
    f1.place(x=0, y=0)

    # Функция создания кнопки
    def bttn(x, y, text, bcolor, fcolor, cmd):
        # Определяет эффект при наведении на кнопку
        def on_entera(e):
            myButton1['background'] = bcolor
            myButton1['foreground'] = '#fcfeff'

        def on_leavea(e):
            myButton1['background'] = fcolor
            myButton1['foreground'] = '#fcfeff'

        # Создает кнопку с указанными параметрами
        myButton1 = Button(f1, text=text, width=25, height=2, fg='white', border=0, bg=fcolor,
                           activeforeground='white', activebackground=bcolor, command=cmd, font=("Geist Mono", 12, 'bold'), anchor='center')

        # Добавляет обработчики событий для эффекта при наведении
        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        # Размещает кнопку на панели
        myButton1.place(x=x, y=y)

    # Создает кнопки для разных функций
    bttn(0, 90, 'Годовой календарь', '#478ed1', '#2b7ecc', default_home)
    bttn(0, 147, 'Календарь по кварталам', '#478ed1', '#2b7ecc', show_quartiles)
    bttn(0, 204, 'Годовой отчет', '#478ed1', '#2b7ecc', show_year)
    bttn(0, 261, 'Настройки', '#478ed1', '#2b7ecc', settings)

    # Функция удаления боковой панели
    def dele():
        f1.destroy()
        b2 = Button(w, image=img1, command=toggle_win, border=0, bg=main_color, activebackground=main_color).place(x=5, y=8)

    # Создает кнопку закрытия
    global img2
    img2 = ImageTk.PhotoImage(file=resource_path("image/close_icon.png"))
    Button(f1, image=img2, border=0, command=dele, bg='#2b7ecc', activebackground='#2b7ecc').place(x=5, y=10)

# Создает кнопку открытия боковой панели
img1 = ImageTk.PhotoImage(file=resource_path("image/open_icon.png"))

global b2
b2 = Button(w, image=img1, command=toggle_win, border=0, activebackground=main_color,  bg=main_color).place(x=5, y=8)

# Отображаем календарь по умолчанию
default_home()
# Запускаем основной цикл событий приложения
w.mainloop()
