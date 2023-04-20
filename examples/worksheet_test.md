---
title: Suchen im Internet
schoolname: pmhs
class: TGG11 - INF
author: bug
date: April 4, 2022
panflute-filters: [exercises, infos, solutions, expectations, code_blocks, mc, student_fields, qrcode]
panflute-path: '/Volumes/Data-S1/code/schule/pandoc-education/filters/'
figPrefix:
  - "Abbildung"
  - "Abbildungen"
figureTemplate: '**$$figureTitle$$ $$i$$$$titleDelim$$** $$t$$'
figureTitle: "Abbildung"
---
# Example information text {.info}
This is an info text [https://zumvideo.de]{qrcode=1}. Suchmaschinen, wie zum Beispiel **google.de** oder **duckduckgo.com**, helfen einem oft dabei Fragen zu beantworten und Probleme schnell und selbstständig zu lösen. Dazu sind aber gezielte Suchanfragen und eine Bewertung der Suchergebnisse notwendig. Der QR Code rechts führt zu einem Video, in dem einige Tipps zur Verwendung von Suchmaschinen gezeigt werden. Sieh dir das Video an und mache dir Notizen. [HTML-Tag Namen]{color="orange"}

Here's a citation [@ludlSimpleEfficientRealtime2019].

Or Footnote Style: [^1] Quarks.

[^1]: [@ludlSimpleEfficientRealtime2019]

Marks, hier gehts weiter. 

# Exercise: Image {.exercise time=1}
This is an exercise with an image, which can be referenced as ich schreib hier See the [@fig:qrcode]. Was ist denn hier los?

![This is the caption](qrcodeYouTubeVideo.png){#fig:qrcode}

This is a question: 

[]{lines=4}

::: solution
Das ist die Lösung für Aufgabe 1
:::

# Exercise: Code {.exercise time=3}
```html
<body>
  <h1>Test</h1>
  <a href="pmhs.de">Link</a>
</body>
```

\newpage

# Lösungen
$solutions

\newpage

# References