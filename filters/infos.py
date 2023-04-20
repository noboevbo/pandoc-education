#!/usr/bin/env python

"""
Appends info symbols to headers.
"""

from panflute import RawInline, Header, run_filter
import logging

def action(elem, doc):
    if type(elem) == Header:
        if "info" in elem.classes:
            return process_info_header(elem, doc)

def process_info_header(elem, doc):
        logging.info("Found Info Header")
        logging.info(elem)
        if doc.format == 'context':
            left = RawInline('\\llap{\\symbol[fontawesome-solid][info-circle]~}',  format="context")
            elem.content = [left] + list(elem.content)
        elif doc.format == 'latex':
            left = RawInline('\\margininfo~',  format="latex")
            elem.content = [left] + list(elem.content)
        return elem

def main(doc=None):
    return run_filter(action, doc=doc)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
