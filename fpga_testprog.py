from pla_parser import *
from canonicals import *
from minimize import *
from utilities import *
from getDelaySOP import *
from fpga import *

from map_utilities import *




filename = 'tests/test5in.pla'
circuit = parse(filename)

minimized_SOP_dict, pi_count, epi_count = minimize_SOP(circuit)
print(minimized_SOP_dict)

# print(literal_count_fn(minimized_SOP_dict['Z'])[1])

# print(tt_onehot (minimized_SOP_dict['X']))

print("f",tt_onehot(['---11'],4))

fpga = FPGA(num_inputs=4, num_outputs=4, num_luts=8, lut_type=4, input_connectionmat=None, lut_connectionmat=None)

print(fpga.map_function(minimized_SOP_dict['F']))

# fpga.printInfo()


