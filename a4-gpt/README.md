# Modul A · Kapitel 2 — Large Language Models

Die Teilnehmenden bauen die Bausteine eines Decoder-Only-Transformers selbst, trainieren daraus
ein kleines GPT auf Goethes *Faust* und lassen es deutsche Verse schreiben.

Vier Notebooks, im Wechsel mit den Folien. Jedes läuft eigenständig — Abschnitt 0 bringt die
Bausteine der vorherigen Teile fertig mit.

| Notebook | Inhalt | Challenges |
|---|---|:--:|
| [`teil1.ipynb`](teil1.ipynb) | Tokenizer, Byte Pair Encoding, Word Embedding, Positional Encoding | 4 |
| [`teil2.ipynb`](teil2.ipynb) | Kausale Maske, Query/Key/Value, Aufmerksamkeitskopf, mehrere Köpfe | 1 |
| [`teil3.ipynb`](teil3.ipynb) | Feed-Forward, Skip Connection, Norm Layer, Block, MiniGPT | 4 |
| [`teil4.ipynb`](teil4.ipynb) | Batches, Cross-Entropy, Training, Textgenerierung | 3 |

Zu jedem Teil liegt eine `_solved.ipynb` daneben: dieselbe Datei ausgefüllt und einmal
durchgelaufen, zum Vorführen. **Verteilt wird nur die Fassung ohne `_solved`.**

## Starten

In Google Colab hochladen und loslegen — für Teil 4 den Laufzeittyp *T4 GPU* wählen, sonst dauert
das Training mehrere Minuten. Lokal:

```bash
pip install "torch>=2.2" "numpy>=1.26" "matplotlib>=3.8" jupyterlab
jupyter lab teil1.ipynb
```

Den Faust-Text lädt Abschnitt 0 beim ersten Lauf selbst von Project Gutenberg und legt ihn als
`faust.txt` ab.

## Gemeinsame Einstellungen

Alle vier Teile rechnen mit `KONTEXT=96`, `BATCH=32`, `N_EMBD=96`, `N_HEAD=4`, `N_LAYER=3`,
`DROPOUT=0.1`, `SCHRITTE=3000`, `LERNRATE=1e-3` und `torch.manual_seed(1337)`.

Die Bezeichner `kodiere`, `dekodiere`, `Kopf`, `MehrereKoepfe`, `FeedForward`, `Block` und
`MiniGPT` ziehen sich durch alle Teile. Wer einen davon umbenennt, bricht die späteren Notebooks.
