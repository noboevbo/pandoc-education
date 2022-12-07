import csv
import os
import pandas as pd
from string import Template
import pandoc

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

def read_csv(csv_path):
    return pd.read_csv(csv_path, encoding="ISO-8859-1", index_col=None, header=None)

def main(df):
    row_names = list(df[0])
    students = row_names[0:3]
    results = row_names[-5:]
    criteria = row_names[3:-7]
    for student in df:
        if student == 0:
            continue
        entry = list(df[student])
        text = f'''Liebe(r) {entry[0]} {entry[1]},

Im Detail wurde deine Arbeit wie folgt bewertet:


| Kriterium | Punkte |
| --- | --- |
'''

        for id, result in enumerate(entry[3:-7]):
            text += f"| {criteria[id]} | {result} |\n"
        text += f"""| Gesamtpunkte | {entry[-5]} |
| von max. | {entry[-4]} |
| **Notenpunkte** | **{entry[-3]}** |
        
Kommentare: 
        
{entry[-2]}

Für Rückfragen stehe ich gerne zur Verfügung."""
        text = template.substitute(content=text)
        print(text)
        doc = pandoc.read(text, format="markdown")
        pandoc.write(doc, file=f"{entry[0]}_{entry[1]}.pdf", format="latex")

if __name__ == "__main__":
    main(read_csv("/mnt/d/c1o/Schule/2022_23/TGG12_INF/22_Publikationen/Projekt/Bewertungsraster.csv"))