from tkinter import Frame, Label, StringVar, ttk
from calendar import monthrange
from holiday_fetcher import get_holidays, get_preholidays  # Import the holiday fetching function

class CalendarApp:
    def __init__(self, parent, selected_year, update_year_callback):
        self.parent = parent
        self.selected_year = selected_year
        self.update_year_callback = update_year_callback

        # Fetch holidays once and store them as an instance variable
        self.holidays = get_holidays(self.selected_year)
        self.preholidays = get_preholidays(self.selected_year)

        # Create label for selected year
        self.year_label = Label(parent, text=f"Производственный календарь {self.selected_year}",
                                font=("Verdana", 20, 'bold'), fg='#08224a')
        self.year_label.pack(pady=10)

        self.selected_year_var = StringVar(value="Выберите год")

        # Create a Combobox
        self.year_dropdown = ttk.Combobox(
            parent,
            textvariable=self.selected_year_var,
            values=[str(year) for year in range(2020, 2026)],
            state="readonly",  # Makes it a dropdown (not editable)
            font=("Arial", 11)
        )

        # Place the Combobox in the window
        self.year_dropdown.place(x=1000, y=20)
        self.year_dropdown.bind("<<ComboboxSelected>>", self.change_year)

        # Frame to hold the calendar
        self.calendar_frame = Frame(parent)
        self.calendar_frame.pack(padx=20)

        # Show the initial calendar
        self.show_calendar(self.selected_year)

    def change_year(self, event):
        """Change the selected year and refresh the holidays."""
        selected_year = self.year_dropdown.get()  # Get the selected year from the Combobox
        self.selected_year = int(selected_year)  # Convert to integer
        self.holidays = get_holidays(self.selected_year)  # Fetch holidays for the new year
        self.preholidays = get_preholidays(self.selected_year)
        self.year_label.config(text=f"Производственный календарь {self.selected_year}")  # Update the label
        self.show_calendar(self.selected_year)  # Refresh the calendar display

        # Call the callback function to update the year in the main file
        self.update_year_callback(self.selected_year)

    def show_calendar(self, year):
        month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                       "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

        # Define specific dates to not highlight
        special_dates = {27: 4, 2: 11, 28: 12}  # {day: month}

        # Clear the previous calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        for month in range(1, 13):
            start_day = monthrange(year, month)[0]
            days_in_month = monthrange(year, month)[1]
            days = {holiday.day for holiday in self.holidays if holiday.month == month}
            preholiday_days = {preholiday.day for preholiday in self.preholidays if preholiday.month == month}

            month_frame = Frame(self.calendar_frame, relief="solid", width=285, height=185, bg='white')
            month_frame.grid(row=(month - 1) // 4, column=(month - 1) % 4, padx=10, pady=4)
            month_frame.grid_propagate(False)

            month_label = Label(month_frame, text=f"{month_names[month - 1].upper()}", font=("Helvetica", 12, "bold"),
                                anchor='w', fg='#061b3b', bg='white')
            month_label.grid(row=0, columnspan=7, sticky='w')
            month_label_decor = Label(month_frame, text=f"___________", font=("Helvetica", 12, "bold"),
                                      anchor='e', fg='#061b3b', bg='white')
            month_label_decor.grid(row=0, columnspan=7, sticky='e')

            days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
            for col, day in enumerate(days_of_week):
                label = Label(month_frame, text=day, font=("Arial", 10, "bold"), fg='#6e6d6d', bg='white')
                label.grid(row=1, column=col, padx=1, pady=2)

            for _ in range(start_day):
                label = Label(month_frame, text="", width=4, bg='white')
                label.grid(row=2, column=_, padx=0, pady=0)

            day_row = 2
            for day in range(1, days_in_month + 1):
                day_of_week = (day + start_day - 1) % 7
                day_label = Label(month_frame, text=str(day), width=4, font=("Helvetica", 10, "bold"), bg='white')
                day_label.grid(row=day_row, column=day_of_week, padx=0, pady=0)

                # Check if the day is Saturday or Sunday
                if day_of_week in (5, 6):  # Saturday or Sunday
                    day_label.config(bg='#e83a3a', fg='white')

                # Check if the day is a holiday
                if day in days:  # Highlight holidays
                    day_label.config(bg='#5da2e3', fg='white')
                if day in preholiday_days:
                    day_label.config(text=f'{day}*')

                # Check if the day is one of the special dates
                if year == 2024 and day in special_dates and special_dates[day] == month:
                    day_label.config(bg='white', fg='black')  # Reset color for special dates to default
                else:
                    if day_of_week in (5, 6):  # Saturday or Sunday
                        day_label.config(bg='#e83a3a', fg='white')
                    elif day in days:  # Highlight holidays
                        day_label.config(bg='#5da2e3', fg='white')

                if day_of_week == 6:  # Move to the next row after Sunday
                    day_row += 1

