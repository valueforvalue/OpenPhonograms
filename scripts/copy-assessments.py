# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Copy stage assessment PDFs into build/assessments/ for the release ZIP.

Usage:
  python scripts/copy-assessments.py
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
OUT = BUILD / "assessments"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for stage in range(1, 6):
        stage_dir = BUILD / f"stage-{stage}"
        if not stage_dir.exists():
            continue
        for pdf in stage_dir.glob("assessment-*.pdf"):
            dest = OUT / pdf.name
            shutil.copy(pdf, dest)
            count += 1
    print(f"==> Copied {count} assessment PDFs to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
