'''
LUTS needs to be placed as well as linking to the buses

'''

numLUTInput = 4
numInputs = 5
numLUTs = 8

expression = "AB ADE BCD ACE CDE"
expressionType = "SOP"

def create_switch_matrix(numInputs, numLUTs):
    total_len = numInputs + numLUTs





def map_connection(expression):
    print('expression:', expression)

    queue = []

    for i, term in enumerate(expression.split(' ')):
        queue.append(('AND'+str(i), len(term), list(term)))

    L2Gates = []
    while len(queue) > 0:
        L1Gates = []
        counter = 0
        while len(queue) > 0 and counter < numLUTInput:
            outputName, _, _ = queue.pop()
            L1Gates.append(outputName)
            counter += 1

        if len(queue) > 0:
            queue.append(('LUT'+str(len(L2Gates)), len(L1Gates), L1Gates))
        L2Gates.append(('OR'+str(len(L2Gates)), len(L1Gates), L1Gates))

    print(L2Gates)

map_connection(expression)






