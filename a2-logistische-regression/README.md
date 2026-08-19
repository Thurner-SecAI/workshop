# Modul A · Kapitel 1.3 — Logistische Regression

Jupyter-Notebook-Challenge zur Folie *Kapitel 1.3 · Logistische Regression*.

Lernziel der Folie: *„Die Teilnehmenden können das Verfahren auf die binäre Klassifikation
übertragen und die Wahrscheinlichkeiten sowie den Schwellenwert interpretieren."*

**Aufgabe im Notebook:** Aus der Größe eines Tumors die Wahrscheinlichkeit schätzen, dass er
bösartig ist.

> ⚠️ Die Daten sind **vollständig synthetisch**. In der Medizin lässt sich Bösartigkeit nicht
> allein aus der Tumorgröße ableiten. Der Hinweis steht auch prominent in der ersten Zelle des
> Notebooks — bitte beim Vorstellen einmal laut sagen.

Das Notebook ist als **Fortsetzung von Kapitel 1.2** gebaut: dieselbe Abschnittsreihenfolge,
dieselben Bausteine, dieselbe Sprache. Am Ende steht eine Vergleichstabelle Linear ↔ Logistisch,
die zeigt: **es sind zwei ausgetauschte Bausteine, kein neues Verfahren.**

---

## Dateien

| Datei | Zweck |
|---|---|
| `logistische_regression.ipynb` | **Fassung für die Teilnehmenden** — 6 Challenges offen |
| `logistische_regression_solved.ipynb` | dieselbe Datei ausgefüllt und ausgeführt, zum Durchklicken |
| `build_logreg.py` | erzeugt beide Notebooks. **Einzige Quelle der Wahrheit für den Inhalt.** |
| `erzeuge_tumordaten.py` | erzeugt `data/tumor_daten.csv` |
| `data/tumor_daten.csv` | 300 synthetische Fälle, 2 Spalten: `tumor_groesse_mm`, `boesartig` |

Die `.ipynb` **nicht direkt bearbeiten** — der nächste Lauf von `build_logreg.py` überschreibt
sie. Ändern, neu bauen, Lösungsfassung ausführen:

```bash
python erzeuge_tumordaten.py     # nur nötig, wenn sich die Daten ändern sollen
python build_logreg.py
jupyter nbconvert --to notebook --execute --inplace logistische_regression_solved.ipynb
```

Der Ausführungslauf ist gleichzeitig der Test: Alle sechs Selbsttests sind `assert`s, ein
Fehler bricht `nbconvert` ab.

---

## Wie die Daten gebaut sind — und warum genau so

Der springende Punkt: Das Label wird **nicht** über eine Regel wie `groesse > 25` gesetzt, denn
dann gäbe es eine scharfe Grenze und das Problem wäre trivial. Stattdessen wird aus der Größe
erst eine Wahrscheinlichkeit berechnet und daraus das Label **gewürfelt**:

```python
score = -5 + 0.2 * tumor_groesse          # 50 % genau bei 25 mm
p     = 1 / (1 + np.exp(-score))
label = np.random.binomial(n=1, p=p)      # <- der entscheidende Schritt
```

Ergebnis ist ein Datensatz mit genau den drei Eigenschaften, auf die es didaktisch ankommt:

| Tumorgröße | Anteil bösartig |
|---|---|
| 0–10 mm | 0 % |
| 10–20 mm | 20,8 % |
| 20–30 mm | 45,8 % |
| 30–40 mm | 76,1 % |
| 40–60 mm | 100 % |

Kleine Tumoren häufiger gutartig, große häufiger bösartig — und dazwischen ein **breiter
Überschneidungsbereich**. Im Datensatz gibt es einen bösartigen Tumor mit 12,6 mm und einen
gutartigen mit 39,0 mm. Genau diese Fälle tragen die Kernaussage: *Es gibt keinen Grenzwert,
also brauchen wir Wahrscheinlichkeiten.*

> 🤐 **Bleibt unter uns.** Im Notebook steht **nicht**, wie die Daten entstanden sind, und schon
> gar nicht die Erzeugungsformel. In einem echten Projekt gibt es keine „wahre" Kurve zum
> Nachschauen — wer sie kennt, für den ist die Übung keine mehr. Das Notebook sagt nur, **dass**
> die Daten synthetisch sind (das gehört bei einem medizinischen Beispiel dazu), nicht wie.
> Wenn du den Ordner an die Teilnehmenden gibst, lass `erzeuge_tumordaten.py` weg — verteile nur
> das Notebook und `data/tumor_daten.csv`.

---

## Aufbau

