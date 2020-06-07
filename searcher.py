class Searcher:
    def __init__(self, pageRank, indexer):
        self.pageRank = pageRank
        self.indexer = indexer

    def search(self, indexdir, term):
        rank = self.pageRank.calculate_rank()
        valid_pages = self.indexer.searchIndex(indexdir, term)
        result = [page for page in rank if page.index in valid_pages]
        return result
