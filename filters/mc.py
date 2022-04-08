#!/usr/bin/env python

"""
Processes exercises
"""

from panflute import Div, run_filter, Span, stringify, RawBlock
import logging

def action(elem, doc):
    if type(elem) == Div:
        if "mc" in elem.classes:
            return process_mc(elem, doc)

def process_mc_item(elem, doc):
    if type(elem) != Span:
        return
    text = stringify(elem)
    is_correct = bool(elem.attributes["correct"]) if "correct" in elem.attributes else False
    symbol = "check-square" if is_correct else "square"
    logging.info(f'{text} ({is_correct})')
    doc.current_mc_items.append(f'\\startxcell \\symbol[fontawesome-regular][{symbol}]~{text} \\stopxcell')

def process_mc(elem, doc):
    logging.info("Found MC")
    logging.info(elem)
    doc.current_mc_items = []
    cols = int(elem.attributes["cols"]) if "cols" in elem.attributes else 3
    table = f"\\startxtable[width={1/cols}\\textwidth,frame=off]"

    elem.walk(process_mc_item, doc)
    rows = [doc.current_mc_items[i:i + cols] for i in range(0, len(doc.current_mc_items), cols)]
    for row in rows:
        table += "\\startxrow"
        for col in row:
            table += col
        table += "\\stopxrow"
    table += "\\stopxtable"
    return RawBlock(table, format="context")



def main(doc=None):
    return run_filter(action, doc=doc)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()

# \startxtable[option=stretch, frame=off]
#   \startxrow
#     \startxcell \symbol[fontawesome-regular][square]~Here with a longer Text, blabla blabla blabal \stopxcell
#     \startxcell \symbol[fontawesome-regular][square]~Here with a longer Text, blabla blabla blabal \stopxcell
#     \startxcell \symbol[fontawesome-regular][square]~Here with a longer Text, blabla blabla blabal \stopxcell
#   \stopxrow
#   \startxrow
#   \startxcell \symbol[fontawesome-regular][square]~Here \stopxcell
#   \startxcell \symbol[fontawesome-regular][square]~Here \stopxcell
#   \startxcell \symbol[fontawesome-regular][square]~Here \stopxcell
#   \stopxrow
#   \startxrow
#   \startxcell \symbol[fontawesome-regular][square]~Here \stopxcell
#   \startxcell \symbol[fontawesome-regular][square]~Here \stopxcell
#   \stopxrow
# \stopxtable