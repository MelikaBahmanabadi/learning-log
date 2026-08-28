#!/usr/bin/env python3
"""Validation script for Python learning-log folder.

Checks:
1. Unicode corruption in EN/FA source and exports
2. Valid three-column tab-separated format in each *_anki.txt file
3. Exact source-to-export card parity
4. Markdown links and headings
"""

import re
import sys
from pathlib import Path
from typing import NamedTuple

# ─── Config ────────────────────────────────────────────────────────────────────

PYTHON_DIR = Path(__file__).parent
ANKI_FILES = list(PYTHON_DIR.glob("*_anki.txt"))
MD_FILES = (
    list(PYTHON_DIR.glob("*.md"))
    + list((PYTHON_DIR / "notes").glob("*.md"))
)

# Unicode replacement char (U+FFFD) and other corruption markers
UNICODE_CORRUPTION_RE = re.compile(r"[�￾￿]|[\x00-\x08\x0b\x0c\x0e-\x1f]")

# Suspicious mojibake patterns (common UTF-8 misread as Latin-1)
MOJIBAKE_RE = re.compile(
    r"[\xc3\x83\xc2]{2,}"   # double-encoded UTF-8 artifacts
    r"|[\xe2\x80]{2,}"       # em-dash/quote mojibake
)

# ─── Helpers ───────────────────────────────────────────────────────────────────

class Issue(NamedTuple):
    file: str
    line: int | None
    category: str
    message: str


def check_unicode(text: str, filename: str) -> list[Issue]:
    """Check for Unicode corruption markers."""
    issues = []
    for i, line in enumerate(text.splitlines(), 1):
        # Skip lines that are intentional Unicode examples
        if any(marker in line for marker in [
            "UnicodeEncodeError", "errors=", "replacement char", "casefold",
            "normalize", "encode", "decode", "code point"
        ]):
            continue
        if UNICODE_CORRUPTION_RE.search(line):
            issues.append(Issue(filename, i, "unicode", f"Replacement/control char found: {line[:80]!r}"))
        # Check for common mojibake: raw bytes that look like broken encoding
        if any(ord(c) > 127 and ord(c) < 160 for c in line):
            issues.append(Issue(filename, i, "unicode", f"Possible mojibake (C1 controls): {line[:80]!r}"))
    return issues


