# Setup — vor dem Workshop erledigen

Die Notebooks in Modul B sprechen ein Sprachmodell an, das **auf deinem eigenen
Rechner läuft**. Dafür brauchst du zwei Dinge: Ollama als Modellserver und eine
Python-Umgebung.

> **Mach das zu Hause, nicht im Workshop.** Es sind rund 1,3 GB Download. Wenn
> das dreißig Leute gleichzeitig über dasselbe WLAN ziehen, wird es ein langer
> Vormittag.

Rechne mit **20 Minuten**, davon der größte Teil Wartezeit.

---

## Was du am Ende haben willst

```
$ ollama list
NAME                       SIZE
qwen3.5:0.8b               1.0 GB
nomic-embed-text:latest    274 MB

$ python -c "import openai, chromadb; print('ok')"
ok
```

---

## Schritt 1 · Ollama installieren

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

## Schritt 2 · Modelle laden

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

## Schritt 3 · Python-Umgebung

Du brauchst **Python 3.10 oder neuer** (`python3 --version`).

```bash
cd 01_prompt-engineering          # oder der Ordner, mit dem du anfängst

python3 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Jeder der vier Ordner hat seine eigene `requirements.txt`. Wer alles
durcharbeiten will, installiert der Reihe nach alle vier in dieselbe Umgebung —
sie vertragen sich.

| Ordner | Was dazukommt |
|---|---|
| `01_prompt-engineering` | `openai`, `jupyter` |
| `02_rag` | `chromadb`, `langchain-text-splitters`, `rank-bm25`, `tiktoken` |
| `03_fine-tuning` | `torch`, `transformers`, `peft` — kein Ollama nötig |
| `04_deployment` | `pandas`, `tiktoken`, für ein Notebook auch `torch` und `transformers` |

---

## Schritt 4 · Prüfen, ob alles zusammenspielt

Diesen Test einmal laufen lassen, bevor du ins Notebook gehst:

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

---

## Schritt 5 · Notebook starten

```bash
jupyter lab
```

Im Browser das erste Notebook des Ordners öffnen und Abschnitt 0 ausführen. Es
meldet, welches Modell es benutzt und ob der Server antwortet.

---

## Welches Notebook braucht was

| Notebook | Ollama | Modelle | Sonstiges |
|---|:--:|---|---|
| 1.1–1.7 Prompt Engineering | ja | `qwen3.5:0.8b` | — |
| 2.1 Chunking | ja | `qwen3.5:0.8b`, `nomic-embed-text` | — |
| 2.2 Keyword Search | **nein** | — | rechnet vollständig deterministisch |
| 2.3 Semantic Search | ja | `nomic-embed-text`, für die letzte Challenge `bge-m3` | — |
| 2.4 Augmented Prompt | ja | `qwen3.5:0.8b`, `nomic-embed-text` | — |
| Bonus Hybrid Search | ja | `nomic-embed-text` | — |
| Bonus HNSW | **nein** | — | benutzt die zwischengespeicherten Embeddings |
| 3 Fine-Tuning | **nein** | — | lädt `SmolLM2-135M` von Hugging Face (~540 MB, einmalig) |
| 4.1 Model Cards | ja | `qwen3.5:0.8b` und ein zweites Chat-Modell | — |
| 4.2 Quantisierung | **nein** | — | lädt `SmolLM2-135M` von Hugging Face |

---

## Ohne lokales Ollama: einen Anbieter eintragen

Wenn dein Rechner zu klein ist oder du lieber einen API-Key benutzt: Der
Zugang steht in jedem Ordner an genau einer Stelle, in `helfer.py`.

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

In Colab gibt es kein lokales Ollama, dort ist die Anbieter-Variante nötig.
Außerdem müssen `helfer.py` und der Ordner `daten/` nach `/content`
hochgeladen werden. Die Notebooks installieren fehlende Pakete selbst.

Die beiden Notebooks ohne Ollama — Fine-Tuning und Quantisierung — laufen in
Colab dagegen sehr gut, und für den QLoRA-Bonus im Fine-Tuning-Notebook ist
Colab sogar nötig: `bitsandbytes` braucht eine CUDA-GPU und läuft auf macOS
nicht.

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

**`ModuleNotFoundError` mitten im Notebook**
Die Umgebung ist nicht aktiv oder das Notebook läuft in einem anderen Kernel.
`source .venv/bin/activate`, dann `jupyter lab` aus derselben Shell starten.

**Der Fine-Tuning-Download hängt**
`SmolLM2-135M` kommt von Hugging Face, nicht von Ollama. Einmal geladen, liegt
er im Cache unter `~/.cache/huggingface`.

---

## Checkliste

- [ ] `ollama --version` gibt eine Version aus
- [ ] `ollama list` zeigt `qwen3.5:0.8b` und `nomic-embed-text`
- [ ] Der Prüf-Schnipsel aus Schritt 4 druckt eine Antwort und `768`
- [ ] `jupyter lab` öffnet sich im Browser
- [ ] Abschnitt 0 des ersten Notebooks läuft ohne Fehler durch
