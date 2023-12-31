'''
Copyright 2023 Robbie Dantonio & Muhammed Abdalla
Fall 2023 
ENG EC551
Professor Densmore
'''

import sys
 
from pla_parser import *
from canonicals import *
from minimize import *
from tkinter import *

WIDTH = 1200
HEIGHT = 600

circuit = {}
cExpressions = None
cLiterals = -1
numberNotation = None

mExpression = None
mLiterals = -1

pi_count = -1 
epi_count = -1
    
root = Tk()

# set title
root.title("EC551 Logic Synthesis Tool")
root.config(bg="grey") #bg is background, bd is border, cursor cursor over the frame
root.geometry(f"{WIDTH}x{HEIGHT}")
# size
root.minsize(320, 500)

def canonical(circuit, eForm, inv):
    global cExpressions, numberNotation, cLiterals
    cExpressions, numberNotation, cLiterals = canonicals(circuit, eForm, inv)

def minimize(circuit, eType):
    global mExpression, pi_count, epi_count, mLiterals

    if eType == 'SOP':
        mExpression, pi_count, epi_count = minimize_SOP(circuit)
    elif eType == 'POS':
        mExpression, pi_count, epi_count = minimize_POS(circuit) 
    

def left_pane():
    global root
    global circuit

    def func():
        if eType == 'CAN':
            canonical(circuit, eForm, inv)
        else:
          minimize(circuit, eType)


    left_frame = Frame(root, width=300, height=HEIGHT, bg='white')
    left_frame.grid(row=0,column=0,padx=50, pady=10)

    eType = StringVar()
    eForm = StringVar()
    inv = BooleanVar()
    inv = BooleanVar()

    Label(left_frame, text="Behavioral Analysis").grid(row=1,column=1,padx=5, pady=5)
    Label(left_frame, text="Expression Type:").grid(row=2,column=0,padx=5, pady=5)
    Radiobutton(left_frame, variable=eForm, value="SOP", text="SOP").grid(row=2,column=1,padx=5, pady=5)
    Radiobutton(left_frame, variable=eForm, value="POS", text="POS").grid(row=2,column=2,padx=5, pady=5)

    Label(left_frame, text="Expression Form:").grid(row=3,column=0,padx=5, pady=5)
    Radiobutton(left_frame, variable=eType, value="CAN", text="Canonical Form").grid(row=3,column=1,padx=5, pady=5)
    Radiobutton(left_frame, variable=eType, value="MIN", text="Minimized Form").grid(row=3,column=2,padx=5, pady=5)

    Label(left_frame, text="Inverse: ").grid(row=4,column=0,padx=5, pady=5)
    Radiobutton(left_frame, variable=inv, value=True, text="Yes").grid(row=4,column=1,padx=5, pady=5)
    Radiobutton(left_frame, variable=inv, value=False, text="No").grid(row=4,column=2,padx=5, pady=5)
    Button(left_frame, text="Build Analysis", command=func).grid(row=5,column=1,padx=5, pady=5)
    
    # Label(left_frame, text="Functions").grid(row=4,column=0,padx=5, pady=5)
    # Button(left_frame, text="Delays").grid(row=4,column=1,padx=5, pady=5)
    # Label(left_frame, text="Implicants").grid(row=4,column=1,padx=5, pady=5)

    Label(left_frame, text="Logic Sythesis").grid(row=6,column=0,padx=5, pady=5)
    Label(left_frame, text="FPGA File Entry").grid(row=7,column=0,padx=5, pady=5)
    Entry(left_frame).grid(row=7,column=1,padx=5, pady=5)
    Button(left_frame, text="Run Implementation").grid(row=7,column=2,padx=5, pady=5)
    Button(left_frame, text="Generate Bitstream").grid(row=7,column=3,padx=5, pady=5)



def right_pane():
    global root
    global circuit

    def getFileName():
        # print(file_name.get())
        circuit = parse_file(file_name.get())
        print(circuit)

    global root
    right_frame = Frame(root, width=300, height=HEIGHT, bg='white')
    right_frame.grid(row=0,column=1,padx=5, pady=10)

    Label(right_frame, text="Circuit File").grid(row=2,column=0,padx=5, pady=5)
    file_name = Entry(right_frame)
    file_name.grid(row=2,column=1)

    Button(right_frame, text="Enter", command=getFileName).grid(row=2,column=2,padx=5, pady=5)

    Label(right_frame, text="Functions").grid(row=0,column=0,columnspan=3,padx=5, pady=5)
    functions_list = Listbox(right_frame)
    functions_list.grid(row=1,column=0, columnspan=2,padx=5, pady=5)

    # Label(right_frame, text="Height:").grid(row=1,column=0,padx=50, pady=10)



def pane3():
    global root
    global circuit
    global cLiterals

    right_frame = Frame(root, width=300, height=HEIGHT, bg='white')
    right_frame.grid(row=0,column=2,padx=5, pady=10)

    Label(right_frame, text="Functions:").grid(row=0,column=0,padx=5, pady=5)
    Label(right_frame, text="# literals:").grid(row=1,column=0,padx=5, pady=5)

    if cLiterals:
        literals = cLiterals
        for i, k in enumerate(cLiterals.keys()):
            Label(right_frame, textvariable=f"# literals: {k}").grid(row=1+i,column=0,padx=5, pady=5)
            Label(right_frame, textvariable=f"{cLiterals[k]} literals").grid(row=1+i,column=1,padx=5, pady=5)

left_pane()
right_pane()
pane3()

circuit

root.mainloop()

	