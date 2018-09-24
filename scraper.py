import requests
import ipdb
import pickle
from src.parse_engine import Parser
from src.dict_index import DictIndex
from src.searcher import Searcher
from src.exceptions import ScraperException
from src.page import empty_page
import logging

LOG_PATH = r"C:\users\carmel\PycharmProjects\scraping"
WIKI_SEARCH_FORMAT = "https://en.wikipedia.org/w/index.php?title=Special:Search&search={value}"


def find_url_by_value(value):
    search_url = WIKI_SEARCH_FORMAT.format(value=value)
    res = requests.get(search_url)
    return res.url


class Scraper(object):
    def __init__(self):
        self.index = DictIndex()
        self.searcher = Searcher(self.index)

    def index_by_value(self, value, depth):
        """
        :param value: a value to look for in wikipedia and scrape from it depth levels deep
        :type value: str
        :param depth: number of levels deep to go from value
        :type depth: int
        """
        values_to_index = {value}
        new_counter = 0
        total_counter = 0
        for i in range(depth):
            current_depth_links = set()
            for value in values_to_index:
                total_counter += 1
                if value in self.index:
                    page = self.index[value]
                else:
                    new_counter += 1
                    page = self.index_a_value(value)
                current_depth_links = current_depth_links.union(page.links)
                curr_size = self.index.size()
                if curr_size % 50 == 0:
                    logging.info("Index size: {size}".format(size=curr_size))
            logging.info("FINISHED DEPTH {depth}".format(depth=i + 1))
            values_to_index = current_depth_links.copy()

    def index_a_value(self, value):
        logging.info("indexing value {value}".format(value=value))
        url = find_url_by_value(value)
        return self._index_a_url(url)

    def _index_a_url(self, url):
        #  TODO: check wikipedia url and response is valid
        res = requests.get(url)
        try:
            parser = Parser(res)
            page = parser.create_page()
            self.index[page.uid] = page
            return page
        except ScraperException:
            logging.warning("ScraperException on url {url}".format(url=url))
            return empty_page(url)

    def remove_value(self, value):
        del self.index[value]


def main():
    logging.basicConfig(
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler("{0}/{1}.log".format(LOG_PATH, "log1.log")),
            logging.StreamHandler()],
        level=logging.INFO)
    logging.info("started")
    scraper = Scraper()
    # scraper.index_by_value("Grenade_(disambiguation)", 3)
    # with open(r"C:\Users\carmel\Desktop\temp\granade3.pickle", 'rb') as h:
    #    scraper.index.dictionary = pickle.load(h)
    logging.info("finished")
    # result = scraper.searcher.search_all("cock tail")
    # result = scraper.searcher.search_all("main issue")
    # result = scraper.searcher.search_all("the american nation")
    result = scraper.searcher.search_by_key('California', "shrinked in the recent years")
    # result = scraper.searcher.search_page(scraper.index["Shako"], "balon")
    # result = scraper.searcher.search_page(scraper.index["Shako"], "bad boy")
    ipdb.set_trace()


if __name__ == '__main__':
    main()
