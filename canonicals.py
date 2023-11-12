'''
Copyright 2023 Robbie Dantonio & Muhammed Abdalla
Fall 2023 
ENG EC551
Professor Densmore
'''


def canonicals(circuit, operation, inverse=False):
    iterms = circuit['inputs']
    oterms = circuit['outputs']
    title = "\n"

    op = "*+"
    if operation == "SOP":
        title += "CANONICAL SUM OF PRODUCTS"
    elif operation == "POS":
        op = "+*"
        title += "CANONICAL PRODUCT OF SUMS"
    
    '''
    SOP noInv   -> 1' *+
    POS noInv   -> 0's +*
    SOP Inv     -> 0's *+
    POS Inv     -> 1's +*
    '''
    
    if inverse:
        title += " INVERSE"

    print(title)

    numberNotation = []
    expressions = []
    for i in range(circuit['noutputs']):
        expressions.append([])
        numberNotation.append([])

    for v in circuit['marked_terms']:
        func, outputBitIndex, binary = v
        term = []
        for j, bit in enumerate(binary):
            # if the tuple contains a minterm, and the operation is SOP then
            # concat ' for OFF and normal for ON
            # else if the tuple contains a MAXTERM and the operation is POS then
            # concat ' for ON and normally for OFF
            if func == '1':
                if not inverse and operation == "SOP" or inverse and operation == "POS":
                    if bit == '0':
                        term.append(iterms[j]+'\'')
                    elif bit == '1':
                        term.append(iterms[j])
            elif func == '0':
                if inverse and operation == "SOP" or not inverse and operation == "POS":
                    if bit == '1':
                        term.append(iterms[j]+'\'')
                    elif bit == '0':
                        term.append(iterms[j])
        
        if term == []:
            continue
        
        t = "("+op[0].join(term)+")"
        numberNotation[outputBitIndex].append(str(int(binary)))
        expressions[outputBitIndex].append(t)
        # print(func, outputBitIndex, binary)
        # print(outputBitIndex, expressions[outputBitIndex])

    for i,expression in enumerate(expressions):
        expressions[i] = oterms[i]+"="+op[1].join(expression)

    for i,num in enumerate(numberNotation):
        notation = "Sigma" if operation == "SOP" else "PI"
        numberNotation[i] = "{}(".format(notation)+",".join(num)+")"

    for e,n in zip(expressions,numberNotation):
        print(e,n)
    print('\n')

    # print(expressions, numberNotation)
    # each expression and notation are big-edian bit index of the output
    return {'expressions':expressions, 'one_hot':numberNotation}