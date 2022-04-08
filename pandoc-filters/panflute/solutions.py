#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="theorem" to LaTeX
theorem environments in LaTeX output, and to numbered theorems
in HTML output.
"""

from panflute import Div, Header, run_filter, Str
from utils.models import Solution
from utils.helpers import get_exercise_for_element
import logging

def prepare(doc):
    doc.solutions = []

def action(elem, doc):
    if type(elem) == Div:
        logging.info("FOUND DIV")
        if "solution" in elem.classes:
            return process_solution(elem, doc)

def process_solution(elem, doc):
    logging.info("Found Solution Block")
    exercise = get_exercise_for_element(elem, doc)
    doc.solutions.append(Solution(exercise, elem))
    return []

def finalize(doc):
    logging.info("Set solutions")
    div = Div()
    for solution in doc.solutions:
        div.content.extend([Header(Str(f'Lösung: Aufgabe {solution.exercise.id} ({solution.exercise.title})'))])
        div.content.extend([solution.elem])
    
    doc = doc.replace_keyword('$solutions', div)

def main(doc=None):
    return run_filter(action, prepare, finalize, doc=doc)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
