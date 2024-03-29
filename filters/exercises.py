#!/usr/bin/env python

"""
Appends exercise and the time to headers.
"""

from panflute import RawInline, Header, run_filter
from utils.models import Exercise
import logging

def prepare(doc):
    doc.exercises = {}
    doc.parts = {}

def action(elem, doc):
    if type(elem) == Header:
        if "exercise" in elem.classes:
            return process_exercise_header(elem, doc)
        
def get_context_elem(elem, exercise_id):
    right = False
    left = RawInline(f'\\llap{{\\getglyphdirect{{ZapfDingbats*dingbats}}{{\\number"270E}}~}}Aufgabe {exercise_id}: ', format="context")
    if "time" in elem.attributes:
        right = RawInline (f'\\wordright{{\\tfx\\symbol[fontawesome-regular][clock]~{elem.attributes["time"]} Minuten}}', format="context")
    elem.content = [left] + list(elem.content)
    if right:
        elem.content += [right]
    return elem

def get_latex_elem(elem, exercise_id):
    right = False
    left = RawInline(f'\\marginexercise Aufgabe {exercise_id}: ', format="latex")
    if "time" in elem.attributes:
        right = RawInline (f'\\hfill\\normalsize\\faIcon[regular]{{clock}} {elem.attributes["time"]}', format="latex")
    elem.content = [left] + list(elem.content)
    if right:
        elem.content += [right]
    return elem

def process_exercise_header(elem, doc):
    logging.info("Found Exercise Header")
    logging.info(elem)
    part = ""
    partname = ""
    if "part" in elem.attributes:
        part = elem.attributes["part"]
        partname = f'{part}.'
    if part not in doc.parts:
        doc.parts[part] = []

    exercise_id = partname + str(len(doc.parts[part])+1)
    elem.attributes["id"] = exercise_id
    doc.parts[part].append(exercise_id)
    exercise_part = str(len(doc.parts[part])+1)
    elem.attributes["part"] = exercise_part

    doc.exercises[exercise_id] = Exercise.get_from_elem(elem)
    
    if doc.format == 'context':
        elem = get_context_elem(elem, exercise_id)
    elif doc.format == 'latex':
        elem = get_latex_elem(elem, exercise_id)

    return elem

def main(doc=None):
    return run_filter(action, prepare, doc=doc)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
