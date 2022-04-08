---
title: Suchen im Internet
schoolname: pmhs
class: TGG11
context-lang: de
author: bug
date: April 4, 2022
panflute-filters: [exercises, infos, solutions, expectations, code_blocks]
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

This is a question: \hrulefill

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
TODO

# Exercise: Textbox {.exercise time=2}
TODO: Generate Textbox for answers

# Exercise: Table {.exercise time=2}
TODO

# Exercise: Querformat Tabelle {.exercise time=42}
TODO


# Suchanfragen {.exercise time=8}
Du möchtest etwas über die Programmiersprache Rust lernen, dafür suchst du nach "Wie kann ich Rust lernen?". 

- Erkläre wie diese Suchanfrage verkürzt werden kann.  
- Die offizielle Domain der Programmiersprache Rust lautet **rust-lang.org**. Nenne den Befehl, der vor die eigentliche Suchanfrage gesetzt werden, damit nur auf dieser Seite gesucht wird.
- Es gibt auch ein Spiel mit dem Namen **Rust**. Um dieses zu lernen suchst du nach "rust einführung", dir werden aber hauptsächlich Websites zur Programmiersprache Rust angezeigt. Wie könnte die Suchanfrage angepasst werden, damit Suchergebnisse für das Spiel erscheinen?

::: solution
- "rust lernen": Groß- und Kleinschreibung sowie häufig genutzte Wörter und Satzzeichen werden ignoriert und können weggelassen werden.
- site:rust-lang.org
- z.B: rust spiel einführung, rust einführung -programmiersprache, rust game einführung, ...
- Bei Anzeigen steht "Anzeige" vor der URL.
:::

::: expectations
[Das erfüllt]{points=1}
[oder das]{points=2}
[oder dies]{points=3}
:::

# Frage2 {.exercise time=2}
ABC

::: solution
Lösung 2
:::

::: expectations
[Das erfüllt2]{points=1}
[oder das2]{points=2}
[oder dies2]{points=3}
:::

# Frage3 {.exercise time=2}
ABC

::: solution
Lösung 3
:::

::: expectations
[Das erfüllt3]{points=1}
[oder das3]{points=2}
[oder dies3]{points=3}
:::

# Frage4 {.exercise time=2}
ABC

::: solution
Lösung 4
:::


::: expectations
[Das erfüllt4]{points=1}
[oder das4]{points=2}
[oder dies4]{points=3}
:::

# Lösungen
$solutions

# Erwartungshorizont
$expectations

# References