import networkx as nx
import networkx.algorithms.isomorphism as iso
import matplotlib.pyplot as plt
import numpy as np
import copy
from map_utilities import *

class LUT:
    def __init__(self, lut_id, lut_type):
        self.lut_id = lut_id          # Unique ID assosiciated with this LUT only
        self.lut_type = lut_type      # Number of inputs into LUT, either 4 or 6
        self.is_available = True      # True if LUT can have function mapped to it, false if function is already mapped
        self.inputs = None            # Inputs into the LUT
        self.function = None          # Function mapped to the LUT in onehot format
        self.local_values=None        # Used for run_input()

    def map_function (self, inputs, function_onehot):
        '''
        Maps a function to the LUT

        function_onehot: one-hot list of length 2**lut_type. The truth table for function
        '''
        self.inputs = inputs
        self.local_values = [0] * len(self.inputs)
        self.function = function_onehot
        self.is_available = False

class FPGA:
    def __init__(self, num_inputs=4, num_outputs=4, num_luts=8, lut_type=4, input_connectionmat=None, lut_connectionmat=None):
        self.num_inputs = num_inputs    # Number of inputs on this FPGA
        self.num_outputs = num_outputs  # Number of outputs on this FPGA
        self.num_luts = num_luts        # Number of LUTs in this FPGA
        self.num_luts_inuse = 0         # Number of LUTs that aren't available
        self.lut_type = lut_type        # Type of LUTs (4-input or 6-input)
        self.input_names = {}           # Dictionary to store mappings between input variable names and internal names (IN0, IN1,...)
        self.output_names = {}          # Dictionary to store mappings between output variable names and internal names (OUT0,...)

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

        ## Initialize input_names
        for i in range(self.num_inputs):
            self.input_names[f'IN{i}'] = None

        ## Initialize output_names
        for i in range(self.num_outputs):
            self.output_names[f'OUT{i}'] = None

        ## Initialize FPGA graphs
        self.graph = self.init_graph()                         ## Constant graph
        self.availability_graph = copy.deepcopy(self.graph)    ## Availability graph - nodes get removed as functions are mapped

        # print(self.input_connectionmat)
        # print(self.lut_connectionmat)

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

    def init_variables(self, input_name_list, output_name_list):
        '''
        Define mapping of external names to internal names
        '''
        ## Inputs
        for i in range(min(self.num_inputs, len(input_name_list))):
            self.input_names[f'IN{i}'] = input_name_list[i]

        ## Initialize output_names
        for i in range(min(self.num_outputs, len(output_name_list))):
            self.output_names[f'OUT{i}'] = output_name_list[i]

    def find_internal_names(self, input_names_list, output_names_list):
        '''
        Returns internal names of external variables stored in input_names_list and output_names_list
        '''
        ip_list = []
        op_list = []

        for internal, external in self.input_names.items():
            if internal is None or external is None:
                continue
            for var in input_names_list:
                if var in external and internal is not None and external is not None:
                    index = external.index(var)
                    ip_list.append(internal)

        for internal, external in self.output_names.items():
            if internal is None or external is None:
                continue
            for var in output_names_list:
                if var in external and internal is not None and external is not None:
                    index = external.index(var)
                    op_list.append(internal)

        return ip_list, op_list


    def init_graph(self):
        '''
        Initializes graph of FPGA using connections defined in the connection matrices
            - networkx library handles graph structure and all graph-related operations
        '''
        graph = nx.DiGraph()

        ## Add input nodes
        for i in range(self.num_inputs):
            # print (f'IN{i} added')
            graph.add_node(f'IN{i}', type="input", id=i, value=None)

        ## Add output nodes
        for i in range(self.num_outputs):
            # print (f'OUT{i} added')
            graph.add_node(f'OUT{i}', type="output", id=i, value=None, lut_assignment=None)

        ## Add LUT nodes
        for i in range(self.num_luts):
            # print(f'LUT{i} added')
            graph.add_node(f'LUT{i}', type="LUT", id=i, value=None, struct=self.lut_list[i])  ## Function gets mapped later!

        ## Connect inputs to LUTs and outputs according to input_connectionmat
        for i in range(self.num_inputs):
            for j in range(self.num_luts):
                if self.input_connectionmat[i][j] == 1:
                    # print(f'adding edge from IN{i} to LUT{j}')
                    graph.add_edge(f'IN{i}', f'LUT{j}')
            for j in (range(self.num_luts, self.num_luts+self.num_outputs)):
                if self.input_connectionmat[i][j] == 1:
                    # print(f'adding edge from IN{i} to OUT{j-self.num_luts}')
                    graph.add_edge(f'IN{i}', f'OUT{j-self.num_luts}')

        ## Connect LUTs to other LUTs and to outputs according to lut_connectionmat
        for i in range(self.num_luts):
            for j in range(self.num_luts):
                if self.lut_connectionmat[i][j] == 1:
                    # print(f'adding edge from LUT{i} to LUT{j}')
                    graph.add_edge(f'LUT{i}', f'LUT{j}')
            for j in (range(self.num_luts, self.num_luts+self.num_outputs)):
                if self.lut_connectionmat[i][j] == 1:
                    # print(f'adding edge from LUT{i} to OUT{j-self.num_luts}')
                    graph.add_edge(f'LUT{i}', f'OUT{j-self.num_luts}')

        # nx.draw(graph, with_labels=True, font_weight='bold', node_color='skyblue', node_size=800, font_size=8, arrowsize=15)
        # plt.show()
        # print(graph.nodes)

        return graph

    def map_function(self, fn_bstring, input_name_list, output_name):
        '''
        Maps a boolean logic expression to the FPGA

        fn_bstring: function in bstring format: ['10-0', '1--0', '1011']
        '''

        ## Get internal mappings for input and output names
        _, ops = self.find_internal_names(input_name_list, [output_name])

        ## If ops is none, return False
        if not ops:
            ops = ['XXXX']
            # print(f"\033[91mmap_function: Failed to map function {output_name} to FPGA - no more output nodes available\033[0m")
            # return False
        
        ## Get LUT mappings and graph of function
        fn_dict, fn_graph, output_lut = fn_make_packet(fn_bstring, self.lut_type, self.num_inputs, ops[0])

        ## Helper function for DiGraphMatcher(), defines when nodes should be considered equal
        def node_match (node1, node2):  
            if node1['type'] == node2['type']:
                if node1['type'] == 'LUT':
                    return True
                elif int(node1['id']) == int(node2['id']):
                    return True
            return False

        # isos = list(iso.DiGraphMatcher(self.availability_graph, fn_graph,node_match=node_match).subgraph_monomorphisms_iter())
        isos = next(iso.DiGraphMatcher(self.availability_graph, fn_graph, node_match=node_match).subgraph_monomorphisms_iter(), None)

        ## Remove mapped LUT and output nodes from availability_graph
        if isos != None:
            ## Get list of all nodes that are being mapped 
            # mapped_nodes = isos[0].keys()
            mapped_nodes = isos

            ## List of nodes to be removed
            to_be_removed = []
            for node in mapped_nodes:
                if node[:2] != 'IN':
                    to_be_removed.append(node)

            ## Remove mapped nodes from availability graph
            self.availability_graph.remove_nodes_from(to_be_removed)

            # print(f"Nodes {to_be_removed} have been mapped and removed from the availability_graph.")
        else:
            print(f"\033[91mmap_function: Failed to map function {output_name} to FPGA\033[0m")
            return False

        ## Map to LUTs
        for fpga_node, fn_node in isos.items():
            if fn_node[:3] == 'LUT':
                lut_inputs = [key for key, value in isos.items() if any(element in value for element in fn_dict[fn_node]['inputs'])]
                idx = int(fpga_node[3:])
                self.lut_list[idx].map_function(lut_inputs, fn_dict[fn_node]['truth_table'])
                self.num_luts_inuse += 1


                if fn_node == output_lut:
                    out_node = [key for key in mapped_nodes.keys() if key[:3] == 'OUT'][0]
                    self.graph.nodes[out_node]['lut_assignment'] = fpga_node
                    # print(fpga_node)


    def run_input(self, input_vec):
        '''
        Evaluates the current FPGA mapping for the inputs in input_vec
        '''
        output_return_dict={}

        def evaluate_LUT(lut_struct, input_val_dict):
            ## Recursive helper function to get value of LUTs
            for i, ip in enumerate(lut_struct.inputs):
                if ip[:3] == 'LUT':
                    lut_struct.local_values[i] = evaluate_LUT(self.lut_list[int(ip[3:])], input_val_dict)
                else:
                    lut_struct.local_values[i] = input_val_dict[ip]
            idx = int(''.join(map(str, lut_struct.local_values)), 2)
            return lut_struct.function[idx]


        if len(input_vec) < self.num_inputs:
            print(f"\033[91mrun_input: Not enough inputs provided - aborting\033[0m")
            return False

        ## Create dictionary of input nodes
        input_val_dict = {}
        for i in range(self.num_inputs):
            input_val_dict[f'IN{i}'] = input_vec[i]

        for node, data in self.graph.nodes(data=True):
            if data['type'] == 'output':
                if data['lut_assignment'] != None:
                    lut_struct = self.graph.nodes[data['lut_assignment']]['struct']
                    output_return_dict[self.output_names[node]] = evaluate_LUT(lut_struct, input_val_dict)

        return output_return_dict

    def get_bitstream(self):
        '''
        Returns a bitstream that represents the current internal state of the FPGA
        '''
        pass
        

    def load_from_bitstream(self, bitstream):
        '''
        Sets the internal state of the FPGA based on data in the bitstream
        '''
        # Reset the FPGA to its initial state
        pass


    def print_info(self):
        '''
        Prints general info on FPGA
        '''
        print("\033[1mFPGA INFORMATION\033[0m")
        print(f"Number of LUTs: \033[94m{self.num_luts}\033[0m")
        print(f"Inputs per LUT: \033[94m{self.lut_type}\033[0m")
        print(f"Number of Inputs to FPGA: \033[94m{self.num_inputs}\033[0m")
        print(f"Number of Outputs from FPGA: \033[94m{self.num_outputs}\033[0m")
        print(f"Input Variable Mappings: \033[94m{self.input_names}\033[0m")
        print(f"Output Variable Mappings: \033[94m{self.output_names}\033[0m")
        print(f"Possible Connections between inputs and LUTs/outputs: \n\033[94m{self.input_connectionmat}\033[0m")
        print(f"Possible Connections between LUTs and other LUTs/outputs: \n\033[94m{self.lut_connectionmat}\033[0m")

        print("\n\033[1mFPGA LUTS INFORMATION\033[0m")
        print(f"\033[1mLUT usage: {round(self.num_luts_inuse / self.num_luts * 100,2)}%\n\033[0m")
        for lut in self.lut_list:
            print(f"\033[1mLUT ID: {lut.lut_id}\033[0m")
            print(f"Number of Inputs: \033[94m{lut.lut_type}\033[0m")
            print(f"LUT inputs: \033[94m{lut.inputs}\033[0m")
            print(f"Is Available?: \033[94m{lut.is_available}\033[0m")
            print(f"Mapped Function: \033[94m{lut.function}\033[0m\n")

        print("\n\033[1mFPGA OUTPUT NODES\033[0m")
        for node, data in self.graph.nodes(data=True):
            if data['type'] == 'output':
                print(f"\033[1mOutput Node: {node}\033[0m")
                print(f"LUT Assignment: \033[94m{data['lut_assignment']}\033[0m\n")














