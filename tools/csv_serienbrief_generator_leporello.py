import dataclasses
import os
import subprocess
from dataclasses import dataclass

import pandas as pd
from string import Template
import panflute as pf
import py7zr
import jellyfish
from pathlib import Path
import numpy as np
import shutil
import pandoc
import argparse

template = Template('''
---
author:
- Dennis Burgermeister
- PMHS Nürtingen
closing: Herzliche Grüße,
date: 12 December 2022
return-address: 
- "E-Mail: bug@pmhs.de"
fontfamily: mathpazo
fontsize: 12pt
geometry: margin=1in
blockquote: true
closing-indentation: 0pt
links-as-notes: true
colorlinks: true
...

$content''')


def get_df(csv_path):
    return pd.read_csv(csv_path, encoding="UTF-8", index_col=None, header=None)

def get_student_name(df_student_col):
    return f"{df_student_col[0]} {df_student_col[1]}"

def get_next_entry_idx(df_col, curr_idx):
    for row_idx, row_value in enumerate(df_col[curr_idx:]):
        if not pd.isna(row_value):
            return row_idx + curr_idx
    return None

@dataclass
class SubCriteria:
    idx: int
    description: str

@dataclass
class StudentSubCriteria:
    description: str
    points: float
    comment: str

@dataclass
class Criteria:
    name: str
    factors: list[SubCriteria]
    points_idx: int

@dataclass
class StudentCriteria:
    name: str
    factors: list[StudentSubCriteria]
    points: float

def get_sub_criteria(df_col, curr_idx) -> list[SubCriteria]:
    factors = []
    for row_idx, row_value in enumerate(df_col[curr_idx:]):
        if pd.isna(row_value):
            return factors
        factors.append(SubCriteria(row_idx+curr_idx, row_value))
    raise IndexError("no subcriteria found")

def get_criteria(text_col, curr_row_idx):
    criteria_idx = get_next_entry_idx(text_col, curr_row_idx)
    x = text_col[criteria_idx]
    if not criteria_idx or text_col[criteria_idx] == "Gesamtpunkte":
        return None
    sub_criteria = get_sub_criteria(text_col, criteria_idx+1)
    points_idx = sub_criteria[-1].idx + 5
    return Criteria(text_col[criteria_idx], sub_criteria, points_idx)

@dataclass
class GradeInfo:
    criteria: list[Criteria]
    reached_points_idx: int
    max_points_idx: int
    grade_idx: int

@dataclass
class StudentGradeInfo:
    student_criteria: list[StudentCriteria]
    reached_points: float
    max_points: float
    grade: int

def get_grade_info(df):
    text_col = df[0]
    criteria_list = []
    curr_row_idx = 5

    while curr_row_idx < len(df):
        criteria = get_criteria(text_col, curr_row_idx)
        if not criteria:
            break
        criteria_list.append(criteria)
        curr_row_idx = criteria.points_idx+1

    reached_points_idx = get_next_entry_idx(text_col, criteria_list[-1].points_idx+1)
    max_points_idx = reached_points_idx + 1
    grade_idx = max_points_idx + 1
    return GradeInfo(criteria_list, reached_points_idx, max_points_idx, grade_idx)

def get_minus_text(minus_points):
    """ Usually 0 - 3, where 3 is worst """
    if minus_points <= 0.1:
        return None
    if minus_points < 2:
        return "Kleinere Mängel"
    elif minus_points < 3:
        return "Mängel"
    return "Größere Mängel"

def get_student_text(student_name: str, student_grade_info: StudentGradeInfo):
    text = f'''# Bewertungsbogen "Projekt Postkarte"
Name: {student_name}
Punkte: {student_grade_info.reached_points:.0f} / {student_grade_info.max_points:.0f} | Note: **{student_grade_info.grade}**
    '''
    text += '''
| Kriterium | Beschreibung | Punkte |
| --------- | -------------------- | --- |
    '''

    for criteria in student_grade_info.student_criteria:
        text += f"| {criteria.name} | TODO | {criteria.points:.2f} |\n"

    text += "\n# Anmerkungen zu Abzügen\n\n"
    for criteria in student_grade_info.student_criteria:
        text += f"\n## {criteria.name}\n\n"
        for factor in criteria.factors:
            if factor.points <= 0:
                continue
            text += f"- *{factor.description}*: {get_minus_text(factor.points)}"
            if factor.comment and factor.comment != "" and not pd.isna(factor.comment):
                text += f" ({factor.comment})"
            text += "\n"
    return text

def get_student_critieria_factors(factors: list[SubCriteria], points_col: pd.DataFrame, comment_col: pd.DataFrame):
    student_factors: list[StudentSubCriteria] = []
    for factor in factors:
        if pd.isna(points_col[factor.idx]):
            continue
        student_factors.append(StudentSubCriteria(factor.description, float(points_col[factor.idx]), comment_col[factor.idx]))
    return student_factors


def get_student_criteria_list(critiera_list: list[Criteria], points_col: pd.DataFrame, comment_col: pd.DataFrame):
    student_criteria_list = []
    for criteria in critiera_list:
        student_factors = get_student_critieria_factors(criteria.factors, points_col, comment_col)
        student_criteria_list.append(StudentCriteria(criteria.name, student_factors, float(points_col[criteria.points_idx])))
    return student_criteria_list


def get_student_grade_info(grade_info: GradeInfo, points_col: pd.DataFrame, comment_col: pd.DataFrame):
    student_criteria_list = get_student_criteria_list(grade_info.criteria, points_col, comment_col)
    return StudentGradeInfo(student_criteria_list,
                            float(points_col[grade_info.reached_points_idx]),
                            float(points_col[grade_info.max_points_idx]),
                            int(round(float(comment_col[grade_info.grade_idx])))
                            )


def get_grade_string(grade_df, out_dir):
    grade_info = get_grade_info(grade_df)
    curr_student_col = 1
    while curr_student_col < len(grade_df):
        points_col = grade_df[curr_student_col]
        comment_col = grade_df[curr_student_col+1]
        student_name = get_student_name(points_col)
        student_grade_info = get_student_grade_info(grade_info, points_col, comment_col)
        text = get_student_text(student_name, student_grade_info)
        md_path = os.path.join(out_dir, f"{student_name.replace(' ', '_')}.md")
        pdf_path = os.path.join(out_dir, f"{student_name.replace(' ', '_')}.pdf")
        my_env = os.environ.copy()
        my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]
        with open(md_path, "w") as writer:
            writer.write(text)
        result = subprocess.run([f"pandoc -s -t context --template gmtsheet.context {md_path} -o {pdf_path}"], capture_output=True, shell=True)

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(
    #     prog='Leporello Bericht Generator',
    #     description='What the program does',
    #     epilog='Text at the bottom of help')
    # parser.add_argument('filename')
    # args = parser.parse_args()
    # TODO: args.filename
    noten_df = get_df("/Volumes/SJ23_24/GMT12/BewertungsbogenLeporello.csv")
    rueckgabe_datei_pfad = "/Volumes/SJ23_24/GMT12/rueckgabe"
    output_path = "/Volumes/SJ23_24/GMT12/output"
    get_grade_string(noten_df, output_path)
    # main(noten_csv, rueckgabe_datei_pfad, output_path)