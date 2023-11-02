
def to_SOP(b_strings, terms):
    '''
    A function to convert a list of binary strings of form ['10-1', 1-0-,...] to 
    proper SOP form ab'd + ac' + ...
    '''
    ret_string = ""

    for j, prod in enumerate(b_strings):
        if j != 0:
            ret_string += " + "
        for i in range(len(prod)):
            if prod[i] == '1':
                ret_string += terms[i]
            elif prod[i] == '0':
                ret_string += terms[i] + '\''

    return ret_string

def invert_onehot(onehot_list):
    '''
    A function to flip all the bits in a one-hot list
    '''
    newlist = [0] * len(onehot_list)
    
    for i in range(len(onehot_list)):
        if onehot_list[i] == '0':
            newlist[i] = '1'

    return newlist




def to_POS(b_strings, terms):
    '''
    A function to convert a list of binary strings of form ['10-1', 1-0-,...] to 
    proper POS form (a+b'+d)*(ac')* ... 11--
    '''
    ret_string = ""

    for j, prod in enumerate(b_strings):
        # print(prod)
        if j != 0:
            ret_string += ' * '
        for i in range(len(prod)):
            if prod[i] == '1':
                ret_string += terms[i]
            elif prod[i] == '0':
                ret_string += terms[i] + '\''

            if i != len(prod)-1 and len(ret_string) > 0 and ret_string[-1] != '+' and ret_string[-1] != ' ':
                ret_string += '+'

    return ret_string



def to_onehot(sop_string):
    '''
    Converts SOP minterm expression of form (1,3,6,7) to onehot vector
    '''
    values = [int(val.strip()) for val in sop_string.split(',')]

    max_value = max(values)

    # Step 3: Create a one-hot vector
    onehot = [0] * (max_value + 1)
    for val in values:
        onehot[val] = 1

    return onehot


