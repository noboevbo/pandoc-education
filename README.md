# pandoc-education

# Installation
- Clone


# Usage
```bash
pandoc -s -t context --template worksheet.context --filter panflute --filter pandoc-crossref --citeproc --bibliography=literature.bib worksheet.md -o worksheet.pdf
```

# Tipps
## References to figures, tables usw.
We use https://lierdakil.github.io/pandoc-crossref/.

# TODOs:
- HTML Linenumber to Input field: doc.replace_keyword('\linenumbers[n=..]', Str('HTML LINES / BOX WHATEVER'))