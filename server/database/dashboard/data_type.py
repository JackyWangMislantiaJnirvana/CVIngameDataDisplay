from abc import abstractmethod

from flask import render_template

import server


class DataType:
    '''
    Represent a datum in the dataset.
    Initialize with a dict (see API)
    '''

    @abstractmethod
    def render(self, *args, **kwargs): pass

    def __init__(self, d):
        self.__class__ = getattr(server.database.dashboard.data_type, d['type'])
        self.__dict__ = d


class PhyQuantity(DataType):
    def __init__(self, d):
        assert('unit' in d and 'value' in d)
        super().__init__(d)

    def __repr__(self):
        return str(self.value) + str(self.unit)

    def render(self, display_name):
        return render_template('dataset/phy_quantity.html',
                               display_name=display_name, value=self.value, unit=self.unit)


class Text(DataType):
    def __init__(self, d):
        assert('value' in d)
        super().__init__(d)

    def render(self, display_name):
        return render_template('dataset/plain_text.html',
                               display_name=display_name, value=self.value)


class Boolean(DataType):
    def __init__(self, d):
        assert('value' in d)
        super().__init__(d)

    def render(self, display_name):
        return render_template('dataset/boolean.html',
                               display_name=display_name, value=self.value)


class Vector(DataType):
    def __init__(self, d):
        assert('value' in d)
        super().__init__(d)

    def render(self, *args, **kwargs):
        raise NotImplementedError('Vector Data cannot be rendered')


class Image(DataType):
    def __init__(self, d):
        assert('value' in d)
        super().__init__(d)

    def render(self, display_name):
        return NotImplementedError('Use Custom Renderer to render an image')
