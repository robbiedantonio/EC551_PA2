'''
Copyright 2023 Robbie Dantonio & Muhammed Abdalla
Fall 2023 
ENG EC551
Professor Densmore
'''

from pla_parser import *
from canonicals import *
from minimize import *
from utilities import *
from getDelaySOP import *
from fpga import *

from map_utilities import *




filename = 'tests/test5in.pla'
circuit = parse(filename)

minimized_SOP_dict, pi_count, epi_count, literals = minimize_SOP(circuit)
print(minimized_SOP_dict)

fpga = FPGA(num_inputs=6, num_outputs=4, num_luts=10, lut_type=4, input_connectionmat=None, lut_connectionmat=None)
fpga.init_variables(circuit['inputs'], circuit['outputs'])

fpga.map_function(minimized_SOP_dict['X'], circuit['inputs'], 'X')
fpga.map_function(minimized_SOP_dict['Y'], circuit['inputs'], 'Y')
fpga.map_function(minimized_SOP_dict['Z'], circuit['inputs'], 'Z')
fpga.map_function(minimized_SOP_dict['F'], circuit['inputs'], 'F')
fpga.map_function(minimized_SOP_dict['G'], circuit['inputs'], 'G')

fpga.print_info()

# print(fpga.map_function(minimized_SOP_dict['F']))

# fpga.printInfo()


