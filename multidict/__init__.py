"""
MultiDict - multi-level dictionary object

"""
import json
import logging
import os


class MultiDict(object):
    def __init__(self, filename=None, data=None, **kwargs):
        self._filename = filename
        self.logger = logging.getLogger(__name__)

        if filename is not None:
            self._data = MultiDictData(data=self.load_from_file())
        elif data is not None:
            assert isinstance(data, dict)
            self._data = MultiDictData(data=data)

    @property
    def data(self):
        return self._data

    @property
    def filename(self):
        return self._filename

    def load_from_file(self):
        """ Load the Configuration from file """
        if os.path.exists(self.filename):
            fh = os.path.realpath(self.filename)
        else:
            msg = "Configuration file {} was not found!".format(self.filename)
            self.logger.error(msg)
            raise ValueError(msg)
        try:
            result = json.load(open(fh))
        except ValueError as e:
            msg = "Unable to load configuration from {}: {}".format(self.filename, e)
            self.logger.error(msg)
            raise ValueError(msg)
        return result


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
