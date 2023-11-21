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

minimized_SOP_dict, pi_count, epi_count = minimize_SOP(circuit)
print(minimized_SOP_dict)

fpga = FPGA(num_inputs=6, num_outputs=5, num_luts=32, lut_type=4, input_connectionmat=None, lut_connectionmat=None)
fpga.init_variables(circuit['inputs'], circuit['outputs'])

for literal in minimized_SOP_dict.keys():
	fpga.map_function(minimized_SOP_dict[literal], circuit['inputs'], literal)

print("Evaluating all 1s on inputs", fpga.run_input([1,1,1,1,1,1]))

# print(fpga.map_function(minimized_SOP_dict['F']))

# fpga.printInfo()


