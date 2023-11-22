'''
A collection of helper functions for mapping a logic 
expression to FPGA

Overall workflow:
1. Read function from .pla file
2. Minimize function
3. Find number of literals of minimized expression (1)
4. 

Things to check before mapping:
1. Which inputs can go where
'''
import networkx as nx

def tt_onehot (fn_bstring):
    '''
    Converts a function in bstring format to its one-hot truth table

    Input: 
        fn_bstring: a list of bstrings representing a boolean expression (['1-01', '-11-'])
    '''
    num_literals, literal_list = literal_count_fn(fn_bstring) ## Number of literals in fn_bstring
    truth_tab_onehot = [0] * 2**num_literals

    for binary_str in fn_bstring:

        temp_bstring = ''.join(char for char, flag in zip(binary_str, literal_list) if flag == 1)
        combinations = expand_term(temp_bstring)

        for bstring in combinations:
            truth_tab_onehot[int(bstring,2)] = 1

    return truth_tab_onehot

def tt_and (length):
    ## Returns truth table for AND gate
    tt = [0] * (2**length - 1)
    tt.append(1)
    return tt

def tt_or (length):
    ## Returns truth table for OR gate
    tt = [1] * 2**length
    tt[0] = 0
    return tt

def expand_term (bstring_term):
    '''
    Expands a bstring term with don't cares ('1-0')to a list of terms covered by it (['100', '110'])
    '''
    if '-' not in bstring_term:
        return [bstring_term]

    index = bstring_term.index('-')
    return (
        expand_term(bstring_term[:index] + '0' + bstring_term[index + 1:]) +
        expand_term(bstring_term[:index] + '1' + bstring_term[index + 1:])
    )


def literal_count_fn (fn_bstring):
    '''
    Calculates number of literals in fn_bstring

    Input: 
        fn_bstring: a list of bstrings representing a boolean expression (['1-01', '-11-'])
    '''
    literal_list = [0] * len(fn_bstring[0])

    for term in fn_bstring:
        for i, literal in enumerate(term):
            if literal == '0' or literal == '1' and literal_list[i] == 0:
                literal_list[i] = 1

    return sum(literal_list), literal_list



def literal_count_term (bstring_term):
    '''
    Calculates number of literals in a single bstring term ('1-01')
    '''
    return sum(1 for char in bstring_term if char.isalnum() and char != '-')



def to_graph (lut_assignments, fn_bstring, output_lut, output_name, lut_type):
    '''
    Generates a graph for a boolean logic expression

    fn_bstring: function in bstring format: ['10-0', '1--0', '1011']
    lut_type: Number of inputs available to a LUT
    '''
    ## Initialize directed graph
    graph = nx.DiGraph()

    ## Add nodes for inputs
    literal_count, literal_list = literal_count_fn(fn_bstring)

    ## Add nodes/edges for LUTs
    for idx, ip in enumerate(literal_list):
        if ip == 1:
            graph.add_node(f'IN{idx}', type='input', id=idx)
    
    for idx, (lut_name, data) in enumerate(lut_assignments.items()):
        graph.add_node(lut_name, type='LUT', id=idx)

        for ip in data['inputs']:
            graph.add_edge(ip, lut_name)

    ## Add node/edges for output
    graph.add_node(output_name, type='output', id=output_name[3])
    graph.add_edge(output_lut, output_name)

    return graph


