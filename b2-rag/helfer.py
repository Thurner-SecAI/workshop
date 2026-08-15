"""Gemeinsame Funktionen der RAG-Notebooks in `moduleB/challenges/02_rag/`.

Alle Notebooks dieses Ordners importieren diese Datei:

    import helfer
    dokumente = helfer.lade_dokumente()
    chunks = helfer.lade_chunks()

Die Datei kapselt vier Dinge: den Zugang zum Modell (`frage_llm`, `embed`),
das Laden der vorbereiteten Daten (`lade_dokumente`, `lade_chunks`,
`lade_fragen`), die Vector Database (`baue_chroma`, `lade_chroma`) und ein
paar Ausgabehilfen (`zaehle_tokens`, `zeige_chunks`, `zeige_treffer`).

Kein Netzzugriff außer zum lokalen Modellserver. Alle Daten liegen in `daten/`.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from openai import OpenAI

# --- Die LLM-Naht ---------------------------------------------------------
# Ollama, lokal. Für einen Provider: base_url und api_key tauschen, Modellname anpassen.
BASIS_URL = "http://localhost:11434/v1"
API_KEY = "ollama"                # Ollama prüft den Key nicht
MODELL = "qwen3.5:0.8b"           # 1,0 GB, läuft auf jedem Laptop
EMBEDDING_MODELL = "nomic-embed-text"

# qwen3.5 denkt vor der Antwort. Über die OpenAI-API kommt dann ein leerer
# `content` zurück, weil das Token-Budget ins Denken geht. `reasoning_effort`
# schaltet das ab; Modelle ohne Reasoning ignorieren das Argument.
# Auf None setzen, falls ein Provider den Parameter nicht kennt.
REASONING = "none"

client = OpenAI(base_url=BASIS_URL, api_key=API_KEY)


def _reasoning_kwargs():
    """Der Zusatz, den Reasoning-Modelle brauchen — oder nichts."""
    return {"reasoning_effort": REASONING} if REASONING else {}

# --- Pfade ----------------------------------------------------------------
HIER = Path(__file__).resolve().parent
DATEN = HIER / "daten"
WISSENSBASIS = DATEN / "wissensbasis"
FALLSTRICKE = DATEN / "fallstricke"
CHUNK_DATEI = DATEN / "chunks.json"
FRAGEN_DATEI = DATEN / "fragen.json"
CACHE_DATEI = DATEN / "embedding_cache.json"
CHROMA_PFAD = DATEN / "chroma"

SAMMLUNG = "wissensbasis"         # Name der Chroma-Collection


# --- Modellaufrufe --------------------------------------------------------
def frage_llm(prompt, system=None, temperature=0.0, modell=MODELL, max_tokens=600):
    """Eine Anfrage an das Modell, Rückgabe ist der reine Antworttext."""
    nachrichten = []
    if system:
        nachrichten.append({"role": "system", "content": system})
    nachrichten.append({"role": "user", "content": prompt})

    antwort = client.chat.completions.create(
        model=modell,
        messages=nachrichten,
        temperature=temperature,
        max_tokens=max_tokens,
        **_reasoning_kwargs(),
    )
    return (antwort.choices[0].message.content or "").strip()


_cache: dict[str, list[float]] | None = None


def _cache_laden():
    """Liest den Embedding-Cache einmalig von der Platte."""
    global _cache
    if _cache is None:
        if CACHE_DATEI.exists():
            _cache = json.loads(CACHE_DATEI.read_text(encoding="utf-8"))
        else:
            _cache = {}
    return _cache


def _schluessel(text, modell):
    """Eindeutiger Schlüssel für ein Textstück und ein Embedding-Modell."""
    roh = f"{modell}\x00{text}".encode("utf-8")
    return hashlib.sha1(roh).hexdigest()


def embed(texte, modell=EMBEDDING_MODELL):
    """Embeddings für eine Liste von Texten, als Liste von Vektoren.

    Bereits berechnete Vektoren kommen aus `daten/embedding_cache.json` und
    werden nicht erneut angefragt. Neue Texte gehen in Blöcken von 32 an den
    Server.
    """
    if isinstance(texte, str):
        raise TypeError("embed() erwartet eine Liste von Texten, keinen einzelnen String")

    cache = _cache_laden()
    schluessel = [_schluessel(t, modell) for t in texte]
    offen = [i for i, s in enumerate(schluessel) if s not in cache]

    for start in range(0, len(offen), 32):
        block = offen[start:start + 32]
        antwort = client.embeddings.create(model=modell, input=[texte[i] for i in block])
        for i, eintrag in zip(block, antwort.data):
            cache[schluessel[i]] = list(eintrag.embedding)

    if offen:
        CACHE_DATEI.parent.mkdir(parents=True, exist_ok=True)
        CACHE_DATEI.write_text(json.dumps(cache), encoding="utf-8")

    return [cache[s] for s in schluessel]


# --- Daten laden ----------------------------------------------------------
def lade_dokumente(ordner=None):
    """Die Wissensbasis aus `daten/wissensbasis/*.md`.

    Rückgabe ist eine Liste von Dicts mit den Schlüsseln `id`, `titel`,
    `quelle` und `text`. Der Titel ist die erste Überschrift der Datei.
    Mit `ordner` lässt sich ein anderes Verzeichnis lesen, etwa
    `helfer.FALLSTRICKE`.
    """
    verzeichnis = Path(ordner) if ordner else WISSENSBASIS
    dokumente = []
    for pfad in sorted(verzeichnis.glob("*.md")):
        text = pfad.read_text(encoding="utf-8").strip()
        treffer = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
        dokumente.append({
            "id": pfad.stem,
            "titel": treffer.group(1).strip() if treffer else pfad.stem,
            "quelle": f"{verzeichnis.name}/{pfad.name}",
            "text": text,
        })
    return dokumente


def lade_chunks():
    """Die vorbereiteten Chunks aus `daten/chunks.json`.

    Jeder Chunk ist ein Dict mit `chunk_id`, `dok_id`, `titel`, `quelle`,
    `text` und `position`. Erzeugt wird die Datei von
    `daten/erzeuge_chunks.py`.
    """
    if not CHUNK_DATEI.exists():
        raise FileNotFoundError(
            f"{CHUNK_DATEI} fehlt. Erzeugen mit: python daten/erzeuge_chunks.py")
    return json.loads(CHUNK_DATEI.read_text(encoding="utf-8"))


def lade_fragen():
    """Die Evaluationsfragen aus `daten/fragen.json`.

    Jede Frage ist ein Dict mit `frage`, `erwartete_dok_ids` und
    `erwartete_antwort`.
    """
    return json.loads(FRAGEN_DATEI.read_text(encoding="utf-8"))


# --- Vector Database ------------------------------------------------------
def baue_chroma(chunks, name=SAMMLUNG, neu=False):
    """Schreibt Chunks in eine persistente Chroma-Collection und gibt sie zurück.

    Die Collection liegt unter `daten/chroma/` und bleibt nach dem Notebook
    erhalten. Chunks, deren `chunk_id` schon in der Collection steht, werden
    übersprungen. Mit `neu=True` wird die Collection vorher gelöscht.
    """
    import chromadb

    CHROMA_PFAD.mkdir(parents=True, exist_ok=True)
    klient = chromadb.PersistentClient(path=str(CHROMA_PFAD))

    if neu:
        try:
            klient.delete_collection(name)
        except Exception:
            pass

    sammlung = klient.get_or_create_collection(name, metadata={"hnsw:space": "cosine"})

    vorhanden = set(sammlung.get(include=[])["ids"])
    fehlend = [c for c in chunks if c["chunk_id"] not in vorhanden]

    for start in range(0, len(fehlend), 64):
        block = fehlend[start:start + 64]
        texte = [c["text"] for c in block]
        sammlung.add(
            ids=[c["chunk_id"] for c in block],
            embeddings=embed(texte),
            documents=texte,
            metadatas=[{"dok_id": c["dok_id"], "titel": c["titel"],
                        "quelle": c["quelle"], "position": int(c["position"])}
                       for c in block],
        )

    return sammlung


def lade_chroma(name=SAMMLUNG):
    """Öffnet die persistente Chroma-Collection aus `daten/chroma/`."""
    import chromadb

    if not CHROMA_PFAD.exists():
        raise FileNotFoundError(
            f"{CHROMA_PFAD} fehlt. Zuerst helfer.baue_chroma(helfer.lade_chunks()) aufrufen.")

    klient = chromadb.PersistentClient(path=str(CHROMA_PFAD))
    return klient.get_collection(name)


# --- Ausgabe --------------------------------------------------------------
_kodierung = None


def zaehle_tokens(text):
    """Zahl der Tokens eines Textes, gemessen mit dem Tokenizer `cl100k_base`.

    Steht tiktoken nicht zur Verfügung, wird mit vier Zeichen je Token
    geschätzt.
    """
    global _kodierung
    if _kodierung is None:
        try:
            import tiktoken
            _kodierung = tiktoken.get_encoding("cl100k_base")
        except Exception:
            _kodierung = False
    if _kodierung is False:
        return max(1, round(len(text) / 4))
    return len(_kodierung.encode(text))


def _als_text(chunk):
    """Ein Chunk ist entweder ein String oder ein Dict mit `text`."""
    return chunk["text"] if isinstance(chunk, dict) else chunk


def zeige_chunks(chunks, n=3):
    """Druckt die ersten `n` Chunks mit Länge, Tokenzahl und Anfang."""
    print(f"{len(chunks)} Chunks, davon die ersten {min(n, len(chunks))}:")
    for i, chunk in enumerate(chunks[:n]):
        text = _als_text(chunk)
        kopf = f"[{i}]"
        if isinstance(chunk, dict):
            kopf = f"[{chunk.get('chunk_id', i)}] {chunk.get('titel', '')}"
        print()
        print(f"{kopf}  ({len(text)} Zeichen, {zaehle_tokens(text)} Tokens)")
        print("  " + text[:280].replace("\n", "\n  ") + ("…" if len(text) > 280 else ""))


def _treffer_liste(ergebnisse):
    """Bringt Chroma-Ergebnisse und eigene Trefferlisten auf dieselbe Form."""
    if isinstance(ergebnisse, dict) and "documents" in ergebnisse:
        dokumente = ergebnisse["documents"][0]
        metadaten = (ergebnisse.get("metadatas") or [[{}] * len(dokumente)])[0]
        abstaende = (ergebnisse.get("distances") or [[None] * len(dokumente)])[0]
        kennungen = (ergebnisse.get("ids") or [[""] * len(dokumente)])[0]
        return [{"chunk_id": k, "titel": (m or {}).get("titel", ""), "text": d,
                 "score": None if a is None else 1 - a}
                for k, m, d, a in zip(kennungen, metadaten, dokumente, abstaende)]

    liste = []
    for eintrag in ergebnisse:
        if isinstance(eintrag, tuple):
            score, chunk = eintrag
        else:
            chunk, score = eintrag, eintrag.get("score")
        liste.append({"chunk_id": chunk.get("chunk_id", ""), "titel": chunk.get("titel", ""),
                      "text": chunk["text"], "score": score})
    return liste


def zeige_treffer(ergebnisse):
    """Druckt Rang, Score, Titel und Textanfang einer Trefferliste.

    Nimmt das Ergebnis von `sammlung.query(...)` oder eine eigene Liste von
    Chunk-Dicts mit `score`.
    """
    treffer = _treffer_liste(ergebnisse)
    if not treffer:
        print("Keine Treffer.")
        return
    for rang, t in enumerate(treffer, start=1):
        score = "  —  " if t["score"] is None else f"{t['score']:.3f}"
        anfang = " ".join(t["text"].split())[:150]
        print(f"{rang}. {score}  {t['titel']}  [{t['chunk_id']}]")
        print(f"     {anfang}…")
