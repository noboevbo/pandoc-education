#!/usr/bin/env python

"""
Writes exercise expectations as csv
"""

import csv
from panflute import run_filter, stringify
import logging

def action(elem, doc):
    return elem

def finalize(doc):
    logging.info("Expectations")
    if not doc.exercise_expectations:
        logging.error("Exercise Expectations not found. Run expectations filter before this.")
        return
    
    with open('expectations.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Erwartung", "Punkte", "Bonuspunkte"])
        for expectations in doc.exercise_expectations:
            writer.writerow([f"{expectations.exercise.id}: {expectations.exercise.title}", None, None])
            for expectation in expectations.expectations:
                bonus = "" if not expectation.bonuspoints or expectation.bonuspoints == 0 else f" (+{expectation.bonuspoints})"
                writer.writerow([stringify(expectation.content), expectation.points, bonus])


def main(doc=None):
    return run_filter(action, finalize=finalize, doc=doc)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
