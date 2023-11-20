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

        print(self.input_connectionmat)
        print(self.lut_connectionmat)

        # print("Graph nodes:", self.graph.nodes)
        # print("Graph edges:", self.graph.edges)

        # print("availability_graph nodes:", self.availability_graph.nodes)
        # print("availability_graph edges:", self.availability_graph.edges)

    def make_ip_connectionmat(self):
        '''
        Generates connection matrix for inputs - assumes that all inputs are connected
        to all LUTs and all outputs
        '''

        connection_mat = np.ones((self.num_inputs, self.num_luts + self.num_outputs), dtype=int)
        # np.fill_diagonal(connection_mat, 0)  # Set diagonal elements to 0
        return connection_mat

    def make_lut_connectionmat(self):
        '''
        Generates connection matrix for LUTs - assumes that all LUTs are connected
        to all other LUTs and all outputs
        '''
        connection_mat = np.ones((self.num_luts, self.num_luts + self.num_outputs), dtype=int)
        np.fill_diagonal(connection_mat, 0)  # Set diagonal elements to 0
        return connection_mat

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
            print (f'IN{i} added')
            graph.add_node(f'IN{i}', type="input", id=i)

        ## Add output nodes
        for i in range(self.num_outputs):
            print (f'OUT{i} added')
            graph.add_node(f'OUT{i}', type="output", id=i)

        ## Add LUT nodes
        for i in range(self.num_luts):
            print(f'LUT{i} added')
            graph.add_node(f'LUT{i}', type="LUT", id=i)

        ## Connect inputs to LUTs and outputs according to input_connectionmat
        for i in range(self.num_inputs):
            for j in range(self.num_luts):
                if self.input_connectionmat[i][j] == 1:
                    print(f'adding edge from IN{i} to LUT{j}')
                    graph.add_edge(f'IN{i}', f'LUT{j}')
            for j in (range(self.num_luts, self.num_luts+self.num_outputs)):
                if self.input_connectionmat[i][j] == 1:
                    print(f'adding edge from IN{i} to OUT{j-self.num_luts}')
                    graph.add_edge(f'IN{i}', f'OUT{j-self.num_luts}')

        ## Connect LUTs to other LUTs and to outputs according to lut_connectionmat
        for i in range(self.num_luts):
            for j in range(self.num_luts):
                if self.lut_connectionmat[i][j] == 1:
                    print(f'adding edge from LUT{i} to LUT{j}')
                    graph.add_edge(f'LUT{i}', f'LUT{j}')
            for j in (range(self.num_luts, self.num_luts+self.num_outputs)):
                if self.lut_connectionmat[i][j] == 1:
                    print(f'adding edge from LUT{i} to OUT{j-self.num_luts}')
                    graph.add_edge(f'LUT{i}', f'OUT{j-self.num_luts}')


        # nx.draw(graph, with_labels=True, font_weight='bold', node_color='skyblue', node_size=800, font_size=8, arrowsize=15)
        # plt.show()

        return graph

    # def map_function(self, fn_bstring, inputs, output):
    def map_function(self):
        '''
        Maps a boolean logic expression to the FPGA

        fn_bstring: function in bstring format: ['10-0', '1--0', '1011']
        '''
        fn_bstring = ['000']
        ## Convert function to graph
        fn_graph = to_graph(fn_bstring)

        print(fn_graph.edges)

        # graph = nx.DiGraph()
        # graph.add_node(f'IN{0}', type="input", id=0)
        # graph.add_node(f'IN{1}', type="input", id=1)
        # graph.add_node(f'IN{2}', type="input", id=2)

        # graph.add_node(f'OUT{1}', type="output", id=1)

        # graph.add_node(f'LUT{0}', type="LUT", id=0)
        # graph.add_node(f'LUT{1}', type="LUT", id=1)
        # graph.add_node(f'LUT{2}', type="LUT", id=2)

        # graph.add_edge(f'IN{0}', f'LUT{0}')
        # graph.add_edge(f'IN{0}', f'LUT{1}')
        # graph.add_edge(f'IN{1}', f'LUT{0}')
        # graph.add_edge(f'IN{1}', f'LUT{1}')
        # graph.add_edge(f'IN{2}', f'LUT{0}')
        # graph.add_edge(f'IN{2}', f'LUT{1}')

        # graph.add_edge(f'LUT{0}', f'LUT{2}')
        # graph.add_edge(f'LUT{1}', f'LUT{2}')

        # graph.add_edge(f'LUT{2}', f'OUT{1}')

        # print(fn_graph.nodes)
        # for edge in fn_graph.nodes:
        #     print(edge)
        # print(" ")
        # # print(self.availability_graph.nodes)
        # for edge in self.availability_graph.nodes:
        #     print (edge)
        # print(self.availability_graph.nodes['IN0']['id'])
        # print(self.availability_graph.nodes['IN0'] == fn_graph.nodes['IN0'])

        ## Check if function can be mapped to FPGA - checking if subgraph exists in larger graph
        def node_match (node1, node2): 
            print(node1, node2, node1['type'] == node2['type'] and node1['id'] == node2['id'])
            return node1['type'] == node2['type'] and node1['id'] == node2['id'] 
        def edge_match (edge1, edge2):
            print("edge1, edge2, edge1==edge2")
            return edge1==edge2

        matcher = nx.algorithms.isomorphism.GraphMatcher(fn_graph, self.availability_graph, node_match=node_match, edge_match=edge_match)

        if matcher.subgraph_is_isomorphic():
            matched_nodes = matcher.mapping
            nodes_to_remove = [larger_node for larger_node, _ in matched_nodes.items()]
            self.availability_graph.remove_nodes_from(nodes_to_remove)
            return True
        else:
            return False
        # matcher = nx.isomorphism.DiGraphMatcher(self.availability_graph, fn_graph, node_match=node_match, edge_match=edge_match)

        # matcher.subgraph_is_isomorphic()
        # print(matcher.mapping)
        # if matcher.subgraph_is_isomorphic():
        #     print("Found isomorphic subgraph.")
        #     matched_nodes = matcher.mapping

        #     for node, _ in matched_nodes.items():
        #         if node['type'] == "LUT":
        #             nodes_to_remove = [larger_node for larger_node in larger_dag.nodes if larger_node['type'] == node['type'] and larger_node['id'] == node['id']]
        #             larger_dag.remove_nodes_from(nodes_to_remove)

        #     return True
        # else:
        #     return False














