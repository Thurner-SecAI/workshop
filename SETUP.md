# Setup — vor dem Workshop erledigen

Direkt zur Anleitung für dein Betriebssystem:
[`Windows`](SETUP-Windows.md) · [`Linux`](SETUP-Linux.md) · [`macOS`](SETUP-Mac.md)

Alle Aufgaben laufen als Jupyter-Notebooks auf deinem eigenen Rechner. Du
brauchst dafür Python und eine virtuelle Umgebung; für Modul B zusätzlich einen
Modellserver, der ein Sprachmodell lokal bereitstellt.

| | Modul A · ML-Grundlagen | Modul B · LLM Engineering |
|---|---|---|
| Python 3.10+ mit venv | ja | ja |
| Jupyter | ja | ja |
| Ollama + Modelle (~1,3 GB) | **nein** | ja |
| Aufwand | ~10 Minuten | ~20 Minuten |

> **Mach das zu Hause, nicht im Workshop.** Modul B lädt rund 1,3 GB Modelle,
> dazu kommen die Python-Pakete — `torch` allein ist mehrere hundert MB. Wenn
> das dreißig Leute gleichzeitig über dasselbe WLAN ziehen, wird es ein langer
> Vormittag.

Schritt 0 bis 2 gelten für beide Module. Ab Schritt 3 geht es nur noch um
Modul B — wer nur Modul A macht, ist nach Schritt 2 fertig.

---

## Schritt 0 · Repo holen

```bash
git clone https://github.com/Thurner-SecAI/workshop.git
cd workshop
```

Wer kein Git hat: auf der Repo-Seite oben rechts **Code → Download ZIP**,
entpacken, in den entpackten Ordner wechseln.

---

## Schritt 1 · Python-Umgebung anlegen

Du brauchst **Python 3.10 oder neuer**:

```bash
python3 --version
```

