from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from .decorators import define_usage

import requests as r
from datetime import datetime, timedelta
import re
import json

week = {0: 'ПН', 1: 'ВТ', 2: 'СР', 3: 'ЧТ', 4: 'ПТ', 5: 'СБ', 6: 'ВС'}


#URL /
@define_usage(returns={'url_usage': 'Dict'})
@api_view(['GET'])
def api_index(request):
    details = {}
    for item in list(globals().items()):
        if item[0][0:4] == 'api_':
            if hasattr(item[1], 'usage'):
                details[reverse(item[1].__name__)] = item[1].usage
    return Response(details)


@define_usage(returns={'schedule_leninka': 'List'})
@api_view(['GET'])
def api_leninka(request):
    resp = json.loads(re.sub(r'[)(;]', '', r.get('https://api.sportbs.net/v1_0/model/index/3148').text))
    schedule = []
    for i in range(14):
        try:
            raw_date = datetime.today() + timedelta(i)
            date = raw_date.strftime('%Y-%m-%d')
            answer = {'date': raw_date.strftime('%d.%m'), 'week': week[raw_date.weekday()]}
            for hour in range(17, 23):
                sec = str(hour * 3600)
                if sec in resp['days'][date]['hours'] and len(resp['days'][date]['hours'][sec]) == 3:
                    answer[str(hour)] = 0
                else:
                    answer[str(hour)] = 1
            schedule.append(answer)
        except IndexError:
            pass
    return Response(schedule)


@define_usage(returns={'schedule_dubrovka': 'List'})
@api_view(['GET'])
def api_dubrovka(request):
    # ближайшие 2 недели, вечер
    schedule = []
    headers_dubrovka = {
        'authorization': 'Bearer yusw3yeu6hrr4r9j3gw6, User ec8ecfaf1072c39041a7cc582a8ac232',
        'user-agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344'''
    }
    for i in range(14):
        try:
            raw_date = datetime.today() + timedelta(i)
            date = raw_date.strftime('%Y-%m-%d')
            answer = {'date': raw_date.strftime('%d.%m'), 'week': week[raw_date.weekday()],
                      '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0}
            day_resp = r.get(
                f'https://n136076.yclients.com/api/v1/book_times/144563/-1/{date}?service_ids%5B%5D=2177728',
                headers=headers_dubrovka).json()
            for time in day_resp:
                if time['time'] in ['17:00', '18:00', '19:00', '20:00', '21:00', '22:00']:
                    answer[time['time'].replace(':00', '')] = 1
            schedule.append(answer)
        except IndexError:
            pass
    return Response(schedule)


@define_usage(returns={'schedule_shabolovka': 'List'})
@api_view(['GET'])
def api_shabolovka(request):
    # ближайшие 2 недели
    schedule = []
    headers_shabolovka = {
        'authorization': 'Bearer yusw3yeu6hrr4r9j3gw6',
        'user-agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344'''
    }
    for i in range(14):
        try:
            raw_date = datetime.today() + timedelta(i)
            date = raw_date.strftime('%Y-%m-%d')
            answer = {'date': raw_date.strftime('%d.%m'), 'week': week[raw_date.weekday()],
                      '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0}
            day_resp = r.get(
                f'https://n116979.yclients.com/api/v1/book_times/127578/-1/{date}?service_ids%5B%5D=1705604',
                headers=headers_shabolovka).json()
            for time in day_resp:
                if time['time'] in ['17:00', '18:00', '19:00', '20:00', '21:00', '22:00']:
                    answer[time['time'].replace(':00', '')] = 1
            schedule.append(answer)
        except IndexError:
            pass
    return Response(schedule)