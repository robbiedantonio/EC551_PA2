

def canonical_SOP(num_inputs, output_dict):
    '''
    A funciton to return a circuit design as a canonical Sum-of-products

    Inputs:
        output_dict: A dictionary, containing output names as the keys and one-hot vectors as the values
        num_inputs: Number of inputs to the funciton

    Return:
        canonSOP_dict: a dictionary
            keys: each element of output_names (names of each output) is a key
            values: a list of binary strings, which make up the canonical SOP expression

    '''

    canonSOP_dict = {}

    for output_name, output_list_onehot in output_dict.items():
        canonSOP_dict[output_name] = []

        for idx, minterm in enumerate(output_list_onehot):
            
            if int(minterm) == 1:
                minterm_binary = bin(idx)[2:].zfill(num_inputs)    ## Convert list index to binary
                
                canonSOP_dict[output_name].append(minterm_binary)


    return canonSOP_dict




def canonical_POS(num_inputs, output_dict):
    '''
    A funciton to return a circuit design as a canonical product of sums

    Inputs:
        output_dict: A dictionary, containing output names as the keys and one-hot vectors as the values
        num_inputs: Number of inputs to the funciton

    Return:
        canonPOS_dict: a dictionary
            keys: each element of output_names (names of each output) is a key
            values: a list of binary strings, which make up the canonical SOP expression

    '''

    canonPOS_dict = {}

    for output_name, output_list_onehot in output_dict.items():
        canonPOS_dict[output_name] = []

        for idx, minterm in enumerate(output_list_onehot):
            
            if int(minterm) == 0:
                minterm_binary = bin(idx)[2:].zfill(num_inputs)    ## Convert list index to binary
                
                canonPOS_dict[output_name].append(minterm_binary)


    return canonPOS_dict


