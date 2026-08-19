# Einmaliges Setup unter Linux

Plane etwa 20 Minuten ein. Die Befehle gelten für Ubuntu/Debian.

## 1. Programme installieren

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip curl
python3 --version
git --version
```

Python muss Version 3.10 oder neuer sein.

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

## 4. Ollama installieren und starten

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
curl http://localhost:11434/api/tags
```

Bei `connection refused` Ollama in einem **zweiten Terminal** starten und dieses
geöffnet lassen:

```bash
ollama serve
```

## 5. Modelle laden

Im ersten Terminal:

```bash
ollama pull qwen3.5:0.8b
ollama pull nomic-embed-text
ollama list
```

`qwen3.5:0.8b` ist das Chat-Modell, `nomic-embed-text` wird für RAG benötigt.
Zusammen sind es rund 1,3 GB.

## 6. Jupyter Lab starten

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

Falls nötig, vorher in einem zweiten Terminal `ollama serve` starten.

## Bonus: Modell wechseln

```bash
ollama run qwen3.5:0.8b
ollama pull gemma3:270m     # kleiner, wenn Ressourcen knapp sind
ollama pull qwen3.5:2b      # größer und leistungsfähiger
ollama pull llama3.2:1b     # ähnlich groß, andere Modellfamilie
```

Zum Wechseln im Notebook `MODELL` auf den exakten Namen aus `ollama list`
setzen. `nomic-embed-text` ist kein Chat-Modell, sondern nur für Embeddings.
