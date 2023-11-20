import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from map_utilities import *

class LUT:
    def __init__(self, lut_id, lut_type):
        self.lut_id = lut_id          # Unique ID assosiciated with this LUT only
        self.lut_type = lut_type      # Number of inputs into LUT, either 4 or 6
        self.is_available = True      # True if LUT can have function mapped to it, false if function is already mapped
        self.function = None          # Function mapped to the LUT in onehot format

    def map_function (self, function_onehot):
        '''
        Maps a function to the LUT

        function_onehot: one-hot list of length 2**lut_type. The truth table for function
        '''
        self.function = function_onehot

class FPGA:
    def __init__(self, num_inputs=4, num_outputs=4, num_luts=8, lut_type=4, input_connectionmat=None, lut_connectionmat=None):
        self.num_inputs = num_inputs    # Number of inputs on this FPGA
        self.num_outputs = num_outputs  # Number of outputs on this FPGA
        self.num_luts = num_luts        # Number of LUTs in this FPGA
        self.lut_type = lut_type        # Type of LUTs (4-input or 6-input)

        ## Initialize input connection matrix
        if input_connectionmat != None:
            self.input_connectionmat = input_connectionmat
        else:
            self.input_connectionmat = self.make_ip_connectionmat()

        ## Initialize LUT connection matrix
        if lut_connectionmat != None:
            self.lut_connectionmat = lut_connectionmat
        else:
            self.lut_connectionmat = self.make_lut_connectionmat()

        ## Initialize LUTs
        self.lut_list = self.init_LUTs()

        ## Initialize FPGA graphs
        self.graph = self.init_graph()          ## Constant graph
        self.availability_graph = self.graph    ## Availability graph - nodes get removed as functions are mapped

    def make_ip_connectionmat(self):
        '''
        Generates connection matrix for inputs - assumes that all inputs are connected
        to all LUTs and all outputs
        '''
        return np.ones((self.num_inputs, self.num_luts+self.num_outputs), dtype=int)

    def make_lut_connectionmat(self):
        '''
        Generates connection matrix for LUTs - assumes that all LUTs are connected
        to all other LUTs and all outputs
        '''
        return np.ones((self.num_luts, self.num_luts+self.num_outputs), dtype=int)

    def init_LUTs(self):
        '''
        Instantiates num_luts instances of LUT class, returns list of LUTs
        '''
        lut_list = []
        for lut_id in range(self.num_luts):
            lut_list.append(LUT(lut_id=lut_id, lut_type=self.lut_type))
        return lut_list

    def init_graph(self):
        '''
        Initializes graph of FPGA using connections defined in the connection matrices
            - networkx library handles graph structure and all graph-related operations
        '''
        graph = nx.DiGraph()

        ## Add input nodes
        for i in range(self.num_inputs):
            graph.add_node(f'IN{i}', type="input", id=i)

        ## Add output nodes
        for i in range(self.num_outputs):
            graph.add_node(f'OUT{i}', type="output", id=i)

        ## Add LUT nodes
        for i in range(self.num_luts):
            graph.add_node(f'LUT{i}', type="LUT", id=i)

        ## Connect inputs to LUTs and outputs according to input_connectionmat
        for i in range(self.num_inputs):
            for j in range(self.num_luts):
                if self.input_connectionmat[i][j] == 1:
                    graph.add_edge(f'IN{i}', f'LUT{j}')
            for j in (range(self.num_luts, self.num_luts+self.num_outputs)):
                if self.input_connectionmat[i][j] == 1:
                    graph.add_edge(f'IN{i}', f'OUT{j-self.num_luts}')

        ## Connect LUTs to other LUTs and to outputs according to lut_connectionmat
        for i in range(self.num_luts):
            for j in range(self.num_luts):
                if self.lut_connectionmat[i][j] == 1:
                    graph.add_edge(f'LUT{i}', f'LUT{j}')
            for j in (range(self.num_luts, self.num_luts+self.num_outputs)):
                if self.lut_connectionmat[i][j] == 1:
                    graph.add_edge(f'LUT{i}', f'OUT{j-self.num_luts}')

        nx.draw(graph, with_labels=True, font_weight='bold', node_color='skyblue', node_size=800, font_size=8, arrowsize=15)
        plt.show()

        return graph

    def map_function(self, fn_bstring, inputs, output):
        '''
        Maps a boolean logic expression to the FPGA

        fn_bstring: function in bstring format: ['10-0', '1--0', '1011']
        '''
        
        ## Convert function to graph
        fn_graph = to_graph(fn_bstring)

        ## Check if function can be mapped to FPGA - checking if subgraph exists in larger graph
        node_match = lambda node1, node2: node1 == node2 
        matcher = nx.algorithms.isomorphism.GraphMatcher(self.availability_graph, fn_graph, node_match=node_match)

        if matcher.subgraph_is_isomorphic():
            matched_nodes = matcher.mapping

            for node, _ in matched_nodes.items():
                if node.type == "LUT"
                    self.lut_list[node.id].is_available = False
                    self.availability_graph.remove_node(node)
                    
            return True
        else:
            return False














