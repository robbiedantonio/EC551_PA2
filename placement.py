'''
LUTS needs to be placed as well as linking to the buses

'''

def input_to_lut_partition(expression, inputs,numInputLUT):
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


if __name__ == "__main__":

    # testing down here

    numLUTs = 8

    inputs1 = ['a', 'b', 'c', 'd', 'e']
    inputs2 = ['a', 'b', 'c', 'd']

    expression1 = '10001 11010 10101 01010, 00010'
    expression2 = '0000 0001 0010 0100 1000 1111'
    lut_mapping, lutCount = input_to_lut_partition(expression1, inputs1, 4)

    print("\033[1mLUT MAPPING\033[0m")
    print(f"Resources used: \033[94m{lutCount/numLUTs * 100}%\033[0m")
    for k,v in lut_mapping.items():
        print(k,v)






