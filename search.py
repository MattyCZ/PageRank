from pageRank import PageRank
from indexer import Index
import sys


class Searcher:

    def __init__(self):
        self.pageRank = PageRank()
        self.index = Index(True)

    def search(self, term=None):
        rank = self.pageRank.calculateRank()
        print("enter the search term:\n")
        term = term or input()
        valid_pages = self.index.query(term)

        result = [page for page in rank if page.index in valid_pages]
        print(result)


if __name__ == '__main__':
    searcher = Searcher()
    searcher.search()
