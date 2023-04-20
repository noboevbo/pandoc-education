#!/usr/bin/env python3

"""
Processes exercises
"""

from panflute import run_filter, Span, RawInline, stringify
import logging


def action(elem, doc):
    if type(elem) == Span:
        if "line" in elem.classes:
            return process_line(elem, doc)
        elif "lines" in elem.attributes:
            return process_lines(elem, doc)

def process_line(elem, doc):
    logging.info("DrawLine")
    if doc.format == "latex":
        return RawInline(f'\\drawLineToEOL \\\\~', format="latex")
    return elem

def process_lines(elem, doc):
    logging.info("DrawLines")
    lines = elem.attributes["lines"]
    if doc.format == "latex":
        return RawInline(f'~\\\\ \\drawLines{{{lines}}}\\\\~', format="latex")
    return elem

def main(doc=None):
    return run_filter(action, doc=doc)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