Kommt hier nichts oder etwas Älteres: <https://www.python.org/downloads/>
(Windows: beim Installieren **„Add python.exe to PATH"** ankreuzen).

Eine virtuelle Umgebung ist ein Ordner, in dem die Pakete dieses Workshops
landen — getrennt von allem anderen auf deinem Rechner. Angelegt wird sie
**einmal, im Wurzelverzeichnis des Repos**:

```bash
python3 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
```

Wenn es geklappt hat, steht `(.venv)` vorn in deiner Eingabezeile. **Diese
Zeile brauchst du in jedem neuen Terminal wieder** — die Umgebung gilt nur für
die Shell, in der du sie aktiviert hast.

---

## Schritt 2 · Pakete installieren

Es gibt **eine** Paketliste für alle Ordner, im Wurzelverzeichnis des Repos.
Ein Befehl, mit aktiver `.venv`:

```bash
pip install -r requirements.txt
```

Das dauert ein paar Minuten — `torch` allein ist mehrere hundert MB.

**Jupyter musst du nicht extra installieren**, es steht mit in der Liste. Ebenso
die Pakete für Modul B: du installierst sie auch dann mit, wenn du nur Modul A
machst. Das ist Absicht — eine Liste, die immer stimmt, ist weniger Ärger als
acht, von denen du die richtige heraussuchen musst.

Probe, dass die Umgebung steht:

```bash
python -c "import numpy, matplotlib; print('ok')"     # Modul A
jupyter --version
```

### Notebook starten

```bash
jupyter lab
```

Das öffnet im Browser eine Dateiübersicht. Dort in den Ordner klicken und das
erste Notebook öffnen. Zellen laufen mit **Shift + Enter**.

> Wichtig: `jupyter lab` **aus derselben Shell** starten, in der `(.venv)`
> aktiv ist. Sonst benutzt das Notebook ein anderes Python und findet die
> Pakete nicht.

**Wer nur Modul A macht, ist hier fertig.** Modul A rechnet mit NumPy,
scikit-learn und PyTorch — kein Sprachmodell, kein Ollama. Die Daten liegen
fertig im Ordner `data/` neben den Notebooks; einzige Ausnahme ist `a4-gpt`,
das seinen Trainingstext in Abschnitt 0 selbst herunterlädt.

---

## Schritt 3 · Ollama installieren (nur Modul B)

Ollama lädt Sprachmodelle herunter und stellt sie unter
`http://localhost:11434` bereit — mit derselben API, die auch OpenAI benutzt.
Deshalb funktionieren die Notebooks später ohne Änderung auch gegen einen
Anbieter.

**macOS** — <https://ollama.com/download> herunterladen, App in den
Programme-Ordner ziehen, einmal starten. Danach läuft Ollama als kleines Symbol
in der Menüleiste und startet künftig von selbst.

Alternativ über Homebrew:

```bash
brew install ollama
brew services start ollama      # startet den Server dauerhaft im Hintergrund
```

**Windows** — Installer von <https://ollama.com/download> ausführen. Ollama
läuft danach als Hintergrunddienst; ein Symbol erscheint im Infobereich der
Taskleiste.

**Linux**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Prüfen, ob der Server läuft:

```bash
ollama --version
curl http://localhost:11434/api/tags
```

Die zweite Zeile muss eine JSON-Antwort geben (am Anfang `{"models":`). Kommt
`connection refused`, läuft der Server nicht — siehe unten bei „Wenn etwas
klemmt".

---

## Schritt 4 · Modelle laden (nur Modul B)

```bash
ollama pull qwen3.5:0.8b        # 1,0 GB — das Chat-Modell für alle Notebooks
ollama pull nomic-embed-text    # 274 MB — Embeddings für die RAG-Notebooks
```

Beide zusammen sind **rund 1,3 GB**. Das reicht für alle Pflicht-Notebooks.

Zwei Modelle sind optional und werden nur an je einer Stelle gebraucht:

| Modell | Größe | Wofür |
|---|---|---|
| `bge-m3` | 1,2 GB | RAG 2.3, letzte Challenge: dasselbe noch einmal mit einem anderen Embedding-Modell |
| ein zweites Chat-Modell | je nach Wahl | Deployment 4.1, Messabschnitt: zwei verschieden große Modelle vergleichen |

Für den Modellvergleich in Deployment 4.1 taugt **jedes** zweite Modell, das du
ohnehin geladen hast — der Punkt ist der Größenunterschied, nicht das konkrete
Modell. In den gespeicherten Outputs steht `gemma4` (9,6 GB); wenn du den Platz
nicht hast, trag in der Messzelle ein anderes Modell aus deiner `ollama list`
ein. Der Abschnitt rechnet dann mit deinen Zahlen weiter.

---

## Schritt 5 · Prüfen, ob alles zusammenspielt (nur Modul B)

Diesen Test einmal laufen lassen, bevor du ins Notebook gehst — mit aktiver
`.venv`:

```bash
python -c "
from openai import OpenAI
c = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
a = c.chat.completions.create(model='qwen3.5:0.8b', reasoning_effort='none',
        messages=[{'role':'user','content':'Answer with one word: ready?'}],
        max_tokens=10)
print('Chat:', a.choices[0].message.content)
e = c.embeddings.create(model='nomic-embed-text', input=['test'])
print('Embedding-Dimensionen:', len(e.data[0].embedding))
"
```

Erwartet:

```
Chat: Yes.
Embedding-Dimensionen: 768
```

Welches Wort das Modell antwortet, ist egal — es muss überhaupt eines kommen.
Die `768` dagegen ist fest: so viele Dimensionen hat ein Embedding von
`nomic-embed-text`.

Der erste Aufruf dauert ein paar Sekunden — Ollama lädt das Modell in den
Speicher. Danach geht es schnell.

Im Notebook selbst macht Abschnitt 0 dieselbe Probe: er meldet, welches Modell
benutzt wird und ob der Server antwortet.

---

## Welches Notebook braucht was

Die Pakete sind mit Schritt 2 alle installiert. Die Spalte sagt nur, womit der
Ordner tatsächlich rechnet.

**Modul A** — kein Ollama, keine Modelle.

| Ordner | Benutzt | Sonstiges |
|---|---|---|
| `a1-lineare-regression` | numpy, pandas, matplotlib, scikit-learn | Daten in `data/` |
| `a2-logistische-regression` | dieselben | Daten in `data/` |
| `a3-neuronale-netze` | numpy, matplotlib, scikit-learn, joblib | Daten in `data/` (11 MB Bilder) |
| `a4-gpt` | torch, numpy, matplotlib | lädt den Faust-Text in Abschnitt 0 selbst — läuft auch in Colab |

**Modul B**

| Notebook | Ollama | Modelle | Sonstiges |
|---|:--:|---|---|
| `b1` 1.1–1.7 Prompt Engineering | ja | `qwen3.5:0.8b` | — |
| `b2` 2.1 Chunking | ja | `qwen3.5:0.8b`, `nomic-embed-text` | — |
| `b2` 2.2 Keyword Search | **nein** | — | rechnet vollständig deterministisch |
| `b2` 2.3 Semantic Search | ja | `nomic-embed-text`, für die letzte Challenge `bge-m3` | — |
| `b2` 2.4 Augmented Prompt | ja | `qwen3.5:0.8b`, `nomic-embed-text` | — |
| `b2` Bonus Hybrid Search | ja | `nomic-embed-text` | — |
| `b2` Bonus HNSW | **nein** | — | benutzt die zwischengespeicherten Embeddings |
| `b3` Fine-Tuning | **nein** | — | lädt `SmolLM2-135M` von Hugging Face (~540 MB, einmalig) |
| `b4` 4.1 Model Cards | ja | `qwen3.5:0.8b` und ein zweites Chat-Modell | — |
| `b4` 4.2 Quantisierung | **nein** | — | lädt `SmolLM2-135M` von Hugging Face |

---

## Ohne lokales Ollama: einen Anbieter eintragen

Wenn dein Rechner zu klein ist oder du lieber einen API-Key benutzt: Der
Zugang steht in jedem Modul-B-Ordner an genau einer Stelle, in `helfer.py`.

```python
BASIS_URL = "http://localhost:11434/v1"
API_KEY = "ollama"
MODELL = "qwen3.5:0.8b"
EMBEDDING_MODELL = "nomic-embed-text"
REASONING = "none"        # schaltet das interne Denken ab, siehe unten
```

Für OpenAI zum Beispiel:

```python
BASIS_URL = "https://api.openai.com/v1"
API_KEY = os.environ["OPENAI_API_KEY"]
MODELL = "gpt-4o-mini"
EMBEDDING_MODELL = "text-embedding-3-small"
```

Jeder Anbieter mit OpenAI-kompatibler API funktioniert genauso — Groq,
Together, Mistral, Azure OpenAI, eine eigene vLLM-Instanz. An den Notebooks
ändert sich dabei nichts. Genau das ist der Punkt, den Kapitel 4 zeigt.

Zwei Dinge, die du dabei wissen solltest: Es kostet Geld pro Aufruf, und die
Notebooks in Kapitel 1 zeigen ihre Effekte mit einem **kleinen** Modell
deutlicher. Ein großes Modell beantwortet manche Aufgabe auch ohne
Chain-of-Thought richtig — dann ist die Messung langweilig.

### Google Colab

Die meisten Notebooks lesen ihre Daten aus dem Ordner daneben (`data/` bzw.
`daten/`) und laufen deshalb lokal, nicht in Colab: dort fehlen die Dateien.

Zwei Ausnahmen laufen in Colab problemlos:

* **`a4-gpt`** braucht keine Datendateien — die vier Teile laden den Text
  selbst, und für das Training in Teil 4 ist eine Colab-GPU sogar der bequemere
  Weg. Links stehen in der README des Repos.
* **`b3` Fine-Tuning und `b4` 4.2 Quantisierung** brauchen kein Ollama. Für den
  QLoRA-Bonus im Fine-Tuning-Notebook ist Colab sogar nötig: `bitsandbytes`
  braucht eine CUDA-GPU und läuft auf macOS nicht.

Für alles Übrige in Modul B gilt in Colab: es gibt dort kein lokales Ollama,
also ist die Anbieter-Variante von oben nötig. Außerdem müssen `helfer.py` und
der Ordner `daten/` nach `/content` hochgeladen werden. Die Notebooks
installieren fehlende Pakete selbst.

---

## Bonus: ein anderes Modell benutzen

Zwei Schritte. Modell ziehen, Namen eintragen:

```bash
ollama pull <modellname>        # Auswahl und exakte Tags: ollama.com/library
ollama list                     # zeigt, wie das Modell jetzt heißt
```

```python
# helfer.py
MODELL = "<modellname>"
```

Das war es — alle Notebooks des Ordners benutzen ab dem nächsten Kernel-Neustart
das neue Modell. Für einen einzelnen Aufruf geht es auch ohne Änderung an
`helfer.py`:

```python
frage_llm(prompt, modell="<modellname>")
```

Der Name muss exakt so geschrieben sein, wie ihn `ollama list` ausgibt,
Tag inklusive.

Drei Dinge, die dabei zählen:

* **Größe gegen Arbeitsspeicher.** Faustregel: das Modell muss in den freien
  RAM passen. Bei 8 GB ist ein 3B-Modell die Obergrenze, bei 16 GB ein 8B.
* **Kleine Modelle zeigen mehr.** Die Kapitel 1 leben davon, dass ein Prompt
  einen Unterschied macht. Ein großes Modell beantwortet die Aufgaben auch ohne
  Chain-of-Thought richtig — dann misst du nichts mehr.
* **Reasoning-Modelle brauchen den Zusatz von unten**, sonst kommt gar nichts
  zurück.

### Warum der Default ein Reasoning-Modell ist

`qwen3.5:0.8b` denkt vor der Antwort. Über die OpenAI-API kommt dann ein
**leerer** `content` zurück — das Token-Budget ist ins Denken gegangen.
Abgeschaltet wird das mit einem regulären OpenAI-Argument:

```python
c.chat.completions.create(..., reasoning_effort="none")
```

Gemessen: ohne den Zusatz 22 Sekunden und nichts, mit ihm 0,5 Sekunden und eine
Antwort.

**Für die Notebooks ist das erledigt.** `helfer.py` setzt `REASONING = "none"`,
und `frage_llm()`, `frage_llm_viele()` und `messe_anfrage()` hängen es an jeden
Aufruf. Du brauchst es nur dort selbst, wo ein Notebook `client.chat.completions
.create` direkt aufruft — und an genau diesen Stellen ist es auch der
Lerngegenstand.

### Zum Vergleich: `llama3.2`

Der frühere Default, 3B und 2,0 GB. Gemessen auf den Testfällen dieses
Workshops:

| | `qwen3.5:0.8b` (Default) | `llama3.2` (3B) |
|---|---|---|
| Zero-Shot: gültiges JSON | 0/8 | 0/8 |
| Few-Shot: gültiges JSON | **8/8** | 4/8 |
| ReAct-Formattreue | 4/4 | 4/4 |
| CVSS-Einstufung direkt | **4/10** | 2/10 |
| CVSS-Einstufung mit Chain-of-Thought | 2/10 | **5/10** |
| Zeit für 8 Anfragen | **6 s** | 23 s |

Die vorletzte Zeile ist bemerkenswert und bleibt so stehen: Bei einem auf
internes Reasoning trainierten Modell **verschlechtert** ein ausgeschriebener
Rechenweg das Ergebnis. Das ist kein Defekt des Setups, sondern ein Befund —
dass ein Verfahren aus einem Paper auf einem konkreten Modell nicht wirkt, ist
die praktisch nützlichere Lektion als die Bestätigung der Theorie. Die Notebooks
in Kapitel 1.3 und 1.4 messen das und schreiben hin, was herauskommt.

Wer den Gegenversuch will, zieht `llama3.2` dazu und trägt es als `MODELL` ein.

**Das Embedding-Modell zu tauschen ist aufwendiger:**

```python
EMBEDDING_MODELL = "bge-m3"
```

Ein anderes Embedding-Modell liefert Vektoren anderer Länge — die alten und die
neuen sind nicht vergleichbar. Die Chroma-Collection muss deshalb komplett neu
gebaut werden:

```python
baue_chroma(lade_chunks(), neu=True)
```

---

## Wenn etwas klemmt

### Umgebung und Notebook (beide Module)

**`ModuleNotFoundError` mitten im Notebook**
Die Umgebung ist nicht aktiv oder das Notebook läuft in einem anderen Kernel.
`source .venv/bin/activate`, dann `jupyter lab` aus derselben Shell starten.

**`python3: command not found` unter Windows**
Dort heißt der Befehl `python`, nicht `python3` — auch beim Anlegen der
Umgebung: `python -m venv .venv`.

**`.venv\Scripts\activate` wird von PowerShell blockiert**
PowerShell verbietet Skripte standardmäßig. Einmalig in derselben Sitzung:
`Set-ExecutionPolicy -Scope Process RemoteSigned`. Oder die Eingabeaufforderung
(`cmd`) statt PowerShell benutzen.

**`FileNotFoundError` beim Laden der Daten**
Das Notebook wurde aus dem falschen Verzeichnis gestartet. Die Notebooks
erwarten den Ordner `data/` bzw. `daten/` direkt daneben — also `jupyter lab`
im Repo starten und das Notebook dort öffnen, nicht die `.ipynb` einzeln
woandershin kopieren.

**`NameError` bei einer Funktion, die es geben müsste**
Die Zellen wurden nicht der Reihe nach ausgeführt. *Kernel → Restart Kernel and
Run All Cells*.

### Ollama (nur Modul B)

**`Connection refused` oder `Failed to connect to localhost port 11434`**
Der Server läuft nicht. macOS: Ollama-App starten, oder `brew services start
ollama`. Linux: `ollama serve` in einem eigenen Terminal. Windows: prüfen, ob
das Symbol im Infobereich da ist.

**`model "qwen3.5:0.8b" not found, try pulling it first`**
`ollama pull qwen3.5:0.8b` nachholen. `ollama list` zeigt, was tatsächlich da ist.

**`Address already in use` beim Start**
Ollama läuft bereits — das ist kein Fehler. `curl
http://localhost:11434/api/tags` bestätigt es.

**Alles ist sehr langsam**
Der allererste Aufruf lädt das Modell in den Speicher, das dauert. Bleibt es
danach zäh, ist zu wenig Arbeitsspeicher frei: andere Programme schließen. Auf
Rechnern mit 8 GB RAM ist ein 3B-Modell die Obergrenze; das Default-Modell mit
0,8B liegt deutlich darunter.

**Meine Antworten sehen anders aus als die gespeicherten Outputs**
Das ist normal und kein Fehler. Sprachmodelle antworten nicht deterministisch,
und mehrere Notebooks arbeiten absichtlich mit `temperature > 0`. Die
Selbsttests prüfen deshalb die Struktur deiner Lösung, nicht den Wortlaut der
Modellantwort. Auch gemessene Quoten schwanken um ein paar Prozentpunkte — die
Richtung zählt, nicht die zweite Nachkommastelle.

**Der Fine-Tuning-Download hängt**
`SmolLM2-135M` kommt von Hugging Face, nicht von Ollama. Einmal geladen, liegt
er im Cache unter `~/.cache/huggingface`.

---

## Checkliste

**Beide Module**

- [ ] `python3 --version` zeigt 3.10 oder neuer
- [ ] `(.venv)` steht vorn in der Eingabezeile
- [ ] `pip install -r requirements.txt` ist ohne Fehler durchgelaufen
- [ ] `jupyter lab` öffnet sich im Browser
- [ ] Das erste Notebook läuft bis Abschnitt 1 ohne Fehler durch

**Zusätzlich für Modul B**

- [ ] `ollama --version` gibt eine Version aus
- [ ] `ollama list` zeigt `qwen3.5:0.8b` und `nomic-embed-text`
- [ ] Der Prüf-Schnipsel aus Schritt 5 druckt eine Antwort und `768`