| Abschnitt | Inhalt | Challenge |
|---|---|---|
| 1 | Regression → Klassifikation, Label, Überblick über die Daten | 1 ⭐ vier Kennzahlen |
| 2 | 0/1-Streudiagramm, Klassenhistogramm, Anteilstabelle → **„Was erkennt ihr?"** | 2 ⭐ Streudiagramm |
| 3 | Train/Test-Split (unverändert aus 1.2) | — |
| 4 | Lineare Regression scheitert (−0,17 / 1,51) → Sigmoid → das Modell | 3 ⭐⭐ `sigmoid()`, 4 ⭐ `wahrscheinlichkeit()` |
| 5 | Warum nicht MSE → Log-Loss, Kostenlandschaft, Gradientenabstieg | 5 ⭐⭐ `log_loss()` |
| 6 | Training, Entscheidungsgrenze, Interpretation von w und b | — |
| 7 | **Schwellenwert**, Konfusionsmatrix, übersehen vs. Fehlalarm | — |
| 8 | Neue Patientin mit 22 mm → 33,8 % → interpretieren | 6 ⭐ Wahrscheinlichkeit schätzen |

(Die Sterne sind eine Einschätzung für die Vorbereitung — im Notebook selbst stehen sie nicht.)

### Die drei Stellen, an denen es im Plenum knallt

1. **Abschnitt 2, Diskussionsfrage.** Erst das Bild zeigen, dann fragen „Was erkennt ihr?" —
   und noch **nichts** über logistische Regression sagen. Die Antworten kommen von selbst:
   größer ist häufiger bösartig, aber es gibt Ausnahmen, und eine perfekte Grenze existiert
   nicht. Damit haben die Teilnehmenden die Motivation selbst formuliert.
2. **Abschnitt 4.** Bewusst zuerst die lineare Regression aus 1.2 auf die 0/1-Spalte werfen. Sie
   sagt für 3 mm „−0,17" und für 60 mm „1,51". Frage in die Runde: *Was soll eine
   Wahrscheinlichkeit von 151 % bedeuten?* Die Sigmoid-Funktion entsteht damit **aus einem
   Problem**, statt einfach präsentiert zu werden.
3. **Abschnitt 7, Schwellenwert.** Bei 0,5 übersieht das Modell 7 von 27 bösartigen Tumoren. Bei
   0,2 nur noch 2 — die Treffergenauigkeit *fällt* dabei von 76,7 % auf 66,7 %. Das schlechtere
   Modell nach Prozentzahl ist das bessere Modell für die Aufgabe. Wer das verstanden hat, hat
   die zweite Hälfte des Lernziels.

---

## Zahlen, auf die sich der Text stützt

Aus `data/tumor_daten.csv` (seed 42) und dem Split mit Zufallszahl 42. Wenn sich die Daten
ändern, müssen sie im Fließtext von `build_logreg.py` mitgezogen werden (sie stehen dort auch im
Modul-Docstring).

| Größe | Wert |
|---|---|
| Fälle | 300, davon 142 bösartig (47,3 %) |
| unter 15 mm / über 35 mm | 8,5 % / 97,4 % bösartig |
| Split | 240 Training (115 bösartig) / 60 Test (27 bösartig) |
| gelerntes `w` / `b` | 0,1775 / −4,5749 |
| Entscheidungsgrenze | 25,8 mm |
| Treffergenauigkeit Test | 76,7 % |
| Vergleichswert: immer „gutartig" | 55,0 % |
| Patientin mit 22 mm | 33,8 % |

---

## Didaktische Entscheidungen

* **Nur ein Merkmal.** Kein Alter, keine Form, keine Dichte. Das Ziel ist die Kette
  *Input → gewichtete Berechnung → Sigmoid → Wahrscheinlichkeit → Schwellenwert → 0/1*.
  Weitere Merkmale würden genau diese Kette verdecken.
* **76,7 % sind kein gutes Modell** — und das Notebook sagt es offen. Der
  Überschneidungsbereich lässt sich nicht wegrechnen, und das ist die Aussage, nicht der Mangel.
* **Gradientenabstieg wieder nur als Idee**, mit dem neuen Hinweis, dass es für die logistische
  Regression *keine* exakte Formel mehr gibt. Wer ihn selbst bauen will, findet das im
  Bonus-Notebook zu Kapitel 1.2.
* **`log_loss()` ohne Clipping.** Die reine Formel ist eine Zeile; dass exakte 0 oder 1 den
  Logarithmus sprengen würden, steht als Warnung in der Lösungsbox. Im Notebook kann es nicht
  passieren — alle verwendeten Kurven bleiben von 0 und 1 weg.
* **Ausblick auf Spam und dann Kapitel 1.4.** Der Schluss zeigt, dass bei mehreren Merkmalen nur
  die Gerade mehr Summanden bekommt, und benennt den Baustein *gewichtete Summe → Sigmoid* als
  das, was in Kapitel 1.4 **Neuron** heißen wird. Die Teilnehmenden haben gerade eines gebaut.
