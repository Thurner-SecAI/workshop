# Modul A · Kapitel 1.2 — Lineare Regression

Jupyter-Notebook-Challenge zur Folie *Kapitel 1.2 · Lineare Regression*.

Die Teilnehmenden bauen Schritt für Schritt das Grundgerüst eines ML-Modells — Modellfunktion und
Kostenfunktion — und trainieren am Ende ein Modell, das aus der Wohnfläche einen Hauspreis
vorhersagt.

**Ein Hauptnotebook, zwei optionale Bonus-Notebooks:**

| Notebook | Inhalt | Challenges | Dauer |
|---|---|---|---|
| **Haupt** | ein Merkmal, kein schweres Mathe. Gradientenabstieg nur als Idee (Bergabgehen im Nebel), gerechnet wird mit `scikit-learn`. | 7 | 70–80 Min. |
| **Bonus: Mehrere Merkmale** | Bauqualität und Baujahr dazu, Koeffizienten interpretieren | 2 | 25–35 Min. |
| **Bonus: Gradientenabstieg** | den Algorithmus von Hand bauen, inkl. Trainingsschleife | 4 | 45–60 Min. |

Das Hauptnotebook endet mit drei Angeboten: eines der Bonus-Notebooks, oder Kaffee trinken und
den Nachbarn helfen, während die anderen fertig werden.

> ⚠️ **Hinweis zur Folie:** Das Lernziel auf der Kapitelfolie lautet aktuell *„können die
> Trainingsschleife für die lineare Regression implementieren"*. Das passiert im
> **Bonus**-Notebook zum Gradientenabstieg. Für das Hauptnotebook passt eher: *„können den
> Aufbau eines linearen Modells erklären, eine Kostenfunktion selbst schreiben und ein Modell
> trainieren und anwenden"*.

---

## Dateien

| Datei | Zweck |
|---|---|
| `lineare_regression.ipynb` | **Hauptnotebook für die Teilnehmenden** — 7 Challenges |
| `lineare_regression_solved.ipynb` | dieselbe Datei ausgefüllt, zum Durchklicken und Vorführen |
| `bonus_mehrere_merkmale_challenge.ipynb` | Bonus 1 — mehrere Merkmale, 2 Challenges |
| `bonus_gradientenabstieg_challenge.ipynb` | Bonus 2 — Gradientenabstieg selbst gebaut, 4 Challenges |
| `data/haus_preise_einfach.csv` | 21.613 Häuser, 2 Spalten: `wohnflaeche_qm`, `preis_usd` |
| `data/haus_preise_multi.csv` | dieselben Häuser, 4 Spalten: `wohnflaeche_qm`, `qualitaet`, `baujahr`, `preis_usd` |

**Verteilt wird nur `lineare_regression.ipynb`** plus die beiden CSVs. Die `_solved`-Fassung ist
für dich: zum Vorführen, zum Nachschlagen und um zu sehen, was am Ende herauskommen soll.

Jede Challenge trägt ihre Lösung zusätzlich selbst — als zugeklappten `<details>`-Block direkt
darunter. Wer feststeckt, kommt allein weiter, statt zu warten oder in der Kette hängen zu
bleiben (die Funktionen bauen aufeinander auf).

Beide Bonus-Notebooks sind **eigenständig lauffähig** und unabhängig voneinander — sie setzen
nur das Hauptnotebook voraus und bringen alles Nötige selbst mit.

---

## Start für die Teilnehmenden

### Variante A — Google Colab (nichts zu installieren, empfohlen)

