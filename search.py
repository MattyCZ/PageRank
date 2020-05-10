from pageRank import PageRank
from indexer import Index
import sys

class Searcher:

    def __init__(self):
        self.pageRank = PageRank()
        self.index = Index(True)
    def search(self):
        rank = self.pageRank.calculateRank()
        print("enter the search term:\n")
        term = input()
        valid_pages = self.index.query(term)

        result = [page for page in rank if page.index in valid_pages]
        print(result)

searcher = Searcher()
searcher.search()