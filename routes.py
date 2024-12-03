from graph import Graph 
from ford_fulkerson import FordFulkerson

# STARTER GRAPH WITH CITIES AND CONNECTIONS
def initialize_graph():
    graph = Graph()
    graph.add_nodes(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 
                     'L', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Z'])
    # BGA
    graph.add_edge('A', 'B', 4250)
    graph.add_edge('A', 'C', 1410)
    graph.add_edge('A', 'F', 4175)

    graph.add_edge('B', 'F', 2010)
    graph.add_edge('B', 'E', 3962)

    graph.add_edge('F', 'G', 5275)

    graph.add_edge('E', 'D', 4975)
    graph.add_edge('E', 'G', 2462)

    graph.add_edge('D', 'J', 3850)
    
    graph.add_edge('J', 'O', 4125)
    graph.add_edge('J', 'K', 4366)

    graph.add_edge('K', 'L', 4025)
    graph.add_edge('K', 'G', 4950)

    graph.add_edge('G', 'L', 4200)
    graph.add_edge('G', 'H', 2984)

    graph.add_edge('L', 'Q', 4300)

    graph.add_edge('O', 'P', 5933)
    graph.add_edge('O', 'S', 4983)

    graph.add_edge('P', 'Q', 4500)

    graph.add_edge('S', 'T', 5900)

    graph.add_edge('T', 'U', 1070)
    
    graph.add_edge('U', 'V', 1070)

    graph.add_edge('Q', 'U', 4300)

    graph.add_edge('H', 'I', 2984)
    graph.add_edge('H', 'R', 980)

    graph.add_edge('Q', 'R', 3525)

    graph.add_edge('R', 'W', 1170)

    graph.add_edge('W', 'N', 1370)
    graph.add_edge('W', 'X', 1170)

    graph.add_edge('V', 'W', 1370)
    graph.add_edge('V', 'X', 1070)

    graph.add_edge('I', 'N', 700)

    graph.add_edge('C', 'I', 215)

    graph.add_edge('X', 'Z', 1070)

    graph.add_edge('N', 'Z', 880)

    return graph

def functionality():
     # Initialize graph
     graph = initialize_graph()
     # Update graph based on API
        


     starting_node = 'A'
     ending_node = 'Z'
     
     method = FordFulkerson(graph, starting_node, ending_node)
     max_flow = method.initiate()
     print(method.paths)
     print(max_flow)

if __name__ == '__main__':
    functionality()
