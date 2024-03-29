import csv
import os
import pandas as pd
from string import Template
import pandoc
import py7zr
import jellyfish
from pathlib import Path
import numpy as np
import shutil

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

criteria_col_idx = 0
weights_col_idx = 1
max_col_idx = 2

def get_similarity(a, b):
    # print(f"check similarity between {a} and {b}")
    return jellyfish.jaro_distance(a, b)

def get_df(csv_path):
    return pd.read_csv(csv_path, encoding="UTF-8", index_col=None, header=None)

def get_graded_data(graded_files_path, student_name, student_surname, out_dir):
    import os
    full_name = f"{student_name}_{student_surname}"
    most_similar = [0, None]
    for fname in os.listdir(graded_files_path):
        # print(f"Search in: {fname} for {student_name} / {student_surname}")
        if not fname.startswith("K_"):
            continue
        if student_name in fname:
            # print(fname, "has the keyword")
            similarity = get_similarity(fname[2:-4], full_name)
            if similarity > most_similar[0]:
                most_similar[0] = similarity
                most_similar[1] = fname 
    if most_similar[0] > 0.7:
        # print(f"similarity between {full_name} and {most_similar[1]}: {most_similar[0]}")   
        out_path = os.path.join(out_dir, f"Korrektur_{student_name}_{student_surname}.pdf")
        if not os.path.exists(out_path):
            shutil.copy(os.path.join(graded_files_path, most_similar[1]), out_path)

def get_student_cols(df):
    reserved = ["Vorname", "Gew.", "Max", "", None, "Gesamt (Max)"]
    start = -1
    stop = -1
    median = -1
    for idx in df:
        student = df[idx]
        first_row = student[0]
        if first_row == "Median":
            median = idx
            continue
        if pd.isna(first_row) or first_row in reserved:
            continue
        if start == -1:
            start = idx
        stop = idx
    return start, stop, median

def get_start_stop_row(first_col):
    start = 3
    for idx, row in enumerate(first_col):
        if pd.isna(row):
            return start, idx
    

def get_grade_rows(first_col):
    for idx, row in enumerate(first_col):
        if row == "Gesamt (Punkte)":
            return idx, idx+1, idx+2, idx+3

def get_max_points(df, points_row):
    return df[max_col_idx][points_row]

def get_weights(df, start_row, stop_row):
    return df[weights_col_idx][start_row:stop_row]

def get_max_per_criteria(df, start_row, stop_row):
    return df[max_col_idx][start_row:stop_row]

def get_median_per_criteria(df, median_col, start_row, stop_row):
    return df[median_col][start_row:stop_row]

def get_grade_medians(df, median_col, points_row, grade_row):
    median = df[median_col]
    return median[points_row], median[grade_row]

def save_encrypted_7z(files_path, output_path):
    with py7zr.SevenZipFile(os.path.join(output_path, f".7z"), 'w', password='secret') as archive:
        archive.writeall(files_path)

def create_dir_if_not_exists(directory):
    Path(directory).mkdir(parents=True, exist_ok=True)

def main(df, graded_files_path, out_dir):
    criteria_col = df[criteria_col_idx]
    student_start_col, student_stop_col, median_col_idx = get_student_cols(df)
    start_row, stop_row = get_start_stop_row(criteria_col)
    points_row, grade_row, comment_row, invite_row = get_grade_rows(criteria_col)
    name_row, surname_row, email_row = 0, 1, 2
    max_col = df[max_col_idx]
    max_points = get_max_points(df, points_row)
    max_per_criteria = get_max_per_criteria(df, start_row, stop_row)
    median_col = None
    if median_col_idx > -1:
        median_col = df[median_col_idx]
        median_per_criteria = get_median_per_criteria(df, median_col_idx, start_row, stop_row)
        points_median, grade_median = get_grade_medians(df, median_col_idx, points_row, grade_row)
    # row_names = list()
    # students = row_names[0:3]
    # results = row_names[-5:]
    # criteria = first_col[start_row:stop_row]
    for student_idx in df:
        if student_idx < student_start_col:
            continue
        if student_idx > student_stop_col:
            break
        student = df[student_idx]
        if pd.isna(student[grade_row]):
            continue
        name = student[name_row]
        surname = student[surname_row]
        print(f"working on {name} {surname} ({student[grade_row]} / {student[points_row]}")
        text = f'''Liebe(r) {name} {surname},

deine Arbeit wurde wie folgt bewertet:


| Kriterium | Punkte | Von | Median Klasse |
| --- | --- | --- | --- |
'''

        for idx in range(start_row, stop_row):
            median = "-"
            if median_col is not None:
                median = median_col[idx]
            text += f"| {criteria_col[idx]} | {student[idx]} | {max_col[idx]} | {median} |\n"
        median_points_all = "-"
        median_grade_all = "-"
        if median_col is not None:
            median_points_all = median_col[points_row]
            median_grade_all = median_col[grade_row]
        text += f"""| Gesamtpunkte | {student[points_row]} | {max_points} | {median_points_all} |
| **Note** | **{student[grade_row]}** | - | {median_grade_all} |"""
        comments = student[comment_row]
        if not pd.isna(comments):
            text += f"""
            
Kommentare: 
        
{comments}"""
        text += """

Für Rückfragen stehe ich gerne zur Verfügung. Sollte sich die vorliegende Bewertung auf eine Klassenarbeit beziehen wird diese in der nächsten Stunde besprochen.


Herzliche Grüße

Dennis Burgermeister"""
        text = template.substitute(content=text)
        name_wo_spaces = name.replace(" ", "_")
        surname_wo_spaces = surname.replace(" ", "_")
        student_out_dir = os.path.join(out_dir, f"{surname_wo_spaces}_{name_wo_spaces}")
        create_dir_if_not_exists(student_out_dir)
        # print(text)
        get_graded_data(graded_files_path, name, surname, student_out_dir)
        doc = pandoc.read(text, format="markdown")
        pandoc.write(doc, file=os.path.join(student_out_dir, f"Bewertung_{name_wo_spaces}_{surname_wo_spaces}.pdf"), format="latex")
        # TODO: Get PDF Entry

if __name__ == "__main__":
    # noten_csv = get_df("/home/dennis/Vaults/SJ2223/F1ML1/Notenverwaltung.csv")
    # rueckgabe_datei_pfad = "/home/dennis/Vaults/SJ2223/F1ML1/KA1/"
    # output_path = "/home/dennis/Vaults/SJ2223/F1ML1/KA1/rueckgabe"
    noten_csv = get_df("/mnt/d/1BK1T2/PraesiLayout/PraesiLayout.csv")
    rueckgabe_datei_pfad = "/mnt/d/1BK1T2/PraesiLayout"
    output_path = "/mnt/d/1BK1T2/PraesiLayout/rueckgabe"
    main(noten_csv, rueckgabe_datei_pfad, output_path)