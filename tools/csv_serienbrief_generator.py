import csv
import os
import pandas as pd

def read_csv(csv_path):
    return pd.read_csv(csv_path, encoding="ISO-8859-1", index_col=None, header=None)

def main(df):
    row_names = list(df[0])
    students = row_names[0:3]
    results = row_names[-5:]
    criteria = row_names[3:-7]
    for student in df:
        entry = list(df[student])
        
        print(f"Hallo {entry[0]} {entry[1]},")
        print("Im Detail wurde deine Arbeit wie folgt bewertet:")
        print("| Kriterium | Punkte |")
        print("| --- | --- |")
        for id, result in enumerate(entry[3:-7]):
            print(f"| {criteria[id]} | {result} |")

if __name__ == "__main__":
    main(read_csv("/mnt/d/zurcloud/Schule/2022_23/TGG12_INF/22_Publikationen/Projekt/Bewertungsraster.csv"))