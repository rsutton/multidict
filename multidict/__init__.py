"""
MultiDict - multi-level dictionary object

Implementation of nested dictionary which can be initialized by a
dict object or json string loaded from a file.

"""
import json
import logging
import os


class MultiDict(object):
    def __init__(self, data=None, filename=None):
        self.logger = logging.getLogger(__name__)

        if filename is not None:
            self.from_file(filename)
        elif data is not None:
            self.with_data(data=data)

    def with_data(self, data):
        assert isinstance(data, dict)
        self.__dict__ = MultiDictData(data=data)

    def from_file(self, filename):
        """ Load the Configuration from file """
        fh = os.path.realpath(filename)
        self.__dict__ = MultiDictData(data=json.load(open(fh)))


class MultiDictData(dict):
    def __init__(self, data):
        super(MultiDictData, self).__init__()
        self.set_data(data)

    def set_data(self, data):
        for k, v in data.items():
            if isinstance(v, dict):
                self[k] = MultiDictData(data=v)
            else:
                self[k] = v

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
