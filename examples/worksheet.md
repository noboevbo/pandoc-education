---
title: Suchen im Internet
schoolname: pmhs
class: TGG11
context-lang: de
author: bug
date: April 4, 2022
panflute-filters: [exercises, infos, solutions, expectations, code_blocks, mc]
panflute-path: '/home/dennis/code/lehre/pandoc-education/filters/'
figPrefix:
  - "Abbildung"
  - "Abbildungen"
figureTemplate: '**$$figureTitle$$ $$i$$$$titleDelim$$** $$t$$'
figureTitle: "Abbildung"
---
# Example information text {.info}
This is an info text. Suchmaschinen, wie zum Beispiel **google.de** oder **duckduckgo.com**, helfen einem oft dabei Fragen zu beantworten und Probleme schnell und selbstständig zu lösen. Dazu sind aber gezielte Suchanfragen und eine Bewertung der Suchergebnisse notwendig. Der QR Code rechts führt zu einem Video, in dem einige Tipps zur Verwendung von Suchmaschinen gezeigt werden. Sieh dir das Video an und mache dir Notizen.

Here's a citation [@ludlSimpleEfficientRealtime2019].

Or Footnote Style: [^1] Quarks.

[^1]: [@ludlSimpleEfficientRealtime2019]

Marks, hier gehts weiter.

# Exercise: Image {.exercise time=1}
This is an exercise with an image, which can be referenced as ich schreib hier See the [@fig:qrcode]. Was ist denn hier los?

![This is the caption](qrcodeYouTubeVideo.png){#fig:qrcode}

This is a question: \thinrule

# Exercise: Code {.exercise time=3}
```html
<body>
  <h1>Test</h1>
  <a href="pmhs.de">Link</a>
</body>
```

::: solution
```html
<body>
  /BTEX\yellowmarker{/ETEX<h1>/BTEX}/ETEXTest</h1>
  <a href="pmhs.de">Link</a>
</body>
```
:::

# Exercise: Lines {.exercise time=3}
Put lines for students. 

- Question 1. \thinrule
- Question 2. \fillinrules[n=2]
- Question 3?  \fillinrules[n=4]

::: solution
- Answer 1
- Answer 2
- Answer 3
:::


# Exercise: Textbox {.exercise time=2}
Adding a textbox for student answers:

&nbsp;

\framed[width=broad, height=5cm]{}

# Exercise: Multiple choice {.exercise time=2}
This is a multiple choice question

::: {.mc n=3}
[Choice A]{}
[Choice B]{}
[Choice C]{}
[Choice D]{}
[Choice E]{}
:::

::: solution
::: {.mc n=3}
[Choice A]{correct=true}
[Choice B]{}
[Choice C]{}
[Choice D]{}
[Choice E]{correct=true}
:::
:::

# Exercise: Table {.exercise time=2}
TODO

# Exercise: Querformat Tabelle {.exercise time=42}
TODO

\page
# Lösungen
$solutions

\page
# References