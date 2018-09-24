from .exceptions import KeyNotFoundException
from .index import Index


class DictIndex(Index):
    def __init__(self):
        self.dictionary = {}

    def __contains__(self, item):
        return item in self.dictionary

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.add(key, value)

    def __delitem__(self, key):
        self.pop(key)

    def add(self, key, value, override=False):
        if key not in self or override:
            self.dictionary[key] = value

    def remove(self, key):
        if key in self.dictionary:
            self.dictionary.pop(key)

    def has_key(self, key):
        return key in self.dictionary

    def get_keys(self):
        return self.dictionary.keys()

    def get(self, key):
        if key not in self:
            raise KeyNotFoundException(key)
        else:
            return self.dictionary[key]

    def size(self):
        return len(self.dictionary)
