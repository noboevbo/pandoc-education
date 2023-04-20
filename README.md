# pandoc-education

# Installation
- Clone


# Usage
```bash
pandoc -s -t context --template worksheet.context --filter panflute --filter pandoc-crossref --citeproc --bibliography=literature.bib worksheet.md -o worksheet.pdf

pandoc -s -t context --template worksheet.context --filter panflute --filter pandoc-crossref --citeproc --bibliography=literature.bib WEBDEV-01-Info-Freie-Schriftarten.md -o WEBDEV-01-Info-Freie-Schriftarten.pdf

 pandoc -s -t latex --template worksheet.latex --pdf-engine=lualatex --filter panflute --filter pandoc-crossref --citeproc --bibliography=literature.bib CAD-AB-03-01_CAD-Technische_Zeichnung_zu_Klemmbaustein.md -o CAD-AB-03-01_CAD-Technische_Zeichnung_zu_Klemmbaustein.pdf
```

# Tipps
## References to figures, tables usw.
We use https://lierdakil.github.io/pandoc-crossref/.

# TODOs:
- HTML Linenumber to Input field: doc.replace_keyword('\linenumbers[n=..]', Str('HTML LINES / BOX WHATEVER'))