

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
 
    circuit = {
        'ninputs':-1,
        'noutputs':-1,
        'inputs':[],
        'outputs':[],

        'boolean_expressions':[],
        'marked_terms':[]
    }
    truth_table = {}

    exp_counter = 0

    file = open(filename, 'r')

    for line in file:
        exp_t = ""

        if '.e' in line:
            break
        if '.ni ' in line:
            circuit['ninputs']=int(line.split(" ")[1])
        elif '.no ' in line:
            circuit['noutputs']=int(line.split(" ")[1])
        elif '.vi ' in line:
            for in_var in line.split(" ")[1::]:
                if "#" in in_var:
                    break
                if in_var == '':
                    continue
                circuit['inputs'].append(in_var.strip())
        elif '.vo ' in line:
            for out_var in line.split(" ")[1::]:
                if "#" in out_var:
                    break
                if out_var == '':
                    continue
                circuit['outputs'].append(out_var.strip())
    #           
    # circuit expression input
    #
        elif '.sop' in line or '.pos' in line:
            terms = []
            expanded_terms = []
            # print(line.split(" ")[1::])
            for term in line.split(" ")[1::]:
                if term.strip() == '': 
                    continue
                
                if '.sop' in line:
                    exp_t = "SOP"
                else:
                    exp_t = "POS"
                terms.append(term.strip())

            expression = parse_term(exp_t, circuit['ninputs'], circuit['inputs'], terms)
            circuit['boolean_expressions'].append(expression)
       
        #   
        # expand the prime implicants into minterms
        #   
            for term in expression:
                # print(term)
                expand_term(0, term)

            set(expanded_terms)
            # print(expanded_terms)

        #
        # create a truth table from the derived boolean expression
        #
            def cleanbin(num):
                numstr = str(num).split('0b')[1]
                zfill = ""
                for _ in range(circuit['ninputs']-len(numstr)):
                    zfill += '0'
                return zfill + numstr
            
            for i in range(2**circuit['ninputs']):
                b = cleanbin(bin(i))

                if truth_table.get(b, -1) == -1:
                    truth_table[b] = ''

                if b in expanded_terms:
                    truth_table[b] += '1'
                    circuit['marked_terms'].append(('1', exp_counter, b))
                else:
                    truth_table[b] += '0'
                    circuit['marked_terms'].append(('0', exp_counter, b))
            exp_counter += 1
            
    for k,v in truth_table.items():
        print(k,v)
    
    circuit['marked_terms'].sort()
    for e in circuit['marked_terms']:
        print(e)

    return circuit



def parse(filename):
    circuit = parse_file(filename)
    # print(circuit)
    # print(boolean_expressions)

parse('tests/adder.pla')

# expand_term(0,'-0-')


