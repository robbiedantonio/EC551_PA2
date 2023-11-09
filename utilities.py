'''
Copyright 2023 Robbie Dantonio & Muhammed Abdalla
Fall 2023 
ENG EC551
Professor Densmore
'''

def to_SOP(b_strings, iterms):
    '''
    A function to convert a list of binary strings of form ['10-1', 1-0-,...] to 
    proper SOP form ab'd + ac' + ...
    '''

    
    expression = []
    for i, term in enumerate(b_strings):
        terms = []
        for j, bit in enumerate(term):
            if bit == '1':
                terms.append(iterms[j])
            elif bit == '0':
                terms.append(iterms[j]+'\'')
        expression.append("*".join(terms))
    return "+".join(expression)



def to_POS(b_strings, iterms):
    '''
    A function to convert a list of binary strings of form ['10-1', 1-0-,...] to 
    proper POS form (a+b'+d)*(ac')* ... 11--
    '''
    expression = []
    for term in b_strings:
        terms = []
        for j, bit in enumerate(term):
            if bit == '0':
                terms.append(iterms[j])
            elif bit == '1':
                terms.append(iterms[j]+'\'')
        expression.append('('+"+".join(terms)+')')
    return "*".join(expression)



def to_onehot(ninputs, sop_string):
    '''
    Converts SOP minterm expression of form (1,3,6,7) to onehot vector
    '''
    values = [int(val.strip()) for val in sop_string.split(',')]

    max_value = max(values)

    # Step 3: Create a one-hot vector
    onehot = ['0'] * (2**ninputs)
    for val in values:  
        onehot[val] = str(1)
    # print(onehot)

    return onehot



def invert_onehot(onehot_list):
    '''
    A function to flip all the bits in a one-hot list
    '''
    invlist = ['0'] * len(onehot_list)

    for i in range(len(onehot_list)):
        if onehot_list[i] == '0':
            invlist[i] = '1'

    return invlist



