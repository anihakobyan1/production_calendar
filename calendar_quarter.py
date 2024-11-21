from tkinter import Frame, Label, RIGHT, TOP
from calendar import monthrange
from holiday_fetcher import get_holidays, get_preholidays  # Import the holiday fetching function


month_frame_cl = 'white'
month_label_cl = '#061b3b'
week_label_cl = '#6e6d6d'
weekend_cl = '#e83a3a'
holiday_cl = '#5da2e3'
day_label_cl = 'black'
header_cl = '#08224a'


class QuarterCalendar:
    def __init__(self, parent, start_month, year, country=None):
        self.parent = parent
        self.selected_year = year
        self.start_month = start_month
        self.country = country.lower() # Store the country parameter

        self.holidays = get_holidays(self.selected_year, self.country)  # Fetch holidays based on the country

        if self.country:
            self.preholidays = get_preholidays(self.selected_year)
        else:
            self.preholidays = []  # Or set to None, depending on your logic

        quarter_names = {1: 'I', 4: 'II', 7: 'III', 10: 'IV'}
        quarter_name = quarter_names.get(self.start_month, '')

        # Create labels
        label_year = Label(parent, text=f'Страна: {self.country.capitalize()}  Год: {year}',
                           font=("Verdana", 13, 'bold'), fg=header_cl)
        label_year.pack(padx=20,  anchor='ne')

        self.year_label = Label(parent, text=f"Календарь {quarter_name} квартала", font=("Verdana", 20, 'bold'),
                                fg=header_cl)
        self.year_label.pack(pady=10)

        # Frame to hold the calendar
        self.calendar_frame = Frame(parent)
        self.calendar_frame.pack(padx=180, pady=20)

        # Show the initial calendar
        self.show_calendar(self.selected_year)

    def show_calendar(self, year):
        month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                       "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        special_dates = {27: 4, 2: 11, 28: 12}  # {day: month}

        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        for month_in in range(3):
            month = (self.start_month + month_in - 1) % 12 + 1
            start_day = monthrange(year, month)[0]
            days_in_month = monthrange(year, month)[1]
            days = {holiday.day for holiday in self.holidays if holiday.month == month}
            preholiday_days = {preholiday.day for preholiday in self.preholidays if preholiday.month == month}

            month_frame = Frame(self.calendar_frame, relief="solid", width=285, height=185, bg=month_frame_cl)
            month_frame.grid(row=0, column=month_in, padx=10, pady=4)
            month_frame.grid_propagate(False)

            month_label = Label(month_frame, text=f"{month_names[month - 1].upper()}", font=("Helvetica", 12, "bold"),
                                anchor='w', fg=month_label_cl, bg=month_frame_cl)
            month_label.grid(row=0, columnspan=7, sticky='w')
            month_label_decor = Label(month_frame, text=f"___________", font=(" Helvetica", 12, "bold"),
                                      anchor='e', fg=month_label_cl, bg=month_frame_cl)
            month_label_decor.grid(row=0, columnspan=7, sticky='e')

            days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
            for col, day in enumerate(days_of_week):
                label = Label(month_frame, text=day, font=("Arial", 10, "bold"), fg=week_label_cl, bg=month_frame_cl)
                label.grid(row=1, column=col, padx=1, pady=2)

            for _ in range(start_day):
                label = Label(month_frame, text="", width=4, bg=month_frame_cl)
                label.grid(row=2, column=_, padx=0, pady=0)

            day_row = 2
            for day in range(1, days_in_month + 1):
                day_of_week = (day + start_day - 1) % 7
                day_label = Label(month_frame, text=str(day), width=4, font=("Helvetica", 10, "bold")
                                  , bg=month_frame_cl, fg=day_label_cl)
                day_label.grid(row=day_row, column=day_of_week, padx=0, pady=0)

                # Check if the day is Saturday or Sunday
                if day_of_week in (5, 6):  # Saturday or Sunday
                    day_label.config(bg=weekend_cl, fg=month_frame_cl)

                # Check if the day is a holiday
                if day in days:  # Highlight holidays
                    day_label.config(bg=holiday_cl, fg=month_frame_cl)
                    # Check if the day is a pre-holiday only if the country is Russia
                if self.country == 'russia' and day in preholiday_days:
                    day_label.config(text=f'{day}*')

                # Check if the day is one of the special dates
                if year == 2024 and day in special_dates and special_dates[day] == month:
                    day_label.config(bg=month_frame_cl, fg=day_label_cl)
                else:
                    if day_of_week in (5, 6):  # Saturday or Sunday
                        day_label.config(bg=weekend_cl, fg=month_frame_cl)
                    elif day in days:  # Highlight holidays
                        day_label.config(bg=holiday_cl, fg=month_frame_cl)
                if self.country == 'russia' and day in preholiday_days:
                    day_label.config(text=f'{day}*', bg=month_frame_cl, fg=day_label_cl)

                if day_of_week == 6:  # Move to the next row after Sunday
                    day_row += 1