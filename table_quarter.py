import tkinter as tk
from calendar import monthrange
from holiday_fetcher import get_holidays, get_preholidays  # Ensure this is available in your environment

class TableQuarter:
    def __init__(self, master, country=None, year=2024, start_month=1, special_days=None, full=False):
        self.master = master
        self.year = year
        self.country = country.lower()
        self.start_month = start_month
        self.special_days = special_days if special_days else {}
        self.full_year = full

        # Fetch holidays once and store them as an instance variable
        self.holidays = get_holidays(year, country)

        # Only fetch pre-holidays if country is provided
        if self.country:
            self.preholidays = get_preholidays(year)
        else:
            self.preholidays = []  # Or set to None, depending on your logic

        # Create a frame for the table
        self.table_frame = tk.Frame(self.master)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Prepare the data and create the table
        self.data = self.prepare_data()
        self.create_table()

    def calculate_month(self, month):
        start_day, days_in_month = monthrange(self.year, month)
        non_work_days = 0

        holidays_this_month = {holiday.day for holiday in self.holidays if holiday.month == month}
        preholidays_this_month = {preholiday.day for preholiday in self.preholidays if preholiday.month == month}

        for day in range(1, days_in_month + 1):
            day_of_week = (start_day + day - 1) % 7
            if day_of_week in (5, 6):  # Saturday or Sunday
                if day not in holidays_this_month:
                    non_work_days += 1

        calc_work_days = days_in_month - (len(holidays_this_month) + non_work_days)

        # Only add pre-holidays if the country is Russia
        if self.country == 'russia':
            for day, m in self.special_days.items():
                if m == month:
                    calc_work_days += 1

        calc_holi_days = days_in_month - calc_work_days
        return days_in_month, calc_work_days, calc_holi_days, preholidays_this_month

    def prepare_data(self):
        columns = ['Количество дней']
        calc_days, work_days, holi_days = [], [], []
        hours_40 = []
        hours_36 = []
        hours_24 = []

        # Define columns based on whether it's a full year or not
        if not self.full_year:
            month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                           "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
            for month_in in range(3):
                month = (self.start_month + month_in - 1) % 12 + 1
                columns.append(month_names[month - 1])
            columns.append("Квартал")

            # Calculate days for the specified three months
            for month_in in range(3):
                month = (self.start_month + month_in - 1) % 12 + 1
                days, work, holidays, preholidays = self.calculate_month(month)
                calc_days.append(days)
                work_days.append(work)
                holi_days.append(holidays)

                # Calculate hours
                hours_40.append((work * 8) - (len(preholidays) if self.country == 'russia' else 0))
                hours_36.append((work * 7.2) - (len(preholidays) if self.country == 'russia' else 0))
                hours_24.append((work * 4.8) - (len(preholidays) if self.country == 'russia' else 0))

        else:
            columns.extend(['I квартал', 'II квартал', 'III квартал', 'IV квартал', 'Итог'])
            for i in range(4):
                days, work, holidays, preholidays = 0, 0, 0, []
                for month in range(3):
                    current_month = (i * 3) + month + 1
                    month_days, month_work, month_holidays, month_preholidays = self.calculate_month(current_month)
                    days += month_days
                    work += month_work
                    holidays += month_holidays
                    preholidays.extend(month_preholidays)

                calc_days.append(days)
                work_days.append(work)
                holi_days.append(holidays)

                # Calculate hours for the quarter
                hours_40.append((work * 8) - (len(preholidays) if self.country == 'russia' else 0))
                hours_36.append((work * 7.2) - (len(preholidays) if self.country == 'russia' else 0))
                hours_24.append((work * 4.8) - (len(preholidays) if self.country == 'russia' else 0))

        data = []
        data.append(columns)  # Add headers

        # Append calculated data to the data list
        data.append(["Календарные"] + calc_days + [sum(calc_days)])
        data.append(["Рабочие"] + work_days + [sum(work_days)])
        data.append(["Выходные, праздники"] + holi_days + [sum(holi_days)])
        data.append(["Рабочее время (в часах)"])
        data.append(["при 40-часовой рабочей неделе"] + [round(d, 1) for d in hours_40] + [sum(hours_40)])
        data.append(["при 36-часовой рабочей неделе"] + [round(d, 1) for d in hours_36] + [round(sum(hours_36), 1)])
        data.append(["при 24-часовой рабочей неделе"] + [round(d, 1) for d in hours_24] + [round(sum(hours_24), 1)])

        return data

    def create_table(self):
        for i, row in enumerate(self.data):
            for j, item in enumerate(row):
                if j == 0:
                    label = tk.Label(self.table_frame, text=item, borderwidth=1, relief="flat", highlightthickness=1,
                                     padx=10, pady=5,
                                     anchor=tk.W, font=('Arial', 11), bg='white', fg='#061b3b')
                elif i == 0 and j in range(1, len(row)):
                    label = tk.Label(self.table_frame, text=item, borderwidth=1, relief="flat", highlightthickness=1,
                                     pady=5,
                                     font=('Arial', 11), fg='#061b3b', bg='white')
                else:
                    label = tk.Label(self.table_frame, text=item, borderwidth=1, relief="flat", highlightthickness=1,
                                     padx=10, pady=5, font=('Arial', 11), bg='#c9def2')
                if j == 0 and i in (0, 4):
                    label = tk.Label(self.table_frame, text=item, borderwidth=1, relief="flat", highlightthickness=1,
                                     padx=10, pady=5,
                                     anchor=tk.W, font=('Arial', 11), fg='#061b3b')
                label.grid(row=i, column=j, sticky="nsew")

        # Configure grid weights to make it responsive
        for i in range(len(self.data[0])):
            self.table_frame.grid_columnconfigure(i, weight=1)