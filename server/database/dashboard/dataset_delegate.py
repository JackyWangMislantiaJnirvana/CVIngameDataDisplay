import json
from copy import deepcopy

from database.dashboard import dashboard_db
from server.renderer.renderer_registry import registry as renderer_registry
from server import database
from server.utils import get_dashboard_name
from server.database.dashboard.data_type import DataType


class DatasetDelegate:
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

    def _get_db_item(self):
        return database.get_database().execute(
            f'SELECT * FROM {get_dashboard_name(self.username)} WHERE id = ?', (self.idx, )).fetchone()

    @property
    def title(self):
        return self._get_db_item()['title']

    @title.setter
    def title(self, value):
        db = database.get_database()
        db.execute(f'UPDATE {get_dashboard_name(self.username)} SET title = ? WHERE id = ?', (value, self.idx))
        db.commit()

    @title.deleter
    def title(self):
        raise ValueError('Cannot delete title')

    def set_layout(self, layout_list):
        """
        Parse the layout to JSON, and store into database
        :param layout_list: list of dicts
        :return: None
        """
        db = database.get_database()
        db.execute(f'UPDATE {get_dashboard_name(self.username)} SET layout = ? WHERE id = ?',
                   (json.dumps(layout_list), self.idx))
        db.commit()

    @property
    def data_content(self) -> dict:
        """
        Retrieve and parse dataset content from sqlite
        :return: dict containing data
        """

        data_str = self._get_db_item()['data']
        data_dict = json.loads(data_str)

        for k in data_dict:
            assert (isinstance(data_dict[k], dict))
            data_dict[k] = DataType(data_dict[k])

        return data_dict

    @data_content.setter
    def data_content(self, data_dict):
        """
        :param data_dict: dictionary containing DataType elements
        :return: None
        """

        d = deepcopy(data_dict)
        for k, v in d.items():
            assert(isinstance(v, DataType))
            d[k] = v.__dict__
        s = json.dumps(d)
        dashboard_db.update_dataset_data(self.username, self.idx, s)

    @data_content.deleter
    def data_content(self): raise ValueError('Cannot delete data')

    @property
    def last_update(self):
        return self._get_db_item()['last_update']

    def __init__(self, username: str, idx: int):
        self._username = username
        self._idx = idx

    def render(self, is_modal=True):
        buf = ''

        layout_list = json.loads(self._get_db_item()['layout'])
        for x in layout_list:
            buf = buf + renderer_registry.get_renderer(x['render_type']).render(self.data_content, x, is_modal=is_modal)

        return buf
