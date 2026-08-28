# Week 1 — Course Overview & Intro to Self-Improving AI Agents

**Lecture:** CS329A Lecture 1 — *Course Overview* (Mon Sep 22, 2025, Autumn 2025) `[cs329a-syllabus]`
**Instructors:** Aakanksha Chowdhery & Azalia Mirhoseini
**Canonical URL:** https://cs329a.stanford.edu/

> **Claim labels used below:**
> - **Lecture claim** — paraphrased from Lecture 1; lecture identifier noted. Exact timestamps not independently verified against the recording in this revision.
> - **Primary-source claim** — backed by a published paper / official report / official site (citation key in brackets, full list in [`references.md`](references.md)).
> - **Interpretation / synthesis** — my summary combining or extending the lecture; clearly marked.
>
> All quantitative, historical, model-specific, and comparative claims are flagged in-line.

---

## 1. Course & Instructors `[cs329a-staff]`, `[achowdhery-site]`, `[azalia-site]`

- **Course code:** CS329A — *Self-Improving AI Agents*. The "CS239A" identifier does not appear on the official site; treat the notes' older "CS239A" label as outdated.
- **Term:** Autumn 2025, Stanford University.
- **Aakanksha Chowdhery** — Adjunct Professor (Stanford). Lead researcher of the 540B PaLM model and core contributor to Gemini pre-training, scaling, and fine-tuning at Google `[achowdhery-site]`.
- **Azalia Mirhoseini** — Assistant Professor of Computer Science (Stanford), director of the Scaling Intelligence Lab; co-founder of Ricursive Intelligence. Prior work at Google Brain, Anthropic (Claude), and Google DeepMind (Gemini); pioneer of AlphaChip and Large Language Monkeys `[azalia-site]`.
- **Misha Laskin (Reflection AI)** appears on the schedule as a guest lecturer on Nov 21, not as an instructor. `[cs329a-syllabus]`
- **Theme (Lecture claim):** how LLMs evolve from chatbots into agents that plan, act, receive feedback, and improve themselves.

---

## 2. LLM Scaling Laws `[kaplan2020scaling]`, `[hoffmann2022chinchilla]`, `[cs329a-syllabus]`

**Lecture claim:** Scaling up parameters produces better models; the three axes below each lower test loss.

| Axis | Effect | Source of claim |
|------|--------|-----------------|
| Compute | More compute → test loss ↓ | `[kaplan2020scaling]` |
| Dataset size | More data → test loss ↓ | `[kaplan2020scaling]` |
| Parameter count | More params / layers → test loss ↓ | `[kaplan2020scaling]` |

### 2.1 Parameter counts (2018 → 2024)

| Model | Parameters | Source |
|-------|-----------|--------|
| BERT (2018) | ~340M | `[devlin2019bert]` |
| GPT-2 (2019) | ~1.5B | `[radford2019gpt2]` |
| GPT-3 (2020) | ~175B | `[brown2020gpt3]` |
| PaLM (2022) | ~540B | `[chowdhery2022palm]` |
| GPT-4 (2023) | **Not officially disclosed** — "trillions" is a third-party estimate (e.g. SemiAnalysis, 2023) and should not be presented as a published figure. | — |

**Lecture claim:** Model sizes grew roughly exponentially. (Interpretation / synthesis: "exponential" describes a trend across widely separated checkpoints; it is not a fitted curve over these few data points.)

### 2.2 Scaling saturation (Lecture claim — qualified)

**Lecture claim:** Scaling held until ~2023–2024, when it began to hit a "saturation point."

> **Caveat:** "Saturation" depends on the chosen metric — test loss kept improving well past 2023, while benchmark-accuracy gains and per-token economics flattened. No single source defines a universal saturation year. Treat this as the lecturer's framing rather than an established fact.

### 2.3 Why bigger models matter (Lecture claim)

1. Better performance on natural-language, reasoning, and other benchmarks.
2. **Few-shot learning** — few examples are enough to adapt without per-domain fine-tuning `[brown2020gpt3]`.
3. **Emergent behavior** — capabilities like reasoning only appear at larger sizes. (Whether emergence is a real discontinuity vs a metric artifact is debated; see e.g. Schaeffer et al., "Are Emergent Abilities of Large Language Models a Mirage?", NeurIPS 2023.)

---

## 3. Zero-shot vs. Few-shot Learning `[brown2020gpt3]`

| | Zero-shot | Few-shot |
|---|-----------|----------|
| Given | Task description only | Task description + a few input→output examples |
| Example | "Translate English to French: cheese →" | description + (English→French) pairs, then "cheese →" |

**Lecture claim:** Few-shot makes prototyping very easy — no task-specific training needed. Interpretation / synthesis: this is the lecturer's framing; the underlying paper `[brown2020gpt3]` describes the same behavior more cautiously.

