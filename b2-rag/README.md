# Modul B · Kapitel 3 — Retrieval Augmented Generation

Ein Sprachmodell weiß nichts über die Systeme, Runbooks und Advisories eines
Unternehmens. RAG legt ihm die passenden Ausschnitte in den Prompt. Dieser
Ordner baut die Kette Schritt für Schritt: Knowledge Base, Chunking, Suche,
Prompt.

Durchgehendes Beispiel ist das Security Operations Center der (erfundenen)
Nordlicht Logistik SE.

## Notebooks

| Notebook | Thema | Was du baust |
|---|---|---|
| `01_chunking` | Knowledge Base und Chunking | zwei eigene Chunking-Verfahren, Vergleich mit `RecursiveCharacterTextSplitter`, Chunks mit Metadaten in Chroma |
| `02_keyword_search` | Keyword Search | Suche über Wortübereinstimmung, BM25, und woran sie scheitert |
| `03_semantic_search` | Semantic Search | Embeddings, Cosine Similarity, Suche über die Vector Database |
| `04_augmented_prompt` | Augmented Prompt | Kontext in den Prompt setzen, Quellenangaben, Antworten ohne Beleg verweigern |
| `bonus_hybrid_search` | Hybrid Search | Keyword und Semantic kombinieren, Reciprocal Rank Fusion |
| `bonus_hnsw` | HNSW | wie eine Vector Database schnell sucht, exakt gegen approximativ |

Zu jedem Notebook gehört ein Paar: `NN_thema.ipynb` ist die Teilnehmenden-Fassung,
`NN_thema_solved.ipynb` enthält alle Lösungen. Jedes Notebook läuft eigenständig;
die Zwischenergebnisse liegen als Datei in `daten/`.

## Setup

```bash
pip install -r requirements.txt

ollama pull qwen3.5:0.8b
ollama pull nomic-embed-text
ollama serve
```

Ohne lokales Ollama läuft alles auch über einen Provider — dafür `BASIS_URL`,
`API_KEY` und die beiden Modellnamen in **`helfer.py`** tauschen. Das ist die
einzige Stelle; die Notebooks importieren die Namen von dort und sprechen
ausschließlich über den OpenAI-Client mit dem Modell.

Alle Notebooks importieren `helfer.py`:

```python
import helfer

dokumente = helfer.lade_dokumente()      # Wissensbasis
chunks    = helfer.lade_chunks()         # vorgechunkte Fassung
fragen    = helfer.lade_fragen()         # Evaluationsfragen
sammlung  = helfer.baue_chroma(chunks)   # Vector Database, persistent
```

## Daten

```
daten/
├── wissensbasis/        11 Markdown-Dokumente — die Knowledge Base
├── fallstricke/          4 Dokumente für die Grenzen der Keyword Search
├── chunks.json          die Wissensbasis vorgechunkt (90 Chunks)
├── fragen.json          10 Fragen mit erwarteten Dokumenten und Antworten
├── erzeuge_chunks.py    erzeugt chunks.json neu
├── embedding_cache.json berechnete Embeddings, damit nichts doppelt läuft
└── chroma/              die persistente Vector Database (wird erzeugt)
```

### Wissensbasis

| Dokument | Art | Umfang |
|---|---|---|
| `cve-2026-3224.md` | CVE-Advisory, Authentication Bypass, CVSS 9.8 | mittel |
| `cve-2026-1187.md` | CVE-Advisory, SQL Injection, CVSS 8.1 | mittel |
| `cve-2026-4410.md` | CVE-Advisory, Denial of Service, CVSS 5.9, kein Patch | mittel |
| `cve-2025-9042.md` | CVE-Advisory, Privilege Escalation, CVSS 7.8, behoben | kurz |
| `runbook-incident-response.md` | Runbook, Schweregrade und Ablauf | mittel |
| `runbook-patch-management.md` | Runbook, Fristen und Notfallweg | mittel |
| `runbook-zugriffskontrolle.md` | Runbook, Eintritt, Wechsel, Austritt | mittel |
| `policy-passwoerter-und-mfa.md` | Richtlinie | mittel |
| `policy-logging-und-aufbewahrung.md` | Richtlinie, Aufbewahrungsfristen | mittel |
| `postmortem-2026-03-14-vpn.md` | Post-Mortem zu CVE-2026-3224 | mittel |
| `systemdoku-sentinelgrid.md` | Systemdokumentation der SIEM-Plattform | lang, rund 2.500 Wörter |

Die Dokumente sind erfunden, aber fachlich stimmig. Sie haben unterschiedliche
Länge und Struktur — mit Überschriften, Tabellen und Listen. Genau daran werden
die Unterschiede zwischen den Chunking-Verfahren messbar.

### Fallstricke

Vier Dokumente rund um den Suchbegriff *Token rotieren*, für die Grenzen der
Keyword Search: ein sehr großes Betriebshandbuch, das den Begriff nebenbei
erwähnt; eine Wiki-Seite mit Keyword Stuffing; das eigentliche Runbook mit der
Antwort; und eine Notiz, in der *Token* und *rotieren* etwas ganz anderes
bedeuten.

### Schema

`chunks.json`:

```json
{"chunk_id": "cve-2026-3224#03", "dok_id": "cve-2026-3224",
 "titel": "CVE-2026-3224 — Authentication Bypass in NorthPeak SecureGate",
 "quelle": "wissensbasis/cve-2026-3224.md", "text": "…", "position": 3}
```

`fragen.json`:

```json
{"frage": "Welchen CVSS-Wert hat CVE-2026-3224?",
 "erwartete_dok_ids": ["cve-2026-3224"],
 "erwartete_antwort": "CVSS v3.1 Base Score 9.8, Einstufung critical."}
```

`chunks.json` neu erzeugen:

```bash
python daten/erzeuge_chunks.py
```

## Vector Database

Die Chroma-Collection heißt `wissensbasis` und liegt persistent unter
`daten/chroma/`. Notebook 1 legt sie an, die folgenden Notebooks öffnen sie
mit `helfer.lade_chroma()`. Fehlt sie, baut `helfer.baue_chroma(helfer.lade_chunks())`
sie in wenigen Sekunden neu — die Embeddings kommen aus dem Cache.
