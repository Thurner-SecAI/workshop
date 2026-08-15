"""Gemeinsame Funktionen für das Fine-Tuning-Kapitel.

Alles, was mechanisch ist und im Notebook nur ablenken würde: Gerätewahl,
Modelle laden, JSONL lesen, Batch-Generierung, Dateigrößen.
"""

from __future__ import annotations

import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

HIER = Path(__file__).resolve().parent
DATEN = HIER / "daten"
AUSGABE = HIER / "ausgabe"

# Modelle von Hugging Face. Beide sind klein genug für einen Laptop.
BASIS_MODELL = "HuggingFaceTB/SmolLM2-135M"
INSTRUCT_MODELL = "HuggingFaceTB/SmolLM2-135M-Instruct"

# Einheitliche Farben für alle Diagramme in diesem Notebook.
BLAU, ORANGE, GRAU = "#2563eb", "#e8590c", "#6b7280"


def waehle_geraet() -> str:
    """MPS auf Apple Silicon, sonst CUDA, sonst CPU."""
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def lade_jsonl(name: str) -> list[dict]:
    """Liest eine JSONL-Datei aus `daten/` als Liste von Dicts."""
    text = (DATEN / name).read_text(encoding="utf-8")
    return [json.loads(zeile) for zeile in text.splitlines() if zeile.strip()]


def lade_modell(name: str, geraet: str):
    """Lädt Tokenizer und Modell. Der Download passiert einmalig."""
    tokenizer = AutoTokenizer.from_pretrained(name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    modell = AutoModelForCausalLM.from_pretrained(name, dtype=torch.float32)
    return tokenizer, modell.to(geraet)


@torch.no_grad()
def erzeuge_antworten(modell, tokenizer, prompts: list[str],
                      max_new_tokens: int = 48, batch: int = 16,
                      bis_zeilenende: bool = True) -> list[str]:
    """Greedy Decoding für viele Prompts auf einmal.

    Mit `bis_zeilenende=True` kommt je Prompt die **erste Zeile** der
    Fortsetzung zurück — das Triage-Objekt steht auf genau einer Zeile.
    Mit `False` kommt die ganze Fortsetzung.
    """
    modell.eval()
    tokenizer.padding_side = "left"   # links auffüllen, damit alle Prompts
    antworten = []                    # an derselben Position enden
    for start in range(0, len(prompts), batch):
        teil = prompts[start:start + batch]
        eingabe = tokenizer(teil, return_tensors="pt", padding=True)
        eingabe = {k: v.to(modell.device) for k, v in eingabe.items()}
        erzeugt = modell.generate(**eingabe, max_new_tokens=max_new_tokens,
                                  do_sample=False,
                                  pad_token_id=tokenizer.pad_token_id)
        neu = erzeugt[:, eingabe["input_ids"].shape[1]:]
        for text in tokenizer.batch_decode(neu, skip_special_tokens=True):
            antworten.append(text.split("\n")[0].strip() if bis_zeilenende
                             else text)
    return antworten


def groesse_mb(pfad: Path) -> float:
    """Belegter Platz einer Datei oder eines Ordners in MB."""
    pfad = Path(pfad)
    if pfad.is_file():
        return pfad.stat().st_size / 1e6
    return sum(p.stat().st_size for p in pfad.rglob("*") if p.is_file()) / 1e6
