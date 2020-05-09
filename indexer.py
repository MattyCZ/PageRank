from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import *
import whoosh
import json
import os, os.path
from whoosh.qparser import QueryParser, MultifieldParser

class Index:
    def __init__(self, remove=False):

        create = False

        if not os.path.exists("indexdir"):
            create = True
            os.mkdir("indexdir")

        self.schema = Schema(title=TEXT, content=TEXT, index=NUMERIC(stored=True))
        self.ix = create_in('indexdir', self.schema) if remove or create else open_dir('indexdir')
        self.writer = self.ix.writer()

        if create or remove:
            self.createIndex()

    def createIndex(self):
        with open("graphScraper/sitegraph.json") as file:
            for index, line in enumerate(file):
                j = json.loads(line)
                self.writer.add_document(title=j["title"], content=j['text'], index=index)
        self.writer.commit()

    def query(self,term):
        with self.ix.searcher() as searcher:
            og = whoosh.qparser.OrGroup.factory(0.9)
            query = MultifieldParser(["content", "title"], self.schema, group=og).parse(term)
            results = searcher.search(query, limit=None)
            return [x['index'] for x in results]