from bfs import BFS

class FordFulkerson():
    def __init__(self, graph, starting_node, ending_node):
        self.graph = graph
        self.starting_node = starting_node
        self.ending_node = ending_node
        self.paths = []
        
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

            self.paths.append(path +  list(str(path_flow)))

            # 5. Update current flow
            max_flow += path_flow

            # 6. Reset BFS and find another path
            bfs.reset() 
        return max_flow