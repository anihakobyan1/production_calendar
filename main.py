import tkinter
from tkinter import *
from PIL import ImageTk, Image
from calendar_full import CalendarApp
from calendar_quarter import QuarterCalendar
from table_quarter import TableQuarter
from PIL import Image, ImageTk  # Import Pillow modules
from datetime import datetime

current_year = datetime.now().year
current_start_month = 1  # Start with January
def update_year(year):
    global current_year
    current_year = year  # Update the global variable
def default_home():
    clear_content()
    CalendarApp(content_frame, current_year, update_year)
    # start_scheduler()

''' Доделать для кварталов,
    Добавь расчеты рабочих дней и т.д
    Доюавить возможность переключения стран и года
    Дизайн'''
def show_quartiles():
    clear_content()

    # Set the height of content_frame to full screen height
    content_frame.config(height=screen_height)

    # Initialize the starting month for the quarte


    # Function to update the quarter display
    def update_quarter():
        clear_content()
        QuarterCalendar(content_frame, start_month=current_start_month, year=current_year)
        quarter_calendar_frame = Frame(content_frame)
        quarter_calendar_frame.pack(padx=180, pady=10, fill='both', expand=True)
        TableQuarter(quarter_calendar_frame, current_year, current_start_month, {27: 4, 2: 11, 28: 12})

        next_arrow_image = ImageTk.PhotoImage(Image.open("image/next_arrow.png").resize((50, 50)))
        prev_arrow_image = ImageTk.PhotoImage(Image.open("image/prev_arrrow.png").resize((60, 60)))
        # Create buttons with images
        next_button = Button(content_frame, image=next_arrow_image, command=next_quarter, borderwidth=0)
        next_button.image = next_arrow_image  # Keep a reference to avoid garbage collection
        next_button.pack(side=RIGHT, padx=20, pady=0)  # Place on the right side

        prev_button = Button(content_frame, image=prev_arrow_image, command=prev_quarter, borderwidth=0)
        prev_button.image = prev_arrow_image  # Keep a reference to avoid garbage collection
        prev_button.pack(side=LEFT, padx=20, pady=0)  # Place on the left side

    # Function to go to the next quarter
    def next_quarter():
        global current_start_month  # Use the outer variable
        if current_start_month < 10:  # Ensure we don't go beyond December
            current_start_month += 3
        else:
            current_start_month = 1  # Loop back to January
        update_quarter()

    # Function to go to the previous quarter
    def prev_quarter():
        global current_start_month  # Use the outer variable
        if current_start_month > 1:  # Ensure we don't go below January
            current_start_month -= 3
        else:
            current_start_month = 10  # Loop back to October
        update_quarter()

    # Initial display of the quarter
    update_quarter()


def show_year():
    # Clear the current content
    clear_content()

    year_label = Label(content_frame, text=f"Нормы рабочего времени в {current_year} году",
                            font=("Verdana", 20, 'bold'), fg='#08224a')
    year_label.pack(pady=10)

    # Create a frame for the quarter calendar with specified size
    quarter_calendar_frame = Frame(content_frame, width=1000, height=400)  # Adjust as necessary
    quarter_calendar_frame.pack_propagate(False)  # Prevent frame from resizing to fit contents
    quarter_calendar_frame.pack(padx=100, pady=50, fill='both', expand=True)

    # Create the TableQuarter instance
    TableQuarter(quarter_calendar_frame, current_year, 1, {27: 4, 2: 11, 28: 12}, full=True)
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

# Main application setup
w = Tk()
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
w.geometry(f"{screen_width}x{screen_height}+0+0")
w.title('Toggle Menu')

content_frame = Frame(w, width=1200, height=screen_height)
content_frame.place(x=5, y=0)  # Ensure it starts at the top of the window


# Toggle menu setup
def toggle_win():
    global f1
    f1 = Frame(w, width=250, height=800, bg='#2b7ecc')
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

    def dele():
        f1.destroy()
        b2 = Button(w, image=img1,
                    command=toggle_win,
                    border=0,
                    # bg='#2b7ecc',
                    #activebackground='#2b7ecc'
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