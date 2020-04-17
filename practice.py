import urllib.request
from html.parser import HTMLParser


class DataScraper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._count = 0
        self._events = dict()
        self._flag = None

    def handle_starttag(self, tag, attrs):
        if tag == 'h3' and attrs.__contains__(('class', 'event-title')):
            self._count += 1
            self._events[self._count] = dict()
            self._flag = 'event-title'
        if tag == 'time':
            self._flag = 'time'
        if tag == 'span' and attrs.__contains__(('class', 'event-location')):
            self._flag = 'event-location'

    def handle_data(self, data):
        if self._flag == 'event-title':
            self._events[self._count][self._flag] = data
        if self._flag == 'time':
            self._events[self._count][self._flag] = data
        if self._flag == 'event-location':
            self._events[self._count][self._flag] = data
        self._flag = None

    def event_list(self):
        print(self._events)
        # print('Recent conventions, ', self._count, 'More details: ')
        # for event in self._events.values():
        #     print("{0:50} {1:50}  {2:50}".format(event['event-title'], event['time'], event['event-location']))


mp = DataScraper()
with urllib.request.urlopen('https://www.python.org/events/python-events/') as response:
    html = str(response.read())

mp.feed(html)
mp.event_list()
