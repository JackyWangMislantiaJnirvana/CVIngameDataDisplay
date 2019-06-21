import time
import datetime

from server.database import auth


def current_unix_time():
    return time.mktime(datetime.datetime.now().timetuple())


def get_dashboard_name(username: str):
    return 'dashboard_' + str(auth.get_user(username)['id'])


def to_percentage(x):
    return "{.2f}%".format(x * 100)


def to_dataset_hash(i: int) -> str:
    return hex(i).split('x')[1]
