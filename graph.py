import json


class Node:
    def __init__(self):
        self.name = None
        self.outlinks = None
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

    def load(self):
        nodes = dict()
        with open("graphScraper/sitegraph.json") as file:
            for index, line in enumerate(file):
                j = json.loads(line)

                node = Node()
                node.name = j["slug"]
                node.title = j["title"]
                node.url = j["url"]
                node.text = j["text"]
                node.outlinks = j["outlinks"]
                node.index = index

                nodes[node.name] = node
        self.size = len(nodes)

        # clean outlinks from unexisting pages and change the slugs to indexes.
        for key in nodes:
            nodes[key].outlinks = [nodes[x].index for x in nodes[key].outlinks if
                                   x in nodes.keys() and x != nodes[key].name]

        for key in nodes:
            self.graph[nodes[key].index] = nodes[key]
