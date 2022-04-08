#!/usr/bin/env python

"""
Processes code blocks and changes code to t-vim based solution
"""

from panflute import run_filter, CodeBlock, RawBlock
import logging

def action(elem, doc):
    if type(elem) == CodeBlock:
        return process_code_block(elem, doc)

def process_code_block(elem, doc):
    logging.info("Found Code Block")
    logging.info(elem)
    newel = RawBlock(elem.text, format="context")
    if doc.format == 'context':
        left = RawBlock('\start' + elem.classes[0], format="context")
        right = RawBlock('\stop' + elem.classes[0], format="context")
    else: 
        return
    if left:
        newel.text = left.text + newel.text
    else:
        newel.text = newel.text
    if right:
        newel.text += right.text
    return newel

def main(doc=None):
    return run_filter(action, doc=doc)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()