1. [colab.research.google.com](https://colab.research.google.com) → *Datei · Notebook hochladen* →
   `lineare_regression.ipynb`
2. Links auf das Ordner-Symbol klicken und **beide CSVs** aus `data/` per Drag & Drop hochladen.
   (Falls das vergessen wird, fragt das Notebook selbst nach dem Upload.)
3. Loslegen.

Das Repository ist privat — ein Laden per URL funktioniert also nicht. Am einfachsten stellst du
den Teilnehmenden vorab einen Ordner mit den Notebooks und den zwei CSVs bereit
(Download-Link, USB-Stick oder geteilter Drive-Ordner).

### Variante B — lokal

Die Pakete stehen zentral in der `requirements.txt` im Wurzelverzeichnis des Repos — einmal
`pip install -r requirements.txt` dort, dann laufen alle Ordner. Danach:

```bash
jupyter lab lineare_regression.ipynb
```

Das Notebook findet die CSVs automatisch, solange der Ordner `data/` daneben liegt.

---

## Ablauf im Workshop

### Hauptnotebook

| Abschnitt | Inhalt | Challenge | Dauer |
|---|---|---|---|
| 0–1 | Setup, Daten kennenlernen (▶️ gegeben) | — | 8 Min. |
| 2 | Histogramm und Streudiagramm — je Erklärung, Beispielcode, eigene Umsetzung | 1 Histogramm, 2 Streudiagramm | 15 Min. |
| 3 | Train/Test-Split (▶️ gegeben) | — | 5 Min. |
| 4 | Modellformel `w·x + b`, drei Geraden raten | 3 `vorhersage()` | 10 Min. |
| 5 | Kostenfunktion: MSE, dann RMSE in Dollar, Kostenlandschaft | 4 `mse()`, 5 `rmse()` | 18 Min. |
| 6 | Gradientenabstieg als **Idee**, dann `scikit-learn` | — | 10 Min. |
| 7 | Das fertige Modell anwenden: ein Haus kommt auf den Markt | 6 Preis schätzen | 8 Min. |
| 8 | Testdaten: RMSE auf ungesehenen Häusern, Overfitting, MAE / R² / Baseline | 7 Test-RMSE | 10 Min. |
| 9 | Zusammenfassung, Brücke zu Kap. 1.3/1.4, Wahl des Bonus | — | 5 Min. |

Zeitangaben nur für deine Planung — in den Notebooks stehen weder Zeitangaben noch
Schwierigkeitssterne.

Challenge 3–7 haben eine **Selbsttest-Zelle** mit `assert`s: sofort `✅`, wenn es stimmt. Bei 1
und 2 geht das nicht sinnvoll — ein Diagramm lässt sich schlecht per `assert` prüfen, dort ist
der Vergleich mit der aufgeklappten Lösung die Kontrolle.

Wo es einen Selbsttest gibt, steht die Lösung **darunter**, nicht darüber: erst das grüne
Häkchen versuchen, die Lösung ist das Auffangnetz.

Der Aufbau in Abschnitt 2 ist bei beiden Diagrammen gleich: kurze Erklärung, was das Diagramm
beantwortet → **Beispielcode** (Wohnfläche bzw. 200 Häuser), der einfach ausgeführt wird → die
Challenge, dasselbe für die eigentliche Spalte zu bauen → Lösung zum Aufklappen.

**Tipp:** Vorher ansagen, dass die Lösungen im Notebook stehen — sonst suchen die Leute danach.
Und dazusagen, dass Aufklappen ausdrücklich erlaubt ist; es geht ums Verstehen, nicht ums
Nicht-Schummeln.

### Die Bonus-Notebooks

Gedacht für alle, die früher fertig sind — und als Material zum Mitnehmen. Beide sind unabhängig,
die Reihenfolge ist egal. Wer keine Lust hat, hilft laut Notebook lieber den Nachbarn oder macht
Pause; das ist ausdrücklich als gleichwertige Option formuliert.

---

## Die Aha-Momente

Darauf ist das Material gebaut — es lohnt sich, an diesen Stellen bewusst innezuhalten:

**Hauptnotebook**

1. **Abschnitt 5: Die Kostenlandschaft ist eine Schüssel.** Damit wird „gut" von Geschmackssache
   zu einer Zahl, die man minimieren kann. Ab hier ist Training kein Zauber mehr, sondern Suche.
2. **Abschnitt 5: Der MSE ist unlesbar, der RMSE nicht.** 69 Milliarden quadrierte Dollar sagen
   niemandem etwas — eine Wurzel später steht dort „263.328 USD daneben". Dieselbe Information,
   plötzlich verhandelbar. Die Teilnehmenden bauen `rmse()` auf ihrer eigenen `mse()` auf.
3. **Abschnitt 6: `scikit-learn` schlägt jeden geratenen Wert** — mit *ihrer eigenen*
   MSE-Funktion nachgerechnet.
4. **Abschnitt 7: Zwei Zahlen genügen.** Das fertige Modell ist nichts als `w` und `b` — und die
   eigene `vorhersage()`-Funktion liefert exakt dasselbe wie `modell.predict()`. Das Exposé
   listet Grundstück, Baujahr, Garage, Lage; das Modell sieht nichts davon. Genau das ist die
   Brücke zum Bonus-Notebook.
5. **Abschnitt 8: Training 260.356, Test 265.763 — kein Unterschied.** Genau *deshalb* trennt man
   vorher. Das Modell ist zu klein, um sich etwas zu merken; die Lücke zwischen beiden Zahlen ist
   das, worauf man bei jedem größeren Modell schaut. Overfitting wird hier greifbar, ohne dass man
   es vorführen muss.
6. **Abschnitt 8: R² 0,49 ist gleichzeitig ein Erfolg und ein Reinfall.** Klar besser als die
   Baseline, als Maklerwerkzeug wertlos. „Ist das gut?" hat keine Antwort ohne „verglichen womit?".

**Bonus: Mehrere Merkmale**

7. **Der Baujahr-Koeffizient ist negativ.** Ältere Häuser sind laut Modell teurer. Perfekter
   Aufhänger für Korrelation vs. Kausalität und für die Frage, was ein fehlendes Merkmal (hier:
   die Lage) mit einem Modell anstellt.
8. **Zwei Merkmale bringen mehr als die Summe ihrer Einzelbeiträge** (+0,03 und +0,03 einzeln,
   aber +0,09 zusammen). Merkmale einzeln zu bewerten führt in die Irre.

**Bonus: Gradientenabstieg**

9. **Das erste Training explodiert.** Mit Lernrate 0.1 auf Rohdaten laufen `w` und `b` in acht
   Schritten nach 10³⁵. Feature Scaling kommt erst *danach* — als Lösung für ein Problem, das man
   gerade selbst gesehen hat, nicht als Rezept vorab.
10. **Die Gegenprobe.** Selbst gebauter Gradientenabstieg und `LinearRegression` liefern auf zwei
   Nachkommastellen dieselben Werte (2.999,93 USD/m²). Der Beweis, dass „die Bibliothek" keine
   Magie ist.

---

## Typische Stolperfallen

| Stolperfalle | Was passiert | Was hilft |
|---|---|---|
| Zellen nicht der Reihe nach ausgeführt | `NameError` | „Alles von oben neu ausführen" — Colab: *Laufzeit · Alle ausführen* |
| `mse` mit vertauschten Argumenten | Selbsttest läuft trotzdem durch (Quadrat!) | Kein Problem — mathematisch identisch |
| `rmse` ohne `float(...)` | Selbsttest läuft durch, Ausgabe sieht nur unschöner aus | Kein Fehler; `float()` ist Kosmetik |
| `.reshape(-1, 1)` bei einem Merkmal vergessen | sklearn-Fehler über 2D-Arrays | sklearn will immer eine Tabelle *(Zeilen × Merkmale)* |
| `.predict(165)` statt `.predict([[165]])` | TypeError | `.predict()` erwartet eine Liste von Häusern |
| Bonus Merkmale: `.reshape` *zusätzlich* benutzt | Formfehler | `X_train` ist bereits eine Tabelle |
| Bonus Gradient: `+` statt `−` im Update | Kosten steigen statt zu fallen | Der Gradient zeigt *bergauf* — wir gehen in die Gegenrichtung |
| Bonus Gradient: auf `x_train` statt `x_train_s` trainiert | explodiert | Trainiert wird auf den skalierten Daten |

---

## Ergebnisse zur Kontrolle

Mit der fest eingestellten Zufallszahl 42 kommt bei allen dasselbe heraus.

**Hauptnotebook**

```
Drei geratene Geraden (Trainingsdaten):
  w=1000, b=0          MSE 217.949.045.990    RMSE 466.850 USD
  w=3000, b=0          MSE  69.341.807.735    RMSE 263.328 USD
  w=5000, b=-200000    MSE 148.395.534.830    RMSE 385.221 USD

Kostenkurve (b = 0 festgehalten):   bestes w ≈ 2.834 USD/m²

Trainiertes Modell:  Preis = 2.999,93 · Wohnfläche − 39.437,30
                     MSE auf den Trainingsdaten: 67.785.388.980

Challenge 6, Haus mit 165 m²  →  455.550,62 USD

Challenge 7:         RMSE Training 260.356 USD   RMSE Test 265.763 USD

Testdaten (4.323 Häuser):
  Baseline (Mittelwert)   MAE 232.181 USD   RMSE 373.657 USD   R² −0,000
  Dein Modell (Fläche)    MAE 171.530 USD   RMSE 265.763 USD   R²  0,494
```

**Bonus: Mehrere Merkmale**

```
3 Merkmale:  +1.881 USD pro m²
             +145.356 USD pro Qualitätsstufe
             −3.713 USD pro Baujahr
             Test:  MAE 148.976 USD   RMSE 240.436 USD   R² 0,586
             Haus mit 140 m², Qualität 8, Baujahr 1995 → 400.729 USD

Nur Fläche         R² 0,494
Fläche + Qualität  R² 0,528     Fläche + Baujahr  R² 0,521
```

**Bonus: Gradientenabstieg** — auf zwei Nachkommastellen identisch mit `scikit-learn`
(2.999,93 USD/m² und −39.437,30 USD nach 200 Epochen mit Lernrate 0.1).

---

## Die Daten

Quelle: [House Pricing Dataset](https://www.kaggle.com/datasets/alyelbadry/house-pricing-dataset)
auf Kaggle — 21.613 tatsächliche Hausverkäufe im King County (Seattle) aus den Jahren 2014/2015.

Für den Workshop aufbereitet: Wohnfläche von Quadratfuß in **Quadratmeter** umgerechnet
(× 0,0929), Preise in **US-Dollar** belassen, keine Zeilen entfernt — Ausreißer inklusive, die
gehören zur Realität und sind Diskussionsstoff.

`qualitaet` ist der *grade* aus dem Originaldatensatz: ein Index der Bauaufsicht des King County
von 1 (einfachste Bauweise) bis 13 (luxuriös).

Beide CSVs liegen fertig in `data/` — es gibt keinen Aufbereitungsschritt mehr im Ordner.
