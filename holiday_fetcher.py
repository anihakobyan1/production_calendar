import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale
import requests_cache
from datetime import timedelta

# Configure the cache
requests_cache.install_cache('holiday_cache', expire_after=timedelta(days=30))  # Cache expires after 30 days

month_mapping = {
    'января': 'Jan',
    'февраля': 'Feb',
    'марта': 'Mar',
    'апреля': 'Apr',
    'мая': 'May',
    'июня': 'Jun',
    'июля': 'Jul',
    'августа': 'Aug',
    'сентября': 'Sep',
    'октября': 'Oct',
    'ноября': 'Nov',
    'декабря': 'Dec'
}


def get_holidays(year, country):
    url = f'https://www.timeanddate.com/holidays/{country.lower()}/{year}?hol=1'
    headers = {'Accept-Language': 'en-US,en;q=0.9'}

    # Use CachedSession instead of Session
    session = requests_cache.CachedSession('holiday_cache')

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        print(f"Error fetching holidays from timeanddate.com: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': "holidays-table"})
    holidays = set()  # Use a set to store unique dates

    for row in table.find_all('tr', {'class': 'showrow'}):
        cols = row.find_all('th')
        if cols:
            date_str = cols[0].text.strip()
            full_date_str = f"{date_str} {year}"
            try:
                date_obj = datetime.strptime(full_date_str, "%d %b %Y").date()
                holidays.add(date_obj)  # Add date to the set
            except ValueError:
                print(f"Date parsing error for 1: {full_date_str}")

    if country.lower == 'russia':
        consultant_url = f'https://www.consultant.ru/law/ref/calendar/proizvodstvennye/{year}/'

        try:
            response = session.get(consultant_url)
            response.raise_for_status()  # Raise an error for bad responses
        except requests.RequestException as e:
            print(f"Error fetching holidays from consultant.ru: {e}")
            return list(holidays)  # Return whatever holidays were found so far

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <ul> element containing the holiday transfers
        ul_elements = soup.find_all('ul')
        if ul_elements:
            target_ul = ul_elements[5]  # Change the index as needed
            for li in target_ul.find_all('li'):
                text = li.get_text(strip=True)
                # Extract the date from the text
                if 'на' in text:
                    parts = text.split('на')
                    if len(parts) == 2:
                        date_str = parts[1].strip()  # Get the date part
                        parts = date_str.split()
                        date_part = ' '.join(parts[1:])  # Join the parts after the day
                        date_part = date_part[:-1]  # Remove the last character (usually a period)

                        # Replace full month names with English month names
                        for full_month, english_month in month_mapping.items():
                            date_part = date_part.replace(full_month, english_month)
                        full_date_str = f"{date_part} {year}"

                        try:
                            date_obj = datetime.strptime(full_date_str, "%d %b %Y").date()
                            holidays.add(date_obj)  # Add date to the set
                        except ValueError as e:
                            print(f"Date parsing error for 2: {full_date_str} - {e}")
    return sorted(holidays)  # Return a sorted list of unique holidays


def get_preholidays(year):
    consultant_url = f'https://www.consultant.ru/law/ref/calendar/proizvodstvennye/{year}/'
    headers = {'Accept-Language': 'ru-RU,ru;q=0.9'}

    # Use CachedSession instead of Session
    session = requests_cache.CachedSession('preholiday_cache')
    try:
        response = session.get(consultant_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        print(f"Error fetching holidays from consultant.ru: {e}")
        return []  # Return an empty list on error

    preholiday_days = []
    soup = BeautifulSoup(response.text, 'html.parser')

    # Russian month mapping
    month_mapping = {
        'Январь': 1,
        'Февраль': 2,
        'Март': 3,
        'Апрель': 4,
        'Май': 5,
        'Июнь': 6,
        'Июль': 7,
        'Август': 8,
        'Сентябрь': 9,
        'Октябрь': 10,
        'Ноябрь': 11,
        'Декабрь': 12
    }

    # Find all 'preholiday' days and their corresponding month
    months = soup.find_all('th', class_='month')
    for month in months:
        # Get the month name
        month_name = month.get_text(strip=True)

        # Find the corresponding table for the month
        month_table = month.find_parent('table')

        # Find all days in the month with class 'preholiday'
        preholiday_cells = month_table.find_all('td', class_='preholiday')
        # Extract the day number and add it to the list
        for cell in preholiday_cells:
            day_number = cell.get_text(strip=True)
            # Remove any additional characters (like asterisks) from the day number

            # Get the month number from the mapping
            month_number = month_mapping.get(month_name)
            if month_number is None:
                print(f"Unknown month: {month_name}")
                continue

            preholiday_str = f'{day_number[:-1]} {month_number} {year}'
            preholiday_obj = datetime.strptime(preholiday_str, "%d %m %Y").date()
            preholiday_days.append(preholiday_obj)

    return preholiday_days  # Return the list of preholiday dates


country_names = ['Australia', 'Canada', 'India', 'Ireland', 'New-Zealand',
 'United-Kingdom', 'United-States', 'Argentina', 'Brazil',
 'China', 'France', 'Germany', 'Greece', 'Italy',
 'Japan', 'Mexico', 'Netherlands', 'Russia', 'South-Africa',
 'South-Korea', 'Spain', 'Sweden', 'Switzerland',
 'Turkey', 'United-Arab-Emirates', 'Vietnam', 'Philippines',
 'Singapore', 'Malaysia', 'Thailand', 'Indonesia', 'Pakistan',
 'Egypt', 'Saudi-Arabia', 'Colombia', 'Chile', 'Peru',
 'Bangladesh', 'Honduras', 'Costa-Rica', 'Dominican-Republic',
 'Puerto-Rico', 'Jamaica', 'Iceland', 'Norway', 'Finland',
 'Denmark', 'Belgium', 'Austria', 'Switzerland', 'Czechia',
 'Slovakia', 'Hungary', 'Portugal', 'Romania', 'Bulgaria',
 'Lithuania', 'Latvia', 'Estonia', 'Ukraine', 'Kazakhstan',
 'South-Africa', 'Zimbabwe', 'Namibia', 'Botswana',
 'Lesotho', 'Eswatini', 'Malawi', 'Zambia', 'Vanuatu',
 'Fiji', 'Samoa', 'Tonga', 'Papua-New-Guinea',
 'Kiribati', 'Tuvalu', 'Micronesia', 'Marshall-Islands',
 'Palau', 'Nauru', 'Solomon-Islands', 'Cook-Islands', 'French-Polynesia', 'New-Caledonia', 'Wallis-and-Futuna',
 'Saint-Vincent-and-the-Grenadines', 'Saint-Lucia',
 'Saint-Kitts-and-Nevis', 'Grenada', 'Dominica',
 'Antigua-and-Barbuda', 'Barbados', 'Bahamas',
 'Trinidad-and-Tobago', 'Guyana', 'Suriname',
 'Cuba', 'Haiti', 'Dominican-Republic', 'El-Salvador',
 'Nicaragua', 'Costa-Rica', 'Panama', 'Colombia',
 'Venezuela', 'Ecuador', 'Paraguay', 'Uruguay',
 'Chile', 'Argentina', 'Brazil', 'Peru', 'Bolivia',
 'Paraguay', 'Guyana', 'Suriname', 'French-Guiana'
]