#!/usr/bin/env python

"""
Processes code blocks and changes code to t-vim based solution
"""

from panflute import run_filter, CodeBlock, RawBlock, Para
import logging

def action(elem, doc):
    if type(elem) == CodeBlock:
        return process_code_block(elem, doc)

def process_code_block(elem, doc):
    logging.info("Found Code Block")
    logging.info(elem)
    if doc.format != 'context':
        return elem
    return RawBlock(f'\\start{elem.classes[0]}\n{elem.text}\n\\stop{elem.classes[0]}', format="context")

def main(doc=None):
    return run_filter(action, doc=doc)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()