# Week 1 — Course Overview & Intro to Self-Improving AI Agents

**Sources:** Stanford CS329A Lecture 1 — Course Overview (Akanksha & Azalia Mirhoseini)

---

## 1. Course & Instructors

- **Akanksha** — adjunct professor at Stanford; research at Reflection AI; long background in LLMs.
- **Azalia Mirhoseini** — assistant professor, Stanford CS. Met Akanksha at Google Brain, then Google DeepMind; also worked on Claude (Anthropic) and Gemini.
- Second time the course is offered; website is **cs239a.stanford.edu** (course code also appears as **CS329A**).
- Theme: how LLMs evolve from single-turn chatbots into **agents** that plan, act, receive feedback, and **improve themselves**.

---

## 2. LLM Scaling Laws

Scaling up parameters → better models. BERT and T5 were good, but more parameters made models *much* better.

**Three axes of scaling** (each lowers test loss):

| Axis | Effect |
|------|--------|
| Compute | More compute → test loss ↓ |
| Dataset size | More data → test loss ↓ |
| Parameter count | More params / layers → test loss ↓ |

**Model size growth (2018 → 2024):**

| Model | Parameters |
|-------|-----------|
| BERT | 340M |
| GPT-2 | 1.5B |
| GPT-3 | 175B |
| PaLM | 540B |
| GPT-4 | trillions (estimated) |

Exponential growth in model size ("large" language models keep getting larger). Scaling held until ~2023–2024, when it began to hit a **saturation point**.

### Why bigger models matter
1. Better performance on natural-language, reasoning, and other benchmarks.
2. **Few-shot learning** — few examples are enough to adapt (no per-domain fine-tuning).
3. **Emergent behavior** — capabilities like reasoning only appear at larger sizes.

---

## 3. Zero-shot vs. Few-shot Learning

| | Zero-shot | Few-shot |
|---|-----------|----------|
| Given | Task description only | Task description + a few input→output examples |
| Example | "Translate English to French: cheese →" | description + a few (English→French) pairs, then "cheese →" |

Few-shot makes prototyping extremely easy: the model follows the example template without task-specific training.

---

## 4. Chain of Thought (CoT)

In a normal prompt you give an example question and answer. With CoT you *also* show the **step-by-step reasoning** to reach the answer.

**Example (from lecture):**
> Roger has five tennis balls. He buys two more cans of tennis balls. Each can has three. How many total?
>
> **Reasoning:** Roger started with 5 balls. Two cans of 3 = 6. 5 + 6 = 11.

### Key facts
- CoT was **not designed in** — it was an **emergent behavior** discovered in large models (the GSM8K paper showed first signs of life; PaLM confirmed it was a big deal, e.g. it could explain jokes).
- **Scale matters:** CoT helps large models (PaLM 540B, GPT-3 175B) but does nothing for small ones (~7–8B LaMDA/GPT).
- CoT is foundational for today's **reasoning / thinking models** (o1, Gemini, DeepSeek).

---

## 5. Training Pipeline: Pre-training → ChatGPT

ChatGPT launched Nov 2022, reached **1M users in 5 days**. Two innovations on top of scaling made it leapfrog GPT-3: **instruction tuning** and **RLHF**.

### 5.1 Pre-training
Predict the **next token** over all sorts of text (internet, books). Model gains statistical knowledge but **no sense of right/wrong or how to follow instructions**.

### 5.2 Fine-tuning (alignment)
Fine-tune the base model on higher-quality, curated data (books, creative essays) to steer it toward human goals/preferences/values. Alignment is *still an unsolved problem*.

### 5.3 Instruction tuning
Show the model `(instruction, question → answer)` pairs so it learns to follow instructions and answer questions. Data mixes **human-generated** and **synthetic** examples.

### 5.4 RLHF (Reinforcement Learning from Human Feedback)
Instead of supervised labels, build a **reward model** from human preference ratings (humans rate which of two answers is better). Then use the reward model to guide the LLM's parameters toward generations the reward model scores highly.

Reward types can be weighted: **correctness, helpfulness, specificity, harmlessness**.

```
pre-training → fine-tuning (high-quality data) → instruction tuning → RLHF
```

---

## 6. Inference Scaling & "Large Language Monkeys"

### 6.1 The idea
Inspired by the **infinite monkey theorem** (a monkey typing forever eventually produces Shakespeare). Let the LLM be the "monkey":
- Ask the model to solve a problem **many times** (parallel sampling).
- Use a **verifier** (e.g. unit tests for code, known answers for math) to pick a correct response.
- Output the correct one.

