import PySimpleGUI as sg
from datetime import date
import pathlib
import glob
import os
import re

# Declarations
tofile = []
today = date.today()
d1 = today.strftime("%d-%m-%Y")

# Window size
size1, size2 = 20, 20
# Conversion for simple math
def convert(args):
    try:
        result = tuple(map(float, args))
        return True, result
    except ValueError:
        return False, 'Wrong number input !'

# Input frame
def input_frame():
    return [
        [sg.Text(item, size=size1, pad=(0, 0)),
         sg.Input('0.00', size=size2, enable_events=True, key=item, expand_x=True)]
        for item in input_items]

# Output frame
def output_frame():
    return [
        [sg.Text(item, size=size1, pad=(0, 0)),
         sg.Input("0.00", size=size2, disabled=True, background_color='CadetBlue1', key=item, expand_x=True)]
        for item in output_items]

def find_last_file_tf():
    dir=os.getcwd()
    dir1 = "*.gp"
    list_of_files = glob.glob(dir1) # means all if need specific format then *.csv
    if not list_of_files:
        return False
    else:
        latest_file = max(list_of_files, key=os.path.getctime)
        if os.path.isfile(latest_file):
            return latest_file


# Dates column
date = ("Date",)

# Left column
# r[0]  = Sales
# r[1]  = Pawn Fees
# r[2]  = Pawn Redeem
# r[3]  = Wholesale / Gift Card
# r[4]  = Register Tax
# r[5]  = Layaways Including Tax
# r[6]  = Total COH
# r[7]  = Purchase
# r[8]  = New Pawns
# r[9]  = Bank Deposits
# r[10] = Cash Pd Out Supplies
# r[11] = Freight + Postage
# r[12] = Yard + Pest Control
# r[13] = Gift Card Redeemed
# r[14] = Misc

input_items = ('Sales', 'Pawn Fees', 'Pawn Redeem', 'Wholesale / Gift Card',
               'Register Tax', 'Layaways Including Tax', 'Total COH', 'Purchase', 'New Pawns', 'Bank Deposits', 'Cash PD Out Supplies', 'Freight & Postage', 'Yard & Pest Control', 'Gift Card Redeemed', 'Misc')

# Right column
output_items = ('Beginning COH', 'Total Register Sales','Layaways', 'Layaway Tax',
                'Total Tax Collected', 'Ending COH', 'Over or Short')

# Theme / font
sg.theme('SandyBeach')
sg.SetOptions(font=('Arial', 10, 'bold'))

# Window layout
layout = [
    [sg.Frame('Input',  input_frame(),  vertical_alignment='top', expand_y=True, expand_x=True),
     sg.Frame('Output', output_frame(), vertical_alignment='top', expand_y=True, expand_x=True)],
    [sg.Text()],
    [sg.Button('Save & Exit', key='Exit')],
]

# Window setup
window = sg.Window('Garys Pawn & Gun', layout, finalize=True)
window.bind("<Return>", "Return")
for item in output_items + ('Exit',):
    window[item].block_focus()

# Event loop
while True:
    event, values = window.read()
    # Hitting exit or close saves to file + closes
    if event in ('Exit',  sg.WIN_CLOSED):
        # f = open("TMP.txt", "w")
        in_list = list(input_items)
        out_list = list(output_items)
        out_list2 = [bcoh, trs, lt, ttc, ecoh, oos]
        with open(d1+".txt"+".gp","w") as f:
            f.write("Input Items:\n") 
            for i in range(0, len(r)):
                # Velocity here is the list
                f.write("{0}\t{1}\n".format(in_list[i],r[i]))
            f.write("\nOutput Items:\n")
            for i in range(0, len(out_list)):
                f.write("{0}\t{1}\n".format(out_list[i],out_list2[i]))
        break
    
    # Enter / tab goes to next cell
    if event == 'Return':
        user_event = window.user_bind_event
        user_event.widget.tk_focusNext().focus()
        user_event.widget.tk_focusNext().select = True
        select = True

    # Math
    else:
        status, r = convert(tuple(map(lambda x: values[x], input_items)))
        if not status:
            window['Status'].update(r)
            continue
        dec=find_last_file_tf()
        if dec == False:
            bcoh = 0.00
        else:
            latest = open(dec)
            content = latest.readlines()
            yesterday_ending = content[23]
            bcoh = float(yesterday_ending[11:])

        layaways=r[5]
        # Total Register Sales = Sales + Layaways
        trs = round(r[0]+layaways, 2)
        # Layaway Tax = Layaways Including Tax - Layaways
        lt = round(r[5]-layaways, 2)
        # Total Tax Collected = Register Tax + Layaway Tax
        ttc = round(r[4] + lt, 2)
        # Ending Cash on Hand = bcoh+sum(trs+ttc+r[2]+r[3]+r[4])-sum(r[7]-r[14])
        leftECOH = [trs, ttc, r[1], r[2], r[3]]
        rightECOH = [r[7], r[8], r[9], r[10], r[11], r[12], r[13], r[14]]
        ecoh = round(bcoh+sum(leftECOH)-sum(rightECOH), 2)
        # Over or Short = Total Cash on Hand - Ending Cash on Hand
        oos = round(r[6]-ecoh, 2)
        for item, value in zip(output_items, (bcoh, trs, lt, ttc, r[6], oos)):
            window[item].update(value)

window.close()
