# Modul B · Kapitel 1 — Prompt Engineering

Sieben Notebooks, je eines pro Prompting-Strategie. Alle arbeiten in derselben
Welt: Security Operations, CVE-Briefings für einen CISO, Log-Auszüge und ein
Asset-Inventar. Alle Daten sind erfunden; zur Laufzeit wird nichts aus dem Netz
geladen.

## Die Notebooks

| Notebook | Inhalt | Challenges |
|---|---|:--:|
| `01_tcrei` | TCREI: Task mit Persona und Format, Context, References, Evaluate, Iterate. PCCSR als Dialogvariante. | 5 |
| `02_shot_prompting` | Zero-, One- und Few-Shot. Warum ein One-Shot ohne Input/Output-Paar nichts bringt. Format-Trefferquote messen. | 4 |
| `03_chain_of_thought` | Eine Log-Zählaufgabe mit Baseline, Zero-Shot-CoT, Few-Shot-CoT und Vergleich auf Testdaten. | 2 |
| `04_self_consistency` | Few-Shot-CoT mehrfach sampeln, per Mehrheit entscheiden und auf 20 Login-Fällen vergleichen. | 1 |
| `05_tree_of_thought` | Incident-Pläne verzweigen, bewerten und mit Normal-Prompt sowie Self-Consistency vergleichen. | 1 |
| `06_least_to_most` | Eine große Frage in Teilfragen zerlegen und die Antworten aufeinander aufbauen. | 5 |
| `07_react` | Thought → Action → Observation als Schleife, mit zwei Offline-Tools über die Daten in `daten/`. | 5 |

Alle sieben sind gebaut und unabhängig voneinander lauffähig.

Jedes Notebook gibt es zweimal:

* `NN_thema.ipynb` — die Arbeitsfassung mit offenen Challenges.
* `NN_thema_solved.ipynb` — dieselbe Datei mit ausgefüllten Lösungen und
  gespeicherten Outputs. Zum Nachlesen, wenn eine Challenge klemmt, und zum
  Vergleichen der Modellantworten.

## Setup

**1. Ollama installieren** — <https://ollama.com/download>, oder auf dem Mac:

```bash
brew install ollama
ollama serve          # läuft danach im Hintergrund auf Port 11434
```

**2. Modell holen** (rund 1 GB):

```bash
ollama pull qwen3.5:0.8b
```

**3. Python-Pakete installieren** — eine Liste für alle Ordner, im Wurzelverzeichnis
des Repos:

```bash
pip install -r requirements.txt
```

**4. Notebook starten:**

```bash
jupyter lab 01_tcrei.ipynb
```

Prüfen, ob der Server antwortet:

```bash
curl http://localhost:11434/v1/models
```

## Ohne lokales Ollama: Provider eintragen

Der Modell-Zugang steht an genau einer Stelle, in `helfer.py`:

```python
BASIS_URL = "http://localhost:11434/v1"
API_KEY = "ollama"
MODELL = "qwen3.5:0.8b"
EMBEDDING_MODELL = "nomic-embed-text"
REASONING = "none"        # schaltet das interne Denken von qwen3.5 ab
```

Für OpenAI etwa:

```python
BASIS_URL = "https://api.openai.com/v1"
API_KEY = "sk-…"                  # besser: os.environ["OPENAI_API_KEY"]
MODELL = "gpt-4o-mini"
EMBEDDING_MODELL = "text-embedding-3-small"
```

Jeder Anbieter mit OpenAI-kompatibler API funktioniert genauso — Groq, Together,
Mistral, Azure OpenAI, eine eigene vLLM-Instanz. Die Notebooks selbst ändern
sich dabei nicht.

In Google Colab gibt es kein lokales Ollama. Dort ist die Provider-Variante
nötig; `helfer.py` und der Ordner `daten/` müssen nach `/content` hochgeladen
werden.

## Die Dateien

```
01_prompt-engineering/
├── README.md
├── helfer.py                 Modell-Zugang, Datenlader, Ausgabe, Messung
├── daten/                    alle Beispieldaten als JSON
└── NN_thema[_solved].ipynb
```

`helfer.py` stellt bereit:

| Funktion | Zweck |
|---|---|
| `frage_llm(prompt, system=None, temperature=0.0, modell=MODELL, max_tokens=600)` | eine Anfrage, zurück kommt der Antworttext |
| `frage_llm_viele(prompt, k=5, temperature=0.8, …)` | dieselbe Frage k-mal, zurück kommt eine Liste |
| `lade_daten(name)` | liest `daten/<name>.json` |
| `zeige(text, titel=None)` | Antwort lesbar ausgeben |
| `zeige_vergleich({"A": text, "B": text})` | zwei bis vier Antworten gegenüberstellen |
| `messe_treffer(vorhersagen, sollwerte)` | Anteil exakter Übereinstimmungen, 0.0–1.0 |

### Daten

| Datei | Inhalt | Schlüssel |
|---|---|---|
| `cve_testfaelle.json` | 12 CVE-Kurzbeschreibungen mit Sollwerten | `id`, `text`, `severity`, `component`, `action` |
| `log_auszuege.json` | 8 Log-Auszüge mit je einer Zählaufgabe | `id`, `frage`, `log`, `antwort` |
| `cvss_faelle.json` | Einstufungsregel und 10 Fälle | `regel`, `faelle` → `id`, `beschreibung`, `merkmale`, `antwort`, `system` |
| `cve_datenbank.json` | 6 CVEs, nach Kennung geschlüsselt | je Eintrag `id`, `title`, `summary`, `severity`, `cvss`, `cwe`, `component`, `affected_versions`, `fixed_version`, `published`, `exploit_status`, `recommended_action`, `references` |
| `incident_report.json` | ein Incident-Report mit Zielfrage | `id`, `titel`, `report`, `frage`, `pruefpunkte` |
| `host_inventory.json` | 12 Systeme des Beispielunternehmens | `host`, `component`, `version`, `criticality`, `environment`, `owner`, `exposure` |

Dazu kommen Dateien, die nur ein Notebook braucht. Sie tragen dessen Nummer im
Namen, damit sichtbar bleibt, wo sie hingehören:

| Datei | Für | Inhalt |
|---|---|---|
| `02_cve_testfaelle.json` | `02_shot_prompting` | 30 Testfälle statt 12 — dieselben Felder, große genug Messbasis für den Vergleich der vier Prompt-Varianten |
| `02_shot_beispiele.json` | `02_shot_prompting` | die Beispiele für One- und Few-Shot, getrennt von der Testmenge |
| `03_log_zaehlaufgaben.json` | `03_chain_of_thought` | zusätzliche Zählaufgaben über Log-Auszüge |
| `03_login_testfaelle.json` | `03_chain_of_thought`, `04_self_consistency` | 20 einheitliche Testfälle zum Zählen fehlgeschlagener Login-Versuche |
| `05_abdeckung.json` | `05_tree_of_thought` | Stichworte je Prüfpunkt für die Abdeckungsmessung |
| `06_pruefpunkte.json` | `06_least_to_most` | Signalwortgruppen je Prüfpunkt des Incident-Reports |

Feste Wertelisten in den Testfällen:

* `severity`: `critical`, `high`, `medium`, `low`
* `action`: `upgrade`, `patch`, `rotate_credentials`, `disable_feature`,
  `isolate`, `monitor`

Damit lassen sich Modellausgaben exakt gegen die Sollwerte vergleichen.
