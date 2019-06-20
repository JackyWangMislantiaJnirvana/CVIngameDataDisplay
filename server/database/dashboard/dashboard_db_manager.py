from server import database
from server.database import auth
from server.database.dashboard.dataset import Dataset


def get_dashboard_name(username: str):
    return 'dashboard_' + str(auth.get_user(username)['id'])


@auth.on_user_creation
def create_dashboard_db(username: str):
    db = database.get_database()
    dashboard_name = get_dashboard_name(username)
    # invulnerable to SQL injection
    # since all parts of `dashboard_name` is auto-generated
    db.execute(
        '''
        CREATE TABLE {} (
            id INTEGER PRIMARY KEY, 
            title TEXT, 
            data TEXT, 
            layout TEXT,
            last_update INTEGER)
        '''.format(dashboard_name)
    )


@auth.on_user_removal
def drop_dashboard_db(username: str):
    db = database.get_database()
    dashboard_name = get_dashboard_name(username)
    db.execute('DROP TABLE IF EXISTS {}'.format(dashboard_name))


def append_dataset(username: str, idx: int, title: str):
    db = database.get_database()

    dashboard_name = get_dashboard_name(username)
    db.execute(
        'INSERT INTO {} (id, title) VALUES (?, ?)'.format(dashboard_name),
        (idx, title)
    )
    return Dataset(username, idx)
