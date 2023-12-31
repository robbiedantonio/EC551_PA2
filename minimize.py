'''
Copyright 2023 Robbie Dantonio & Muhammed Abdalla
Fall 2023 
ENG EC551
Professor Densmore
'''

import numpy as np

from utilities import *


def mt_compare (min1, min2):
    '''
    A function that checks if two minterms differ by only one bit

    Inputs: 
        min1, min2: two minterms strings in binary representation
    Returns:
        True/False: True if minterms differ by only one bit
        idx: If true, this is the index where the bits are different. If false, returns None
    '''
    count=0
    
    for i in range(len(min1)):
        if(min1[i] != min2[i]):
            count+=1
            idx = i

    if(count != 1):
        # >1 bits are different
        return False, None
    else:
        return True, idx


def mt_merge (min1, min2, idx):
    '''
    A function that merges two minterms by changing the mismatched bit of two minterms to a '-'

    Inputs: 
        min1, min2: two minterm strings in binary representation with only one bit different
        idx: index of mismatched bit
    Returns:
        min_merged: merged minterm where mismatched bit is '-'
    Eg. min1 = 1011, min2 = 1001 => min_merged = 10-1
    '''
    return min1[:idx] + '-' + min1[idx + 1:]


def is_covered (ninputs, pi, minterm):
    '''
    A function to check if a prime implicant pi covers a minterm. Returns True/False

    Inputs:
        pi: prime implicant, a string
        minterm: minterm, an integer
        num_inputs: number of inputs a,b,c,... to circuit
    Return:
        True if pi covers the minterm
    '''
    ## Convert minterm to string
    mt_str = bin(minterm)[2:].zfill(ninputs)

    for i in range(len(mt_str)):
        if mt_str[i] != pi[i] and pi[i] != '-':
            return False
    return True


def is_represented(pi, minterm, pi_dict):
    '''
    A function to check if a minterm in pi is represented by other prime implicants

    Inputs:
        pi: prime implicant, a string
        minterm: minterm, a string
        pi_dict: dictionary of all prime implicants and the minterms they represent
    Return:
        True if minterm is covered by other prime implicants
    '''
    for pi_compare in pi_dict:
        if pi_compare != pi:
            for minterm_compare in pi_dict[pi_compare]:
                if minterm_compare == minterm:
                    return True
    return False


def find_PIs (ninputs, minterms_onehot):
    '''
    A function to find the prime implicants of a boolean expression

    Input: 
        minterms_onehot: one-hot vector (numpy array) corresponding to SOP minterm expression
    Return: 
        prime_implicants: A list of the expression's prime implicants
        pi_count: Number of prime implicants
    '''
    num_inputs = ninputs

    # List of prime implicants
    prime_implicants = []

    # Master data structure (eventually becomes a dictionary of dictionaries of dictionaries)
    groups = {}

    ## Step 1: Initial Grouping - place minterms with same number of '1' bits in the same group
    groups[0] = {} # group dictionary

    # print(ninputs, minterms_onehot)
    for minterm in range(len(minterms_onehot)):
        if minterms_onehot[minterm] == '1':
            num_bits = bin(minterm).count('1')
            if num_bits not in groups[0]:
                # Create a new group
                groups[0][num_bits] = {bin(minterm)[2:].zfill(num_inputs) : False} ## Convert minterm to string of its binary representation
            else:
                # Add to existing group
                groups[0][num_bits][bin(minterm)[2:].zfill(num_inputs)] = False
    
    ## Sort keys in increasing order
    groups[0] = dict(sorted(groups[0].items()))


    ## Step 2: Iterative grouping - find prime implicants, brute force comparison method
    k = 0

    while groups[k]:
        groups[k + 1] = {}
        keylist = list(groups[k].keys())

        for i in range(len(groups[k]) - 1):
            id1, id2 = keylist[i], keylist[i] + 1

            if id1 in groups[k] and id2 in groups[k]:
                for min1 in groups[k][id1]:
                    for min2 in groups[k][id2]:
                        oneBitDif, idx = mt_compare(min1, min2)

                        if oneBitDif:
                            groups[k][id1][min1] = True # Set status to reduced
                            groups[k][id2][min2] = True

                            min_merged = mt_merge(min1, min2, idx)

                            if i not in groups[k + 1]:
                                groups[k + 1][i] = {min_merged: False}  # Create new group
                            else:
                                groups[k + 1][i][min_merged] = False    # Add to existing group
        
        ## Loop through groups[k] to find any prime implicants that haven't been reduced
        for inner_dict in groups[k].values():
            for inner_key, reduced in inner_dict.items():
                if not reduced:
                    prime_implicants.append(inner_key)

        k += 1

    pi_count = len(prime_implicants)
    return prime_implicants, pi_count

 

