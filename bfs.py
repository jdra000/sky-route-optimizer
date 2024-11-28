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