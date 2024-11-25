from datetime import datetime
from tkinter import Frame, Label, StringVar
from calendar import monthrange
from holiday_fetcher import get_holidays, get_preholidays, country_names

# Константы цветов
main_color = '#e6f2fc'
month_frame_cl = 'white'
month_label_cl = '#061b3b'
week_label_cl = '#6e6d6d'
weekend_cl = '#5da2e3'
holiday_cl = '#e83a3a'
today_border_cl = '#28256e'
day_label_cl = 'black'
header_cl = '#08224a'


class BaseCalendar:
    def __init__(self, parent, selected_year, country=None, bg_color=main_color):
        self.parent = parent
        self.selected_year = selected_year
        self.country = country.lower() if country else None
        self.special_days = {2016: {20: 2}, 2017: {}, 2018: {28: 4, 9: 6}, 2019: {}, 2020: {}, 2021: {20: 2},
                             2022: {5: 3}, 2023: {}, 2024: {27: 4, 2: 11, 28: 12}, 2025: {1: 11}}  # {day: month}
        # Получаем праздники и предпраздники
        self.holidays = get_holidays(self.selected_year, self.country)
        self.preholidays = get_preholidays(self.selected_year) if self.country else []

        # Получаем текущую дату
        today = datetime.now()
        self.today_day = today.day
        self.today_month = today.month
        self.today_year = today.year

        # Создаем фрейм для календаря
        self.calendar_frame = Frame(parent, bg=bg_color)
        self.calendar_frame.pack(padx=20)

    def show_calendar(self):
        month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                       "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

        # Очищаем предыдущий календарь
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        for month in range(1, 13):
            self._create_month_frame(month, month_names, self.special_days[self.selected_year], 4)

    def _create_month_frame(self, month, month_names, special_dates, sections=4):
        start_day = monthrange(self.selected_year, month)[0]
        days_in_month = monthrange(self.selected_year, month)[1]
        days = {holiday.day for holiday in self.holidays if holiday.month == month}
        preholiday_days = {preholiday.day for preholiday in self.preholidays if preholiday.month == month}

        # Создаем фрейм для месяца
        month_frame = Frame(self.calendar_frame, relief="solid", width=285, height=185, bg=month_frame_cl)
        month_frame.grid(row=(month - 1) // sections, column=(month - 1) % sections, padx=10, pady=4)
        month_frame.grid_propagate(False)

        # Заголовок месяца
        month_label = Label(month_frame, text=f"{month_names[month - 1].upper()}", font=("Helvetica", 12, "bold"),
                            anchor='w', fg=month_label_cl, bg=month_frame_cl)
        month_label.grid(row=0, columnspan=7, sticky='w')
        month_label_decor = Label(month_frame, text=f"_________", font=("Arial", 12, "bold"),
                                  anchor='e', fg=month_label_cl, bg=month_frame_cl)
        month_label_decor.grid(row=0, columnspan=7, sticky='e')

        # Заголовки дней недели
        days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for col, day in enumerate(days_of_week):
            label = Label(month_frame, text=day, font=("Arial", 10, "bold"), fg=week_label_cl, bg=month_frame_cl)
            label.grid(row=1, column=col, padx=1, pady=2)

        # Пустые ячейки для начала месяца
        for _ in range(start_day):
            label = Label(month_frame, text="", width=4, bg=month_frame_cl)
            label.grid(row=2, column=_, padx=0, pady=0)

        day_row = 2
        for day in range(1, days_in_month + 1):
            day_of_week = (day + start_day - 1) % 7

            # Создаем кнопку для дня
            day_label = Label(month_frame, text=str(day), width=4, font=("Poppins", 10, "bold"),
                              bg=month_frame_cl, fg=day_label_cl)
            day_label.grid(row=day_row, column=day_of_week, padx=0, pady=0)

            # Выделяем текущий день
            if (day == self.today_day and month == self.today_month and
                    self.selected_year == self.today_year):
                day_label.config(borderwidth=1, font=("Poppins", 10, "bold"))

            # Обозначаем выходные дни
            if day_of_week in (5, 6):  # Суббота или воскресенье
                day_label.config(bg=weekend_cl, fg=day_label_cl)

            # Обозначаем праздники
            if day in days:
                day_label.config(bg=holiday_cl, fg=month_frame_cl)

            # Обозначаем пред праздники только для России
            if self.country == 'russia' and day in preholiday_days:
                day_label.config(text=f'{day}*', bg=month_frame_cl, fg=day_label_cl)

            # Обозначаем особые даты
            if (self.selected_year == 2024 and day in special_dates and special_dates[day] == month and
                    self.country.lower() == 'russia'):
                day_label.config(bg=month_frame_cl, fg=day_label_cl)

            # Переход на новую строку после субботы
            if day_of_week == 6:
                day_row += 1


class CalendarApp(BaseCalendar):
    def __init__(self, parent, selected_year, update_year_callback,
                 country=None, bg_color=main_color):
        super().__init__(parent, selected_year, country)
        self.update_year_callback = update_year_callback

        # Получаем праздники один раз и храним как атрибут экземпляра
        self.holidays = get_holidays(self.selected_year, self.country)
        self.today = datetime.now().day
        # Получаем предпраздники только если указана страна
        if self.country:
            self.preholidays = get_preholidays(self.selected_year)
        else:
            self.preholidays = []  # Или установите None, в зависимости от вашей логики

        # Создаем метку с названием выбранного года
        self.year_label = Label(parent, text=f"Производственный календарь {self.selected_year}",
                                font=("Verdana", 20, 'bold'), fg=header_cl, bg=main_color)
        self.year_label.pack(pady=20)

        # Создаем переменную для выбора года
        self.selected_year_var = StringVar(value="Выберите год")

        # Фрейм для календаря
        self.calendar_frame = Frame(parent, bg=bg_color)
        self.calendar_frame.pack(padx=20)

        # Отображаем начальный календарь
        self.show_calendar()

    def update_calendar(self, year):
        self.selected_year = year
        self.holidays = get_holidays(year, self.country)
        self.preholidays = get_preholidays(year) if self.country else []
        self.show_calendar()


class QuarterCalendar(BaseCalendar):
    def __init__(self, parent, start_month, year, country=None, bg_color=main_color):
        super().__init__(parent, year, country)
        self.country_names = country_names
        self.year = year
        self.start_month = start_month
        quarter_names = {1: 'I', 4: 'II', 7: 'III', 10: 'IV'}
        quarter_name = quarter_names.get(self.start_month, '')

        # Получаем праздники на основе страны
        self.holidays = get_holidays(self.selected_year, self.country)

        # Получаем предпраздники только если указана страна
        if self.country:
            self.preholidays = get_preholidays(self.selected_year)
        else:
            self.preholidays = []  # Или установите None, в зависимости от вашей логики

        # Create labels
        label_year = Label(parent, text=f'Страна: {self.country_names[country]}  Год: {year}',
                           font=("Verdana", 13, 'bold'), fg=header_cl, bg=main_color)
        label_year.pack(padx=20, anchor='ne')

        self.year_label = Label(parent, text=f"Календарь {quarter_name} квартала", font=("Verdana", 20, 'bold'),
                                fg=header_cl, bg=main_color)
        self.year_label.pack(pady=10)

        self.calendar_frame = Frame(parent, bg=bg_color)
        self.calendar_frame.pack(padx=180, pady=20)

        self.show_quarter_calendar()

    def show_quarter_calendar(self):
        month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                       "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

        # Создаем заголовок календаря четвертого квартала
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Отображаем три месяца четвертого квартала
        for month_in in range(3):
            month = (self.start_month + month_in - 1) % 12 + 1
            self._create_month_frame(month, month_names, self.special_days[self.year], 3)
