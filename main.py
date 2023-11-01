from parser import *
from canonicals import *
from canonicals_inverse import *
from minimize import *
from utilities import *


filename = 'tests/adder2bit.pla'



## Parse filename
## if (filename)
num_inputs, num_outputs, input_names, output_names, output_dict = parse(filename)


canonSOP_dict = canonical_SOP(num_inputs, output_dict)
canonPOS_dict = canonical_POS(num_inputs, output_dict)
canonSOP_inv_dict = canonical_SOP_inverse(num_inputs, output_dict)
canonPOS_inv_dict = canonical_POS_inverse(num_inputs, output_dict)
minimized_SOP_dict = minimize_SOP(output_dict)
minimized_POS_dict = minimize_POS(output_dict)


for op, op_list in output_dict.items():
	print(op,':', to_SOP(canonSOP_dict[op], input_names))

print('\n')

for op, op_list in output_dict.items():
	print(op,':', to_POS(canonPOS_dict[op], input_names))

print('\n')

for op, op_list in output_dict.items():
	print(op,':', to_SOP(canonSOP_inv_dict[op], input_names))

print('\n')

for op, op_list in output_dict.items():
	print(op,':', to_POS(canonPOS_inv_dict[op], input_names))

print('\n')

for op, op_list in output_dict.items():
	print(op,':', to_SOP(minimized_SOP_dict[op], input_names))

print('\n')

for op, op_list in output_dict.items():
	print(op,':', to_POS(minimized_POS_dict[op], input_names))
