---

## 4. Chain of Thought (CoT) `[wei2022cot]`, `[cobbe2021gsm8k]`, `[chowdhery2022palm]`

In a normal prompt you give an example question and answer; with CoT you also show the **step-by-step reasoning** to reach the answer.

**Example (from lecture):**
> Roger has five tennis balls. He buys two more cans of tennis balls. Each can has three. How many total?
>
> **Reasoning:** Roger started with 5 balls. Two cans of 3 = 6. 5 + 6 = 11.

### 4.1 Key facts

- CoT was **not designed in** — it was an **emergent behavior** discovered in large models.
  - `[cobbe2021gsm8k]` (GSM8K paper) is cited by the lecture as showing "first signs of life."
  - `[chowdhery2022palm]` (PaLM 540B) is cited as confirming the result on a larger model.
  - The phrase "first signs of life" and "a big deal" is **Interpretation / synthesis** based on lecture emphasis, not literal phrasing from those papers.

- **Scale matters** for CoT in the experiments cited by the lecture.
  - `[wei2022cot]` reports the CoT gain for large LaMDA / PaLM models (540B) and notes that smaller-scale models in the same experiments showed little or no benefit on GSM8K.
  - **Bound:** "small models (~7–8B) get no benefit" applies to the specific LaMDA/GPT variants and the specific benchmarks in `[wei2022cot]` and follow-ups. It is not a universal law. Different model families, training recipes, and tasks can yield different thresholds.
  - The exact ~7–8B threshold quoted in the lecture is a paraphrase; the original paper reports results across multiple model sizes (e.g. LaMDA 422M / 2B / 8B / 67B, PaLM 8B / 62B / 540B) without a clean single cutoff.

- CoT is foundational for today's **reasoning / thinking models** (o1, Gemini, DeepSeek) — Lecture claim. (Interpretation / synthesis: the lecturer is drawing a connection; see §7 for scoped claims about each model family.)

---

## 5. Training Pipeline: Pre-training → ChatGPT `[ouyang2022instructgpt]`, `[schulman2023chatgpt]`

> **Caveat:** "ChatGPT = pre-training + instruction tuning + RLHF" is the **canonical 3-step pipeline introduced in the InstructGPT paper `[ouyang2022instructgpt]`** and reused as a pedagogical diagram in the lecture. It is not a literal training spec for any specific ChatGPT release, which has additional steps (safety tuning, red-teaming, tool integrations, model merging, etc.).

### 5.1 Pre-training (Lecture claim; standard practice)
Predict the **next token** over a huge text corpus. The model gains statistical knowledge but **no built-in sense of right/wrong or how to follow instructions.**

### 5.2 Fine-tuning / alignment (Lecture claim)
Fine-tune the base model on higher-quality, curated data (books, curated essays) to steer it toward human goals/preferences/values. The lecturer noted that alignment is **still an unsolved problem.**

### 5.3 Instruction tuning `[ouyang2022instructgpt]`
Train on `(instruction, question → answer)` pairs so the model learns to follow instructions. Data mixes **human-generated and synthetic** examples.

### 5.4 RLHF `[ouyang2022instructgpt]`
Instead of supervised labels, build a **reward model** from human preference ratings (humans rate which of two answers is better), then use it to guide the LLM's parameters toward high-scoring generations.

Reward types can be weighted: **correctness, helpfulness, specificity, harmlessness** (Lecture claim; also discussed in `[ouyang2022instructgpt]`).

```
pre-training → fine-tuning → instruction tuning → RLHF
```

### 5.5 Launch metric (Lecture claim, qualified)
ChatGPT launched in Nov 2022 and was widely reported to have reached ~1M users within 5 days. Treat as a contemporaneous press claim; no Stanford/OAI official number exists.

---

## 6. Inference Scaling & "Large Language Monkeys" `[brown2024llm-monkeys]`, `[snell2024testtime]`, `[wang2023self-consistency]`

### 6.1 The idea (Lecture claim)
Inspired by the **infinite monkey theorem**: let the LLM be the "monkey."
- Ask the model to solve a problem **many times** (parallel sampling).
- Use a **verifier** (e.g. unit tests for code, known answers for math) to pick a correct response.
- Output the correct one.

Models are **non-deterministic**; **temperature** controls response diversity (Lecture claim: temperatures much above ~1 produce gibberish — this is a paraphrase of standard sampling behavior).

### 6.2 Results — `[brown2024llm-monkeys]` (Lecture claim)

