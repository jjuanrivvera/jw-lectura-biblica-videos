#!/usr/bin/env python3
"""Imprime cada palabra de la voz con su tiempo dentro de la escena (ya sumado el silencio inicial)."""
import json, sys
from pathlib import Path
A = Path(__file__).resolve().parent.parent / "video/audio"
LEAD = 0.6
for n in sys.argv[1:]:
    W = json.loads((A / f"escena-{n}.words.json").read_text())
    print(n, " ".join(f"{w['w']}@{w['t']+LEAD:.1f}" for w in W), "\n")
