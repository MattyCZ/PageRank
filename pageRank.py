from graph import Graph
import numpy as np


class ResultNode:
    def __init__(self, rank=0, url='', title='', index=0):
        self.rank = rank
        self.url = url
        self.title = title
        self.index = index

    def __repr__(self):
        return f'title: {self.title}, url: {self.url}, rank: {self.rank} \n'

    def __str__(self):
        return f'title: {self.title}, url: {self.url}, rank: {self.rank} \n'


class PageRank:

    def __init__(self, dumping=0.15, iterations=10):
        # graph, on which the PageRank will be calculated.
        self.graph = None
        # dumping factor
        self.p = dumping
        # number of max iterations
        self.MAX_ITER = iterations
        # number of pages to be searched
        self.num_of_pages = None
        # google matrix for ranking
        self.google_matrix = None
        # load graph and adjanced data
        self.result = []
        self.load()

    def load(self):
        self.graph = Graph()
        self.graph.load()
        self.num_of_pages = self.graph.size

        '''
        creates the google matrix where M = (1-p)*A + p.B. B = 1/n * [[1...1]...[1...1]]
        more explained on following url : https://bit.ly/2SPN3LA
        '''
        matrixA = np.zeros(shape=(self.num_of_pages, self.num_of_pages))

        # load matrix A
        for key in self.graph:
            value = 0 if len(self.graph[key].outlinks) == 0 else 1 / len(self.graph[key].outlinks)

            for key2 in self.graph[key].outlinks:
                matrixA[key2][key] = value

        matrixA = (1 - self.p) * matrixA

        # load matrix B
        value = 1 / self.num_of_pages
        matrixB = np.full((self.num_of_pages, self.num_of_pages), value)
        matrixB = self.p * matrixB

        # final google matrix
        self.google_matrix = matrixA + matrixB

    def calculateRank(self):
        # create vector V and iterate over it to gain better results
        vec = np.full(self.num_of_pages, 1 / self.num_of_pages)
        for i in range(self.MAX_ITER):
            vec = self.google_matrix @ vec

        # create the result
        for i in self.graph:
            resultNode = ResultNode(vec[i], self.graph[i].url, self.graph[i].title, i)
            self.result.append(resultNode)

        # sort the result according to the ranking
        self.result.sort(key=lambda x: x.rank, reverse=True)
        return self.result


if __name__ == '__main__':
    rank = PageRank()
    rank.calculateRank()