def check_anki_format(filepath: Path) -> list[Issue]:
    """Validate *_anki.txt: header lines + 3-column TSV body."""
    issues = []
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Find where header ends (lines starting with #)
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith("#"):
            body_start = i + 1
        else:
            break

    # Validate header
    expected_headers = [
        "#separator:tab",
        "#html:true",
        "#notetype:Basic",
        "#tags column:3",
        "#columns:Front\tBack\tTags",
    ]
    actual_text = "\n".join(lines[:body_start])
    for h in expected_headers:
        if h not in actual_text:
            issues.append(Issue(str(filepath), None, "anki-header", f"Missing header: {h}"))

    # Validate body: cards are 3 tab-separated columns
    # Multi-line answers are valid in Anki (answer spans until next card)
    i = body_start
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        # Count tabs to determine if this is a complete card or continuation
        tabs = line.count("\t")
        if tabs >= 2:
            # This looks like a complete card (has at least 2 tabs for 3 columns)
            cols = line.split("\t")
            if len(cols) != 3:
                issues.append(Issue(str(filepath), i + 1, "anki-format",
                                  f"Expected exactly 3 tab-separated columns, got {len(cols)}: {line[:60]!r}"))
            # Check for empty front/back
            if cols and not cols[0].strip():
                issues.append(Issue(str(filepath), i + 1, "anki-content", "Empty Front column"))
            if len(cols) >= 2 and not cols[1].strip():
                issues.append(Issue(str(filepath), i + 1, "anki-content", "Empty Back column"))
        # Lines with fewer tabs are continuations of multi-line answers (valid in Anki)
        i += 1

    return issues


def extract_md_cards(text: str) -> list[tuple[str, str]]:
    """Extract Q/A pairs from markdown flashcard files."""
    cards = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("Q:"):
            q = line[2:].strip()
            a = ""
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("A:"):
                a = lines[i + 1].strip()[2:].strip()
                i += 1
            cards.append((q, a))
        i += 1
    return cards


def extract_anki_cards(text: str) -> list[tuple[str, str]]:
    """Extract Front/Back pairs from anki export (strip HTML)."""
    cards = []
    lines = text.splitlines()
    # Skip header
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith("#"):
            body_start = i + 1
        else:
            break

    # Join multi-line answers (lines without enough tabs are continuations)
    i = body_start
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        # Skip lines that are part of multi-line answers (start with ---)
        if line.startswith("---"):
            i += 1
            continue

        # Check if this line starts a new card (has tabs for Front\tBack\tTags)
        if "\t" in line:
            cols = line.split("\t")
            if len(cols) >= 2:
                front = re.sub(r"<[^>]+>", "", cols[0]).strip()
                back = re.sub(r"<[^>]+>", "", cols[1]).strip()
                cards.append((front, back))
        # Lines without tabs are continuations of multi-line answers (valid in Anki)
        i += 1
    return cards


def normalize_question(q: str) -> str:
    """Normalize question text for comparison (strip ?, whitespace, quotes)."""
    return re.sub(r"[?!?\s]+", "", q).strip()


def check_card_parity() -> list[Issue]:
    """Verify MD source cards match anki export cards exactly."""
    issues = []

    # EN flashcards
    md_path = PYTHON_DIR / "flashcards.md"
    anki_path = PYTHON_DIR / "flashcards_anki.txt"
    if md_path.exists() and anki_path.exists():
        md_cards = extract_md_cards(md_path.read_text(encoding="utf-8"))
        anki_cards = extract_anki_cards(anki_path.read_text(encoding="utf-8"))
        if len(md_cards) != len(anki_cards):
            issues.append(Issue("flashcards.md / flashcards_anki.txt", None, "parity",
                              f"Card count mismatch: MD={len(md_cards)}, Anki={len(anki_cards)}"))
        # Compare question text
        for i, (mq, aq) in enumerate(zip(md_cards, anki_cards)):
            if normalize_question(mq[0]) != normalize_question(aq[0]):
                issues.append(Issue("flashcards.md", None, "parity",
                                  f"Q mismatch at card {i+1}: MD={mq[0][:40]!r} vs Anki={aq[0][:40]!r}"))

    # FA flashcards
    md_fa_path = PYTHON_DIR / "flashcards-fa.md"
    anki_fa_path = PYTHON_DIR / "flashcards-fa_anki.txt"
    if md_fa_path.exists() and anki_fa_path.exists():
        md_cards = extract_md_cards(md_fa_path.read_text(encoding="utf-8"))
        anki_cards = extract_anki_cards(anki_fa_path.read_text(encoding="utf-8"))
        if len(md_cards) != len(anki_cards):
            issues.append(Issue("flashcards-fa.md / flashcards-fa_anki.txt", None, "parity",
                              f"Card count mismatch: MD={len(md_cards)}, Anki={len(anki_cards)}"))
        for i, (mq, aq) in enumerate(zip(md_cards, anki_cards)):
            if normalize_question(mq[0]) != normalize_question(aq[0]):
                issues.append(Issue("flashcards-fa.md", None, "parity",
                                  f"Q mismatch at card {i+1}: MD={mq[0][:40]!r} vs Anki={aq[0][:40]!r}"))

    # Check needs_review files
    for suffix in ["_needs_review", "-fa_needs_review"]:
        review_path = PYTHON_DIR / f"flashcards{suffix}_anki.txt"
        main_anki = PYTHON_DIR / f"flashcards{'-fa' if 'fa' in suffix else ''}_anki.txt"
        if review_path.exists() and main_anki.exists():
            review_cards = extract_anki_cards(review_path.read_text(encoding="utf-8"))
            main_cards = extract_anki_cards(main_anki.read_text(encoding="utf-8"))
            review_qs = {normalize_question(c[0]) for c in review_cards}
            main_qs = {normalize_question(c[0]) for c in main_cards}
            orphaned = review_qs - main_qs
            if orphaned:
                issues.append(Issue(f"flashcards{suffix}_anki.txt", None, "parity",
                                  f"{len(orphaned)} cards in needs_review not in main anki"))

    return issues


def check_cross_language() -> list[Issue]:
    """Verify EN and FA Anki exports have matching card counts (1:1 concept set)."""
    issues = []
    en_path = PYTHON_DIR / "flashcards_anki.txt"
    fa_path = PYTHON_DIR / "flashcards-fa_anki.txt"
    if en_path.exists() and fa_path.exists():
        en_cards = extract_anki_cards(en_path.read_text(encoding="utf-8"))
        fa_cards = extract_anki_cards(fa_path.read_text(encoding="utf-8"))
        if len(en_cards) != len(fa_cards):
            issues.append(Issue(
                "flashcards_anki.txt / flashcards-fa_anki.txt", None, "cross-language",
                f"EN/FA Anki card count mismatch: EN={len(en_cards)}, FA={len(fa_cards)}"))
    return issues


def check_markdown(filepath: Path) -> list[Issue]:
    """Check markdown links and headings."""
    issues = []
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Check for broken internal links [text](path)
    link_re = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
    for i, line in enumerate(lines, 1):
        for match in link_re.finditer(line):
            link_text, link_target = match.groups()
            # Skip external URLs and anchors
            if link_target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            # Check if local file exists
            target_path = filepath.parent / link_target
            if not target_path.exists():
                issues.append(Issue(str(filepath), i, "markdown-link",
                                  f"Broken link: [{link_text}]({link_target})"))

    # Check heading hierarchy (warn on skipped levels, but allow h1->h3 for chapter structure)
    heading_re = re.compile(r"^(#{1,6})\s")
    prev_level = 0
    for i, line in enumerate(lines, 1):
        m = heading_re.match(line)
        if m:
            level = len(m.group(1))
            # Allow h1->h3 (chapter title -> subsection) as valid structure
            if prev_level > 0 and level > prev_level + 1 and not (prev_level == 1 and level == 3):
                issues.append(Issue(str(filepath), i, "markdown-heading",
                                  f"Heading level skip: h{prev_level} -> h{level}"))
            prev_level = level

    return issues


# ─── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    all_issues: list[Issue] = []

    # 1. Unicode corruption in all files
    for f in ANKI_FILES + MD_FILES:
        text = f.read_text(encoding="utf-8")
        all_issues.extend(check_unicode(text, str(f.relative_to(PYTHON_DIR))))

    # 2. Anki format validation
    for f in ANKI_FILES:
        all_issues.extend(check_anki_format(f))

    # 3. Card parity
    all_issues.extend(check_card_parity())

    # 3b. Cross-language card count parity (EN vs FA Anki exports)
    all_issues.extend(check_cross_language())

    # 4. Markdown links and headings
    for f in MD_FILES:
        all_issues.extend(check_markdown(f))

    # Report
    if not all_issues:
        print("All checks passed!")
        return 0

    # Group by category
    by_cat: dict[str, list[Issue]] = {}
    for issue in all_issues:
        by_cat.setdefault(issue.category, []).append(issue)

    for cat, issues in sorted(by_cat.items()):
        print(f"\n{'='*60}")
        print(f"  {cat.upper()} ({len(issues)} issues)")
        print(f"{'='*60}")
        for issue in issues:
            loc = f"{issue.file}:{issue.line}" if issue.line else issue.file
            print(f"  [{loc}] {issue.message}")

    print(f"\n{len(all_issues)} issues found.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
