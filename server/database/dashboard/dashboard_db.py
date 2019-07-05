import random

from server import database
from server.database import auth
from server.utils import current_unix_time, get_dashboard_name


def generate_unique_id(username: str):
    HEXDIGITS = 'abcdef0123456789'

    idx = int(''.join(random.sample(HEXDIGITS, 8)), 16)
    while database.get_database().execute(f'SELECT * FROM {get_dashboard_name(username)} WHERE id = ?', (idx, ))\
                                                .fetchone() is not None:
        idx = int(''.join(random.sample(HEXDIGITS, 8)), 16)
    return idx


@auth.on_user_creation
def create_dashboard_table(username: str):
    db = database.get_database()
    dashboard_name = get_dashboard_name(username)
    # invulnerable to SQL injection
    # since all parts of `dashboard_name` is auto-generated
    db.execute(
        f'''
        CREATE TABLE {dashboard_name} (
            id INTEGER PRIMARY KEY, 
            title TEXT, 
            data TEXT, 
            layout TEXT,
            last_update INTEGER)
        '''
    )


@auth.on_user_removal
def drop_dashboard_table(username: str):
    db = database.get_database()
    dashboard_name = get_dashboard_name(username)
    db.execute('DROP TABLE IF EXISTS {}'.format(dashboard_name))


def append_dataset(username: str, title: str):
    db = database.get_database()
    idx = generate_unique_id(username)
    dashboard_name = get_dashboard_name(username)

    db.execute(
        f'INSERT INTO {dashboard_name} (id, title, data, layout, last_update) VALUES (?, ?, ?, ?, ?)',
        (idx, title, '{}', '[]', 0)
    )
    db.commit()


def remove_dataset(username: str, idx: int):
    db = database.get_database()
    db.execute(f'DELETE FROM {get_dashboard_name(username)} WHERE id = ?', (idx,))
    db.commit()


def update_dataset_data(username: str, idx: int, pld: str):
    """
    A low-level interface for editing dataset

    :param username: the user who possess the dataset
    :param idx: id of the dataset
    :param pld: a JSON-formatted string carrying data
    :return: None
    """
    db = database.get_database()
    db.execute(f'UPDATE {get_dashboard_name(username)} SET data = ?, last_update = ? WHERE id = ?',
               (pld, current_unix_time(), idx))
    db.commit()


def get_datasets(username):
    return database.get_database().execute(f'SELECT * FROM {get_dashboard_name(username)}').fetchall()
