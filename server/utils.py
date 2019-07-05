import time
import datetime
import simpleeval

from server.database import auth


def current_unix_time():
    return time.mktime(datetime.datetime.now().timetuple())


def get_dashboard_name(username: str):
    return 'dashboard_' + str(auth.get_user(username)['id'])


def to_percentage(x):
    return "{:.2f}%".format(x * 100)


def to_dataset_hash(i: int) -> str:
    return hex(i).split('x')[1]


def fill_and_calc(s, data):
    return simpleeval.simple_eval(s.format(**data))
