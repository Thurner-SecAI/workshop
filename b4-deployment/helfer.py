"""Gemeinsame Funktionen für die Notebooks in `04_deployment`.

Alle fünf Notebooks importieren diese Datei:

    import helfer
    from helfer import GB, frage_llm, lade_daten, messe_anfrage, zeige_tabelle

Die LLM-Naht ist der Konfigurationsblock unten. Wer einen anderen Provider
benutzt, tauscht `BASIS_URL`, `API_KEY` und `MODELL` — sonst ändert sich nichts.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

from openai import OpenAI

# --- Die LLM-Naht ----------------------------------------------------------
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

# --- Einheiten -------------------------------------------------------------
# VRAM und Modellgrößen werden in Dezimal-Gigabyte ausgewiesen, nicht in GiB.
# Alle Notebooks rechnen mit dieser Konstanten, damit die Zahlen vergleichbar
# bleiben.
GB = 10**9

_ORDNER = Path(__file__).resolve().parent
_KODIERER = None


# --- Modellzugriff ---------------------------------------------------------
def frage_llm(prompt, system=None, temperature=0.0, modell=MODELL, max_tokens=600):
    """Eine Anfrage an das Modell, Rückgabe ist der reine Antworttext.

    `system` ist optional und wird als System Prompt vorangestellt.
    `temperature=0.0` hält die Antworten so reproduzierbar wie möglich.
    """
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


def messe_anfrage(prompt, modell=MODELL, **kwargs):
    """Eine Anfrage messen: Latency, Time to First Token und Throughput.

    Die Anfrage läuft als Stream, damit die Zeit bis zum ersten Token (`ttft`)
    wirklich gemessen und nicht geschätzt wird.

    Rückgabe:
        {"antwort": str,               der vollständige Antworttext
         "sekunden": float,            gesamte Dauer der Anfrage
         "ttft": float,                Sekunden bis zum ersten Token
         "prompt_tokens": int,         Tokens im Prompt
         "antwort_tokens": int,        Tokens in der Antwort
         "tokens_pro_sekunde": float}  Antwort-Tokens je Sekunde nach dem ersten
    """
    system = kwargs.pop("system", None)
    temperature = kwargs.pop("temperature", 0.0)
    max_tokens = kwargs.pop("max_tokens", 600)

    nachrichten = []
    if system:
        nachrichten.append({"role": "system", "content": system})
    nachrichten.append({"role": "user", "content": prompt})

    # Ein ausdrücklich übergebenes reasoning_effort hat Vorrang: der
    # Messabschnitt zu Reasoning-Modellen braucht beide Fälle.
    for name, wert in _reasoning_kwargs().items():
        kwargs.setdefault(name, wert)

    start = time.perf_counter()
    ttft = None
    stuecke = []
    verbrauch = None

    strom = client.chat.completions.create(
        model=modell,
        messages=nachrichten,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
        stream_options={"include_usage": True},
        **kwargs,
    )
    for teil in strom:
        if getattr(teil, "usage", None):
            verbrauch = teil.usage
        if not teil.choices:
            continue
        inhalt = teil.choices[0].delta.content
        if inhalt:
            if ttft is None:
                ttft = time.perf_counter() - start
            stuecke.append(inhalt)

    dauer = time.perf_counter() - start
    antwort = "".join(stuecke)

    if verbrauch is not None:
        prompt_tokens = verbrauch.prompt_tokens
        antwort_tokens = verbrauch.completion_tokens
    else:
        prompt_tokens = zaehle_tokens(prompt)
        antwort_tokens = zaehle_tokens(antwort)

    # Die Generierung beginnt erst mit dem ersten Token. Vorher läuft das
    # Prefill über den Prompt, das gehört nicht in die Generierungsrate.
    if ttft is None:
        ttft = dauer
    generierung = dauer - ttft
    if antwort_tokens > 1 and generierung > 0.01:
        tokens_pro_sekunde = (antwort_tokens - 1) / generierung
    else:
        # Kam alles in einem Stück, ist die Rate über die ganze Anfrage die
        # einzige Zahl, die sich sinnvoll angeben lässt.
        tokens_pro_sekunde = antwort_tokens / dauer if dauer > 0 else 0.0

    return {
        "antwort": antwort.strip(),
        "sekunden": dauer,
        "ttft": ttft,
        "prompt_tokens": prompt_tokens,
        "antwort_tokens": antwort_tokens,
        "tokens_pro_sekunde": tokens_pro_sekunde,
    }


# --- Daten -----------------------------------------------------------------
def lade_daten(name):
    """Lädt `daten/<name>.json` und gibt Liste oder Dictionary zurück.

    Gesucht wird neben dieser Datei, im aktuellen Verzeichnis und in dessen
    übergeordneten Ordnern — damit der Aufruf auch dann funktioniert, wenn das
    Notebook in Colab aus einem anderen Arbeitsverzeichnis heraus läuft.
    """
    if not name.endswith(".json"):
        name += ".json"

    kandidaten = [_ORDNER, Path.cwd(), *Path.cwd().parents]
    for wurzel in kandidaten:
        pfad = wurzel / "daten" / name
        if pfad.exists():
            return json.loads(pfad.read_text(encoding="utf-8"))
        pfad = wurzel / "04_deployment" / "daten" / name
        if pfad.exists():
            return json.loads(pfad.read_text(encoding="utf-8"))

    orte = ", ".join(str(k / "daten" / name) for k in kandidaten[:3])
    raise FileNotFoundError(
        f"{name} nicht gefunden. Gesucht in: {orte}. "
        f"In Colab: den Ordner 04_deployment mit hochladen."
    )


# --- Tokens ----------------------------------------------------------------
def zaehle_tokens(text):
    """Zählt die Tokens eines Textes mit dem Tokenizer `cl100k_base`.

    Der Tokenizer eines lokalen Modells ist ein anderer; die Zahl ist eine
    belastbare Näherung für Kontextlänge und Kosten, kein exakter Wert für
    Llama oder Gemma.
    """
    global _KODIERER
    if _KODIERER is None:
        import tiktoken
        _KODIERER = tiktoken.get_encoding("cl100k_base")
    return len(_KODIERER.encode(text))


# --- Ausgabe ---------------------------------------------------------------
def zeige_tabelle(zeilen, spalten=None):
    """Zeigt eine Liste von Dictionaries als Tabelle an.

    `spalten` wählt die Spalten aus und legt ihre Reihenfolge fest. Ohne
    Angabe werden alle Schlüssel in der Reihenfolge des ersten Eintrags
    genommen. Zahlen werden auf zwei Nachkommastellen gerundet.
    """
    import pandas as pd

    if not zeilen:
        print("(keine Zeilen)")
        return

    rahmen = pd.DataFrame(zeilen)
    if spalten:
        rahmen = rahmen[[s for s in spalten if s in rahmen.columns]]

    for spalte in rahmen.columns:
        if pd.api.types.is_float_dtype(rahmen[spalte]):
            rahmen[spalte] = rahmen[spalte].round(2)

    try:
        from IPython.display import display
        display(rahmen.style.hide(axis="index").format(precision=2))
    except Exception:
        print(rahmen.to_string(index=False))


# --- Selbsttest ------------------------------------------------------------
if __name__ == "__main__":
    print(f"Ordner:     {_ORDNER}")
    print(f"Modell:     {MODELL} über {BASIS_URL}")
    print(f"GB:         {GB:,}".replace(",", "."))
    for name, schluessel in (("model_cards", "modelle"), ("hardware", "karten"),
                             ("szenarien", "szenarien")):
        daten = lade_daten(name)
        print(f"daten/{name}.json: {len(daten[schluessel])} Einträge "
              f"(Stand {daten['stand']})")
    print(f"zaehle_tokens: {zaehle_tokens('CVE-2026-3224 im Runbook')} Tokens")
    if os.environ.get("MIT_LLM"):
        messung = messe_anfrage("Answer with one word: ready?")
        print(f"messe_anfrage: {messung['antwort_tokens']} Tokens, "
              f"{messung['tokens_pro_sekunde']:.1f} Tokens/s, "
              f"TTFT {messung['ttft']:.2f} s")
