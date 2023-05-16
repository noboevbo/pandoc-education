#!/usr/bin/env python

"""
Processes exercises
"""

from panflute import Div, run_filter, Str, Span, Table, TableBody, TableHead, TableCell, TableRow, Caption, Para, convert_text, TableFoot, RawInline
from utils.helpers import get_exercise_for_element
from utils.models import Expectation, ExerciseExpectation
import logging

def prepare(doc):
    doc.exercise_expectations = []

def action(elem, doc):
    if type(elem) == Div:
        if "expectations" in elem.classes:
            return process_expectations(elem, doc)

def process_expectation(elem, doc):
    if type(elem) != Span:
        return
    points = elem.attributes["points"] if "points" in elem.attributes else 0
    bonus_points = elem.attributes["bonus-points"] if "bonus-points" in elem.attributes else 0
    doc.exercise_expectations[-1].expectations.append(Expectation(elem.content, float(points),  float(bonus_points)))

def add_points_to_exercise(elem, doc, points, bonuspoints):
    elem.attributes["points"] = str(points)
    elem.attributes["bonus-points"] = str(bonuspoints)
    bonus_points_text = f" (+{bonuspoints})" if bonuspoints > 0 else ""
    if doc.format == 'context':
        elem.content = list(elem.content) + [RawInline(f'\\tfxx\\inrightmargin{{\\hl[2] / ~{points}{bonus_points_text} P.}}', format="context")]
    elif doc.format == 'latex':
        elem.content = list(elem.content) + [RawInline(f'\\marginpoints{{{points}{bonus_points_text}}}', format="latex")]
    return elem

def process_expectations(elem, doc):
    logging.info("Found Expectations Block")
    exercise = get_exercise_for_element(elem, doc)
    # TODO: Update exercise with points!
    doc.exercise_expectations.append(ExerciseExpectation(exercise, []))
    elem.walk(process_expectation, doc)
    return []

def write_expectations_table(exercise_expectations, doc):
    header1 = TableCell(*convert_text('Die Schülerin/der Schüler'))
    header2 = TableCell(*convert_text('max. Punkte'))
    header3 = TableCell(*convert_text('erreicht'))
    header_row = TableRow(header1, header2, header3)
    header = TableHead(header_row)
    rows = []
    points = 0
    bonuspoints = 0
    for expectations in exercise_expectations:
        exercise_points = 0
        exercise_bonuspoints = 0
        rows.append(TableRow(TableCell(*convert_text(f"**Aufgabe {expectations.exercise.id}**"), colspan=3)))
        for expectation in expectations.expectations:
            points += expectation.points
            bonuspoints += expectation.bonuspoints
            exercise_points += expectation.points
            exercise_bonuspoints += expectation.bonuspoints
            bonus = "" if expectation.bonuspoints == 0 else f" (+{expectation.bonuspoints})"
            cell1 = TableCell(Para(*expectation.content))
            cell2 = TableCell(*convert_text((f"{expectation.points}{bonus}")))
            cell3 = TableCell()
            rows.append(TableRow(cell1, cell2, cell3))
        add_points_to_exercise(expectations.exercise.elem, doc, exercise_points, exercise_bonuspoints)
    footer1 = TableCell(*convert_text('**Gesamt**'))
    footer2 = TableCell(*convert_text(f"{points} (+{bonuspoints})"))
    footer3 = TableCell()
    footer_row = TableRow(footer1, footer2, footer3)
    footer = TableFoot(footer_row)
    body = TableBody(*rows)
    caption = Caption(Para(Str('Erwartungshorizont')))
    table = Table(body, head=header, foot=footer, caption=caption, colspec=[('AlignDefault', 0.7), ('AlignDefault', 0.18), ('AlignDefault', 0.12)])
    doc.replace_keyword('$expectations', table)

def finalize(doc):
    logging.info("Expectations")
    write_expectations_table(doc.exercise_expectations, doc)

def main(doc=None):
    return run_filter(action, prepare, finalize, doc=doc)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
