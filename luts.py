import numpy as np


class LUT:
    def __init__(self, lut_id, lut_type):
        self.lut_id = lut_id          # ID assosiciated with this LUT only
        self.lut_type = lut_type      # Number of inputs into LUT, either 4 or 6
        self.is_available = True      # True if LUT can have function mapped to it, false if function is already mapped
        self.input_list = None        # List of inputs into LUT can be either overall inputs or other LUTs 
        self.output = None            # Output of LUT
        self.function = None          # Function mapped to the LUT in onehot format

    def map_function (self, function_onehot, input_list, output):
        '''
        Maps a function to the LUT

        function_onehot: one-hot list representing function to be mapped
            ** Conversion from b-string to onehot must be handled externally!!!! **
        input_list: A list of input literal names
        output: Name of output
        '''
        self.input_list = input_list
        self.output = output
        self.function = function_onehot



class FPGA:
    def __init__(self, num_luts, lut_type, num_inputs, num_outputs, connection_mat=None)
        self.num_luts = num_luts        # Number of LUTs in this FPGA
        self.lut_type = lut_type        # Type of LUTs (4-input or 6-input)
        self.num_inputs = num_inputs    # Number of inputs on this FPGA
        self.num_outputs = num_outputs  # Number of outputs on this FPGA

        ## Initialize connection matrix
        if connection_mat != None:
            self.connection_mat = connection_mat
        else:
            self.connection_mat = self.make_connect_mat()

        ## Initialize LUTs
        self.lut_list = init_LUTs()

    def make_connect_mat(self):
        ## Generates connection matrix for LUTs - assumes that all LUTs are conected
        connection_mat = np.ones((self.num_luts, self.num_luts), dtype=int)
        return connection_mat

    def init_LUTs(self):
        ## Instantiates num_luts instances of LUT class, returns list of LUTs
        lut_list = []
        for lut_id in range(self.num_luts):
            lut_list.append(LUT(lut_id=lut_id, lut_type=self.lut_type))
        return lut_list

    def map_function(self, fn_bstring, inputs, output):
        '''
        Adds a function to the FPGA

        fn_bstring: function in bstring format: ['10-0', '1--0', '1011']
        '''
        
        '''
        General Algorithm:
            1. Check number of literals in function
                - If greater than number of inputs per LUT, then function
                    needs to be broken up into multiple functions with fewer
                    literals. Then make recursive calls (?) on additional functions
                    (this is a big task!!)
            2. Determine names of literals and name of output for function
                - If any inputs are the output of another LUT, then check self.connection_mat
                  to see if there are any connection restrictions
            3. Convert bstring to onehot format 
            4. Find free LUT
                - Keep self.connection_mat in mind here!!
            5. Call lut.map_function() and return


        Extras (might not implement):
            1. Make sure that bstring is in correct format
            2. Check that there are still free LUTs
            3. Add matrix of actual lut connections as extra redundancy check
        '''

        pass






















