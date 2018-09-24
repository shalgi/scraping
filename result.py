class SingleResult(object):
    def __init__(self, page, text_offset, match_str):
        self.page = page
        self.offset = text_offset
        self.matched_string = match_str


class QueryResults(object):
    def __init__(self, results_dict):
        self.dictionary = results_dict

    def size(self):
        return len(self.dictionary)
