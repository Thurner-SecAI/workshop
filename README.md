# Workshop-Challenges

Die Aufgaben zu den ML-Workshops. Ein Ordner pro Thema, darin
Jupyter-Notebooks mit Erklärung, Code zum Ergänzen und Selbsttests.

> Dieses Repo wird aus dem Autorenrepo erzeugt. Änderungen hier werden
> beim nächsten Lauf überschrieben — für Rückmeldungen bitte ein Issue.

## Loslegen

```bash
git clone https://github.com/Thurner-SecAI/workshop.git
cd workshop
```

Wer kein Git hat: oben rechts **Code → Download ZIP**.

## Modul A · Machine-Learning-Grundlagen

Reines Python mit NumPy, scikit-learn und PyTorch. Kein Sprachmodell, kein Ollama. Die `requirements.txt` im jeweiligen Ordner reicht.

| Ordner | Thema | Notebooks |
|---|---|:--:|
| [`a1-lineare-regression/`](a1-lineare-regression/) — Lineare Regression | Modellfunktion, Kostenfunktion, Gradientenabstieg — am Hauspreis | 3 |
| [`a2-logistische-regression/`](a2-logistische-regression/) — Logistische Regression | Sigmoid, Log-Loss, Schwellenwert — Klassifikation auf Tumordaten | 1 |
| [`a3-neuronale-netze/`](a3-neuronale-netze/) — Neuronale Netze | ReLU, Softmax, drei Schichten — handgeschriebene Ziffern erkennen | 1 |
| [`a4-gpt/`](a4-gpt/) — GPT selbst bauen | Tokenizer, Attention, Transformer-Block, Training — vier Teile bis zum MiniGPT | 4 |

`a4-gpt` braucht keine Datendateien und läuft deshalb auch in Google Colab: [teil1](https://colab.research.google.com/github/Thurner-SecAI/workshop/blob/main/a4-gpt/teil1.ipynb) · [teil2](https://colab.research.google.com/github/Thurner-SecAI/workshop/blob/main/a4-gpt/teil2.ipynb) · [teil3](https://colab.research.google.com/github/Thurner-SecAI/workshop/blob/main/a4-gpt/teil3.ipynb) · [teil4](https://colab.research.google.com/github/Thurner-SecAI/workshop/blob/main/a4-gpt/teil4.ipynb)

## Modul B · LLM Engineering

Braucht ein Sprachmodell auf dem eigenen Rechner. Die Anleitung steht in [`SETUP.md`](SETUP.md) und gehört **vor** den Workshop erledigt — rund 1,3 GB Download.

| Ordner | Thema | Notebooks |
|---|---|:--:|
| [`b1-prompt-engineering/`](b1-prompt-engineering/) — Prompt Engineering | TCREI, Few-Shot, Chain of Thought, Self-Consistency, Tree of Thought, ReAct | 7 |
| [`b2-rag/`](b2-rag/) — Retrieval Augmented Generation | Chunking, Keyword Search, Semantic Search, Augmented Prompt | 6 |
| [`b3-fine-tuning/`](b3-fine-tuning/) — Fine-Tuning | Base gegen Instruct, LoRA, Bonus QLoRA | 1 |
| [`b4-deployment/`](b4-deployment/) — Deployment und Inference | Model Cards, Quantisierung, Runtime und API, Durchsatz, Modellauswahl | 5 |

## Wie ein Notebook aufgebaut ist

Erklärender Text, ausgeführter Beispielcode, dann eine Aufgabe mit
vorbereiteter Funktion und Selbsttest. Der Selbsttest sagt dir, ob deine
Lösung stimmt — es gibt keine Lösungsdateien in diesem Repo.

Bis auf die oben genannte Ausnahme lesen die Notebooks ihre Daten aus dem
Ordner daneben (`data/` bzw. `daten/`). Sie laufen deshalb lokal, nicht in
Google Colab: dort fehlen die Dateien.

Stand: 17.08.2026
