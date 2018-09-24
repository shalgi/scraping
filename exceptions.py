class ScraperException(Exception):
    pass


class KeyNotFoundException(ScraperException):
    def __init__(self, key):
        super().__init__(
            "key {key} not found".format(key=key))


class WikiValueException(ScraperException):
    def __init__(self, uid):
        super().__init__(
            "wiki value not found {uid}".format(uid=uid))
