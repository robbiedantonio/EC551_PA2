import numpy as np
import math


def getDelayPOS (POS_expression, delay_AND=1, delay_OR=1):
	'''
	Function to calculate number of fan-in 2 gates required for POS function
	
	Inputs:
		SOP_expression: A sum-of-products expression, passed in as a list of strings of form '1-01' for a+c'+d
		delay_AND (optional): Delay of an AND gate
		delay_OR (optional): Delay of an OR gate
	Return:
		delay: Total gate delay of circuit's critical path
			- If delay_AND and delay_OR are not set, this is equivalent to number of gates on the critical path
		num_gates: Total number of gates required to implement function
	'''

	POS_local = POS_expression

	OR_gates = []	# list containing number of OR gates for each product term

	## Compute number of OR gates required for each product term
	for product in range(len(POS_local)):
		OR_gates.append(POS_local[product].count('0') + POS_local[product].count('1') - 1)	

	## Compute total AND gates required
	OR_gates = len(POS_local) - 1

	## Compute total number of gates required for function
	num_gates = OR_gates + sum(OR_gates)

	## Compute delay of critical path
	num_OR_gates = max(OR_gates)
	num_AND_gates = int(math.ceil(math.log2(len(POS_local))))
	delay = (num_AND_gates * delay_AND) + (num_OR_gates * delay_OR)

	return delay, num_gates


