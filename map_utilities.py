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



def to_graph (fn_bstring, lut_type):
    '''
    Generates a graph for a boolean logic expression

    fn_bstring: function in bstring format: ['10-0', '1--0', '1011']
    lut_type: Number of inputs available to a LUT
    '''
    ## Initialize directed graph
    graph = nx.DiGraph()

    ## Add nodes for inputs
    literal_count, literal_list = literal_count_fn(fn_bstring)

    for idx, ip in enumerate(literal_list):
        if ip == 1:
            graph.add_node(f'IN{idx}', type='input', id=idx)
    
    if literal_count <= lut_type:
        graph.add_node(f'LUT{0}', type='LUT', id=0)
        graph.add_node(f'OUT{0}', type='output', id=0)

    # print(input_to_lut_partition(fn_bstring, lut_type=4))

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
    print('expression:', fn_bstring)

    LUTs = {}
    queue = []
    lutCount = 0

    ## Generate input list
    inputs=[]
    num_literals = literal_count_fn(fn_bstring)[0]
    for i in range(num_literals):
        inputs.append(f'IN{i}')


    for term in fn_bstring:
        # decode to primary inputs
        for i, literal in enumerate(term):
            if literal == '0':
                queue.append(inputs[i]+'\'')
            elif literal == '1':
                queue.append(inputs[i])

        print("queue", queue)

        while len(queue) > 0:
            if not LUTs.get('LUT'+str(lutCount), 0):
                LUTs['LUT'+str(lutCount)] = []

            counter = 0
            while len(queue) > 0 and counter < lut_type:
                LUTs['LUT'+str(lutCount)].append(queue.pop(0)) 
                counter += 1  

            if len(queue) > 0:
                queue.append('LUT'+str(lutCount))
            
            lutCount += 1
    
    queue = []
    for k in LUTs.keys():
        queue.append(k)
    
    while len(queue) > 0:
        if not LUTs.get('LUT'+str(lutCount), 0):
            LUTs['LUT'+str(lutCount)] = []

        counter = 0
        while len(queue) > 0 and counter < lut_type:
            LUTs['LUT'+str(lutCount)].append(queue.pop(0))
            counter += 1

        if len(queue) > 0:
            queue.append('LUT'+str(lutCount))

        lutCount += 1

    return LUTs, lutCount 

def split_function(fn_bstring, lut_type):
    '''
    Splits a function fn_bstring so that it can be mapped to FPGA
    Returns a dictionary
    {M0: ['0010-', '1--1-']
     M1: ['--100', '-1010']
     OUT0: ['---11']
    '''
    print('expression:', fn_bstring)

    lut_assignments = {}

    ## Get number of literals, and literal list
    literal_count, literal_list = literal_count_fn(fn_bstring)

    ## If function has fewer than lut_type literals
    if literal_count <= lut_type:
        lut_assignments['LUT0'] = fn_bstring
        return lut_assignments

    for term in fn_bstring:
        num_lits = literal_count_term(term)




def fn_make_packet (fn_bstring, lut_type, fpga_num_inputs):
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
    fn_dict = split_function(fn_bstring, lut_type)


































