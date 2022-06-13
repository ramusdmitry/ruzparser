from sql_wrapper import SQL
from parsing.parser import Parser
import json
p = Parser(university="МИЭТ", group="ПИН-11").get_schedule() # получаем объект (класса вуз) расписания на неделю
x = p.return_json_object()
print(x)
# import requests
# response = requests.get('http://127.0.0.1:8000/?uni=МИЭТ&group=ПИН-11').text
# data = json.loads(response)
# schedule = data['schedule']
# monday = schedule['Monday'] # или data['schedule']['Monday']
# for i in monday: #вывод всех пар для понедельника
#     print(i)
#if __name__ == "__main__":
    #db = SQL('schedule.db')
    #db.connect()
    #db.fill_week(p)
    #db.get_data()