def input_to_lut_partition (fn_bstring, lut_type):
    '''
    Splits a function into subterms, each with num_literals <= lut_type

    Inputs:
        fn_bstring: a list of bstrings representing a boolean expression (['1-01', '-11-'])
        lut_type: Number of inputs available to a LUT
        
    output:
        dictionary LUTs     - key value mapping (adjcency list) of primary inputs to LUTs and LUTs to LUTs; covering partitioning
        int lutCount        - number of required number of LUTs for this configuration
    '''

    LUTs = {}
    ip_queue = []
    bstring_queue = []
    lut_queue = []
    mt_lut_list = []
    lutCount = 0
    fn_output_lut = None    ## LUT corresponding to function's output

    ## Generate input list
    inputs=[]
    # num_literals = literal_count_fn(fn_bstring)[0]
    num_literals = len(fn_bstring[0])
    for i in range(num_literals):
        inputs.append(f'IN{i}')


    for term in fn_bstring:
        mt_output_lut = None    ## The output of this specific minterm

        # decode to primary inputs
        for i, literal in enumerate(term):
            if literal == '0':
                ip_queue.append(inputs[i])#+'\'')
                bstring_queue.append(literal)
            elif literal == '1':
                ip_queue.append(inputs[i])
                bstring_queue.append(literal)

        while len(ip_queue) > 0:
            if not LUTs.get('LUT'+str(lutCount), 0):
                LUTs['LUT'+str(lutCount)] = {} 
                temp_list = []
                temp_bstring_list=[]

            counter = 0
            while len(ip_queue) > 0 and counter < lut_type:
                temp_list.append(ip_queue.pop(0))
                temp_bstring_list.append(bstring_queue.pop(0))

                counter += 1  

            bstring = [''.join(map(str, temp_bstring_list[:counter]))]

            LUTs['LUT'+str(lutCount)] = {'inputs':temp_list, 'truth_table':tt_onehot(bstring)}
            lut_queue.append('LUT'+str(lutCount))
            mt_output_lut = 'LUT'+str(lutCount)
            fn_output_lut = 'LUT'+str(lutCount)

            if len(ip_queue) > 0:
                ip_queue.append('LUT'+str(lutCount))
                bstring_queue.append(1)
            
            lutCount += 1
       
        mt_lut_list.append(mt_output_lut)  ## Add the LUT representing this particular minterm

    ## OR all the minterms together
    queue = []
    bstring_queue = []

    for k in mt_lut_list:
        queue.append(k)
    
    if len(queue) > 1:
        while len(queue) > 0:
            if not LUTs.get('LUT'+str(lutCount), 0):
                LUTs['LUT'+str(lutCount)] = {}
                temp_list = []

            counter = 0
            while len(queue) > 0 and counter < lut_type:
                temp_list.append(queue.pop(0))
                counter += 1
            LUTs['LUT'+str(lutCount)] = {'inputs':temp_list, 'truth_table':tt_or(len(temp_list))}
            fn_output_lut = 'LUT'+str(lutCount)     ## In case of multiple minterms, this LUT will be output of the function

            if len(queue) > 0:
                queue.append('LUT'+str(lutCount))

            lutCount += 1

    return LUTs, lutCount, fn_output_lut

def split_function(fn_bstring, lut_type):
    '''
    Splits a function fn_bstring so that it can be mapped to FPGA
    
    Returns a tuple with following data:
        lut_assignments: a dictionary of dictionaries describing LUT mappings:
            {LUT0: {inputs=['IN1','IN2'],
                    truth_table=[0,1,0,0]}.
             LUT1: {"
                                        "}
            }
        
        lut_count: number of LUTs reqired for this expression
        output_lut: which LUT is the output of this expression
    '''
    lut_assignments = {}

    ## Get number of literals, and literal list
    literal_count, literal_list = literal_count_fn(fn_bstring)

    # If function has fewer than lut_type literals, generate truth table and return
    if literal_count <= lut_type:
        lut_assignments['LUT0'] = {'inputs': list_to_inputs(literal_list), 'truth_table': tt_onehot(fn_bstring)}
        lut_count=1
        output_lut='LUT0'
    else:
        lut_assignments, lut_count, output_lut = input_to_lut_partition(fn_bstring, lut_type)

    return lut_assignments, lut_count, output_lut



def list_to_inputs(literal_list):
    '''
    Converts the one-hot literal_list to a list of input names 
    Example: [1,1,0,0] -> ['IN0', 'IN1']
    '''
    input_names = []
    for idx, i in enumerate(literal_list):
        if i == 1:
            input_names.append(f'IN{idx}')

    return input_names



def fn_make_packet (fn_bstring, lut_type, fpga_num_inputs, output_name):
    '''
    Master function to convert fn_bstring into mappable function

    1. Does some error checking: Number of inputs to function, valid format, etc.
    2. Calls input_to_lut_partition() to split fn_bstring into smaller pieces
    3. Calls tt_onehot() to generate truth table for each of the smaller pieces
    4. Calls to_graph() to create graph of the function
    5. Returns data structure containing all of this
    '''

    ## Get number of literals, and literal list
    literal_count, literal_list = literal_count_fn(fn_bstring)

    ## Error check
    if literal_count > fpga_num_inputs:
        print("Function cannot be mapped; too many inputs")
        return False

    ## Split function
    lut_assignments, lut_count, output_lut = split_function(fn_bstring, lut_type)

    ## Get function graph
    fn_graph = to_graph(lut_assignments, fn_bstring, output_lut, output_name, lut_type)

    ## Eventually, this should return a tuple of (fn_dict, fn_graph)
    return lut_assignments, fn_graph, output_lut


































