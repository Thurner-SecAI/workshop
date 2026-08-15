"""Gemeinsame Funktionen für die Notebooks in `01_prompt-engineering`.

Alle Notebooks des Ordners importieren diese Datei:

    from helfer import MODELL, frage_llm, lade_daten, zeige

Der Konfigurationsblock unten ist die einzige Stelle, an der der Modell-Zugang
steht. Wer statt Ollama einen Provider benutzt, tauscht `BASIS_URL`, `API_KEY`
und die beiden Modellnamen — sonst nichts.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

from openai import OpenAI

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

BREITE = 88                       # Zeichen je Zeile bei der Ausgabe

HINWEIS_KEIN_SERVER = f"""
Kein Kontakt zum Modell-Server unter {BASIS_URL}.

Prüfe der Reihe nach:
  1. Läuft Ollama?            ollama serve      (oder die Ollama-App starten)
  2. Ist das Modell da?       ollama pull {MODELL}
  3. Antwortet der Server?    curl {BASIS_URL}/models

Mit einem Provider statt Ollama: BASIS_URL, API_KEY und MODELL in helfer.py
austauschen.
""".strip()


# --------------------------------------------------------------------------- #
# Modell
# --------------------------------------------------------------------------- #

def frage_llm(prompt, system=None, temperature=0.0, modell=MODELL, max_tokens=600):
    """Eine Anfrage an das Modell, Rückgabe ist der reine Antworttext.

    Argumente:
        prompt: der User-Prompt.
        system: optionaler System Prompt.
        temperature: 0.0 antwortet so stabil wie möglich, höhere Werte streuen.
        modell: Modellname, per Voreinstellung `MODELL`.
        max_tokens: Obergrenze für die Antwortlänge.
    """
    nachrichten = []
    if system:
        nachrichten.append({"role": "system", "content": system})
    nachrichten.append({"role": "user", "content": prompt})

    try:
        antwort = client.chat.completions.create(
            model=modell,
            messages=nachrichten,
            temperature=temperature,
            max_tokens=max_tokens,
            **_reasoning_kwargs(),
        )
    except Exception as fehler:
        if _ist_verbindungsfehler(fehler):
            print(HINWEIS_KEIN_SERVER)
            raise RuntimeError(f"Modell-Server unter {BASIS_URL} nicht erreichbar") from None
        raise

    return (antwort.choices[0].message.content or "").strip()


def frage_dialog(nachrichten, temperature=0.0, modell=MODELL, max_tokens=600):
    """Sendet einen vollständigen Gesprächsverlauf und gibt den Antworttext zurück."""
    try:
        antwort = client.chat.completions.create(
            model=modell,
            messages=nachrichten,
            temperature=temperature,
            max_tokens=max_tokens,
            **_reasoning_kwargs(),
        )
    except Exception as fehler:
        if _ist_verbindungsfehler(fehler):
            print(HINWEIS_KEIN_SERVER)
            raise RuntimeError(f"Modell-Server unter {BASIS_URL} nicht erreichbar") from None
        raise

    return (antwort.choices[0].message.content or "").strip()


def frage_llm_viele(prompt, k=5, temperature=0.8, system=None, modell=MODELL,
                    max_tokens=600):
    """Stellt dieselbe Frage k-mal und gibt die k Antworten als Liste zurück.

    Die Aufrufe laufen nacheinander, nicht parallel — der Ablauf bleibt damit
    lesbar, und ein kleines Modell auf einem Laptop wird nicht überlastet.
    Sinnvoll ist eine `temperature` über 0, sonst kommt k-mal dasselbe heraus.
    """
    return [
        frage_llm(prompt, system=system, temperature=temperature,
                  modell=modell, max_tokens=max_tokens)
        for _ in range(k)
    ]


def _ist_verbindungsfehler(fehler) -> bool:
    """Erkennt Verbindungsfehler des OpenAI-Clients, ohne dessen Interna zu importieren."""
    namen = {typ.__name__ for typ in type(fehler).__mro__}
    if "APIConnectionError" in namen or "ConnectionError" in namen:
        return True
    return "connection error" in str(fehler).lower()


# --------------------------------------------------------------------------- #
# Daten
# --------------------------------------------------------------------------- #

def lade_daten(name):
    """Lädt `daten/<name>.json` und gibt den Inhalt als Liste oder Dictionary zurück.

    Der Ordner `daten/` wird neben dieser Datei gesucht, danach im aktuellen
    Verzeichnis und dessen übergeordneten Ordnern — so findet der Aufruf die
    Daten auch aus Google Colab heraus, wo die Dateien unter `/content` liegen.
    """
    datei = _daten_ordner() / f"{name.removesuffix('.json')}.json"
    if not datei.exists():
        vorhanden = sorted(p.stem for p in datei.parent.glob("*.json"))
        raise FileNotFoundError(
            f"{datei} fehlt. Vorhanden sind: {', '.join(vorhanden) or '(nichts)'}"
        )
    return json.loads(datei.read_text(encoding="utf-8"))


def _daten_ordner() -> Path:
    """Sucht den Ordner `daten/` — lokal wie in Colab."""
    hier = Path(__file__).resolve().parent
    basen = [hier, Path.cwd(), *Path.cwd().parents, Path("/content")]
    for basis in basen:
        for kandidat in (basis / "daten", basis / "01_prompt-engineering" / "daten"):
            if kandidat.is_dir():
                return kandidat
    raise FileNotFoundError(
        "Ordner 'daten/' nicht gefunden. Lege ihn neben helfer.py ab — in Colab "
        "nach /content/daten/ hochladen."
    )


# --------------------------------------------------------------------------- #
# Ausgabe
# --------------------------------------------------------------------------- #

def zeige(text, titel=None):
    """Gibt eine Modellantwort lesbar aus: optionale Überschrift, Zeilen umgebrochen."""
    if titel:
        print(titel)
        print("─" * min(BREITE, max(len(titel), 12)))
    print(_umbrich(str(text), BREITE))
    print()


def zeige_vergleich(spalten):
    """Stellt zwei bis vier Antworttexte gegenüber.

    `spalten` ist ein Dictionary aus Überschrift → Text, zum Beispiel
    `{"Zero-Shot": a, "Few-Shot": b}`. Kurze Texte stehen nebeneinander,
    lange untereinander — sonst bleibt je Spalte kein lesbarer Rest.
    """
    if not 2 <= len(spalten) <= 4:
        raise ValueError(f"zwei bis vier Spalten, nicht {len(spalten)}")

    texte = {str(k): str(v) for k, v in spalten.items()}
    laengste = max(len(t) for t in texte.values())

    if len(texte) <= 3 and laengste <= 500:
        breite = max(24, (BREITE - 3 * (len(texte) - 1)) // len(texte))
        bloecke = [_umbrich(t, breite).split("\n") for t in texte.values()]
        hoehe = max(len(b) for b in bloecke)

        kopf = "   ".join(f"{k[:breite]:<{breite}}" for k in texte)
        print(kopf.rstrip())
        print("   ".join("─" * breite for _ in texte))
        for zeile in range(hoehe):
            teile = [(b[zeile] if zeile < len(b) else "") for b in bloecke]
            print("   ".join(f"{t:<{breite}}" for t in teile).rstrip())
        print()
        return

    for kopf, text in texte.items():
        zeige(text, titel=kopf)


def _umbrich(text: str, breite: int) -> str:
    """Bricht Zeilen um, behält Absätze und Zeilenumbrüche des Originals."""
    zeilen = []
    for zeile in text.splitlines():
        if not zeile.strip():
            zeilen.append("")
            continue
        zeilen += textwrap.wrap(zeile, width=breite,
                                break_long_words=False, break_on_hyphens=False) or [""]
    return "\n".join(zeilen)


# --------------------------------------------------------------------------- #
# Messen
# --------------------------------------------------------------------------- #

def messe_treffer(vorhersagen, sollwerte) -> float:
    """Anteil exakter Übereinstimmungen zwischen Vorhersagen und Sollwerten (0.0–1.0).

    Verglichen wird nach Kleinschreibung und ohne umgebende Leerzeichen; ein
    fehlender Wert (`None`) zählt nie als Treffer.
    """
    vorhersagen, sollwerte = list(vorhersagen), list(sollwerte)
    if len(vorhersagen) != len(sollwerte):
        raise ValueError(
            f"{len(vorhersagen)} Vorhersagen, aber {len(sollwerte)} Sollwerte"
        )
    if not sollwerte:
        return 0.0

    treffer = sum(
        1 for v, s in zip(vorhersagen, sollwerte)
        if v is not None and str(v).strip().lower() == str(s).strip().lower()
    )
    return treffer / len(sollwerte)
