# Modul B · Kapitel 4 — Deployment und Inference

Fünf kurze Notebooks führen von der Model Card bis zur begründeten
Modellauswahl. Am Ende kannst du entscheiden, welches Modell in welcher
Präzision auf welcher Hardware mit welcher Runtime läuft — auf Basis eigener
Rechnungen und Messungen.

## Die Notebooks

| Notebook | Thema | Das kannst du danach | Ollama nötig |
|---|---|---|:--:|
| `01_model_cards` | Speicherbudget | Gewichtsspeicher berechnen und ein vollständiges VRAM-Budget prüfen | teilweise |
| `02_quantisierung` | Präzision | einfache und blockweise Quantisierung verstehen und den Fehler messen | **nein** |
| `03_runtime_und_api` | Runtime und Zugriff | einen portablen Client bauen und Streaming messen | ja |
| `04_durchsatz_und_last` | Leistung unter Last | Messreihen auswerten und Kapazität planen | ja |
| `05_modellauswahl` | Auswahl | Modelle fair evaluieren und mit einer klaren Regel auswählen | ja |

Jedes Notebook hat denselben Aufbau: Begriff verstehen, Rechnung oder Messung
durchführen und das Ergebnis für eine Deployment-Entscheidung nutzen. Pro
Notebook gibt es genau zwei Kernaufgaben; Hilfs- und Visualisierungscode ist
vorgegeben. Die Reihenfolge ist sinnvoll, aber keine Pflicht.

## Setup

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m jupyter lab
```

Prüfen, ob die gemeinsamen Funktionen und die Daten gefunden werden:

```bash
.venv/bin/python helfer.py
```

## Ollama

Vier der fünf Notebooks messen an einem laufenden Modell. Ohne Ollama laufen
sie nicht durch — die Zellen brauchen echte Antworten, keine erfundenen.
`02_quantisierung` ist die Ausnahme: Es rechnet mit PyTorch direkt auf den
Gewichten eines kleinen Modells von Hugging Face und braucht keinen Modellserver.

```bash
ollama serve                 # Dienst starten, hört auf 127.0.0.1:11434
ollama pull qwen3.5:0.8b     # 0,8B, rund 1 GB — der Default
ollama pull nomic-embed-text # Embeddings
```

`01_model_cards` und `05_modellauswahl` vergleichen mehrere Modelle
gegeneinander. In den gespeicherten Outputs stehen `llama3.2` (2,0 GB) und
`gemma4` (9,6 GB) daneben. Wer den Platz nicht hat, trägt dort ein, was
`ollama list` hergibt — die Notebooks rechnen mit den eigenen Zahlen weiter.

Das Default-Modell ist ein Reasoning-Modell: Ohne `reasoning_effort="none"`
gibt es über die OpenAI-API einen leeren `content` zurück. `helfer.py` setzt das
zentral (`REASONING`), `frage_llm()` und `messe_anfrage()` hängen es an jeden
Aufruf. Wer im Notebook direkt `client.chat.completions.create` benutzt, muss es
selbst mitgeben — `03_runtime_und_api` behandelt genau das.

Mit einem anderen Provider statt Ollama: in `helfer.py` `BASIS_URL`, `API_KEY`
und `MODELL` ändern. Sonst ändert sich nichts, die Notebooks sprechen
ausschließlich über die OpenAI-kompatible API.

In Google Colab gibt es kein lokales Ollama. Dort ist die Provider-Variante
nötig; die Rechenabschnitte laufen auch ohne Modell.

## Dateien

```
04_deployment/
├── helfer.py                  gemeinsame Funktionen, von allen Notebooks importiert
├── requirements.txt
├── daten/
│   ├── model_cards.json       12 offene Modelle mit ihren Architekturzahlen
│   ├── hardware.json          10 Karten und Geräte mit VRAM und Speicherbandbreite
│   ├── szenarien.json         6 Deployment-Situationen mit Sollantworten
│   ├── 03_runtime.json        Runtimes, Zugriffsarten, drei Deployment-Ziele
│   ├── 04_lasttest.json       Fülltext für Prefill-Messungen, drei Planungsfälle
│   ├── 05_evalset.json        30 CVE-Fälle als eigene Eval-Menge
│   └── 05_kandidaten.json     die verglichenen Modelle mit ihren Eckdaten
├── NN_thema_solved.ipynb      Lösungsfassung, ausgeführt
└── NN_thema.ipynb             Teilnehmenden-Fassung
```

Alle Zahlen in `daten/` tragen ein Stand-Datum. Sie sind für das Rechnen da,
nicht als Nachschlagewerk — Modelle und Karten ändern sich.

## Einheiten

Durchgehend `GB = 10⁹ Byte`, weil VRAM so ausgewiesen wird. Präzision zählt
nominell: FP16 zwei Byte je Parameter, INT8 ein Byte, INT4 ein halbes. Echte
4-Bit-Formate landen bei 4,5 bis 5 Bit je Gewicht; wo das eine Rolle spielt,
steht es im Notebook.
