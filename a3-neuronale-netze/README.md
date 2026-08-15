# Modul A · Kapitel 1.4 — Neuronale Netze

Jupyter-Notebook-Challenge zur Folie *Kapitel 1.4 · Neuronale Netze*.

Die Teilnehmenden bauen den **Vorwärtsdurchlauf eines neuronalen Netzes selbst** — ReLU, Softmax,
drei Schichten — trainieren ein Netz auf MNIST und lesen damit eine handgeschriebene
Postleitzahl. Am Ende bewerten sie es ehrlich auf Testdaten und sehen, wo es zusammenbricht.

**Ein Notebook, 7 Challenges, rund 80 Minuten.**

Der Aufbau ist bewusst identisch zu 1.2 und 1.3: Daten → anschauen → Vorverarbeitung → Modell →
Kostenfunktion → Training → Anwendung → ehrliche Prüfung. **Neu ist nur die Modellfunktion.**
Genau das ist die Botschaft des Kapitels, und das Notebook sagt sie an vier Stellen laut.

---

## Dateien

| Datei | Zweck |
|---|---|
| `neuronale_netze.ipynb` | **Hauptnotebook für die Teilnehmenden** — 7 Challenges |
| `neuronale_netze_solved.ipynb` | dieselbe Datei ausgefüllt und einmal durchgelaufen, zum Vorführen |
| `build_nn.py` | erzeugt **beide** Notebooks aus einer Quelle |
| `data/mnist.npz` | 70.000 Ziffernbilder (11 MB) |
| `requirements.txt` | Abhängigkeiten für den lokalen Start |
| `01_digit_recognition_workshop.ipynb` | **alte Fassung (v1, englisch, Keras)** — dient nur noch als Vorlage, kann weg |

> ⚠️ **Die `.ipynb` nicht direkt bearbeiten.** Beide Notebooks werden aus `build_nn.py` erzeugt,
> der nächste Lauf überschreibt sie:
> ```bash
> python build_nn.py
> ```
> Der Vorteil: Teilnehmenden- und Lösungsfassung können nicht auseinanderlaufen. Eine Challenge
> steht genau einmal im Skript, mit beiden Varianten der Code-Zelle direkt nebeneinander.

**Verteilt wird nur `neuronale_netze.ipynb`.** Die CSV-Verteilung von 1.2/1.3 entfällt — das
Notebook lädt MNIST selbst herunter (siehe unten).

Jede Challenge trägt ihre Lösung als zugeklappten `<details>`-Block direkt darunter. Challenge
2–7 haben zusätzlich eine **Selbsttest-Zelle** mit `assert`s. Bei Challenge 1 (ein Diagramm)
geht das nicht sinnvoll — dort ist der Vergleich mit der aufgeklappten Lösung die Kontrolle.

---

## Warum `scikit-learn` und nicht TensorFlow/Keras

Die alte Fassung (`01_digit_recognition_workshop.ipynb`) benutzte Keras. Die neue benutzt
`MLPClassifier` aus `scikit-learn`. Drei Gründe:

1. **Dieselbe Bibliothek wie in 1.2 und 1.3.** Der Wechsel von `LogisticRegression()` zu
   `MLPClassifier()` ist *ein Wort* — und genau das ist die Pointe des Kapitels. Mit einem
   Framework-Wechsel im selben Moment ginge sie unter.
2. **Keine Installation.** TensorFlow sind ~500 MB und auf Apple Silicon regelmäßig eine
   Fehlerquelle. `scikit-learn` liegt schon auf jedem Rechner, der 1.2 gemacht hat.
3. **Es ist schneller.** Das komplette Notebook läuft in **rund 20 Sekunden** durch, das
   Training selbst in etwa 6. Keras bräuchte für dieselbe Architektur ein Vielfaches.

