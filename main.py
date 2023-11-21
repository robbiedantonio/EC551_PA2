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


filename = 'tests/test.pla'

def canonical(circuit, eForm, inv):
    global cExpressions, numberNotation, cLiterals
    cExpressions, numberNotation, cLiterals = canonicals(circuit, eForm, inv)

def minimize(circuit, eType):
    global mExpression, pi_count, epi_count, mLiterals

    if eType == 'SOP':
        mExpression, pi_count, epi_count = minimize_SOP(circuit)
    elif eType == 'POS':
        mExpression, pi_count, epi_count = minimize_POS(circuit) 

'''
1. Return the design as a canonical SOP
2. Return the design as a canonical POS
3. Return the design INVERSE as a canonical SOP
4. Return the design INVERSE as a canonical POS
5. Return a minimized number of literals representation in SOP
a. Report on the number of saved literals vs. the canonical version
6. Return a minimized number of literals representation in POS
a. Report on the number of saved literals vs. the canonical version
7. Report the number of Prime Implicants
8. Report the number of Essential Prime Implicants
9. Report the number of ON-Set minterms
10. Report the number of ON-Set maxterms
11. SOP Gate Delay
12. POS Gate Delay
'''

command = {
      'default': "press Q to quit or C to continue.\ntype \'help'\' for help",
      'file': "input a file to get started",
      'func': "please select a function 1 - 12",
      "help": 
'''
	Engine functions
		type \'file\' to input file
		type \'func\' to select a function
		type \'synth\' to map functions to LUTs
		type \'synth-info\' to print LUT info
		type \'fpga-map\' to map LUTs onto FPGA
		type \'fpga-info\' to print FPGA info

	Synthesis Functions:
		1. Return the design as a canonical SOP
		2. Return the design as a canonical POS
		3. Return the design INVERSE as a canonical SOP
		4. Return the design INVERSE as a canonical POS
		5. Return a minimized number of literals representation in SOP
		\ta. Report on the number of saved literals vs. the canonical version
		6. Return a minimized number of literals representation in POS
		\ta. Report on the number of saved literals vs. the canonical version
		7. Report the number of Prime Implicants
		8. Report the number of Essential Prime Implicants
		9. Report the number of ON-Set minterms
		10. Report the number of ON-Set maxterms
		11. SOP Gate Delay
		12. POS Gate Delay
'''
}
	
    
## Parse filename
## if (filename)
# circuit = parse(filename)
# print(circuit)

# canonical_POS, numberNotation_POS, literals2 = canonicals(circuit, 'POS', False)
# canonical_SOP_I, numberNotation_SOP_I, literals3 = canonicals(circuit, 'SOP', True)
# canonical_POS_I, numberNotation_POS_I, literals4 = canonicals(circuit, 'POS', True)

# minimized_SOP_dict, pi_count, epi_count, literals5 = minimize_SOP(circuit)
# minimized_POS_dict, pi_count, epi_count, literals6 = minimize_POS(circuit)

# print('literals')
# # print(canonical_SOP, literals1)
# print(minimized_SOP_dict, literals5)

# print("\nMINIMIZED SUM OF PRODUCT")
# for ovar, oexp in minimized_SOP_dict.items():
# 	print(ovar,oexp)
# print('\n')


# # print('\n')

# print("\nMINIMIZED PRODUCT OF SUM")
# for ovar, oexp in minimized_POS_dict.items():
# 	print(ovar,oexp)
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


'''
UI should have:
	textbox for input equations functions
	

	Behavioral Analysis:
		12 functions
		Simple Waveform
		input .tst file or manually input truth table
		# literals 
		# implicants

	FPGA drop down:
		run synthesis
		run implementation
		generate bitstream -> save to file
		upload to FPGA



'''

def decode(mExp, op):
	m = []
	for ovar, oexp in mExp.items():
		print(ovar,oexp)
		exp = []
		for term in oexp:
			t = []
			for i, bit in enumerate(list(term)):
				# print(i, bit)
				if op[0] == '*':
					if bit == '1':
						t.append(circuit['inputs'][i])
					elif bit == '0':
						t.append(circuit['inputs'][i] + '\'')
				elif op[0] == '+':
					if bit == '0':
						t.append(circuit['inputs'][i])
					elif bit == '1':
						t.append(circuit['inputs'][i] + '\'')

			exp.append("("+op[0].join(t)+")")
		m.append(ovar + '=' + op[1].join(exp))
	return m


cmd = ""
i = 0
print('\n\nWelcome to Logic Synthesizer 551')

while cmd != 'Q':

	cmd = input(command['default']+'\n>> ')

	if cmd.lower() == 'help':
		print(command['help'])
		continue
	
	if cmd.lower() == 'file':
		# cmd = input('enter a file\n>> ')
		# if i == 0:
		# 	try:
		# 		f = open(cmd, 'r')
		# 	except:
		# 		pass

		circuit = parse_file('tests/test.pla')
	
	if cmd.lower() == 'func':
		cmd = input('select a function 1 - 12, press help\n>> ')
		funcNum = int(cmd)
		if funcNum > 12 or funcNum < 1:
			print("\n<< Invalid Function. Please try again.")
			continue

		if funcNum in [1, 2, 3, 4]:
			eType = 'SOP'
			inv = False

			if funcNum == 1:
				eType = 'SOP'
				inv = False
			elif funcNum == 2:
				eType = 'POS'
				inv = False
			elif funcNum == 3:
				eType = 'SOP'
				inv = True
			elif funcNum == 4:
				eType = 'POS'
				inv = True

			expressions, numberNotation, literals = canonicals(circuit, eType, inv)

			for e,n,l in zip(expressions, numberNotation, literals):
				print('Function:',l)
				print('\t'+e)
				print('\t'+circuit['outputs'][i] + " = " + n)
				print('\tnumber of literals in ' + l + ": " + str(literals[l])+'\n')

		elif funcNum in [5, 7]:
			cExp, _, canon_literals = canonicals(circuit, 'SOP', False)
			mExp, pi_count, epi_count, min_literals = minimize_SOP(circuit)
			mExp = decode(mExp,['*','+'])

			print('DEBUG', mExp)
			for ce, me, cl, ml in zip(cExp, mExp, canon_literals, min_literals):
				print('Function:',cl)
				print('\tCanonical '+ce)
				print('\tMinimized '+me)
				print('\t'+cl+' saved ' + str(canon_literals[cl]-min_literals[ml]) + ' literals')
				print('\tprime implicants in '+cl+': '+str(pi_count))
				print('\tessential prime implicants in '+cl+': '+str(epi_count))
		elif funcNum in [6, 8]:
			cExp, _, canon_literals = canonicals(circuit, 'POS', False)
			mExp, pi_count, epi_count, min_literals = minimize_POS(circuit)
			mExp = decode(mExp,['+','*'])

			print('DEBUG', mExp)
			for ce, me, cl, ml in zip(cExp, mExp, canon_literals, min_literals):
				print('Function:',cl)
				print('\tCanonical '+ce)
				print('\tMinimized '+me)
				print('\t'+cl+' saved ' + str(canon_literals[cl]-min_literals[ml]) + ' literals')
				print('\tprime implicants in '+cl+': '+str(pi_count))
				print('\tessential prime implicants in '+cl+': '+str(epi_count))

				













