import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from calendar_full import CalendarApp
from calendar_quarter import QuarterCalendar
from table_quarter import TableQuarter
from datetime import datetime
from holiday_fetcher import country_names

# Initialize global variables
current_year = datetime.now().year
current_start_month = 1  # Start with January
current_country = 'Russia'  # Initialize the country variable

def update_year(year):
    global current_year
    current_year = year  # Update the global variable

def default_home():
    clear_content()
    CalendarApp(content_frame, current_year, update_year, current_country)

def show_quartiles():
    clear_content()
    content_frame.config(height=screen_height)

    def update_quarter():
        clear_content()
        QuarterCalendar(content_frame, current_start_month, current_year, current_country)
        quarter_calendar_frame = Frame(content_frame)
        quarter_calendar_frame.pack(padx=180, pady=10, fill='both', expand=True)
        TableQuarter(quarter_calendar_frame, current_country, current_year, current_start_month, {27: 4, 2: 11, 28: 12})

        next_arrow_image = ImageTk.PhotoImage(Image.open("image/next_arrow.png").resize((50, 50)))
        prev_arrow_image = ImageTk.PhotoImage(Image.open("image/prev_arrow.png").resize((60, 60)))

        next_button = Button(content_frame, image=next_arrow_image, command=next_quarter, borderwidth=0)
        next_button.image = next_arrow_image  # Keep a reference to avoid garbage collection
        next_button.pack(side=RIGHT, padx=20, pady=0)

        prev_button = Button(content_frame, image=prev_arrow_image, command=prev_quarter, borderwidth=0)
        prev_button.image = prev_arrow_image  # Keep a reference to avoid garbage collection
        prev_button.pack(side=LEFT, padx=20, pady=0)

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

    # Initial display of the quarter
    update_quarter()

def show_year():
    clear_content()
    year_label = Label(content_frame, text=f"Нормы рабочего времени в {current_year} году",
                       font=("Verdana", 20, 'bold'), fg='#08224a')
    year_label.pack(pady=10)

    quarter_calendar_frame = Frame(content_frame, width=1000, height=400)
    quarter_calendar_frame.pack_propagate(False)
    quarter_calendar_frame.pack(padx=100, pady=50, fill='both', expand=True)

    TableQuarter(quarter_calendar_frame, current_country, current_year, 1, {27: 4, 2: 11, 28: 12}, full=True)

def settings():
    clear_content()
    year_label = Label(content_frame, text="Выбрать страну", font=("Verdana", 14), fg='#08224a')
    year_label.pack(padx=200, pady=10)

    country_var = StringVar(value=current_country)  # Set default to current country
    country_dropdown = ttk.Combobox(content_frame, textvariable=country_var,
                                    values=country_names, state='normal')
    country_dropdown.pack(pady=10)

    def set_country():
        global current_country
        current_country = country_var.get()  # Update the global country variable
        clear_content()
        default_home()  # Return to the default home view

    select_button = Button(content_frame, text="Выбрать", command=set_country)
    select_button.pack(pady=10)

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

# Main application setup
w = Tk()
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
img = PhotoImage(file='image/calendar_icon.png')
w.iconphoto(False, img)
w.geometry(f"{screen_width}x{screen_height}+0+0")
w.title('Производственный календарь')

content_frame = Frame(w, width=screen_width, height=screen_height)
content_frame.place(x=5, y=0)

# Toggle menu setup
def toggle_win():
    global f1
    f1 = Frame(w, width=screen_width * 0.2, height=800, bg='#2b7ecc')
    f1.place(x=0, y=0)

    def bttn(x, y, text, bcolor, fcolor, cmd):
        def on_entera(e):
            myButton1['background'] = bcolor
            myButton1['foreground'] = '#fcfeff'

        def on_leavea(e):
            myButton1['background'] = fcolor
            myButton1['foreground'] = '#fcfeff'

        myButton1 = Button(f1, text=text,
                           width=25,
                           height=2,
                           fg='white',
                           border=0,
                           bg=fcolor,
                           activeforeground='white',
                           activebackground=bcolor,
                           command=cmd,
                           font=("Geist Mono", 12, 'bold'),
                           anchor='center')

        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x, y=y)

    bttn(0, 90, 'Годовой календарь', '#478ed1', '#2b7ecc', default_home)
    bttn(0, 147, 'Календарь по кварталам', '#478ed1', '#2b7ecc', show_quartiles)
    bttn(0, 204, 'Годовой отчет', '#478ed1', '#2b7ecc', show_year)
    bttn(0, 261, 'Настройки', '#478ed1', '#2b7ecc', settings)

    def dele():
        f1.destroy()
        b2 = Button(w, image=img1,
                    command=toggle_win,
                    border=0,
                    )
        b2.place(x=5, y=8)

    global img2
    img2 = ImageTk.PhotoImage(Image.open("image/close_icon.png"))

    Button(f1,
           image=img2,
           border=0,
           command=dele,
           bg='#2b7ecc',
           activebackground='#2b7ecc'
           ).place(x=5, y=10)

img1 = ImageTk.PhotoImage(Image.open("image/open_icon.png"))

global b2
b2 = Button(w, image=img1,
            command=toggle_win,
            border=0
            )
b2.place(x=5, y=8)

default_home()  # Show the calendar by default
w.mainloop()