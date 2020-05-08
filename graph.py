import json

class Node:
    def __init__(self):
        self.outlinks = None
        self.name = None
        self.url = None
        self.text = None
        self.index = None

class Graph:
    def __init__(self):
        self.nodes = []
        self.size = 0
        self.graph = dict()

        self.load()

    def __iter__(self):
        return iter(self.graph)

    def __getitem__(self, item):
        return self.graph[item]

    def load(self):
        files = []
        num = 0
        with open("graphScraper/sitegraph.json") as file :
            for line in file:
                j = json.loads(line)

                node = Node()
                node.url = j["url"]
                node.name = j["slug"]
                node.text = j["text"]
                node.outlinks = j["outlinks"]
                node.index = num

                self.nodes.append(node)
                files.append(j["slug"])

                num+=1

        self.size = len(files)

        for node in self.nodes:
            node.outlinks = [x for x in node.outlinks if x in files and x != node.name]

        for node in self.nodes:
            print(len(node.outlinks))
            self.graph[node.name] = node


        return self.graph
