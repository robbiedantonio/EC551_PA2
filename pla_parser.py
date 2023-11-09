from collections import Counter

# global behaves like a static vector, easier than cascade returning
expanded_terms = []
def expand_term(index, term):
    global expanded_terms
    '''
    this recursive function takes a string term in the form of xxx...x with do not cares '-'
    example: 
        1-0- expands to
            1000
            1001
            1100
            1101
    input: term <string>
    output minters <string>
    '''
    
    if index == len(term):
        # print(index, term)
        expanded_terms.append(term)
    else:
        if term[index] == '-':
            x = list(term)
            arr = []

            x[index] = '0'
            expand_term(index+1, "".join(x))

            x[index] = '1'
            expand_term(index+1, "".join(x))
    
        else:
            expand_term(index+1, term)



def parse_term(exp_T, ninputs, inputs, terms):
    '''
    a function to parse the function into expanded boolean expression
    return: binary form of the expanded equation
    input:
        exp_T
        ninputs 
        inputs 
        terms

    output: 
        binform <array <string>>

    '''

    op = "*"
    if exp_T == "POS":
        op = "+"

    # map input to index - MSB to LSB of a minterm
    input_mapping = {}
    for i,c in enumerate(inputs):
        input_mapping[c] = i
        input_mapping[c+'\''] = i
    # print(input_mapping)

    # create string array of 0's of the len of
    binform = []
    for i in range(len(terms)):
        binform.append(list("-"*ninputs))

    # print(binform)
    nullable_terms = []
    for i, term in enumerate(terms):
        running_index = 0
        for var in term.split(op):
            if var in term and (var+'\'') in term:
                nullable_terms.append(i)
                break
            if input_mapping.get(var) != None:
                # print(var)
                running_index = input_mapping.get(var)
                binform[i][running_index] = '1' if exp_T == "SOP" else '0'
                if '\'' in var:
                    binform[i][running_index] = '0' if exp_T == "SOP" else '1'
        binform[i] = "".join(binform[i])

    while nullable_terms:
        x = nullable_terms.pop()
        # print("popping term",x+1)
        binform.pop(x)

    print(binform)

    return binform

def parse_file(filename):
    global expanded_terms
    '''
    A function to open and parse a .pla file

    Input:
        file: a .pla file

    Return:
        circuit: a dictionary
            keys: each element of output_names (names of each output) is a key
            values: 
                a one-hot list, where index i is 1 if the i is a minterm and 0 if not
                numerical values of number of I/O vars
                truth table

    '''

    inputs = []
    outputs = []
    boolean_expressions = []
    circuit = {}

    ninputs = -1
    noutputs = -1
    
    tt_true = False

    file = open(filename, 'r')

    for line in file:
        exp_t = ""
        terms = []

        if '.e' in line:
            break
        if '.ni ' in line:
            ninputs=int(line.split(" ")[1])
        elif '.no ' in line:
            noutputs=int(line.split(" ")[1])
        elif '.vi ' in line:
            for in_var in line.split(" ")[1::]:
                if "#" in in_var:
                    break
                if in_var == '':
                    continue
                inputs.append(in_var.strip())
        elif '.vo ' in line:
            for out_var in line.split(" ")[1::]:
                if "#" in out_var:
                    break
                if out_var == '':
                    continue
                outputs.append(out_var.strip())
    #           
    # circuit expression input
    #
        elif '.sop' in line or '.pos' in line:
            # print(line.split(" ")[1::])
            for term in line.split(" ")[1::]:
                if term.strip() == '': 
                    continue
                
                if '.sop' in line:
                    exp_t = "SOP"
                else:
                    exp_t = "POS"
                terms.append(term.strip())

            expression = parse_term(exp_t, ninputs, inputs, terms)
            boolean_expressions.append(expression)
       
        #   
        # expand the prime implicants into minterms
        #   
            for term in expression:
                # print(term)
                expand_term(0,term)
            
            print(set(expanded_terms))

        #
        # create a truth table from the derived boolean expression
        #
            def cleanbin(num):
                numstr = str(num).split('0b')[1]
                zfill = ""
                for _ in range(ninputs-len(numstr)):
                    zfill += '0'
                return zfill + numstr
            
            for i in range(2**ninputs):
                b = cleanbin(bin(i))
                print(b)

    #
    # truth-table input           
    #
        if '.tt' in line or tt_true:
            binary_io = []  ## List with element[0]=input binary, element[1] = output binaryS
            for b in line.split(" "):
                if b != '':
                    binary_io.append(b)

            for i, val in enumerate(binary_io[1].strip()):

                if outputs[i] not in circuit:
                    ## Add new entry in dictionary 
                    circuit[outputs[i]] = [0] * 2**ninputs # initialize as array of zeros
                
                circuit[outputs[i]][int(binary_io[0].strip(), 2)] = val



    return boolean_expressions, circuit



def parse(filename):
    boolean_expressions, output_dict = parse_file(filename)
    # print(output_dict)
    # print(boolean_expressions)
parse('tests/adder.pla')

# expand_term(0,'-0-')