Models are **non-deterministic**; **temperature** controls response diversity (too high, ~>1.2, gives gibberish).

### 6.2 Results
Increasing samples per problem from 1 → 10,000 raised **coverage** (fraction solved by ≥1 sample). A 7B model with many samples beat GPT-4o with one sample — "models already know more than you get by asking once."

### 6.3 Inference (test-time) scaling
Keep the model **fixed**; spend more compute **at inference time**. Shows a **log-linear** scaling law: accuracy/coverage grows with number of samples / test-time compute — previously only shown for training, now for test time too.

**Key distinction:** *pass@1* (accuracy of a single generation) vs *coverage / pass@k* (solved by ≥1 of k samples). Reasoning training raises pass@1; repeated sampling raises coverage.

---

## 7. Reasoning Models (o1, DeepSeek, Gemini)

### 7.1 The self-improvement loop
DeepSeek (Dec 2024) and o1/Gemini combine **fine-tuning + test-time scaling**: generate lots of synthetic data at test time (e.g. math solutions with known golden answers, code solutions), then feed it back to **fine-tune** the model. This is the **self-improving** piece of the course.

### 7.2 How reasoning models solve hard problems
| Step | Meaning |
|------|---------|
| Problem analysis | Understand inputs/outputs first |
| Task decomposition | Break into smaller addressable tasks |
| Self-evaluation | Try, get feedback (run tests, use calculator, judge) |
| Self-correction | Notice errors, fix them ("wait, something's wrong") |
| Alternative proposals | Backtrack and try a different approach |

### 7.3 Reasoning vs. non-reasoning
o1 outperforms GPT-4o on math, data analysis, programming — but not necessarily on personal writing/editing.

### 7.4 Notes on provenance
- CoT was discovered (emergent), not baked in — but reasoning models are now **explicitly trained** to reason.
- Models **prefer their own traces** over another model's traces (relevant to the Swirl / multi-step reasoning papers).
- It's still an open question whether RL or diverse pre-training data drives the jump — no consensus yet.

---

## 8. From LLM to Agents

Chatbots/reasoning models are still essentially **single-turn**. An **agent**:
1. Gets a **goal**
2. **Plans** steps
3. Interacts with the **environment / tools**
4. Gets **feedback**
5. **Corrects** until the goal is reached (or reports failure)
6. Uses **memory** to track the task

This year agents (Claude Code, Codex, Deep Research) started doing real end-to-end workflows.

### Why coding agents became reliable recently
Not a fundamentally new architecture — mostly **more powerful models + better RL with verifiable rewards**. A **self-improvement loop** kicks in: the model generates its own unit tests, which become a reliable verifier.

---

## 9. Agentic Workflow Components & Patterns

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

**The bottleneck: verification.** In verifiable domains (math, code) you can give feedback; in open-ended domains (creative writing) feedback is scarce and human feedback becomes the bottleneck — the **generator-verifier gap**.

---

## 10. Agent Applications

| Domain | Use cases |
|--------|-----------|
| Repetitive dev tasks | Code migration, version upgrades, restructure, data engineering, warehouse migration, unit tests |
| Customer support | Live transcription, knowledge assist, smart reply, call summary |
| Deep research | Identify references → outline → summarize → synthesize full report |
| AI scientist | Idea generation (brainstorming), experiment iteration, paper writeup |

---

## 11. Course Logistics

- **Grading:** 3 homeworks = 50% · course project = 50%.
- **Project:** teams of 2–4; API credits provided. Hypothesis-driven, "more than glue coding."
  - *Good:* new benchmark/eval set, reliability study, hill-climb a benchmark, question/improve a paper's decision.
  - *Bad:* survey paper, or a plain app with no hypothesis.
- **Milestones:** proposal (early Oct) → midterm presentation (progress expected) → final report + poster (Dec 12, 4–6pm).
- **Tools:** Canvas (updates), Ed (questions), Gradescope (submissions). Honor code + late policy; no audits.

---

## 12. Key Takeaways

1. Models improved via **scaling** (compute, data, params) — but scaling is saturating.
2. **CoT reasoning was emergent**, not designed; reasoning models are now trained for it.
3. ChatGPT = pre-training + instruction tuning + **RLHF**.
4. **Inference scaling** (repeated sampling + verifiers) unlocks capability without touching parameters; log-linear scaling.
5. **Self-improvement** = test-time synthetic data fed back into fine-tuning (DeepSeek/o1).
6. Agents = goal + plan + act + feedback + self-correct, orchestrated with verifiers/judges/tools.
7. **Verification is the key bottleneck** (generator-verifier gap).
