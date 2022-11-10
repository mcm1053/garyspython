import PySimpleGUI as sg
from datetime import date

# Declarations
today = date.today()


def convert(args):
    try:
        result = tuple(map(float, args))
        return True, result
    except ValueError:
        return False, 'Wrong number input !'


def input_frame():
    return [
        [sg.Text(item, size=size1, pad=(0, 0)),
         sg.Input('0.00', size=size2, enable_events=True, key=item, expand_x=True)]
        for item in input_items]


def output_frame():
    return [
        [sg.Text(item, size=size1, pad=(0, 0)),
         sg.Input("0.00", size=size2, disabled=True, background_color='CadetBlue1', key=item, expand_x=True)]
        for item in output_items]


# Window size
size1, size2 = 20, 20

# Dates column
date = ("Date",)

# Left column
# r[0]  = Sales
# r[1]  = Layaways
# r[2]  = Pawn Fees
# r[3]  = Pawn Redeem
# r[4]  = Wholesale / Gift Card
# r[5]  = Register Tax
# r[6]  = Layaways Including Tax
# r[7]  = Purchase
# r[8]  = New Pawns
# r[9]  = Bank Deposits
# r[10] = Cash Pd Out Supplies
# r[11] = Freight + Postage
# r[12] = Yard + Pest Control
# r[13] = Gift Card Redeemed
# r[14] = Misc
input_items = ('Sales', 'Layaways', 'Pawn Fees', 'Pawn Redeem', 'Wholesale / Gift Card',
               'Register Tax', 'Layaways Including Tax', 'Purchase', 'New Pawns', 'Bank Deposits', 'Cash PD Out Supplies', 'Freight & Postage', 'Yard & Pest Control', 'Gift Card Redeemed', 'Misc')

# Right column
output_items = ('Beginning COH', 'Total Register Sales', 'Layaway Tax',
                'Total Tax Collected', 'Ending COH', 'Over or Short')

# Theme / font
sg.theme('SandyBeach')
sg.SetOptions(font=('Arial', 10, 'bold'))

# Window layout
layout = [
    [sg.Input(key='-INPUT-'),
     sg.FileBrowse(file_types=(("TXT Files", "*.txt"), ("ALL Files", "*.*"))),
     sg.Button("Open"),
     ],
    # [sg.Button('Date', button_color='red', key='Open')],
    [sg.Text()],
    [sg.Frame('Input',  input_frame(),  vertical_alignment='top', expand_y=True, expand_x=True),
     sg.Frame('Output', output_frame(), vertical_alignment='top', expand_y=True, expand_x=True)],
    [sg.Text()],
    [sg.Button('Save & Exit', key='Exit')]
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
    # TODO: export to excel sheets based on date
    if event in ('Exit',  sg.WIN_CLOSED):
        f = open("TMP.txt", "w")
        f.write(f"{ecoh}\n")
        f.close()
        break
    # Enter / tab goes to next cell
    if event == 'Return':
        user_event = window.user_bind_event
        user_event.widget.tk_focusNext().focus()
        user_event.widget.tk_focusNext().select = True
        select = True
    if event == 'Open':
        filename = values['-INPUT-']
        if Path(filename).is_file():
            try:
                with open(filename, "rt", encoding='utf-8') as f:
                    text = f.read()
                popup_text(filename, text)
            except Exception as e:
                print("Error: ", e)
    # Math
    else:
        status, r = convert(tuple(map(lambda x: values[x], input_items)))
        if not status:
            window['Status'].update(r)
            continue
        # Total Register Sales = Sales + Layaways
        bcoh = 30909.39
        trs = round(r[0]+r[1], 2)
        # Layaway Tax = Layaways Including Tax - Layaways
        lt = round(r[6]-r[1], 2)
        # Total Tax Collected = Register Tax + Layaway Tax
        ttc = round(r[5] + lt, 2)
        # Ending Cash on Hand = bcoh+sum(trs+ttc+r[2]+r[3]+r[4])-sum(r[7]-r[14])
        leftECOH = [trs, ttc, r[2], r[3], r[4]]
        rightECOH = [r[7], r[8], r[9], r[10], r[11], r[12], r[13], r[14]]
        ecoh = round(bcoh+sum(leftECOH)-sum(rightECOH), 2)
        for item, value in zip(output_items, (bcoh, trs, lt, ttc, ecoh)):
            window[item].update(value)

window.close()