Inhaltlich fehlt dadurch nichts: Dense-Schichten, ReLU, Softmax, Adam, Cross-Entropy, Epochen,
Batch-Größe, Validierungsdaten und Overfitting kommen alle vor — die Kernbausteine sogar als
Handarbeit in den Challenges statt als Keras-Aufruf. Dropout ist der einzige Baustein aus der
v1, der nicht als Code vorkommt; er wird im Overfitting-Abschnitt erklärt.

Alles, was in v1 stand, ist enthalten: MNIST laden, anschauen, normalisieren, flach machen,
One-Hot, Netz bauen, Kostenfunktion, trainieren, Trainingskurve, Testauswertung,
Konfusionsmatrix, Fehlerbilder, häufigste Verwechslungen, Bericht je Ziffer, Modell speichern
und laden.

---

## Start für die Teilnehmenden

### Variante A — Google Colab (nichts zu installieren, empfohlen)

1. [colab.research.google.com](https://colab.research.google.com) → *Datei · Notebook hochladen* →
   `neuronale_netze.ipynb`
2. Loslegen. **Keine Dateien hochladen nötig** — das Notebook lädt MNIST beim ersten Ausführen
   selbst herunter (11 MB, ein paar Sekunden).

### Variante B — lokal

```bash
pip install -r requirements.txt
jupyter lab neuronale_netze.ipynb
```

Liegt `data/mnist.npz` daneben, wird die Datei benutzt; sonst wird sie einmalig heruntergeladen
und neben dem Notebook abgelegt.

> ⚠️ **Wenn das Workshop-WLAN oder ein Firmenproxy den Download blockiert**, verteile
> `data/mnist.npz` vorab mit — das Notebook findet die Datei automatisch in `data/`, `../data/`
> oder direkt neben sich. Das ist der einzige Punkt, an dem der Ablauf am Netz hängt; im Zweifel
> vorher testen.

Der Lauf erzeugt eine Datei `ziffern_netz.joblib` (Abschnitt 9, rund 2,5 MB). Sie ist ein
Wegwerf-Artefakt und über `.gitignore` ausgenommen.

---

## Ablauf im Workshop

| Abschnitt | Inhalt | Challenge | Dauer |
|---|---|---|---|
| 0–1 | Setup, MNIST kennenlernen (▶️ gegeben) | — | 8 Min. |
| 2 | Ein Bild **ist** eine Tabelle aus Zahlen; Ziffern-Raster | 1 Raster | 8 Min. |
| 3 | Normalisieren und flach machen | 2 Vorverarbeitung | 6 Min. |
| 4 | Schichten, ReLU, Softmax, Vorwärtsdurchlauf | 3 `relu()`, 4 `softmax()`, 5 `vorwaerts()` | 24 Min. |
| 5 | One-Hot und Cross-Entropy, Backpropagation als Idee | — | 6 Min. |
| 6 | `MLPClassifier` trainieren, Trainingskurve, gelernte Muster der 1. Schicht | — | 10 Min. |
| 7 | Die Postleitzahl auf dem Umschlag lesen | 6 PLZ | 7 Min. |
| 8 | Testdaten, Overfitting, Konfusionsmatrix, Fehlerbilder, verschobene Ziffern | 7 Trefferquote | 13 Min. |
| 9–10 | Modell speichern, Zusammenfassung über die Kapitel 1.2–1.4 | — | 5 Min. |

Zeitangaben nur für deine Planung — in den Notebooks stehen weder Zeitangaben noch
Schwierigkeitssterne.

**Der Kern liegt in Abschnitt 4.** Wenn die Zeit knapp wird, kürze bei 9 (Speichern) und bei
den Diskussionsfragen in 8 — nicht bei 4.

**Tipp:** Vorher ansagen, dass die Lösungen im Notebook stehen und Aufklappen ausdrücklich
erlaubt ist. Die Funktionen bauen aufeinander auf — wer bei `relu()` hängt, kommt sonst bei
`vorwaerts()` gar nicht erst an.

---

## Die Aha-Momente

Darauf ist das Material gebaut — es lohnt sich, an diesen Stellen bewusst innezuhalten:

1. **Abschnitt 2: Ein Bild ist eine Tabelle aus Zahlen.** Links das Bild, rechts derselbe
   Ausschnitt mit den echten Pixelwerten. Danach ist „Computer Vision" kein eigenes Fachgebiet
   mehr, sondern dieselbe Rechnung wie mit Hauspreisen — nur mit 784 Spalten statt einer.
2. **Abschnitt 4: Ohne Aktivierungsfunktion wäre das Netz sinnlos.** Zwei Geraden hintereinander
   sind wieder eine Gerade. Die Nichtlinearität der ReLU ist buchstäblich das Einzige, was ein
   tiefes Netz von Kapitel 1.2 unterscheidet. (Nachprüfbar im Experimentierfeld:
   `activation="identity"`.)
3. **Abschnitt 4: Das untrainierte Netz trifft zu 10 %.** Es ist vollständig gebaut und rechnet
   fehlerfrei — es weiß nur nichts. Modell und Wissen sind zwei verschiedene Dinge.
4. **Abschnitt 6: Die zwei Trainingskurven widersprechen sich.** Kosten fallen weiter, Treffer
   stagnieren ab Epoche 5. Overfitting live beim Entstehen — und der Grund, warum man
   mitmisst, statt einfach lange zu trainieren.
5. **Abschnitt 6: Die erste Schicht zeigt Striche und Bögen, keine Ziffern.** 128 selbst
   gefundene Teilmuster statt 10 Schablonen. Niemand hat dem Netz gesagt, worauf es achten soll.
6. **Abschnitt 7: Die eigene `vorwaerts()`-Funktion liefert exakt dasselbe wie
   `netz.predict_proba()`** — Abweichung rund 10⁻¹⁹. Die Bibliothek ist keine Magie; der ganze
   Unterschied liegt im Training.
7. **Abschnitt 8: Training 99,5 %, Test 97,7 %.** In Kapitel 1.2 waren beide Zahlen gleich, weil
   zwei Parameter sich nichts merken können. 109.386 können es. Overfitting wird von einer
   Warnung zu einer Messung.
8. **Abschnitt 8: 4 Pixel Verschiebung — und aus 97,7 % werden 37,5 %.** Der Moment, in dem
   klar wird, dass das Netz nicht weiß, was eine 3 *ist*. Beste Brücke zu CNNs. Die
   Verallgemeinerung — ein Modell ist nur so gut wie die Ähnlichkeit von Trainings- und
   Einsatzdaten — steht bewusst **nicht** im Notebook; die ist zum Sagen, nicht zum Lesen.

---

## Typische Stolperfallen

| Stolperfalle | Was passiert | Was hilft |
|---|---|---|
| Zellen nicht der Reihe nach ausgeführt | `NameError` | „Alles von oben neu ausführen" — Colab: *Laufzeit · Alle ausführen* |
| Challenge 3: `np.max` statt `np.maximum` | gibt eine einzelne Zahl zurück statt eines Arrays | `np.max` sucht das Maximum *eines* Arrays, `np.maximum` vergleicht *zwei* elementweise |
| Challenge 4: Klammern verrutscht | `nan` oder Werte, die sich nicht zu 1 addieren | erst `np.exp(z)`, dann durch die Summe **derselben** exp-Werte teilen |
| Challenge 5: `W1 @ x` statt `x @ W1` | `ValueError` über nicht passende Formen | Die Eingabe steht links: `(784,) @ (784, 128) → (128,)` |
| Challenge 5: ReLU auch auf die Ausgabeschicht | Wahrscheinlichkeiten addieren sich nicht zu 1 | Letzte Schicht ist **Softmax**, nur die versteckten bekommen ReLU |
| Challenge 5: `vorwaerts()` mit vielen Bildern gleichzeitig | Ergebnis sieht plausibel aus, ist aber falsch | Unsere `softmax()` normiert über *alles*; die Funktion ist für **ein** Bild gedacht |
| Challenge 2: `.reshape(28*28)` statt `.reshape(-1, 784)` | `ValueError` | `-1` heißt „Zeilenzahl selbst ausrechnen" |
| Challenge 2: durch 255 zu teilen vergessen | Selbsttest schlägt fehl, Training wäre viel schlechter | Ohne Normalisierung explodieren die Zwischenergebnisse |
| `predict_proba(x_test[i])` ohne `.reshape(1, -1)` | sklearn-Fehler über 2D-Arrays | sklearn will immer eine Tabelle *(Zeilen × Merkmale)* — wie in 1.2 |
| Download von `mnist.npz` blockiert | Timeout in Zelle 2 | Datei vorab verteilen, siehe oben |

---

## Ergebnisse zur Kontrolle

Mit `random_state=42` und der Vorverarbeitung `/ 255.0` kommt bei allen dasselbe heraus
(kleine Abweichungen in der letzten Stelle sind je nach BLAS/sklearn-Version möglich —
die `assert`s haben Toleranz).

```
Daten:            60.000 Trainings-, 10.000 Testbilder, 28 × 28, Werte 0–255
Baseline:         immer "1" raten                  11,35 %

Untrainiertes Netz (zufällig initialisiert)
                  Treffer 10,9 %    Cross-Entropy 2,381
                  (blind raten = -log(0,1) = 2,303)

Netz (128, 64), ReLU, Adam, batch_size 128, 15 Epochen    109.386 Parameter
                  Kosten   Epoche 1: 0,347  →  Epoche 15: 0,010
                  Treffer  Epoche 1: 94,0 %  →  Epoche 15: 97,5 %
                  Training 99,49 %   Test 97,70 %   230 Fehler

Challenge 6:      Postleitzahl 10115, Abweichung zu predict_proba() rund 2e-19
Challenge 7:      Test 97,70 %

Häufigste Verwechslungen:  7→9 (15×), 7→2 (12×), 9→4 (12×), 2→8 (9×), 4→9 (9×)
Beste Ziffern:    0 und 1 (je 99,0 %)      schlechteste: 7 (95,9 %) und 9 (96,8 %)

Verschiebung um 4 Pixel:   97,7 %  →  37,5 %

Experimentierfeld:  (8,)        6.370 Parameter   91,87 %
                    (128,)    101.770 Parameter   97,59 %
                    (128, 64) 109.386 Parameter   97,70 %
```

Laufzeit des kompletten Notebooks: **rund 20 Sekunden** (M-Serie, ohne Download). Das Training
selbst dauert etwa 6 Sekunden, das Experimentierfeld am Ende noch einmal 12.

Neu bauen und nachprüfen:

```bash
python build_nn.py
jupyter nbconvert --to notebook --execute --inplace neuronale_netze_solved.ipynb
```

---

## Die Daten

**MNIST** — 70.000 handgeschriebene Ziffern, zusammengestellt von Yann LeCun, Corinna Cortes und
Christopher Burges aus den NIST-Datenbanken. Die Schreibenden waren Angestellte des
US-Volkszählungsamts und amerikanische Schülerinnen und Schüler.

Die Datei `data/mnist.npz` ist die Keras-Fassung des Datensatzes (auf 28 × 28 zentriert und
normiert), gespiegelt unter
`https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz`. Genau diese URL benutzt
das Notebook, wenn die Datei nicht lokal liegt — dieselbe, die auch `keras.datasets.mnist`
aufruft, nur ohne TensorFlow drumherum.

Aufbereitet wurde nichts: Die Bilder gehen unverändert ins Notebook, Normalisieren und
Flachmachen ist Challenge 2.
