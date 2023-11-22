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

from tqdm import tqdm



filename = 'tests/test5in.pla'
circuit = parse(filename)

<<<<<<< HEAD
minimized_SOP_dict, pi_count, epi_count, literals = minimize_SOP(circuit)
print(minimized_SOP_dict)
=======
minimized_SOP_dict, pi_count, epi_count = minimize_SOP(circuit)
# print(minimized_SOP_dict)
>>>>>>> 7c83245ced63b86181f44564c3a6f815bf09b645

fpga = FPGA(num_inputs=6, num_outputs=4, num_luts=8, lut_type=4, input_connectionmat=None, lut_connectionmat=None)
fpga.init_variables(circuit['inputs'], circuit['outputs'])

for literal in minimized_SOP_dict.keys():
	fpga.map_function(minimized_SOP_dict[literal], circuit['inputs'], literal)

print("Evaluating all 1s on inputs", fpga.run_input([1,1,1,1,1,1]))

# print(fpga.map_function(minimized_SOP_dict['F']))

fpga.print_info()

# bitstream = fpga.get_bitstream()
# print(bitstream)


