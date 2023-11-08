from collections import Counter

def parse_term(ninputs, inputs, terms):
    '''
    a function to parse the function into expanded boolean expression
    return: binary form of the expanded equation
    '''
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
        for var in term.split('*'):
            if term.count(var) > 1:
                nullable_terms.append(i)
                break
            if input_mapping.get(var) != None:
                print(var)
                running_index = input_mapping.get(var)
                binform[i][running_index] = '1'
                if '\'' in var:
                    binform[i][running_index] = '0'
        binform[i] = "".join(binform[i])

    while nullable_terms:
        x = nullable_terms.pop()
        print("popping term",x+1)
        binform.pop(x)

    print(binform)

    return 

def parse_file(filename):
    '''
    A function to open and parse a .pla file

    Input:
        file: a .pla file

    Return:
        num_inputs: number of inputs to the circuit
        num_output: number of outputs from the circuit
        input_names: list containing the names of the inputs
        output_names: list containing the names of the outputs
        output_dict: a dictionary
            keys: each element of output_names (names of each output) is a key
            values: a one-hot list, where index i is 1 if the i is a minterm and 0 if not
    '''

    inputs = []
    outputs = []
    ninputs = -1
    noutputs = -1

    expression = ""
    terms = []



    output_dict = {}

    file = open(filename, 'r')

    for line in file:
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
        elif '.sop' in line or '.pos' in line:
            # print(line.split(" ")[1::])
            for term in line.split(" ")[1::]:
                if term.strip() == '': 
                    continue
                
                if '.sop' in line:
                    expression = "SOP"
                else:
                    expression = "POS"

                terms.append(term.strip())

        elif '.tt' in line:
            binary_io = []  ## List with element[0]=input binary, element[1] = output binary

            for b in line.split(" "):
                if b != '':
                    binary_io.append(b)

            for i, val in enumerate(binary_io[1].strip()):

                if outputs[i] not in output_dict:
                    ## Add new entry in dictionary 
                    output_dict[outputs[i]] = [0] * 2**ninputs # initialize as array of zeros
                
                output_dict[outputs[i]][int(binary_io[0].strip(), 2)] = val


    return ninputs, noutputs, inputs, outputs, terms, output_dict



def parse(filename):
    ninputs, noutputs, inputs, outputs, terms, output_dict = parse_file(filename)
    minterms_binary = parse_term(ninputs, inputs, terms)

parse('tests/adder.pla')

