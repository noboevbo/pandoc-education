#!/usr/bin/env python3

"""
Processes exercises
"""

from panflute import run_filter, Div
import logging


def action(elem, doc):
    if type(elem) == Div:
        if "framed" in elem.classes:
            return add_frame(elem, doc)

def add_frame(elem, doc):
    logging.info("Add frame")
    if doc.format == "html":
        elem.attributes["style"] = f'border: 1px black solid;'
    # if doc.format == "context": % TODO: not that easy ...
    #     elem.content = [RawInline(f'\\framed{{', format="context")] + list(elem.content) + [RawInline("}", format="context")]
    return elem

def main(doc=None):
    return run_filter(action, doc=doc)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
