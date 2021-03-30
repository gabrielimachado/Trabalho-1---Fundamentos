import random
import collections
import json
import csv

class Graph:
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def make_undirected(self):
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist

    def connect(self, A, B, distance=1):
        self.graph_dict.setdefault(A, {})[B] = distance
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = distance

    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values()
                  for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)

class Node:
    def __init__(self, name: str, parent: str):
        self.name = name
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return ('({0},{1})'.format(self.name, self.f))

def astar_search(graph, heuristics, start, end):

    open = []
    closed = []
    start_node = Node(start, None)
    goal_node = Node(end, None)
    # Add the start node
    open.append(start_node)

    while len(open) > 0:
        open.sort()
        current_node = open.pop(0)
        closed.append(current_node)

        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.name + ': ' + str(current_node.g))
                current_node = current_node.parent
            path.append(start_node.name + ': ' + str(start_node.g))
            return path[::-1]
        neighbors = graph.get(current_node.name)
        for key, value in neighbors.items():
            neighbor = Node(key, current_node)
            if(neighbor in closed):
                continue
            neighbor.g = current_node.g + \
                graph.get(current_node.name, neighbor.name)
            #neighbor.h = heuristics[neighbor.name]
            neighbor.f = neighbor.g + neighbor.h
            if(add_to_open(open, neighbor) == True):
                open.append(neighbor)
    return None


def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f > node.f):
            return False
    return True

def main():
    graph = Graph()

    #Carrega as cidades do arquivo JSON
    cidades = []
    with open('distancias.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data:  
            cidades = i.split(':')
            #Conecta as cidades baseando no separador ':', e a distância entre elas
            graph.connect(cidades[0], cidades[1], data[i])

    graph.make_undirected()
    heuristics = {}

    #Lê a cidade de saida e a de destino e executa a busca
    cidade_saida = ''
    cidade_destino = ''
    cidade_saida = input('Digite a cidade de saída: ')
    cidade_destino = input('Digite a cidade de destino: ')

    path = astar_search(graph, heuristics, cidade_saida, cidade_destino)
    print(path)
    print()


if __name__ == "__main__":
    main()
