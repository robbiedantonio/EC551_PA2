'''
Copyright 2023 Robbie Dantonio & Muhammed Abdalla
Fall 2023 
ENG EC551
Professor Densmore
'''
from tkinter import *
from pla_parser import *
from canonicals import *
from minimize import *
from utilities import *
from getDelaySOP import *


filename = 'tests/test.pla'



## Parse filename
## if (filename)
circuit = parse(filename)
# print(circuit)
canonical_SOP 	= canonicals(circuit, 'SOP', False)
canonical_POS 	= canonicals(circuit, 'POS', False)
canonical_SOP_I = canonicals(circuit, 'SOP', True)
canonical_POS_I = canonicals(circuit, 'POS', True)

minimized_SOP_dict, pi_count, epi_count = minimize_SOP(circuit)
minimized_POS_dict, pi_count, epi_count = minimize_POS(circuit)

print(canonical_SOP['expressions'])
print(canonical_SOP['one_hot'])

print("\nMINIMIZED SUM OF PRODUCT")
for ovar, oexp in minimized_SOP_dict.items():
	print(ovar,oexp)
print('\n')



for op, op_list in output_dict.items():
	print(op,':', to_SOP(canonSOP_dict[op], input_names))
# print('\n')

print("\nMINIMIZED PRODUCT OF SUM")
for ovar, oexp in minimized_POS_dict.items():
	print(ovar,oexp)
print('\n')




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


'''
UI should have:
	textbox for input equations functions
	

	Behavioral Analysis:
		12 functions
		Run Simulation
			Simple Waveform
			input .tst file or manually input truth table

	FPGA drop down:
		run synthesis
		run implementation
		generate bitstream -> save to file
		upload to FPGA

'''











