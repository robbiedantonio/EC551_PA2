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



def to_graph (fn_bstring):
    '''
    Generates a graph for a boolean logic expression

    fn_bstring: function in bstring format: ['10-0', '1--0', '1011']
    '''

    graph = nx.DiGraph()

    ## Add nodes for inputs
    literal_list = literal_count_fn(fn_bstring)[1]
    for idx, ip in enumerate(literal_list):
        if ip == 1:
            graph.add_node('IN{idx}', type="input", id=idx)




def split_function (fn_bstring, lut_type):
    '''
    Splits a function into subterms, each with num_literals <= lut_type

    Inputs:
        fn_bstring: a list of bstrings representing a boolean expression (['1-01', '-11-'])
        lut_type: Number of inputs available to a LUT
    '''
    split_dict = {}








