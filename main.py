import requests
import json
import datetime


class Parser:

    def __init__(self, university, stage, group):
        self.university = university
        self.stage = stage
        self.group = group

    @staticmethod
    def convert_time(s):
        from datetime import datetime
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').time()

    @staticmethod
    def get_current_number_of_week():
        return int((datetime.datetime.now() - (datetime.datetime.strptime("2016-08-29", "%Y-%m-%d"))).days / 7)


class MIET(Parser):

    def get_json_resut(self):
        try:
            data = json.loads(requests.post(f'https://miet.ru/schedule/data?group={self.group}').text)
            return data
        except ValueError as e:
            print(f'Parsing error {e}')
            return None

    def parser_of_scheduler(self, response):
        data = response['Data']
        WEEK = self.get_current_number_of_week()
        while WEEK > 4:
            WEEK -= 4
        mon, tue, wed, thu, fri, sat = [], [], [], [], [], []
        for i in data:
            day, week = i['Day'], i['DayNumber']
            number, start, finish = i['Time']['Code'], i['Time']['TimeFrom'], i['Time']['TimeTo']
            lesson, lecturer = i['Class']['Name'], i['Class']['Teacher']
            group, room = i['Group']['Name'], i['Room']['Name']

            schedule = {'number': number,
                        'time': f'{self.convert_time(start)} - {self.convert_time(finish)}',
                        'lesson': lesson,
                        'lecturer': lecturer,
                        'room': room,
                        'week': week}

            if day == 1 and week == WEEK:
                mon.append(schedule)
            if day == 2 and week == WEEK:
                tue.append(schedule)
            if day == 3 and week == WEEK:
                wed.append(schedule)
            if day == 4 and week == WEEK:
                thu.append(schedule)
            if day == 5 and week == WEEK:
                fri.append(schedule)
            if day == 6 and week == WEEK:
                sat.append(schedule)

        mon = sorted(mon, key=lambda x: x['number'] and x['week'])
        tue = sorted(tue, key=lambda x: x['number'] and x['week'])
        wed = sorted(wed, key=lambda x: x['number'] and x['week'])
        thu = sorted(thu, key=lambda x: x['number'] and x['week'])
        fri = sorted(fri, key=lambda x: x['number'] and x['week'])
        sat = sorted(sat, key=lambda x: x['number'] and x['week'])

        week = [mon, tue, wed, thu, fri, sat]
        return week

    def print_result(self):
        result = self.parser_of_scheduler(self.get_json_resut())
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        for d, w in zip(days, result):
            print(d)
            for i in sorted(w, key=lambda x: x['number']):
                print(f"#{i['number']} ({i['time']}) Неделя {i['week']}\n\t"
                      f"{i['lesson']} [{i['room']}] ({i['lecturer']})\n")
            print()


MIET(group='ПИН-11', university='', stage='').print_result()
