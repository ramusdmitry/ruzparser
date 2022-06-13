'''
import requests
import json
from sql_wrapper import SQL
from datetime import datetime, date


class Lesson:
    def __init__(self, number, subject, teacher, room, url, timeFrom, timeTo, group):
        self.number = number
        self.subject = subject
        self.teacher = teacher
        self.room = room
        self.url = url
        self.timeFrom = timeFrom
        self.timeTo = timeTo
        self.group = group


class Parser:

    def __init__(self, university, group):
        self.university = university
        self.group = group

    def get_schedule(self):
        universities = {'МИЭТ': MIET(self.university, self.group)}
        return universities[self.university]

    @staticmethod
    def convert_time(s):
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').time()

    @staticmethod
    def get_json_schedule(request):
        try:
            return json.loads(requests.get(request).text)
        except ValueError as e:
            print(f'Parsing error {e}')


class MIET(Parser):

    def __init__(self, university, group):
        super().__init__(university, group)
        self.req = f'https://miet.ru/schedule/data?group={self.group}'
        self.schedule = self.parser_of_scheduler()

    def __getitem__(self, item):
        return self.schedule[item]

    def __len__(self):
        return len(self.schedule)

    def parser_of_scheduler(self):
        data = self.get_json_schedule(self.req)['Data']
        current_week = self.get_current_number_of_week()
        result = [[] for _ in range(6)]
        for i in data:
            day, week = int(i['Day']), i['DayNumber']

            number, start, finish = int(i['Time']['Time'][0]), i['Time']['TimeFrom'], i['Time']['TimeTo']
            timeFrom, timeTo = self.convert_time(start), self.convert_time(finish)
            # time = f'{self.convert_time(start)} - {self.convert_time(finish)}'

            subject, lecturer = i['Class']['Name'], i['Class']['Teacher']
            group, room = i['Group']['Name'], i['Room']['Name']

            # schedule = {'number': number,
            #             'time': f'{self.convert_time(start)} - {self.convert_time(finish)}',
            #             'lesson': subject,
            #             'lecturer': lecturer,
            #             'room': room,
            #             'day': day}
            item = Lesson(number, subject, lecturer, room, str(), timeFrom, timeTo, group)

            if week == current_week:
                result[day - 1].append(item)
                result[day - 1].sort(key=lambda x: x.number)

        return result

    @staticmethod
    def get_current_number_of_week():
        return int((datetime.now().date() - date(2016, 8, 29)).days / 7) % 4


p = Parser(university="МИЭТ", group="ПИН-11").get_schedule()
db = SQL()
db.connect('schedule.db')
db.fill_week(p)


def output_schedule():
    days = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 4: 'Четверг', 5: 'Пятница', 6: 'Суббота'}
    for i in range(len(p)):
        print(days[i + 1])
        for j in p[i]:
            print(f'{j.number} пара ({j.time})')
            print(f'Предмет: {j.subject}')
            print(f'Учитель: {j.teacher}')
            print(f'Кабинет: {j.room}')
            print(f'Ссылка: {j.url}')
            print(f'Группа: {j.group}')
            print(j.subject, j.teacher, j.room, j.url, j.time, j.group)
            print()
        print()

'''
