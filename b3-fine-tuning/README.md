# Modul B · Kapitel 3 — Fine-Tuning

Ein Sprachmodell mit **LoRA** auf eine konkrete Aufgabe anpassen: aus einer
englischen CVE-Kurzbeschreibung wird ein striktes JSON-Triage-Objekt.

```
### CVE
An SQL injection flaw in PostgreSQL 14.2.0 allows a remote attacker,
unauthenticated, to read arbitrary rows from the application database.

### TRIAGE
{"severity": "high", "component": "postgresql", "action": "patch_7d", "owner": "data-team"}
```

Das Basismodell hat 135 Millionen Parameter und kann diese Aufgabe vorher
nicht. Trainiert wird nur ein Adapter mit unter einem Prozent der Parameter.

## Notebooks

| Datei | Inhalt |
|---|---|
| `01_lora.ipynb` | didaktisch geführter LoRA-Workshop mit zwei Programmieraufgaben |
| `01_lora_solved.ipynb` | dieselbe Fassung mit ausgefüllten Lösungen |

Der Hauptpfad folgt fünf Fragen: Wann ist Fine-Tuning sinnvoll? Was verändert
LoRA? Wie werden Trainingsbeispiele vorbereitet? Was passiert beim Training?
Hat es auf ungesehenen Daten funktioniert? Es gibt zwei fokussierte Aufgaben:
den Adapter konfigurieren und die Prompt-Tokens im Loss maskieren. Beide haben
einen Selbsttest und eine aufklappbare Lösung.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Beim ersten Start lädt das Notebook `HuggingFaceTB/SmolLM2-135M` von Hugging
Face. Danach liegt das Modell im lokalen Cache. Das ist der einzige Netzzugriff
in diesem Kapitel — alle Trainings- und Testdaten liegen fertig in `daten/`.

Das Training läuft auf Apple Silicon (MPS), CUDA oder CPU. Die Zelle mit der
Trainingsschleife ist die längste im Notebook: 400 Schritte, auf einem
M-series-Laptop je nach Auslastung 3 bis 7 Minuten. Alle anderen Zellen laufen
in Sekunden.

## Dateien

```
03_fine-tuning/
├── README.md
├── requirements.txt
├── helfer.py                        Gerätewahl, Modelle laden, Batch-Generierung
├── daten/
│   ├── erzeuge_trainingsdaten.py    Generator mit festem Seed
│   ├── triage_train.jsonl           600 Beispiele
│   └── triage_test.jsonl            60 Beispiele, ohne Überschneidung
├── ausgabe/                         trainierter Adapter (nicht versioniert)
├── 01_lora_solved.ipynb
└── 01_lora.ipynb
```

Die Daten sind erfunden und werden aus Bausteinen erzeugt: 13
Schwachstellenklassen, 25 Komponenten, Versionen, Angriffsvektoren,
Zugriffsvoraussetzungen und sieben Satzvorlagen.

Die Zielfelder folgen festen Regeln: `severity` hängt an der
Schwachstellenklasse, `component` und `owner` an der betroffenen Komponente,
`action` an `severity` und daran, ob die Lücke aktiv ausgenutzt wird. Keine
dieser Zuordnungen steht wörtlich im Satz — das Modell kann sie nur aus den
Trainingsdaten lernen. Der Generator lässt sich mit anderen Bausteinen erneut
laufen lassen:

```bash
python daten/erzeuge_trainingsdaten.py
```

## Abweichung von der LLM-Naht

Die übrigen Kapitel sprechen über einen OpenAI-kompatiblen Client mit einem
Modell hinter einer API. Fine-Tuning braucht Zugriff auf die Gewichte selbst,
deshalb lädt dieses Kapitel die Modelle mit `transformers` direkt in den
Prozess. `helfer.erzeuge_antworten()` übernimmt die Rolle von `frage_llm()`.

## Weiterführend

QLoRA und das Mergen eines Adapters werden am Ende bewusst nur kurz erklärt.
Beide Themen sind nützlich, gehören aber nicht zum Kern des ersten
LoRA-Trainingslaufs.
