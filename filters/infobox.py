#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="theorem" to LaTeX
theorem environments in LaTeX output, and to numbered theorems
in HTML output.
"""

from panflute import Div, Header, run_filter, Str, RawBlock
import logging

def prepare(doc):
    doc.solutions = []

def action(elem, doc):
    if type(elem) == Div:
        logging.info("FOUND DIV")
        if "info" in elem.classes:
            return process_info(elem, doc)

def get_context_info(elem):
    # left = RawBlock(f'\\startframedtext[width=\\makeupwidth,frame=off,before=,]\\startframedtext[width=\\makeupwidth,frame=on,background=color,backgroundcolor=noteyellow,corner=round,framecolor=black,rulethickness=1pt]', format="context")
    # right = RawBlock(f'\\stopframedtext\\stopframedtext', format="context")
    left = RawBlock("\\startinformation", format="context");
    right = RawBlock("\\stopinformation", format="context");
    elem.content = [left] + list(elem.content) + [right]
    return elem

def get_latex_info(elem):
    left = RawBlock(f'\\notebox{{', format="latex")
    right = RawBlock(f'}}', format="latex")
    elem.content = [left] + list(elem.content) + [right]
    return elem

def process_info(elem, doc):
    logging.info("Found Info Block")
    if doc.format == 'context':
        elem = get_context_info(elem)
    elif doc.format == 'latex':
        elem = get_latex_info(elem)

    return elem


def main(doc=None):
    return run_filter(action, prepare, doc=doc)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
