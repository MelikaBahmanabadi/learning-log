# Flashcards

<!-- Cards in Anki format: Question? ; Answer -->

---

## W1 — Course Overview

What is CS329A about? ; Self-improving AI agents — agents that plan, act, receive feedback, and improve themselves. It covers how LLMs evolve from single-turn chatbots into agents that accomplish end-to-end tasks.

Who teaches CS329A and where did they meet? ; Akanksha (adjunct professor, Reflection AI) and Azalia Mirhoseini (assistant professor, Stanford CS). They met at Google Brain, then Google DeepMind; Azalia also worked on Claude (Anthropic) and Gemini.

---

## W1 — Scaling Laws

What are the three axes of LLM scaling? ; Compute, dataset size, and parameter count. Increasing any of them reduces test loss and produces a better model.

How did model sizes grow from 2018 to 2024? ; BERT (340M) → GPT-2 (1.5B) → GPT-3 (175B) → PaLM (540B) → GPT-4 (estimated trillions). Exponential growth in parameter count.

What three benefits come from bigger models? ; 1) Better benchmark performance, 2) few-shot learning ability, 3) emergent behaviors like reasoning.

---

## W1 — Zero-shot & Few-shot

What's the difference between zero-shot and few-shot learning? ; Zero-shot gives only a task description. Few-shot gives the task description plus a few input→output examples the model follows as a template.

Why is few-shot learning so useful? ; You no longer need to fine-tune for every domain — a few examples let the model adapt, making prototyping very easy.

---

## W1 — Chain of Thought

What is chain of thought prompting? ; Giving the model not just an example answer but the step-by-step reasoning to reach it, so it learns the process and can solve new problems.

Was chain of thought baked in by design? ; No — it was an emergent behavior discovered in larger models. GSM8K was the first paper showing signs of life; PaLM confirmed it was a big deal.

Which model sizes benefit from chain of thought? ; Large models (PaLM 540B, GPT-3 175B). Small models (~7–8B like LaMDA/GPT) get no benefit from it.

---

## W1 — Training Pipeline

What is pre-training? ; Training the model to predict the next token over a huge corpus (internet, books). The model gains statistical knowledge but no sense of right/wrong or how to follow instructions.

What is instruction tuning? ; Fine-tuning on (instruction, question → answer) pairs so the model learns to follow instructions and answer questions.

What is RLHF? ; Reinforcement Learning from Human Feedback — build a reward model from human preference ratings, then use it to guide the LLM's parameters toward generations the reward model scores highly.

What reward types can be combined in RLHF? ; Correctness, helpfulness, specificity, and harmlessness — weighted according to what we care most about.

What two innovations made ChatGPT leapfrog GPT-3? ; Instruction tuning and RLHF (Reinforcement Learning from Human Feedback).

---

## W1 — Inference Scaling

What is the "Large Language Monkeys" idea? ; Inspired by the infinite monkey theorem: repeatedly sample the LLM on the same problem (parallel sampling) and use a verifier to pick the correct answer.

What is a verifier? ; A selection mechanism that checks generated responses (e.g. unit tests for code, known answers for math) and picks the correct one.

What did repeated sampling (1 → 10,000 samples) show? ; Coverage (fraction of problems solved by ≥1 sample) rises log-linearly. A 7B model with many samples beat GPT-4o with one sample.

What is inference (test-time) scaling? ; Keeping model parameters fixed and spending more compute at inference time (more samples / thinking) to get better answers. Shows a log-linear scaling law.

What's the difference between pass@1 and coverage (pass@k)? ; pass@1 is accuracy of a single generation; coverage/pass@k is the fraction solved by at least one of k samples. Reasoning training raises pass@1; repeated sampling raises coverage.

---

## W1 — Reasoning Models

What did DeepSeek and o1 do differently? ; Brought fine-tuning and test-time scaling together — generate synthetic data during test-time scaling, then feed it back to fine-tune the model (a self-improvement loop).

What steps do reasoning models take on hard problems? ; Problem analysis, task decomposition, self-evaluation (feedback), self-correction, and alternative proposals (backtracking).

Where do reasoning models (o1) beat GPT-4o? ; Math, data analysis, and programming — but not necessarily personal writing or text editing.

---

## W1 — Agents

How is an agent different from a chatbot? ; An agent has a goal, plans steps, interacts with an environment/tools, gets feedback, corrects itself, and decides when to stop. Chatbots are single-turn.

What building blocks do agentic workflows use? ; LLM calls, verifiers, critics/judges (LLM-as-judge), tool calls (search, terminal), and orchestration.

Name the common orchestration patterns. ; Prompt chaining, routing, parallelization, orchestrator (planning LLM), evaluator/judge, and verifiers.

Why is verification the bottleneck for agents? ; In verifiable domains (math, code) you can give feedback, but in open-ended domains feedback is scarce and human feedback becomes the bottleneck — the generator-verifier gap.

---

## W1 — Course Logistics

What is the grading breakdown for CS329A? ; Three homeworks = 50%, course project = 50%.

What makes a good vs. bad course project? ; Good: new benchmark/eval set, reliability study, hill-climbing a benchmark, questioning a paper's decision. Bad: a survey paper or a plain app with no hypothesis.
