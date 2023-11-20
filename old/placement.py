'''
LUTS needs to be placed as well as linking to the buses

'''

def contraints(nInputs, file):
    nLUT = 0
    file = open(file,'r')

    cMatrix = []
    cDict = {}

    for line in file:
        if '.nLUT' in line:
            nLUT = int(line.split(' ')[1].strip())
        if ':LUT' in line:
            t = line.split(' ')
            lut = t[0][1::]
            print(lut, t[1])
        
    for i in range(nInputs+nLUT):
        cMatrix.append([])
        for j in range(nInputs+nLUT):
            cMatrix[i]

    return nLUT, cMatrix


def input_to_lut_partition(expression, inputs, numInputLUT):
    '''
        input: 
            string expression   - one hot encoding representing a boolean expression
            arr<string> inputs  - string array of the input names in order from MSB to LSB
        
        output:
            dictionary LUTs     - key value mapping (adjcency list) of primary inputs to LUTs and LUTs to LUTs; covering partitioning
            int lutCount        - number of required number of LUTs for this configuration
    '''
    print('expression:', expression)

    LUTs = {}
    queue = []
    lutCount = 0

    for term in expression.split(' '):
        # decode to primary inputs
        for i, literal in enumerate(term):
            if literal == '0':
                queue.append(inputs[i]+'\'')
            elif literal == '1':
                queue.append(inputs[i])

        print("queue", queue)

        while len(queue) > 0:
            if not LUTs.get('LUT'+str(lutCount), 0):
                LUTs['LUT'+str(lutCount)] = []

            counter = 0
            while len(queue) > 0 and counter < numInputLUT:
                LUTs['LUT'+str(lutCount)].append(queue.pop(0)) 
                counter += 1  

            if len(queue) > 0:
                queue.append('LUT'+str(lutCount))
            
            lutCount += 1
    
    queue = []
    for k in LUTs.keys():
        queue.append(k)
    
    while len(queue) > 0:
        if not LUTs.get('LUT'+str(lutCount), 0):
            LUTs['LUT'+str(lutCount)] = []

        counter = 0
        while len(queue) > 0 and counter < numInputLUT:
            LUTs['LUT'+str(lutCount)].append(queue.pop(0))
            counter += 1

        if len(queue) > 0:
            queue.append('LUT'+str(lutCount))

        lutCount += 1

    return LUTs, lutCount 

stack = []
pi = {}

def topological_sort(adjList, node):
    global stack
    global pi

    if adjList.get(node, None) == None:
        return
    else:
        while adjList[node]:
            child = adjList[node].pop(0)

            if pi.get(child,0) == 0:
                pi[child] = []

            pi[child].append(node)

            if child in stack:
                continue
            topological_sort(adjList, child)
            
            stack.append(child)

        if node not in stack:
            stack.append(node)

if __name__ == "__main__":

    # testing down here

    numLUTs, cMatrix = contraints('tests/FPGA.pla')

    inputs1 = list('ABCDE')
    inputs2 = ['a', 'b', 'c', 'd']
    inputs3 = list('ABCDEFG')

    expression1 = '11--- 1--11 -111- 1-1-1, --111'
    expression2 = '0000 0001 0010 0100 1000 1111'
    expression3 = '1111111 --11111 11-11-- -11--11'

    lut_mapping, lutCount = input_to_lut_partition(expression1, inputs1, 4)

    print("\033[1mLUT MAPPING\033[0m")
    print(f"Resources used: \033[94m{lutCount/numLUTs * 100}%\033[0m")
    for k,v in lut_mapping.items():
        print(k,v)

    for k in lut_mapping.keys():
        topological_sort(lut_mapping, k)

    for k,v in pi.items():
        print(k,v)
    print(stack)






