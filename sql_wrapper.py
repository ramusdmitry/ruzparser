import sqlite3 as sql
import logging
import chromalog

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

chromalog.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class SQL:
    def __init__(self, name):
        self.conn = None
        self.cur = None
        self.name = name

    def connect(self):
        try:
            self.conn = sql.connect(self.name)
            self.cur = self.conn.cursor()
            logger.info(f"Database {self.name} has been created")
            return 0
        except:
            logger.critical(f"Database {self.name} hasn`t been created. See a error:")
            return -1

    def create_table(self, day):
        r = f"""CREATE TABLE IF NOT EXISTS {day}
        (number INT, 
        subject NCHAR, 
        teacher NCHAR, 
        room NCHAR, 
        url NCHAR, 
        timeFrom NCHAR, 
        timeTo NCHAR, 
        group_name NCHAR);"""
        try:
            self.cur.execute(r)
            self.conn.commit()
            logger.info(f'\tTable {day} has been successfully created')
        except:
            logger.error(f"Cannot create table '{day}', because ")

    def insert_schedule(self, day, lesson):
        r = f"""INSERT INTO {day}(number, subject, teacher, room, url, timeFrom, timeTo, group_name)
        VALUES({lesson.number}, '{lesson.subject}', '{lesson.teacher}', '{lesson.room}', '{lesson.url}', '{lesson.timeFrom}', '{lesson.timeTo}', '{lesson.group}');
        """
        try:
            self.cur.execute(r)
            self.conn.commit()
            logger.info(f'\tInsert lesson to {day} has been successfully')
        except:
            logger.error(f'Cannot insert lessons to {day}, because')

    def create_body(self, uni_name):

        pass

    def create_week(self):
        for i in days_of_week:
            self.create_table(i)

    def insert_week(self, day, lessons):
        for l in lessons:
            self.insert_schedule(day, l)

    def fill_week(self, lessons):
        self.create_week()
        for days_schedule, d in zip(lessons, days_of_week):
            self.insert_week(d, days_schedule)

    def get_data(self):
        r = f"""SELECT * from MIET"""
        self.cur.execute(r)
        data = self.cur.fetchall()
        for i in data:
            print(i)

'''
TIMETABLE:
UNIVERSITY
    -MIET
        -MONDAY
            -number,
            -subject
            -teacher
            -room
            -url
            -time
            -group
        -TUESDAY
        -WEDNESDAY
        -THURSDAY
        -FRIDAY
        -SATURDAY
'''
