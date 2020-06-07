from whoosh.index import create_in, open_dir, exists_in
import shutil
from whoosh.fields import *
import whoosh
import json
import os, os.path
from whoosh.qparser import QueryParser, MultifieldParser


class Indexer:
    def __init__(self):
        self.schema = Schema(title=TEXT, content=TEXT, index=NUMERIC(stored=True))
        self.ix = None
        self.writer = None
        self.directory = ''

    def updateIndex(self, file, dir):
        if not os.path.exists(dir) or not exists_in(dir):
            print(f'the given directory {dir} does not exists or does not contain valid index.\n')
            return
        self.ix = open_dir(dir)
        self.writer = self.ix.writer()
        all_data = self.ix.searcher().documents()
        indexes = [x['index'] for x in all_data]

        with open(file, 'r', encoding='utf8') as f:
            for line in f:
                j = json.loads(line)
                if j['index'] in indexes:
                    continue
                self.writer.add_document(title=j["title"], content=j['text'], index=j['index'])
        self.directory = dir
        self.writer.commit()

    def createIndex(self, file, directory):
        if os.path.exists(directory) and not exists_in(directory):
            print('Directory already exists and does not contain any index, deleting and creating new index...\n')
            shutil.rmtree(directory)
            os.mkdir(directory)

        if not os.path.exists(directory):
            os.mkdir(directory)

        if exists_in(directory):
            print('overwriting current index...\n')

        self.directory = directory
        self.ix = create_in(directory, self.schema)
        self.writer = self.ix.writer()
        self.writeToIndex(file)

    def writeToIndex(self, file):
        with open(file, 'r', encoding='utf8') as f:
            for line in f:
                j = json.loads(line)
                self.writer.add_document(title=j['title'], content=j['text'], index=j['index'])
        self.writer.commit()

    def searchIndex(self, directory, term):
        if not os.path.exists(directory) or not exists_in(directory):
            print(
                'Selected directory does not exists or does not contain any valid index. Please try again with valid directory..\n')
            return

        self.ix = open_dir(directory)

        with self.ix.searcher() as searcher:
            og = whoosh.qparser.OrGroup.factory(0.9)
            query = MultifieldParser(['content', 'title'], self.schema, group=og).parse(term)
            results = searcher.search(query, limit=None)
            return [x['index'] for x in results]
