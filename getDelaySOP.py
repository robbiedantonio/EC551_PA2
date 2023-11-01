import numpy as np
import math


def getDelaySOP (SOP_expression, delay_AND=1, delay_OR=1):
	'''
	Function to calculate number of fan-in 2 gates required for SOP function
	
	Inputs:
		SOP_expression: A sum-of-products expression, passed in as a list of strings of form '1-01' for ac'd
		delay_AND (optional): Delay of an AND gate
		delay_OR (optional): Delay of an OR gate
	Return:
		delay: Total gate delay of circuit's critical path
			- If delay_AND and delay_OR are not set, this is equivalent to number of gates on the critical path
		num_gates: Total number of gates required to implement function
	'''

	SOP_local = SOP_expression

	AND_gates = []	# list containing number of AND gates for each product term

	## Compute number of AND gates required for each product term
	for product in range(len(SOP_local)):
		AND_gates.append(SOP_local[product].count('0') + SOP_local[product].count('1') - 1)	

	## Compute total OR gates required
	OR_gates = len(SOP_local) - 1

	## Compute total number of gates required for function
	num_gates = OR_gates + sum(AND_gates)

	## Compute delay of critical path
	num_AND_gates = max(AND_gates)
	num_OR_gates = int(math.ceil(math.log2(len(SOP_local))))
	delay = (num_AND_gates * delay_AND) + (num_OR_gates * delay_OR)

	return delay, num_gates