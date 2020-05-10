import json
import os
class Node:
    def __init__(self):
        self.name = None
        self.outlinks = None
        self.pointsTo = None
        self.title = None
        self.url = None
        self.text = None
        self.index = None

class Graph:
    def __init__(self):
        self.size = 0
        self.graph = dict()

    def __iter__(self):
        return iter(self.graph)

    def __getitem__(self, item):
        return self.graph[item]

    def readInput(self, input, start=0):
        nodes = dict()
        if not os.path.exists(input):
            print(f'the given file{input} does not exists.\n')
            return
        with open(input, 'r', encoding='utf8') as file:
            for index, line in enumerate(file,start=start):
                j = json.loads(line)
                node = Node()
                node.name = j["slug"]
                node.title = j["title"]
                node.url = j["url"]
                node.text = j["text"]
                node.outlinks = j["outlinks"]
                node.pointsTo = j["outlinks"]
                node.index = index
                nodes[node.name] = node

        return nodes

    def save(self,output, overwrite=True):
        if os.path.exists(output) and overwrite:
            print(f'the given file{output} already exists, overwriting...\n')
            os.remove(output)

        with open(output, 'w', encoding='utf8') as f:
            for index, node in enumerate(self.graph):
                data = {
                    'name': self.graph[node].name,
                    'title': self.graph[node].title,
                    'url': self.graph[node].url,
                    'text': self.graph[node].text,
                    'outlinks' : self.graph[node].outlinks,
                    'index' : self.graph[node].index,
                    'pointsTo' : self.graph[node].pointsTo
                }
                json.dump(data,f)
                f.write('\n')

    def createNewGraph(self, input, output='', save=True):

        nodes = self.readInput(input)
        self.size = len(nodes)
        # clean outlinks from unexisting pages and change the slugs to indexes.
        for key in nodes:
            nodes[key].outlinks = [nodes[x].index for x in nodes[key].outlinks if x in nodes.keys() and x != nodes[key].name]
        for key in nodes:
            self.graph[nodes[key].index] = nodes[key]
        if save:
            self.save(output)

    def loadExisting(self, input):
        if not os.path.exists(input):
            print(f'the given file{input} does not exists.\n')
            return

        with open(input, 'r', encoding='utf8') as file :
            for line in file:
                j = json.loads(line)

                node = Node()
                node.name = j["name"]
                node.title = j["title"]
                node.url = j["url"]
                node.text = j["text"]
                node.outlinks = j["outlinks"]
                node.pointsTo = j["pointsTo"]
                node.index = j["index"]

                self.graph[node.index] = node

        self.size = len(self.graph)

    def addToExisting(self,input_graph, input_file, output, save=True):
        self.loadExisting(input_graph)
        nodes = self.readInput(input_file, self.size)
        for key in self.graph:
            self.graph[key].outlinks = self.graph[key].pointsTo
            nodes[self.graph[key].name] = self.graph[key]
        for key in nodes:
            nodes[key].outlinks = [nodes[x].index for x in nodes[key].outlinks if x in nodes.keys() and x != nodes[key].name]
        self.graph = dict()
        for key in nodes:
            self.graph[nodes[key].index] = nodes[key]
        self.size = len(self.graph)
        if save:
            self.save(output)

