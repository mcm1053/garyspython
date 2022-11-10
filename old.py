# type: ignore

import PySimpleGUI as sg
from datetime import date

# Theme
sg.theme('DarkAmber')

# Variable declaration
today = date.today().strftime("%m/%d/%y")

# Column definition
first_column = [[sg.Text("Date:", size=(21, 1)), sg.Text(today)],
                [sg.Text("Beginning Cash on Hand:",
                         size=(21, 1)), sg.Input(s=15)],
                [sg.Text("Sales:", size=(21, 1)), sg.Input(s=15)],
                [sg.Text("Layaways:", size=(21, 1)), sg.Input(s=15)],

                # TRS output
                [sg.Text("Total Register Sales:", size=(21, 1)),
                 sg.Input(s=15, disabled=True, key="-TRS")],

                [sg.Text("Pawn Fees:", size=(21, 1)), sg.Input(s=15)],
                [sg.Text("Pawn Redeem:", size=(21, 1)), sg.Input(s=15)],
                [sg.Text("Wholesale/Giftcard:", size=(21, 1)), sg.Input(s=15)],
                [sg.Text("Register Tax:", size=(21, 1)), sg.Input(s=15)],

                # LWT output
                [sg.Text("Layaway Tax:", size=(21, 1)),
                 sg.Input(s=15, disabled=True, key="-LWT")],

                [sg.Text("Total Tax Collected:", size=(21, 1)),
                 sg.Text("0", key="-TTC-")],
                [sg.Text("Total:", size=(21, 1)), sg.Text("tmp")]]

second_column = [[sg.Text("Total Cash on Hand:", size=(21, 1)), sg.Text("tmp")],
                 [sg.Text("Purchase:", size=(21, 1)), sg.Input(s=15)],
                 [sg.Text("New Mdde. Purchase:", size=(21, 1)), sg.Input(s=15)],
                 [sg.Text("New Pawns:", size=(21, 1)), sg.Input(s=15)],
                 [sg.Text("Bank Deposits:", size=(21, 1)), sg.Input(s=15)],
                 [sg.Text("Cash PD Out Supplies:", size=(21, 1)),
                  sg.Input(s=15)],
                 [sg.Text("Freight & Postage:", size=(21, 1)), sg.Input(s=15)],
                 [sg.Text("Yard & Pest Control: ", size=(21, 1)),
                  sg.Input(s=15)],
                 [sg.Text("Gift Card Redeemed:", size=(21, 1)), sg.Input(s=15)],
                 [sg.Text("Miscellaneous Expense:", size=(21, 1)),
                  sg.Input(s=15)],
                 [sg.Text("Ending Cash on Hand:", size=(21, 1)),
                  sg.Text("tmp")],
                 [sg.Text("Total:", size=(21, 1)), sg.Text("tmp")]]

bottom_column = [[sg.Text("Layaways Including Tax:"), sg.Text("tmp"),
                  sg.Text("Over or Short:"), sg.Text("tmp"),
                  sg.Text("Pawn Fees:"), sg.Text("tmp")]]

###################
# Column | Column #
# --------------- #
#  Bottom Column  #
# --------------- #
#     Buttons     #
###################
# Layout
layout = [[sg.Column(first_column),
           sg.VerticalSeparator(),
           sg.Column(second_column)],
          [sg.HorizontalSeparator()],
          [sg.Column(bottom_column)],
          [sg.HorizontalSeparator()],
          [sg.Button("Calculate")]]

# Create the window
window = sg.Window("Garys Pawn - Daily Report", layout,
                   element_justification="center", finalize=True)
# window = sg.Window('Garys Pawn - Daily Report', layout, element_justification='center', resizable=True)

# Event loop
while True:
    event, values = window.read()
    status, r = convert(tuple(map(lambda x: values[x], input_items)))
    # End program is window closed
    if event == sg.WIN_CLOSED:
        break
    # On calculate, add required things
    if event == "Calculate":
        # Total Register Sales = Sales + Layaways
        sales = float(values[0])
        layaways = float(values[1])
        trs = round((sales + layaways), 2)
        window['-TRS-'].update(trs)

        # Register Tax + Layaway Tax = Total Tax
        # register_tax = float(values[3])
        # layaway_tax = float(values[4])
        # ttc = round((register_tax + layaway_tax), 2)
        # window['-TTC-'].update(ttc)

# event, values= window.read()
# Do something with the information gathered
# print('Hello', values[0], "! Thanks for trying PySimpleGUI")

# Finish up by removing from the screen
window.close()
