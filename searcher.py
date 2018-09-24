import difflib
import re
from abc import ABCMeta, abstractmethod
from src.result import SingleResult
from src.result import QueryResults

MAX_WORD_MATCHES = 5
MIN_MATCH_SCORE = 0.8


class Search(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def search_all(self, query):
        pass

    @abstractmethod
    def search_by_key(self, key, query):
        pass

    @abstractmethod
    def search_page(self, page, query):
        pass


class Searcher(Search):
    def __init__(self, index):
        self.index = index

    def search_all(self, query):
        results_dict = {}
        for value in self.index.get_keys():
            page = self.index[value]
            page_matches = self._search_page(page, query)
            if len(page_matches) > 0:
                if page.uid not in results_dict:
                    results_dict[page.uid] = []
                results_dict[page.uid].extend(page_matches)
        return QueryResults(results_dict)

    def search_by_key(self, key, query):
        page = self.index[key]
        return self.search_page(page, query)

    @classmethod
    def search_page(cls, page, query):
        result = QueryResults({page.uid: cls._search_page(page, query)})
        return result

    @classmethod
    def _search_page(cls, page, query):
        results_list = []
        text_results = cls._search_in_text(page.text, query)
        # text_results = cls.search_word_in_text(page.text, query)
        for offset, match_str in text_results:
            results_list.append(SingleResult(page, offset, match_str))
        return results_list

    # currently just finding the first occurrence of the (exact) query
    @classmethod
    def _simple_search_text(cls, text, query):
        results_list = []
        text_offset = text.find(query)
        results_list.extend([(text_offset, query)])
        return results_list

    @classmethod
    def _search_in_text(cls, text, query):
        '''
        searching with difflib using terms of n words
        :param text: text to search in
        :type text: str
        :param query: query to look for
        :type query: "str"
        :return: list of tuples containing offset and query
        :rtype: list tuples
        '''
        results_list = []
        text_list = make_n_terms(text, len(query.split()))
        matches = difflib.get_close_matches(query, text_list,
                                            MAX_WORD_MATCHES, MIN_MATCH_SCORE)
        for match in matches:
            results_list.extend(cls._simple_search_text(text, match))
        return results_list

    '''
    @classmethod
    def search_word_in_text(cls, text, word):
        results_list = []
        uni_text_list = split_text(text)
        matches = difflib.get_close_matches(word, uni_text_list,
                                            MAX_WORD_MATCHES, MIN_MATCH_SCORE)
        for match in matches:
            results_list.extend(cls.simple_search_text(text, match))
        return results_list
    '''


def split_text(text):
    text_list = split_text_ordered(text)
    return list(set(text_list))


def split_text_ordered(text):
    return re.split('["\'()!?., \\r\\n]', text)


def make_n_terms(text, n):
    splited = split_text_ordered(text)
    n_terms = [" ".join(splited[i:i+n]) for i in range(len(splited) - (n - 1))]
    return n_terms

'''
    @staticmethod
    def search_text(text, query):
        difflib.get_close_matches(query, word)
        return results_list
'''