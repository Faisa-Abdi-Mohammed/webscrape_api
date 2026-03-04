import json
import os
from typing import Any


def ensure_dir(path: str) -> None:
    """Skapar mappen om den inte finns."""
    os.makedirs(path, exist_ok=True)


def read_json(path: str, default: Any):
    """
    Läser JSON från fil.
    Om filen inte finns returneras 'default' (t.ex. None eller []).
    """
    if not os.path.exists(path):
        return default

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, data: Any) -> None:
    """
    Skriver data som JSON till fil.
    Skapar mapparna automatiskt om de saknas.
    """
    folder = os.path.dirname(path)
    if folder:
        ensure_dir(folder)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)