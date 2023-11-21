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

tool_frame_dict = {
    "HOME":[200,50],
    "Behavioral Analysis":[200,50],
}
    
root = Tk()

# set title
root.title("EC551 Logic Synthesis Tool")
root.config(bg="grey") #bg is background, bd is border, cursor cursor over the frame
root.geometry(f"{WIDTH}x{HEIGHT}")
# size
root.minsize(320, 500)

def canonical(circuit, eForm, inv):
    expressions, numberNotation = canonicals(circuit, eForm, inv)

def minimize(circuit, eForm):
    expression, pi_count, epi_count

    if eForm == 'SOP':
        expression, pi_count, epi_count = minimize_SOP(circuit)
    elif eForm == 'POS':
        expression, pi_count, epi_count = minimize_POS(circuit) 
    
    return expression, pi_count, epi_count

def left_pane():
    global root
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
    Button(left_frame, text="Build Analysis").grid(row=5,column=1,padx=5, pady=5)
    
    # Label(left_frame, text="Functions").grid(row=4,column=0,padx=5, pady=5)
    # Button(left_frame, text="Delays").grid(row=4,column=1,padx=5, pady=5)
    # Label(left_frame, text="Implicants").grid(row=4,column=1,padx=5, pady=5)

    Label(left_frame, text="Logic Sythesis").grid(row=6,column=0,padx=5, pady=5)
    Label(left_frame, text="FPGA File Entry").grid(row=7,column=0,padx=5, pady=5)
    Entry(left_frame).grid(row=7,column=1,padx=5, pady=5)
    Button(left_frame, text="Run Implementation").grid(row=7,column=2,padx=5, pady=5)
    Button(left_frame, text="Generate Bitstream").grid(row=7,column=3,padx=5, pady=5)



def right_pane():
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
    right_frame = Frame(root, width=300, height=HEIGHT, bg='white')
    right_frame.grid(row=0,column=2,padx=5, pady=10)

    Label(right_frame, text="Functions:").grid(row=0,column=0,columnspan=3,padx=5, pady=5)
    Label(right_frame, text="# literals:").grid(row=1,column=0,columnspan=3,padx=5, pady=5)
    # Label(right_frame, textvariable=).grid(row=1,column=1,columnspan=3,padx=5, pady=5)

left_pane()
right_pane()
pane3()

circuit

root.mainloop()

	