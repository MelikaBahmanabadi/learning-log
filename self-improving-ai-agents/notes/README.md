# Self-Improving AI Agents — Notes

Structured study notes for Stanford **CS329A: Self-Improving AI Agents** (Autumn 2025).

## Course

| # | Item | Details |
|---|------|---------|
| 1 | Course code | **CS329A** |
| 2 | Title | Self-Improving AI Agents |
| 3 | Term | Autumn 2025 |
| 4 | Instructors | **Aakanksha Chowdhery** (Adjunct Professor, Stanford) and **Azalia Mirhoseini** (Assistant Professor of CS, Stanford; director, Scaling Intelligence Lab) |
| 5 | Website | https://cs329a.stanford.edu/ |
| 6 | Schedule | https://cs329a.stanford.edu/ — see *Schedule* section |
| 7 | Recordings | Stanford Online hosts the course; a YouTube playlist circulates among students. See [`references.md`](references.md) for stable links. |

**Source for the above:** the canonical CS329A course page (https://cs329a.stanford.edu/), verified against the instructors' personal sites:

- Aakanksha Chowdhery — https://www.achowdhery.com/
- Azalia Mirhoseini — http://azaliamirhoseini.com/

Earlier drafts referenced "CS239A" and `cs239a.stanford.edu`; the official course uses only **CS329A** at `cs329a.stanford.edu/`. The earlier URL/code has been removed from the notes.

> **Note on guest lecturers:** the syllabus lists guest speakers including Misha Laskin (Reflection AI). Reflection AI is his affiliation, not Aakanksha Chowdhery's.

## Lectures

| # | Lecture | Primary Topics | Status |
|---|---------|----------------|--------|
| 1 | [Course Overview & Intro to Self-Improving AI Agents](W1-summary.md) | LLM scaling laws, chain of thought, RLHF, inference scaling, reasoning models, agents | 🟢 Done |
| 2 | Scaling & Emergent Abilities (TBD) | — | 🔜 |
| 3 | Reinforcement Learning / RLHF (TBD) | — | 🔜 |
| 4 | Verifiers & Rewards (TBD) | — | 🔜 |
| 5 | Reasoning Models & Test-Time Scaling (TBD) | — | 🔜 |
| 6 | Agentic Workflows & Orchestration (TBD) | — | 🔜 |
| 7 | Multi-Agent Systems (TBD) | — | 🔜 |
| 8 | Multimodal & Robotics Agents (TBD) | — | 🔜 |
| 9 | Self-Improvement Loops (TBD) | — | 🔜 |
| 10 | Course Project & Guest Lectures (TBD) | — | 🔜 |

## Structure

- `W<n>-summary.md` — Weekly/session summary notes (concepts, examples, Q&A)
- `flashcards.md` — Anki-ready Q&A cards (English)
- `flashcards-fa.md` — Anki-ready Q&A cards (فارسی)
- `references.md` — Source map: every external citation used in the notes, with stable links and topics covered
- `progress.md` — What's done, what's next
- `*_anki.txt` — Import-ready Anki text files (TSV format)
- `*_needs_review_anki.txt` — Cards flagged for review

## Conventions

- Claim labels in `W<n>-summary.md`: **Lecture claim** (with lecture identifier), **Primary-source claim** (with citation key from `references.md`), **Interpretation / synthesis**.
- Flashcards are atomic: one concept per card. Compound cards (e.g. "who teaches X and where did they meet") are split into separate cards.
- `_needs_review_anki.txt` files and the `## Needs Review` section in the markdown flashcards are kept as empty placeholders for the convention; cards are added when actually flagged.