import tkinter as tk
from calendar import monthrange
from holiday_fetcher import get_holidays, get_preholidays  # Ensure this is available in your environment


class TableQuarter:
    def __init__(self, master, year, start_month, special_days, full=False):
        self.master = master
        self.year = year
        self.start_month = start_month
        self.special_days = special_days
        self.full_year = full
        self.holidays = get_holidays(year)
        self.preholidays = get_preholidays(year)


        # Create a frame for the table
        self.table_frame = tk.Frame(self.master)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Prepare the data and create the table
        self.data = self.prepare_data()
        self.create_table()


    def calculate_year(self, start_month):
        calc_days = []
        work_days = []
        holi_days = []

        for month_in in range(3):
            month = (self.start_month + month_in - 1) % 12 + 1
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
            for m, day in self.special_days.items():
                if m == month:
                    calc_work_days += 1

            calc_holi_days = days_in_month - calc_work_days
            calc_days.append(days_in_month)
            work_days.append(calc_work_days)
            holi_days.append(calc_holi_days)

        return calc_days, work_days, holi_days

    def prepare_data(self):
        columns = ['Количество дней']
        calc_days, work_days, holi_days = [], [], []

        # Define columns based on whether it's a full year or not
        if not self.full_year:
            month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                               "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
            for month_in in range(3):
                month = (self.start_month + month_in - 1) % 12 + 1
                columns.append(month_names[month - 1])
            columns.append("Квартал")

                # Calculate days for the specified three months
            calc_days, work_days, holi_days = self.calculate_year(self.start_month)

        else:
            columns.extend(['I квартал', 'II квартал', 'III квартал', 'IV квартал', 'Итог'])
            self.start_month = 1  # Start from January for full year calculation
            for i in range(4):
                days, work, holidays = self.calculate_year(self.start_month)
                calc_days.append(sum(days))
                work_days.append(sum(work))
                holi_days.append(sum(holidays))
                self.start_month += 3  # Move to the next quarter

            # Prepare the final data for the table
        data = []
        data.append(columns)  # Add headers

            # Add rows for each type of data
        data.append(["Календарные"] + calc_days + [sum(calc_days)])
        data.append(["Рабочие"] + work_days + [sum(work_days)])
        data.append(["Выходные, праздники"] + holi_days + [sum(holi_days)])
        data.append(["Рабочее время (в часах)"])
        data.append(
                ["при 40-часовой рабочей неделе"] + [d * 8 for d in work_days] + [sum(d * 8 for d in work_days)])
        data.append(["при 36-часовой рабочей неделе"] + [round(d * 7.2, 1) for d in work_days] + [
                round(sum(d * 7.2 for d in work_days), 1)])
        data.append(["при 24-часовой рабочей неделе"] + [round(d * 4.8, 1) for d in work_days] + [
                round(sum(d * 4.8 for d in work_days), 1)])

        return data


    def create_table(self):
        for i, row in enumerate(self.data):
            for j, item in enumerate(row):
                if j == 0:
                    label = tk.Label(self.table_frame, text=item, borderwidth=1, relief="flat", highlightthickness=1,
                                     padx=10, pady=5,
                                     anchor=tk.W, font=('Arial', 10), bg='white', fg='#061b3b')
                elif i == 0 and j in range(1, len(row)):
                    label = tk.Label(self.table_frame, text=item, borderwidth=1, relief="flat", highlightthickness=1,
                                     pady=5,
                                     font=('Arial', 11), fg='#061b3b', bg='white')
                else:
                    label = tk.Label(self.table_frame, text=item, borderwidth=1, relief="flat", highlightthickness=1,
                                     padx=10, pady=5, bg='#c9def2')
                if j == 0 and i in (0, 4):
                    label = tk.Label(self.table_frame, text=item, borderwidth=1, relief="flat", highlightthickness=1,
                                     padx=10, pady=5,
                                     anchor=tk.W, font=('Arial', 11), fg='#061b3b')
                label.grid(row=i, column=j, sticky="nsew")

            # Configure grid weights to make it responsive
        for i in range(len(self.data[0])):
            self.table_frame.grid_columnconfigure(i, weight=1)

