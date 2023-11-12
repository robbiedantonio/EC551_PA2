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


filename = 'tests/adder.pla'



## Parse filename
## if (filename)
circuit = parse(filename)
# print(circuit)
canonical_SOP 	= canonicals(circuit, 'SOP', False)
canonical_POS 	= canonicals(circuit, 'POS', False)
canonical_SOP_I = canonicals(circuit, 'SOP', True)
canonical_POS_I = canonicals(circuit, 'POS', True)

minimized_SOP_dict = minimize_SOP(circuit)
minimized_POS_dict = minimize_POS(circuit)

# print(canonical_SOP['expressions'])
# print(canonical_SOP['one_hot'])

# for op, op_list in circuit.items():
# 	print(op,':', to_SOP(circuit[op], input_names))


for op, op_list in output_dict.items():
	print(op,':', to_SOP(canonSOP_dict[op], input_names))
# print('\n')

# for op, op_list in output_dict.items():
# 	print(op,':', to_POS(canonPOS_dict[op], input_names))

# print('\n')

# for op, op_list in output_dict.items():
# 	print(op,':', to_SOP(canonSOP_inv_dict[op], input_names))

# print('\n')

# for op, op_list in output_dict.items():
# 	print(op,':', to_POS(canonPOS_inv_dict[op], input_names))

# print('\n')

# for op, op_list in output_dict.items():
# 	print(op,':', to_SOP(minimized_SOP_dict[op], input_names))

# print('\n')

# for op, op_list in output_dict.items():
# 	print(op,':', to_POS(minimized_POS_dict[op], input_names))


for op, op_list in output_dict.items():
	print(op,':', getDelaySOP(minimized_SOP_dict[op]), input_names)














