from abc import ABCMeta, abstractmethod


class Index(object, metaclass=ABCMeta):

    @abstractmethod
    def __contains__(self, item):
        pass

    @abstractmethod
    def __getitem__(self, item):
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        pass

    @abstractmethod
    def __delitem__(self, key):
        pass

    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def add(self, key, value, override=False):
        pass

    @abstractmethod
    def remove(self, key):
        pass

    @abstractmethod
    def has_key(self, key):
        pass

    @abstractmethod
    def get_keys(self):
        pass

    @abstractmethod
    def get(self, key):
        pass
