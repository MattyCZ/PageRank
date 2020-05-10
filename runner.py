from scraper import Scraper
from graph import Graph
from indexer import Indexer
from pageRank import PageRank
from searcher import Searcher
import os

scraped_data = f'{os.path.dirname(os.path.realpath(__file__))}/scraped_data.json'
graph_data = f'{os.path.dirname(os.path.realpath(__file__))}/graph_data.json'
indexdir = 'indexdir'

#scraper = Scraper(scraped_data)
#scraper.run(max_pages=100, start_urls=['https://en.wikipedia.org/wiki/Main_Page', 'https://dmoz-odp.org/'], stay_on_domains=False)

graph = Graph()
#graph.createNewGraph(scraped_data,graph_data)
graph.loadExisting(graph_data)

indexer = Indexer()
#indexer.createIndex(graph_data, indexdir)

pageRank = PageRank(graph)

searcher = Searcher(pageRank, indexer)
searcher.search(indexdir, 'black hole')

