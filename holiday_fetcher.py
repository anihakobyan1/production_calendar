import requests
from bs4 import BeautifulSoup
from datetime import datetime
import requests_cache
from datetime import timedelta

# Настройка кэша для запросов, который будет действовать 30 дней
requests_cache.install_cache('holiday_cache', expire_after=timedelta(days=30))

# Сопоставление месяцев с английскими названиями
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


# Функция для получения праздников по году и стране
def get_holidays(year, country):
    # Формируем URL для запроса
    url = f'https://www.timeanddate.com/holidays/{country.lower()}/{year}?hol=1'
    headers = {'Accept-Language': 'en-US,en;q=0.9'}

    # Используем кэшированные сессии для оптимизации запросов
    session = requests_cache.CachedSession('holiday_cache')

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки HTTP
    except requests.RequestException as e:
        print(f"Ошибка при получении праздников: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': "holidays-table"})
    holidays = set()  # Множество для уникальных дат праздников

    # Извлечение праздников из таблицы
    for row in table.find_all('tr', {'class': 'showrow'}):
        cols = row.find_all('th')
        if cols:
            date_str = cols[0].text.strip()
            full_date_str = f"{date_str} {year}"  # Формируем полную дату
            try:
                date_obj = datetime.strptime(full_date_str, "%d %b %Y").date()
                holidays.add(date_obj)  # Добавляем дату в множество
            except ValueError:
                print(f"Ошибка разбора даты: {full_date_str}")

    # Обработка дополнительных праздников для России
    if country.lower() == 'russia':
        if year == 2020:
            year = '2020b'  # Специальный случай для 2020 года
        consultant_url = f'https://www.consultant.ru/law/ref/calendar/proizvodstvennye/{year}/'

        try:
            response = session.get(consultant_url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка при получении праздников с consultant.ru: {e}")
            return list(holidays)

        soup = BeautifulSoup(response.text, 'html.parser')
        ul_elements = soup.find_all('ul')

        # Извлечение переносов праздников
        if ul_elements:
            target_ul = ul_elements[5]  # Индекс может потребовать корректировки
            for li in target_ul.find_all('li'):
                text = li.get_text(strip=True)
                if 'на' in text:
                    parts = text.split('на')
                    if len(parts) == 2:
                        date_str = parts[1].strip()  # Получаем часть с датой
                        parts = date_str.split()
                        date_part = ' '.join(parts[1:])  # Объединяем части после дня
                        date_part = date_part[:-1]  # Убираем последний символ (обычно точка)

                        # Заменяем месяцы на английские названия
                        for full_month, english_month in month_mapping.items():
                            date_part = date_part.replace(full_month, english_month)
                        full_date_str = f"{date_part} {year}"

                        try:
                            date_obj = datetime.strptime(full_date_str, "%d %b %Y").date()
                            holidays.add(date_obj)
                        except ValueError as e:
                            print(f"Ошибка разбора даты: {full_date_str} - {e}")

    return sorted(holidays)  # Возвращаем отсортированный список уникальных праздников


# Функция для получения предпраздничных дней
def get_preholidays(year):
    consultant_url = f'https://www.consultant.ru/law/ref/calendar/proizvodstvennye/{year}/'
    headers = {'Accept-Language': 'ru-RU,ru;q =0.9'}

    # Используем кэшированные сессии для оптимизации запросов
    session = requests_cache.CachedSession('preholiday_cache')
    try:
        response = session.get(consultant_url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки HTTP
    except requests.RequestException as e:
        print(f"Ошибка при получении предпраздничных дней: {e}")
        return []  # Возвращаем пустой список в случае ошибки

    preholiday_days = []
    soup = BeautifulSoup(response.text, 'html.parser')

    # Сопоставление месяцев с их номерами
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

    # Извлечение предпраздничных дней
    months = soup.find_all('th', class_='month')
    for month in months:
        month_name = month.get_text(strip=True)  # Получаем название месяца
        month_table = month.find_parent('table')  # Находим соответствующую таблицу

        preholiday_cells = month_table.find_all('td', class_='preholiday')  # Находим ячейки с предпраздничными днями
        for cell in preholiday_cells:
            day_number = cell.get_text(strip=True)  # Извлекаем номер дня
            month_number = month_mapping.get(month_name)  # Получаем номер месяца
            if month_number is None:
                print(f"Неизвестный месяц: {month_name}")
                continue

            preholiday_str = f'{day_number[:-1]} {month_number} {year}'  # Формируем строку даты
            preholiday_obj = datetime.strptime(preholiday_str, "%d %m %Y").date()  # Преобразуем в объект даты
            preholiday_days.append(preholiday_obj)  # Добавляем в список

    return preholiday_days  # Возвращаем список предпраздничных дат


# Список стран для получения праздников
country_names = {
    'Australia': 'Австралия',
    'Canada': 'Канада',
    'India': 'Индия',
    'Ireland': 'Ирландия',
    'New-Zealand': 'Новая Зеландия',
    'UK': 'Великобритания',
    'United-States': 'США',
    'Argentina': 'Аргентина',
    'Brazil': 'Бразилия',
    'China': 'Китай',
    'France': 'Франция',
    'Germany': 'Германия',
    'Greece': 'Греция',
    'Italy': 'Италия',
    'Japan': 'Япония',
    'Mexico': 'Мексика',
    'Netherlands': 'Нидерланды',
    'Russia': 'Россия',
    'South-Africa': 'Южная Африка',
    'South-Korea': 'Южная Корея',
    'Spain': 'Испания',
    'Sweden': 'Швеция',
    'Switzerland': 'Швейцария',
    'Turkey': 'Турция',
    'United-Arab-Emirates': 'Объединенные Арабские Эмираты',
    'Vietnam': 'Вьетнам',
    'Philippines': 'Филиппины',
    'Singapore': 'Сингапур',
    'Malaysia': 'Малайзия',
    'Thailand': 'Таиланд',
    'Indonesia': 'Индонезия',
    'Pakistan': 'Пакистан',
    'Egypt': 'Египет',
    'Saudi-Arabia': 'Саудовская Аравия',
    'Colombia': 'Колумбия',
    'Chile': 'Чили',
    'Peru': 'Перу',
    'Bangladesh': 'Бангладеш',
    'Honduras': 'Гондурас',
    'Costa-Rica': 'Коста-Рика',
    'Dominican-Republic': 'Доминиканская Республика',
    'Puerto-Rico': 'Пуэрто-Рико',
    'Jamaica': 'Ямайка',
    'Iceland': 'Исландия',
    'Norway': 'Норвегия',
    'Finland': 'Финляндия',
    'Denmark': 'Дания',
    'Belgium': 'Бельгия',
    'Austria': 'Австрия',
    'Czechia': 'Чешская Республика',
    'Slovakia': 'Словакия',
    'Hungary': 'Венгрия',
    'Portugal': 'Португалия',
    'Romania': 'Румыния',
    'Bulgaria': 'Болгария',
    'Lithuania': 'Литва',
    'Latvia': 'Латвия',
    'Estonia': 'Эстония',
    'Ukraine': 'Украина',
    'Kazakhstan': 'Казахстан',
    'Namibia': 'Намибия',
    'Botswana': 'Ботсвана',
    'Lesotho': 'Лесото',
    'Eswatini': 'Эсватини',
    'Malawi': 'Малави',
    'Zambia': 'Замбия',
    'Vanuatu': 'Вануату',
    'Fiji': 'Фиджи',
    'Samoa': 'Самоа',
    'Tonga': 'Тонга',
    'Papua-New-Guinea': 'Папуа-Новая Гвинея',
    'Kiribati': 'Кирибати',
    'Tuvalu': 'Тувалу',
    'Micronesia': 'Федеративные Штаты Микронезии',
    'Marshall-Islands': 'Маршалловы Острова',
    'Palau': 'Палау',
    'Nauru': 'Науру',
    'Solomon-Islands': 'Соломоновы Острова',
    'Cook-Islands': 'Острова Кука',
    'French-Polynesia': 'Французская Полинезия',
    'New-Caledonia': 'Новая Каледония',
    'Wallis-and-Futuna': 'Уоллис и Футуна',
    'Saint-Vincent-and-the-Grenadines': 'Сент-Винсент и Гренадины',
    'Saint-Lucia': 'Сент-Люсия',
    'Saint-Kitts-and-Nevis': 'Сент-Китс и Невис',
    'Grenada': 'Гренада',
    'Dominica': 'Доминика',
    'Antigua-and-Barbuda': 'Антигуа и Барбуда',
    'Barbados': 'Барбадос',
    'Bahamas': 'Багамские Острова',
    'Trinidad-and-Tobago': 'Тринидад и Тобаго',
    'Guyana': 'Гайана',
    'Suriname': 'Суринам',
    'Cuba': 'Куба',
    'Haiti': 'Гаити',
    'El-Salvador': 'Сальвадор',
    'Nicaragua': 'Никарагуа',
    'Panama': 'Панама',
    'Venezuela': 'Венесуэла',
    'Ecuador': 'Эквадор',
    'Paraguay': 'Парагвай',
    'Uruguay': 'Уругвай',
    'Chile': 'Чили',
    'Argentina': 'Аргентина',
    'Brazil': 'Бразилия',
    'Peru': 'Перу',
    'Bolivia': 'Боливия',
    'Paraguay': 'Парагвай',
    'Guyana': 'Гайана',
    'Suriname': 'Суринам',
    'French-Guiana': 'Французская Гвиана'
}