- Increasing samples per problem from 1 → 10,000 raises **coverage** (fraction of problems solved by ≥1 of the k samples). The coverage-vs-samples curve is **log-linear** on SWE-bench Lite and other coding/math benchmarks.
- The paper reports coverage on **SWE-bench Lite** rising from **15.9% with 1 sample to 56% with 250 samples** for the best-sampled model.
- **Bound on the "7B with many samples beat GPT-4o with one sample" claim:**
  - This refers to the SWE-bench Lite / HumanEval experiments in `[brown2024llm-monkeys]`, comparing a smaller model with a high sampling budget to a larger model with k=1.
  - The exact model identities, sampling budgets, verifiers, and benchmark metrics used must be quoted from the paper, not paraphrased as a universal result.

### 6.3 Inference (test-time) scaling `[snell2024testtime]`

Keep the model **fixed**; spend more compute **at inference time**. Shows a **log-linear** scaling law on coverage, not just on training loss.

### 6.4 pass@1 vs. coverage — terminology `[brown2024llm-monkeys]`, `[wang2023self-consistency]`

> **Important:** The lecture uses "coverage" and "pass@k" as synonyms. They are **related but not identical** in the literature:
>
> - **pass@k** — the standard Codex-style metric (`[chen2021codex]`): probability that at least one of k samples passes all unit tests, **with duplicates removed** and an unbiased estimator.
> - **coverage** (as used in `[brown2024llm-monkeys]`) — fraction of benchmark problems for which at least one of k samples is correct.
>
> In `[brown2024llm-monkeys]`, the "coverage" curve is the metric most directly tracked, and it matches the practical meaning of pass@k closely but uses the paper's own estimator. Use the paper's definition when quoting a number.

**Lecture claim (paraphrase):** Reasoning training raises pass@1; repeated sampling raises coverage. This is the lecturer's framing; in the public papers, RL-based reasoning training improves pass@1 *and* (often) coverage, while repeated sampling primarily improves coverage.

---

## 7. Reasoning Models (o1, DeepSeek, Gemini) `[openai-o1-system]`, `[guo2025deepseekr1]`, `[gemini-team-2024]`

### 7.1 The "self-improvement loop" — scoped to the public reports

