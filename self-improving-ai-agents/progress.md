# Self-Improving AI Agents — Learning Progress

**Course:** CS329A — Self-Improving AI Agents
**Platform:** Stanford (Autumn 2025) — https://cs329a.stanford.edu/
**Instructors:** Aakanksha Chowdhery & Azalia Mirhoseini
**Domain:** Self-improving AI agents, LLMs, RL, reasoning models, agentic systems

---

## Status
- W1 / Course Overview & Intro to Self-Improving AI Agents — ✅ DONE
  - Lecture 1 (Mon Sep 22, 2025): scaling laws, CoT, RLHF, inference scaling, reasoning models, agents — DONE
  - Source map + claim labeling revision — DONE

**Last covered:** Lecture 1 — Course Overview (Stanford CS329A, Mon Sep 22, 2025).
**Next action:** Watch Lecture 2 (Fri Sep 26, 2025 — Test-time Compute Scaling), confirm W1 claim labels against the recording, and produce `notes/W2-summary.md`.
**Needs Review:** 0 cards

---

## Lectures

| # | Lecture | Status | Primary Topics |
| -- | ------- | ------ | -------------- |
| 1 | Course Overview & Intro | 🟢 Done | Scaling laws, CoT, RLHF, inference scaling, reasoning models, agents |
| 2 | Test-time Compute Scaling | 🔜 | Large Language Monkeys, test-time scaling laws, verifiers |
| 3 | Robust Verification | 🔜 | — |
| 4 | Learning from feedback with tools/code | 🔜 | ReAct, RLEF, Constitutional AI |
| 5 | Multi-step Reasoning / Planning | 🔜 | SWiRL, LATS, ADaPT |
| 6 | Train Time Scaling / Scaling RL | 🔜 | STaR, DeepSeekMath, DAPO |
| 7 | Open-Ended Evolution of Self-Improving Agents | 🔜 | — |
| 8 | Self improvement with Search & Deep Research Agents | 🔜 | AlphaCode, Search-o1 |
| 9 | Guest: Melvin Johnson (Google DeepMind) | 🔜 | — |
| 10–12 | Midterm presentations | 🔜 | — |
| 13 | Agentic Frameworks for Software Engineering | 🔜 | CodeMonkeys, KernelBench |
| 14 | Augmenting Agents with Memory (Guest: Junchen Jiang) | 🔜 | — |
| 15 | Guest: Denny Zhou — LLM Reasoning | 🔜 | — |
| 16 | Guest: Thang Luong — AlphaProof, AlphaGeometry, Gemini IMO Gold | 🔜 | — |
| 17 | Agentic Evaluations & Long-Horizon Tasks | 🔜 | — |
| 18 | Guest: Misha Laskin (Reflection AI) — Building Agentic Systems | 🔜 | — |
| 19 | Guest: Danny Driess (Physical Intelligence) — Multimodal AI Agents in Robotics | 🔜 | — |
| 20 | Future Research Areas | 🔜 | — |

---

## Artifacts

| File | Description |
|---|---|
| `notes/W1-summary.md` | Full W1 notes with claim labels and source citations |
| `notes/references.md` | Source map — every external citation, with stable links and topics |
| `flashcards.md` | English Anki cards (39 cards, W1) |
| `flashcards-fa.md` | Persian Anki cards (39 cards, W1) |
| `flashcards_anki.txt` / `flashcards-fa_anki.txt` | Anki import TSVs |
| `flashcards_needs_review_anki.txt` / `flashcards-fa_needs_review_anki.txt` | Empty placeholder for flagged cards |
| `progress.md` | This file |

---

## Validation

Run from the repo root:

```bash
python3 tools/validate_anki.py self-improving-ai-agents
```

This verifies:
1. `flashcards_anki.txt` and `flashcards-fa_anki.txt` have the same number of data rows.
2. Every data row has exactly 3 tab-separated columns (Front, Back, Tags).
3. No raw newline or embedded tab in any Front/Back/Tags value.