from server import database
from server.database.dashboard.dashboard_db_manager import get_dashboard_name


class Dataset:
    @property
    def username(self): return self._username

    @username.setter
    def username(self, val): raise ValueError('Cannot change username')

    @username.deleter
    def username(self): raise ValueError('Cannot delete username')


    @property
    def idx(self): return self._idx

    @idx.setter
    def idx(self, val): raise ValueError('Cannot change idx')

    @idx.deleter
    def idx(self): raise ValueError('Cannot delete idx')


    @property
    def title(self):
        return database.get_database().execute('SELECT * FROM {} WHERE id = ?'
                                               .format(get_dashboard_name(self.username)), (self.idx,)).fetchone()[
            'title']

    @title.setter
    def title(self, value):
        db = database.get_database()
        db.execute('UPDATE {} SET title = ? WHERE id = ?'
                   .format(get_dashboard_name(self.username)), (value, self.idx))
        db.commit()

    @title.deleter
    def title(self): raise ValueError('Cannot delete title')



    def __init__(self, username, idx):
        self._username = username
        self._idx = idx