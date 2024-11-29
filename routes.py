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

from flask import Flask,request, jsonify, render_template
app = Flask(__name__)

from graph import Graph 
from api import API
from ford_fulkerson import FordFulkerson
from api import api_key
import asyncio


# STARTER GRAPH WITH CITIES AND CONNECTIONS
def initialize_graph():
    STARTER_GRAPH = Graph()
    STARTER_GRAPH.add_nodes(['BGA', 'BOG', 'MDE', 'CUC', 'BAC', 'EYP',
            'NVA', 'AXM', 'CRC', 'UIB', 'APO', 'MTR',
            'CTG'])
    # BGA
    STARTER_GRAPH.add_edge('BGA', 'BOG', 5)
    STARTER_GRAPH.add_edge('BGA', 'CUC', 5)
    STARTER_GRAPH.add_edge('BGA', 'CTG', 5)
    STARTER_GRAPH.add_edge('BGA', 'MDE', 5)
    # BOG
    STARTER_GRAPH.add_edge('BOG', 'EYP', 5)
    STARTER_GRAPH.add_edge('BOG', 'NVA', 5)
    STARTER_GRAPH.add_edge('BOG', 'MDE', 5)
    STARTER_GRAPH.add_edge('BOG', 'BAC', 5)
    STARTER_GRAPH.add_edge('BOG', 'AXM', 5)
    STARTER_GRAPH.add_edge('BOG', 'CRC', 5)
    STARTER_GRAPH.add_edge('BOG', 'UIB', 5)
    # MED
    STARTER_GRAPH.add_edge('MDE', 'NVA', 5)
    STARTER_GRAPH.add_edge('MDE', 'AXM', 5)
    STARTER_GRAPH.add_edge('MDE', 'UIB', 5)
    STARTER_GRAPH.add_edge('MDE', 'MTR', 5)
    STARTER_GRAPH.add_edge('MDE', 'APO', 5)
    STARTER_GRAPH.add_edge('MDE', 'CUC', 5)
    # CTG
    STARTER_GRAPH.add_edge('CTG', 'MDE', 5)
    STARTER_GRAPH.add_edge('CTG', 'MTR', 5)
    # AXM
    STARTER_GRAPH.add_edge('AXM', 'CRC', 5)
    # UIB
    STARTER_GRAPH.add_edge('UIB', 'APO', 5)

    return STARTER_GRAPH

api = API(api_key)
#report = asyncio.run(api.main())
#STARTER_GRAPH.update_availability(report)
#print('\nGRAPH UPDATED\n')
#print(STARTER_GRAPH)
#print()

#starting_node = 'BGA'
#ending_node ='NVA'
#method = FordFulkerson(STARTER_GRAPH, starting_node, ending_node)
#print(f"The maximum possible flow is {method.initiate()}")
#print(method.paths)

city_codes = {
    'Bucaramanga':'BGA', 
    'Bogotá':'BOG', 
    'Medellín':'MDE', 
    'Cúcuta':'CUC', 
    'Barrancabermeja':'BAC',
    'Yopal':'EYP', 
    'Neiva':'NVA', 
    'Armenia':'AXM', 
    'Cartago':'CRC', 
    'Quibdó':'UIB', 
    'Apartadó':'APO', 
    'Montería':'MTR', 
    'Cartagena':'CTG'
}

@app.route('/check_data', methods=['POST'])
def functionality():

     # Get data
     data = request.get_json()
     print(data)
     print(city_codes[data])
     # Run Api and Initialize new Graph
     report = asyncio.run(api.main())
     graph = initialize_graph()
     # Update graph based on API
     graph.update_availability(report)
     print(report) # Misiing climate implementation
        


     starting_node = 'BGA'
     ending_node = city_codes[data]

     method = FordFulkerson(graph, starting_node, ending_node)
     method.initiate()
     print(method.paths)

     return jsonify({'paths': method.paths, 'report':report})
@app.route('/', methods = ['GET'])
def render():
    return render_template('map.html')


if __name__ == '__main__':
    app.run(port = 8000, debug=True)
