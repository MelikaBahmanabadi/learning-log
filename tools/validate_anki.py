#!/usr/bin/env python3
"""
Validate Anki flashcard TSV files in each learning area.

Checks for every <deck>_anki.txt file under a learning area:
  1. The corresponding <deck>-fa_anki.txt file exists, and both files have
     the same number of data rows (Front/Back/Tags).
  2. Every data row has exactly 3 tab-separated columns (Front, Back, Tags).
  3. No unescaped tab or newline is embedded inside a Front or Back field
     (i.e. inside the <div ...>...</div> block for that column).

Run with no arguments to validate every area, or pass a path:

    python3 tools/validate_anki.py
    python3 tools/validate_anki.py self-improving-ai-agents
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HEAD_LINE = re.compile(r"^#(?!columns:)(?!tags column:)(?!notetype:)(?!deck:)(?!separator:)(?!html:)")
COLUMNS_HEADER = re.compile(r"^#columns:\s*(\S+)\s+(\S+)\s+(\S+)\s*$")


def find_anki_pairs(area: Path) -> list[tuple[Path, Path]]:
    """Return list of (en_tsv, fa_tsv) pairs in `area`."""
    en_files = sorted(area.glob("*_anki.txt"))
    pairs: list[tuple[Path, Path]] = []
    for en in en_files:
        if en.name.endswith("_needs_review_anki.txt"):
            continue
        # Skip Persian TSVs; we'll find them via the English file.
        if "-fa_" in en.name or "_fa_" in en.name:
            continue
        stem = en.name[: -len("_anki.txt")]
        fa = area / f"{stem}-fa_anki.txt"
        if fa.exists():
            pairs.append((en, fa))
        else:
            print(f"  WARN: {en.relative_to(REPO_ROOT)} has no Persian counterpart")
    return pairs


def data_rows(path: Path) -> list[tuple[str, str, str]]:
    """Parse `path` and return only the data rows (skip #-prefixed metadata)."""
    rows: list[tuple[str, str, str]] = []
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            rows.append((parts[0], parts[1] if len(parts) > 1 else "",
                         parts[2] if len(parts) > 2 else ""))
    return rows


def validate_field(name: str, value: str, line_no: int, path: Path,
                   errs: list[str]) -> None:
    """Reject tabs and raw newlines inside a Front/Back/Tags value."""
    # Tab inside the field would have already split it; we count those in the
    # column-count check. Here we just look for embedded newlines (which would
    # only appear if the file was hand-edited without quoting).
    if "\n" in value or "\r" in value:
        errs.append(f"{path}:{line_no}: {name} contains a raw newline")


def validate_file(path: Path, errs: list[str], warn_missing_fa: bool) -> int:
    """Validate one TSV file. Returns data-row count."""
    rows = data_rows(path)
    count = 0
    with path.open("r", encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            count += 1
            parts = line.split("\t")
            if len(parts) != 3:
                errs.append(
                    f"{path}:{lineno}: expected 3 tab-separated columns, "
                    f"got {len(parts)}"
                )
                continue
            front, back, tags = parts
            validate_field("Front", front, lineno, path, errs)
            validate_field("Back", back, lineno, path, errs)
            validate_field("Tags", tags, lineno, path, errs)
            if not front.strip():
                errs.append(f"{path}:{lineno}: empty Front")
            if not back.strip():
                errs.append(f"{path}:{lineno}: empty Back")
    return count


def validate_area(area: Path) -> int:
    print(f"\n=== {area.relative_to(REPO_ROOT)} ===")
    errs: list[str] = []
    pairs = find_anki_pairs(area)
    if not pairs:
        print("  (no *_anki.txt pairs found)")
        return 0
    failures = 0
    for en, fa in pairs:
        en_count = validate_file(en, errs, True)
        fa_count = validate_file(fa, errs, True)
        same = en_count == fa_count
        status = "OK" if same else "FAIL"
        print(f"  [{status}] {en.relative_to(REPO_ROOT)}: {en_count} cards  |  "
              f"{fa.relative_to(REPO_ROOT)}: {fa_count} cards")
        if not same:
            failures += 1
            errs.append(
                f"{en.name} and {fa.name} card counts differ "
                f"({en_count} vs {fa_count})"
            )
    if errs:
        failures += 1
        for e in errs:
            print(f"  ERR: {e}")
    return failures


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        areas = [REPO_ROOT / a for a in argv[1:]]
    else:
        areas = sorted(
            p for p in REPO_ROOT.iterdir()
            if p.is_dir() and not p.name.startswith(".") and p.name != "tools"
        )
    total_failures = 0
    for area in areas:
        total_failures += validate_area(area)
    print()
    if total_failures:
        print(f"FAILED — {total_failures} area(s) with errors.")
        return 1
    print("OK — all Anki TSVs are valid and synchronized.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))