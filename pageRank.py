from graph import Graph
import numpy as np

class PageRank :

    def __init__(self, dumping = 0.15, iterations = 10):
        # graph, on which the PageRank will be calculated.
        self.graph = None
        # dumping factor
        self.p = dumping
        # number of max iterations
        self.MAX_ITER = iterations
        # number of pages to be searched
        self.num_of_pages  = None
        # google matrix for ranking
        self.google_matrix = None
        # load graph and adjanced data
        self.load()

    def load(self):
        self.graph = Graph()
        self.num_of_pages = self.graph.size

        '''
        creates the google matrix where M = (1-p)*A + p.B. B = 1/n * [[1...1]...[1...1]]
        more explained on following url : https://bit.ly/2SPN3LA
        '''
        matrixA = np.zeros(shape=(self.num_of_pages, self.num_of_pages))

        # load matrix A
        for key in self.graph:
            value = 0 if len(self.graph[key].outlinks) == 0 else 1 / len(self.graph[key].outlinks)
            first_index = self.graph[key].index

            for key2 in self.graph[key].outlinks:
                second_index = self.graph[key2].index
                matrixA[second_index][first_index] = value
        print(matrixA)
        matrixA = (1-self.p)*matrixA

        # load matrix B
        value = 1/self.num_of_pages
        matrixB = np.full((self.num_of_pages,self.num_of_pages), value)
        matrixB = self.p*matrixB

        # final google matrix
        self.google_matrix = matrixA + matrixB

    def calculateRank(self):
        #create vector V and iterate over it to gain better results

        vec = np.full(self.num_of_pages,1/self.num_of_pages)
        for i in range(self.MAX_ITER):
            vec = self.google_matrix @ vec
        return vec

rank = PageRank().calculateRank()
print(rank)
