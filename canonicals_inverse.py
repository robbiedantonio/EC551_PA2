from canonicals import *

def canonical_SOP_inverse(num_inputs, output_dict):
    '''
    A funciton to return inverse of a circuit design as a canonical Sum-of-products

    Inputs:
        output_dict: A dictionary, containing output names as the keys and one-hot vectors as the values
        num_inputs: Number of inputs to the funciton

    Return:
        canonSOP_inv_dict: a dictionary
            keys: each element of output_names (names of each output) is a key
            values: a list of binary strings, which make up the canonical SOP expression

    '''

    return canonical_POS(num_inputs, output_dict)




def canonical_POS_inverse(num_inputs, output_dict):
    '''
    A funciton to return inverse of a circuit design as a canonical product of sums

    Inputs:
        output_dict: A dictionary, containing output names as the keys and one-hot vectors as the values
        num_inputs: Number of inputs to the funciton

    Return:
        canonPOS_inv_dict: a dictionary
            keys: each element of output_names (names of each output) is a key
            values: a list of binary strings, which make up the canonical SOP expression

    '''

    return canonical_SOP(num_inputs, output_dict)


