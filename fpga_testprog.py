from pla_parser import *
from canonicals import *
from minimize import *
from utilities import *
from getDelaySOP import *
from luts import *



filename = 'tests/test.pla'
circuit = parse(filename)
minimized_SOP_dict, pi_count, epi_count = minimize_SOP(circuit)
print(minimized_SOP_dict)

fpga = FPGA(num_luts=8, lut_type=4, num_inputs=4, num_outputs=1, connection_mat=None)


fpga.printInfo()