- **`[guo2025deepseekr1]`** (DeepSeek-R1 technical report) describes a public RL pipeline (GRPO + verifiable rewards) that uses model-generated reasoning traces as training data. This supports the lecture's claim **for DeepSeek-R1 specifically.**
- **`[openai-o1-system]`** (OpenAI's o1 system page / o1 system card) describes o1 as trained with large-scale reinforcement learning and chain-of-thought reasoning, but does **not** disclose the proprietary training data recipe in detail. Treat the "generate-synthetic-data-at-test-time-and-fine-tune" loop as a **high-level course hypothesis** for o1, not as a confirmed fact.
- **`[gemini-team-2024]`** (Gemini technical report) similarly does not disclose a closed-loop self-improvement pipeline. The "Gemini does this" framing should be removed or marked as a high-level hypothesis.

### 7.2 How reasoning models solve hard problems (Lecture claim)

| Step | Meaning |
|------|---------|
| Problem analysis | Understand inputs/outputs first |
| Task decomposition | Break into smaller addressable tasks |
| Self-evaluation | Try, get feedback (run tests, use calculator, judge) |
| Self-correction | Notice errors, fix them ("wait, something's wrong") |
| Alternative proposals | Backtrack and try a different approach |

### 7.3 o1 vs. GPT-4o — benchmark-scoped (Lecture claim, qualified)

> **Bound:** "o1 outperforms GPT-4o on math, data analysis, programming" — scoped to the benchmarks reported on `[openai-o1-system]` (AIME, MATH, GPQA, Codeforces). Not a universal claim; OpenAI also reports GPT-4o competitive or superior on writing/editing tasks.

### 7.4 Open questions (Lecture claim / Interpretation)

- CoT was discovered (emergent), not baked in — but reasoning models are now **explicitly trained** to reason.
- Models **prefer their own traces** over another model's traces (relevant to the SWiRL / multi-step reasoning literature `[azalia-site]`).
- It's still an open question whether RL or diverse pre-training data drives the jump — no consensus yet.

---

## 8. From LLM to Agents

> **Revise the original framing:** chatbots and reasoning models are not strictly single-turn systems — modern chat products are multi-turn. The defining property of an **agent** is the autonomy/control loop, not turn count.

### 8.1 Agent definition (Lecture claim, refined)

An **agent** combines:
1. A **goal** to satisfy.
2. A **plan** that can be revised.
3. Interaction with an **environment / tools** (APIs, code execution, search, the file system).
4. A **feedback signal** (verifier, judge, environment reward).
5. A **self-correction loop** until the goal is reached (or termination criteria met).
6. **State / memory** to track task progress across steps.

### 8.2 Why coding agents became reliable recently (Lecture claim, qualified)

- Not a fundamentally new architecture — mostly **more powerful models + better RL with verifiable rewards.**
- A **self-improvement loop** kicks in: the model generates its own unit tests, which become a reliable verifier.
- "Recently" should be dated — the rise of reliable coding agents (Claude Code, Codex, Cursor, etc.) is in the **2024–2025** window; this is a paraphrase of the lecture's framing and should be checked against product launch dates before being repeated.

### 8.3 "This year agents started doing real end-to-end workflows" — Lecture claim, qualified

Treat as a paraphrase of the lecturer's framing rather than a universal statement. Different agentic products launched on different timelines; "end-to-end" is itself a continuum (a chat model with web search vs. a multi-hour autonomous task agent).

---

## 9. Agentic Workflow Components & Patterns (Lecture claim)

**Building blocks:** LLM calls, verifiers, critics/judges (LLM-as-judge), tool calls (search, weather, terminal), orchestration.

**Orchestration patterns:**

| Pattern | Description |
|---------|-------------|
| Prompt chaining | Decompose the task into chained subtasks |
| Routing | Complex task → complex LLM call path; simple → simple path |
| Parallelization | Multiple LLM calls on different inputs, then aggregate (Deep Research) |
| Orchestrator | A central "manager" LLM plans, then makes sub-calls (Claude Code) |
| Evaluator / judge | LLM-as-judge gives feedback instead of ground truth |
| Verifier | Objective check — unit tests for code, known answers for math |

**The bottleneck: verification.** In verifiable domains (math, code) you can give feedback; in open-ended domains (creative writing) feedback is scarce and human feedback becomes the bottleneck — the **generator-verifier gap** (Lecture claim).

---

## 10. Agent Applications (Lecture claim)

| Domain | Use cases |
|--------|-----------|
| Repetitive dev tasks | Code migration, version upgrades, restructure, data engineering, warehouse migration, unit tests |
| Customer support | Live transcription, knowledge assist, smart reply, call summary |
| Deep research | Identify references → outline → summarize → synthesize full report |
| AI scientist | Idea generation (brainstorming), experiment iteration, paper writeup |

---

## 11. Course Logistics `[cs329a-syllabus]`

> **Correction:** The original notes reported "3 homeworks = 50%, project = 50%." The official CS329A grading breakdown is more granular and slightly different. Use the values below.

| Component | Weight |
|-----------|--------|
| Homework 1 | 15% |
| Homework 2 | 15% |
| Homework 3 | 20% |
| Project Proposal | 2.5% |
| Midterm presentation + Report | 10% |
| Final project | 35% |
| Poster | 2.5% |

- **Lecture time:** Mon/Fri 4:30 PM – 5:50 PM PT, Skilling Auditorium, Autumn 2025.
- **Project:** teams of 2–4; API credits provided; "more than glue coding."
  - *Good:* new benchmark/eval set, reliability study, hill-climb a benchmark, question/improve a paper's decision.
  - *Bad:* survey paper, or a plain app with no hypothesis.
- **Milestones (Autumn 2025):** Project Proposal due Oct 10 → Midterm presentations Oct 24/27/31 → Final report due Dec 10 → Poster session Dec 12.
- **Tools:** EdStem (questions), Gradescope (submissions).
- **Policies:** 4 free late days for the quarter (max 2 per assignment), no audits allowed.

---

## 12. Key Takeaways (Lecture claim)

1. Models improved via **scaling** (compute, data, params) — but scaling's gains depend on the chosen metric and may be flattening.
2. **CoT reasoning was emergent**, not designed; reasoning models are now trained for it.
3. ChatGPT's training is **commonly summarized** as pre-training + instruction tuning + RLHF; the actual production pipeline has more steps.
4. **Inference scaling** (repeated sampling + verifiers) unlocks capability without touching parameters; log-linear scaling on coverage.
5. **Self-improvement** = test-time-generated reasoning traces used as RL training data — directly documented for DeepSeek-R1; not publicly documented for o1 / Gemini.
6. Agents = goal + plan + act + feedback + self-correct, orchestrated with verifiers / judges / tools; defined by autonomy and the control loop, not by being "single-turn."
7. **Verification is the key bottleneck** (generator-verifier gap).

---

## 13. What still needs verification

- Exact timestamps within the Lecture 1 recording for each claim above.
- The lecturer's specific phrasing of "scaling saturation" (year, metric).
- The "Aakanksha (Reflection AI)" attribution in earlier draft notes — Aakanksha's site lists Stanford + Google; "Reflection AI" in the Autumn 2025 syllabus refers to guest lecturer Misha Laskin.
- "1M users in 5 days" ChatGPT launch metric — re-source from a contemporaneous press report if kept in study notes.