#!/usr/bin/env python3

"""
Processes exercises
"""

from panflute import run_filter, Span, RawInline, stringify
import logging


def action(elem, doc):
    if type(elem) == Span:
        if "qrcode" in elem.attributes:
            return process_color(elem, doc)

def process_color(elem, doc):
    logging.info("Draw QRCode")
    qrcode = elem.content
    if doc.format == "latex":
        return RawInline(f'~\\drawQRCode{{{qrcode}}}', format="latex")
    return elem

def main(doc=None):
    return run_filter(action, doc=doc)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
