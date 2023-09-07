#!/usr/bin/env python3

"""
Processes exercises
"""

from panflute import run_filter, Span, RawInline, stringify
import logging


def action(elem, doc):
    """
    []{.line}
    []{lines=3}
    []{grid=5 steps=0.5}
    []{box=5}
    """
    if type(elem) == Span:
        if "line" in elem.classes:
            return process_line(elem, doc)
        elif "lines" in elem.attributes:
            return process_lines(elem, doc)
        elif "box" in elem.attributes:
            return process_box(elem, doc)
        elif "grid" in elem.attributes:
            return process_grid(elem, doc)

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
    if doc.format == "context":
        return RawInline(f'\\fillinrules[n={lines}]', format="context")
    return elem

def process_box(elem, doc):
    logging.info("Draw Box")
    box = elem.attributes["box"]
    if doc.format == "latex":
        if "grid" in elem.classes:
            return RawInline(f'~\\\\ \\drawGridBox{{{box}}}\\\\~', format="latex")
        return RawInline(f'~\\\\ \\drawBox{{{box}}}\\\\~', format="latex")

    return elem

def process_grid(elem, doc):
    logging.info("Draw Grid")
    grid = elem.attributes["grid"]
    if doc.format == "latex":
        if "steps" in elem.attributes:
            steps = elem.attributes["steps"]
            return RawInline(f'~\\\\ \\drawGrid[1.0][{steps}]{{{grid}}}\\\\~', format="latex")
    
        return RawInline(f'~\\\\ \\drawGrid[1.0][1.0]{{{grid}}}\\\\~', format="latex")

    return elem

def main(doc=None):
    return run_filter(action, doc=doc)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
