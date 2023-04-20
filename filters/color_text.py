#!/usr/bin/env python3

"""
Processes exercises
"""

from panflute import run_filter, Span, RawInline, stringify
import logging


def action(elem, doc):
    if type(elem) == Span:
        if "color" in elem.attributes:
            return process_color(elem, doc)

def process_color(elem, doc):
    logging.info("Apply color")
    color = elem.attributes["color"]
    if doc.format == "html":
        elem.attributes["style"] = f'color: {color};'
        return elem
    if doc.format == "context":
        logging.info("Set context color")
        text = stringify(elem).replace('""', '')
        return RawInline(f'\\color[{color}]{{{text}}}', format="context")
    if doc.format == "latex":
        logging.info("Set color LaTex")
        text = stringify(elem).replace('""', '') 
        return RawInline(f'\\textcolor{{{color}}}{{{text}}}', format="latex")
    return elem

def main(doc=None):
    return run_filter(action, doc=doc)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
