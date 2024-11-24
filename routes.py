# AIRPORT CODES:
# BGA = BUCARAMANGA
# BOG = BOGOTA
# MDE = MEDELLIN
# CUC = CUCUTA
# BAC = BARRANCA
# EYP = YOPAL
# NVA = NEIVA
# AXM = ARMENIA
# CRC = CARTAGO
# UIB = QUIBDO
# APO = APARTADO
# MTR = MONTERIA
# CTG = CARTAGENA

NODES = ['BGA', 'BOG', 'MDE', 'CUC', 'BAC', 'EYP'
         'NVA', 'AXM', 'CRC', 'UIB', 'APO', 'MTR'
         'CTG']

class Graph():

    def __init__(self):
        self.representation ={}
  
    def add_nodes(self, nodes):
        for node in nodes:
            self.representation[node] = {}
     
    def add_edge(self, tail, head, weight = None):
        self.representation[tail][head] = weight

    def create_residual_graph(self, path):
        path_flow = float('Inf')
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            path_flow = min(self.representation[u][v], path_flow)
        return path_flow
    
    def update_residual_graph(self, path, flow):
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            self.representation[u][v] -= flow
            if u not in self.representation[v]:
                self.representation[v][u] = 0
            self.representation[v][u] += flow

    def __repr__(self):
        return str(self.representation)
    


from collections import deque

class BFS():
    def __init__(self, graph, starting_node, ending_node):
        self.graph = graph
        self.starting_node = starting_node
        self.ending_node = ending_node

        self.path_reconstructed = []
        self.visited = {node: False for node in self.graph}
        self.parent = {node: None for node in self.graph}
    
    def initiate(self):
        queue = deque()

        queue.append(self.starting_node)
        self.visited[self.starting_node] = True

        while queue:
            m = queue.popleft()

            for neighbour, weight in self.graph[m].items():
                if not self.visited[neighbour] and weight > 0:
                    queue.append(neighbour)
                    self.visited[neighbour] = True
                    self.parent[neighbour] = m
                    if neighbour == self.ending_node:
                        return True
        return False

    def reconstruct_path(self):
        e = self.ending_node

        while e is not None:
            self.path_reconstructed.append(e)
            e = self.parent[e]
        return self.path_reconstructed[::-1]

    def reset(self):
        self.path_reconstructed = []
        self.visited = {node: False for node in self.graph}
        self.parent = {node: None for node in self.graph}
    

class FordFulkerson():
    def __init__(self, graph, starting_node, ending_node):
        self.graph = graph
        self.starting_node = starting_node
        self.ending_node = ending_node
        
    def initiate(self):
        # 1. Initialize flow to 0
        max_flow = 0

        # 2. Find a path
        bfs = BFS(self.graph.representation, self.starting_node, self.ending_node)

        # 3. While path exists
        while bfs.initiate():
            
            path = bfs.reconstruct_path()

            # 4. create residual graph and update it
            path_flow = self.graph.create_residual_graph(path)
            self.graph.update_residual_graph(path, path_flow)

            print(path + list(str(path_flow)))

            # 5. Update current flow
            max_flow += path_flow

            # 6. Reset BFS and find another path
            bfs.reset() 
        return max_flow

graph = Graph()
graph.add_nodes(['S', 'A', 'C', 'B', 'D', 'T'])
graph.add_edge('S', 'A', 4)
graph.add_edge('S', 'C', 3)
graph.add_edge('A', 'B', 4)
graph.add_edge('B', 'C', 3)
graph.add_edge('B', 'T', 2)
graph.add_edge('C', 'D', 6)
graph.add_edge('D', 'T', 6)

starting_node = 'S'
ending_node = 'T'
method = FordFulkerson(graph, starting_node, ending_node)

print(f"The maximum possible flow is {method.initiate()}")