import json
from copy import deepcopy
from pprint import pprint

from server import database
from server.database.dashboard.dashboard_db_manager import get_dashboard_name
from server.database.dashboard.data_type import DataType


class Dataset:
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, val):
        raise ValueError('Cannot change username')

    @username.deleter
    def username(self):
        raise ValueError('Cannot delete username')

    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, val):
        raise ValueError('Cannot change idx')

    @idx.deleter
    def idx(self):
        raise ValueError('Cannot delete idx')

    @property
    def title(self):
        return database.get_database().execute(f'SELECT * FROM {get_dashboard_name(self.username)} WHERE id = ?',
                                                        (self.idx,)).fetchone()['title']

    @title.setter
    def title(self, value):
        db = database.get_database()
        db.execute(f'UPDATE {get_dashboard_name(self.username)} SET title = ? WHERE id = ?', (value, self.idx))
        db.commit()

    @title.deleter
    def title(self):
        raise ValueError('Cannot delete title')

    def _get_db_item(self):
        return database.get_database().execute(
            f'SELECT * FROM {get_dashboard_name(self.username)} WHERE id = ?', (self.idx, ))

    @property
    def data(self) -> dict:
        """
        Retrieve and parse dataset content from sqlite
        :return: dict containing data
        """

        data_str = self._get_db_item()
        data_dict = json.loads(data_str)

        for k in data_dict:
            assert (isinstance(data_dict[k], dict))
            data_dict[k] = DataType(data_dict[k])

        pprint(data_dict)
        return data_dict

    @data.setter
    def data(self, data_dict):
        """
        :param data_dict: dictionary containing DataType elements
        :return: None
        """
        db = database.get_database()

        d = deepcopy(data_dict)
        for k, v in d.items():
            assert (isinstance(v, DataType))
            d[k] = v.__dict__
        s = json.dumps(d)
        pprint(s)
        db.execute(f'UPDATE {get_dashboard_name(self.username)} SET data=? WHERE id=?'
                   , (s, self.idx))
        db.commit()

    @data.deleter
    def data(self): raise ValueError('Cannot delete data')

    def __init__(self, username, idx):
        self._username = username
        self._idx = idx
