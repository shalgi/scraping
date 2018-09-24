from bs4 import BeautifulSoup
from .page import Page
from .exceptions import WikiValueException

HTML_PARSER = 'lxml'


class Parser(object):
    def __init__(self, response):
        self.data = response
        self.uid = response.url[response.url.find(r'/wiki/') + 6:]
        self.bs = BeautifulSoup(response.content, HTML_PARSER)
        self.check_result_found()
        self.body_content = self._get_body_content()

    def _get_body_content(self):
        mw_parser_output = self.bs.body.find_all("div",
                                                 class_="mw-parser-output")
        if len(mw_parser_output) != 1:
            raise WikiValueException(self.uid)
        return mw_parser_output[0]

    def get_all_wiki_links(self):
        links = self.body_content.find_all("a")
        href_links = _filter_by_attribute(links, False, "href", "/wiki/")
        wiki_links = _filter_by_attribute(href_links, True, "class", "image")
        no_wiktionary = _filter_by_attribute(wiki_links, True, "href",
                                             "wiktionary")
        wiki_entries = [a.get('href')[6:] for a in
                        no_wiktionary]  # cutting the /wiki/ beginning
        return wiki_entries

    def get_text(self):
        return self.body_content.get_text()

    def create_page(self):
        links = self.get_all_wiki_links()
        text = self.get_text()
        page = Page(self.uid, text, links)
        return page

    def check_result_found(self):
        if self.bs.body.find('p', class_="mw-search-nonefound"):
            raise WikiValueException(self.uid)


def _filter_by_attribute(rs, remove_tags_with_attribute, attribute,
                         attribute_value):
    """
    :param remove_tags_with_attribute: whether we want to keep tags that has
     this attribute and its value
    :type remove_tags_with_attribute: bool
    :param attribute_value: a part of the value of the attribute we want to
    filter by
    :type attribute_value: str
    :return: filtered list
    :rtype: list of Tags
    """
    return [tag for tag in rs if (((tag.get(attribute) is not None)
                                   and attribute_value in tag.get(
        attribute))
                                  ^ remove_tags_with_attribute)]
