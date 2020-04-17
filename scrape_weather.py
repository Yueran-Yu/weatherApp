from html.parser import HTMLParser
import urllib.request
from datetime import datetime
from pprint import pprint


class WeatherScraper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.is_tbody = False
        self.is_td = False
        self.is_tr = False
        self.is_span = False
        self.is_a = False
        self.weather = False
        self.has_title = False
        self.count = 0
        self._container = dict()

    def handle_starttag(self, tag, attrs):
        if tag == 'tbody':
            self.is_tbody = True
        if tag == 'tr' and self.is_tbody:
            self.is_tr = True
        if tag == 'td':
            self.is_td = True

        if self.is_tbody and tag == 'span' and attrs.__contains__(('class', 'wb-inv')):
            self.is_span = True

        if self.is_tbody and tag == 'a' and attrs.__contains__(('href', '#legendE')):
            self.is_a = True
            # print(self.count, ' subtag <<a>> !!!!!!')

        for attr in attrs:
            if self.is_tbody and attr[0] == 'title' and attr[1].__contains__(','):
                self.weather = datetime.strptime(str(attr[1]), '%B %d, %Y').date()
                self._container[str(self.weather)] = dict()
                self.count = 0
                # print('=============', self.weather)

    def handle_endtag(self, tag):
        if tag == 'tbody':
            self.is_tbody = False
        if tag == 'tr':
            self.is_tr = False
        if tag == 'td':
            self.is_td = False
        if tag == 'span':
            self.is_span = False
        if tag == 'a':
            self.is_a = False

    def handle_data(self, data):
        if self.is_tbody and self.is_tr and self.is_td and bool(data.strip()):
            self.count += 1
            if self.is_span:
                self.count -= 1
            elif self.is_a:
                self.count -= 1
            else:
                # print(self.count, len(self._container), data)
                for x in range(1, 4):
                    if self.count == 1:
                        self._container[str(self.weather)]['Max'] = data

                    if self.count == 2:
                        self._container[str(self.weather)]['Min'] = data

                    if self.count == 3:
                        self._container[str(self.weather)]['Mean'] = data

    def weather_dic(self):
        return self._container


def url_collection():
    year_of_today = datetime.today().year
    month_of_today = datetime.today().month
    years = range(1996, year_of_today + 1, 1)
    urls = list()
    for current_y in years:
        start_month = 10 if current_y == 1996 else 1
        total_months = range(start_month, 13) if current_y != year_of_today else range(start_month, month_of_today + 1)
        for current_m in total_months:
            url = "https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear" \
                  "=1840&EndYear=2019&Day=1&Year=" + str(current_y) + "&Month=" + str(current_m)
            urls.append(url)
    return urls


def weather_data():
    weather_dict = dict()
    for weather_url in url_collection():
        myp = WeatherScraper()
        with urllib.request.urlopen(str(weather_url)) as response:
            html = str(response.read())
            myp.feed(html)
            weather_dict.update(myp.weather_dic())
    return weather_dict


pprint(weather_data())
# weather_data()


# myp = WeatherScraper() with urllib.request.urlopen(
# 'http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear
# =2018&Day=1&Year=2011&Month=11#') as response: html = str(response.read()) myp.feed(html) myp.print_content()
