# Einmaliges Setup unter macOS

Plane etwa 20 Minuten ein. Führe alle Befehle in **Terminal** aus.

## 1. Programme installieren

```bash
python3 --version
git --version
```

Python muss Version 3.10 oder neuer sein. Falls etwas fehlt:

1. Python installieren: <https://www.python.org/downloads/macos/>
2. Für Git `xcode-select --install` ausführen und bestätigen.
3. Ollama von <https://ollama.com/download/mac> laden, in **Programme** ziehen
   und einmal öffnen. Die Einrichtung der Kommandozeile erlauben.

```bash
ollama --version
```

## 2. Repo herunterladen

```bash
git clone https://github.com/Thurner-SecAI/workshop.git
cd workshop
```

Ohne Git: Auf GitHub **Code → Download ZIP** wählen, entpacken und im Terminal
in den Ordner wechseln.

## 3. Python-Umgebung anlegen

Einmal im Repo-Ordner ausführen:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`(.venv)` vor der Eingabe zeigt, dass die Umgebung aktiv ist. Prüfen:

```bash
python -c "import numpy, matplotlib; print('Python-Setup OK')"
jupyter --version
```

## 4. Ollama starten und Modelle laden

```bash
curl http://localhost:11434/api/tags
ollama pull qwen3.5:0.8b
ollama pull nomic-embed-text
ollama list
```

Bei `connection refused` Ollama im Programme-Ordner öffnen. `qwen3.5:0.8b` ist
das Chat-Modell, `nomic-embed-text` wird für RAG benötigt. Zusammen sind es rund
1,3 GB.

## 5. Jupyter Lab starten

```bash
jupyter lab
```

Im Browser ein Notebook öffnen; Zellen mit **Shift + Enter** ausführen. Das
Terminal geöffnet lassen.

## Bei jedem späteren Start

```bash
cd workshop
source .venv/bin/activate
jupyter lab
```

Ollama bei Bedarf zusätzlich aus dem Programme-Ordner öffnen.

## Bonus: Modell wechseln

```bash
ollama run qwen3.5:0.8b
ollama pull gemma3:270m     # kleiner, wenn Ressourcen knapp sind
ollama pull qwen3.5:2b      # größer und leistungsfähiger
ollama pull llama3.2:1b     # ähnlich groß, andere Modellfamilie
```

Zum Wechseln im Notebook `MODELL` auf den exakten Namen aus `ollama list`
setzen. `nomic-embed-text` ist kein Chat-Modell, sondern nur für Embeddings.