def find_single_min (ninputs, minterms_onehot):
    '''
    A function to find the mininized SOP/POS representation of a boolean expression using Quine McCluskey algorithm

    Input:
        minterms_onehot: one-hot vector (numpy array) corresponding to SOP minterm expression
    Returns:
        minimized_function: list of prime implicants that make up minimized function
        epi_count: number of essential prime implicants
    '''

    num_inputs = ninputs

    ## Step 1: Find prime implicants
    prime_implicants, pi_count = find_PIs(num_inputs, minterms_onehot)
    
    ## Step 2: For each prime implicant, create a list of minterms for which it represents
    pi_dict = {}    #format {pi1:[mt1, mt2, ...], pi2:[mt2, mt7, ...], ...}

    for pi in prime_implicants:
        for minterm in range(len(minterms_onehot)):

            if minterms_onehot[minterm] == '1':
                if is_covered (num_inputs, pi, minterm):
                    if pi not in pi_dict:
                        pi_dict[pi] = [bin(minterm)[2:].zfill(num_inputs)]  # Create new group
                    else:
                        pi_dict[pi].append(bin(minterm)[2:].zfill(num_inputs))  # Add to existing group

    ## Step 3: Remove any dominated PIs
    epi_list = []
    iter_num = 0
    
    while True:
        to_be_removed = None

        for pi in pi_dict:
            count = 0
            covered_minterms = []

            for minterm in pi_dict[pi]:

                if is_represented(pi, minterm, pi_dict) and minterm not in covered_minterms:
                    covered_minterms.append(minterm)
                    count+=1
                else:
                    if iter_num == 0:
                        epi_list.append(pi) # Minterm is covered exclusively by this PI, meaning it's essential
                    break

            if count == len(pi_dict[pi]):
                to_be_removed = pi

        if to_be_removed != None:
            del pi_dict[to_be_removed]
        else:
            break

        iter_num+=1

    minimized_function = list(pi_dict)
    epi_count = len(epi_list)

    return minimized_function, pi_count, epi_count


def minimize_SOP (circuit):
    '''
    A function to find the mininized SOP representation of multiple boolean expressions using Quine McCluskey algorithm

    Inputs:
        output_dict: A dictionary, containing output names as the keys and one-hot vectors as the values

    Returns:
        minimized_dict: A dictionary, containing output names as the keys and a minimized SOP list for the value of each output key
    '''
    minimized_dict = {}
    literals = {}

    for op, op_list in circuit['output_vector'].items():
        minimized_exp, pi_count, epi_count = ( find_single_min(circuit['ninputs'], to_onehot(circuit['ninputs'], ",".join(op_list)) ))
        # minimized_dict[op] = to_SOP(minimized_exp, circuit['inputs'])
        minimized_dict[op] = minimized_exp

        literals[op] = 0
        for term in minimized_exp:
            for bit in term:
                if bit != '-':
                    literals[op] += 1

    return minimized_dict, pi_count, epi_count, literals

def minimize_POS (circuit):
    '''
    A function to find the mininized POS representation of multiple boolean expressions using Quine McCluskey algorithm

    Inputs:
        output_dict: A dictionary, containing output names as the keys and one-hot vectors as the values

    Returns:
        minimized_dict: A dictionary, containing output names as the keys and a minimized SOP list for the value of each output key
    '''
    minimized_dict = {}
    literals = {}

    for op, op_list in circuit['output_vector'].items():
        inverted_list = invert_onehot(to_onehot(circuit['ninputs'], ",".join(op_list)))
        minimized_exp, pi_count, epi_count = (find_single_min(circuit['ninputs'], inverted_list))
        # minimized_dict[op] = to_POS(minimized_exp, circuit['inputs'])
        minimized_dict[op] = minimized_exp

        literals[op] = 0
        for term in minimized_exp:
            for bit in term:
                if bit != '-':
                    literals[op] += 1

    return minimized_dict, pi_count, epi_count, literals























