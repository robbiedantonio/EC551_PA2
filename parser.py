

def parse(filename):
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

    input_names = []
    output_names = []

    output_dict = {}

    file = open(filename, 'r')

    for line in file:

        if '.e' in line:
            break
        if '.i ' in line:
            num_inputs=int(line.split(" ")[1])
        elif '.o ' in line:
            num_outputs=int(line.split(" ")[1])
        elif '.ilb ' in line:
            for in_var in line.split(" ")[1::]:
                if "#" in in_var:
                    break
                if in_var == '':
                    continue
                input_names.append(in_var.strip())
        elif '.ob ' in line:
            for out_var in line.split(" ")[1::]:
                if "#" in out_var:
                    break
                if out_var == '':
                    continue
                output_names.append(out_var.strip())
        elif '.' not in line:
            binary_io = []  ## List with element[0]=input binary, element[1] = output binary

            for b in line.split(" "):
                if b != '':
                    binary_io.append(b)

            for i, val in enumerate(binary_io[1].strip()):

                if output_names[i] not in output_dict:
                    ## Add new entry in dictionary 
                    output_dict[output_names[i]] = [0] * 2**num_inputs # initialize as array of zeros
                
                output_dict[output_names[i]][int(binary_io[0].strip(), 2)] = val


    return num_inputs, num_outputs, input_names, output_names, output_dict


