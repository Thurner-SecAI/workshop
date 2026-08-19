# Einmaliges Setup unter Windows

Plane etwa 20 Minuten ein. Führe alle Befehle in **PowerShell** aus.

## 1. Programme installieren

1. Python 3.10 oder neuer: <https://www.python.org/downloads/windows/>
   Im Installer **Add python.exe to PATH** aktivieren.
2. Git: <https://git-scm.com/download/win>
3. Ollama: <https://ollama.com/download/windows>
   Ollama nach der Installation einmal öffnen. Es läuft danach im Hintergrund.

PowerShell neu öffnen und prüfen:

```powershell
py --version
git --version
ollama --version
```

## 2. Repo herunterladen

```powershell
git clone https://github.com/Thurner-SecAI/workshop.git
cd workshop
```

Ohne Git: Auf GitHub **Code → Download ZIP** wählen, entpacken und den Ordner
in PowerShell öffnen.

## 3. Python-Umgebung anlegen

Einmal im Repo-Ordner ausführen:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`(.venv)` vor der Eingabe zeigt, dass die Umgebung aktiv ist. Falls PowerShell
das Aktivieren blockiert:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Prüfen:

```powershell
python -c "import numpy, matplotlib; print('Python-Setup OK')"
jupyter --version
```

## 4. Ollama starten und Modelle laden

```powershell
Invoke-RestMethod http://localhost:11434/api/tags
ollama pull qwen3.5:0.8b
ollama pull nomic-embed-text
ollama list
```

Bei einem Verbindungsfehler Ollama über das Startmenü öffnen. `qwen3.5:0.8b`
ist das Chat-Modell, `nomic-embed-text` wird für RAG benötigt. Zusammen sind es
rund 1,3 GB.

## 5. Jupyter Lab starten

```powershell
jupyter lab
```

Im Browser ein Notebook öffnen; Zellen mit **Shift + Enter** ausführen. Das
PowerShell-Fenster geöffnet lassen.

## Bei jedem späteren Start

```powershell
cd workshop
.\.venv\Scripts\Activate.ps1
jupyter lab
```

Ollama bei Bedarf zusätzlich über das Startmenü öffnen.

## Bonus: Modell wechseln

```powershell
ollama run qwen3.5:0.8b
ollama pull gemma3:270m     # kleiner, wenn Ressourcen knapp sind
ollama pull qwen3.5:2b      # größer und leistungsfähiger
ollama pull llama3.2:1b     # ähnlich groß, andere Modellfamilie
```

Zum Wechseln im Notebook `MODELL` auf den exakten Namen aus `ollama list`
setzen. `nomic-embed-text` ist kein Chat-Modell, sondern nur für Embeddings.
