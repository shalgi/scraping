def empty_page(url):
    return Page(url, "", [])


class Page(object):
    def __init__(self, uid, text, links):
        self.uid = uid
        self.text = text
        self.links = links

