# Flashcards

<!-- Cards in Anki format: Question? ; Answer -->

---

## W1 — Course Overview

What is CS329A about? ; Self-improving AI agents — agents that plan, act, receive feedback, and improve themselves. It covers how LLMs evolve into agents that accomplish end-to-end tasks.

What is the canonical course code and URL for this course? ; CS329A — Self-Improving AI Agents. Canonical URL: https://cs329a.stanford.edu/. (Earlier drafts used "CS239A" / cs239a.stanford.edu, which is not the official identifier.)

Who is Aakanksha Chowdhery? ; Adjunct Professor at Stanford, co-instructor of CS329A. Previously the technical lead of the 540B PaLM model and a lead researcher on Gemini pre-training, scaling, and fine-tuning at Google. Source: https://www.achowdhery.com/.

Who is Azalia Mirhoseini? ; Assistant Professor of Computer Science at Stanford and director of the Scaling Intelligence Lab; co-instructor of CS329A. Co-founder of Ricursive Intelligence. Prior work at Google Brain, Anthropic (Claude), and Google DeepMind (Gemini); pioneer of AlphaChip and the Large Language Monkeys paper. Source: http://azaliamirhoseini.com/.

---

## W1 — Scaling Laws

What are the three axes of LLM scaling? ; Compute, dataset size, and parameter count. Increasing any of them reduces test loss and produces a better model.

What were the parameter counts of BERT, GPT-2, GPT-3, and PaLM? ; BERT ≈ 340M (Devlin et al. 2019); GPT-2 ≈ 1.5B (Radford et al. 2019); GPT-3 ≈ 175B (Brown et al. 2020); PaLM ≈ 540B (Chowdhery et al. 2022). All from the respective model papers.

What is the status of GPT-4's parameter count? ; Officially undisclosed. The "trillions" figure is a third-party estimate (e.g. SemiAnalysis, 2023); it is not an OpenAI-published number.

What is one caveat about claiming that "scaling saturated around 2023–2024"? ; Saturation depends on the metric. Test loss continued to improve past 2023, while benchmark-accuracy gains and per-token economics flattened. No single source defines a universal cutoff year.

What is the first benefit of bigger models? ; Better performance on natural-language, reasoning, and other benchmarks.

What is the second benefit of bigger models? ; Few-shot learning — a few examples are enough to adapt without per-domain fine-tuning.

What is the third benefit of bigger models? ; Emergent behavior — capabilities like reasoning only appear at larger sizes (debated as discontinuities vs metric artifacts).

---

## W1 — Zero-shot & Few-shot

What is the difference between zero-shot and few-shot learning? ; Zero-shot gives only a task description. Few-shot gives the task description plus a few input→output examples the model follows as a template.

Why is few-shot learning useful? ; A few examples let the model adapt without per-domain fine-tuning, making prototyping very easy.

---

## W1 — Chain of Thought

What is chain-of-thought (CoT) prompting? ; Giving the model not just an example answer but the step-by-step reasoning to reach it, so it learns the process and can solve new problems.

Was chain of thought designed in? ; No — it was an emergent behavior discovered in larger models. The GSM8K paper (Cobbe et al. 2021) is cited as the "first signs of life"; PaLM 540B (Chowdhery et al. 2022) is cited as the larger-scale confirmation.

For which models does CoT show the gain reported in the lecture? ; In Wei et al. 2022 the gain appears on larger LaMDA / PaLM models (up to 540B). Smaller models in the same experiments show little or no benefit on the same benchmarks. The "~7–8B threshold" is a paraphrase; the original paper reports results across multiple sizes without a single sharp cutoff.

---

## W1 — Training Pipeline

What is pre-training? ; Training the model to predict the next token over a huge corpus (internet, books). The model gains statistical knowledge but no built-in sense of right/wrong or how to follow instructions.

What is fine-tuning / alignment? ; Fine-tuning the base model on higher-quality, curated data to steer it toward human goals, preferences, and values. Alignment is still an unsolved problem (lecture framing).

What is instruction tuning? ; Training on `(instruction, question → answer)` pairs so the model learns to follow instructions. Data mixes human-generated and synthetic examples (Ouyang et al. 2022 / InstructGPT).

What is RLHF? ; Reinforcement Learning from Human Feedback — build a reward model from human preference ratings, then use it to guide the LLM's parameters toward generations the reward model scores highly.

Which reward types can be combined in RLHF? ; Correctness, helpfulness, specificity, and harmlessness — weighted according to what we care most about.

What is the canonical 3-step pipeline the lecture uses for ChatGPT? ; Pre-training → instruction tuning → RLHF, introduced in Ouyang et al. 2022 (InstructGPT). Treat this as a pedagogical diagram, not a literal training spec for any specific ChatGPT release.

---

## W1 — Inference Scaling

What is the "Large Language Monkeys" idea? ; Inspired by the infinite monkey theorem: repeatedly sample the LLM on the same problem (parallel sampling) and use a verifier to pick the correct answer. (Brown et al. 2024.)

What is a verifier in the context of inference scaling? ; A selection mechanism that checks generated responses (e.g. unit tests for code, known answers for math) and picks the correct one.

What did repeated sampling show in the Large Language Monkeys paper? ; Increasing samples per problem raises coverage (fraction of problems solved by ≥1 of k samples). On SWE-bench Lite, coverage rose from 15.9% with 1 sample to 56% with 250 samples for the best-sampled model. The relationship is log-linear.

What is the scoped reading of "a 7B model with many samples beat GPT-4o with one sample"? ; It refers to specific SWE-bench Lite / HumanEval experiments in Brown et al. 2024, comparing a smaller model with a high sampling budget to a larger model with k=1. The exact model identities, sampling budget, verifier, and benchmark must be quoted from the paper.

What is inference (test-time) scaling? ; Keeping model parameters fixed and spending more compute at inference time (more samples / more thinking) to get better answers. Shows a log-linear scaling law on coverage.

How does the lecture define coverage vs. pass@k? ; In Brown et al. 2024, **coverage** = fraction of benchmark problems solved by ≥1 of k samples. **pass@k** (Codex / Chen et al. 2021) = probability that at least one of k samples passes, with duplicates removed and an unbiased estimator. They are related but use different estimators; quote the paper's exact definition when citing a number.

---

## W1 — Reasoning Models

What did DeepSeek-R1 do differently? ; Per the public technical report (DeepSeek-AI, 2025, arXiv 2501.12948), DeepSeek-R1 uses an RL pipeline (GRPO + verifiable rewards) where model-generated reasoning traces become training data. This is the **documented** version of the "self-improvement loop" the lecture describes.

What did OpenAI disclose about o1's training pipeline? ; OpenAI's o1 system page / o1 system card describes large-scale RL with chain-of-thought reasoning, but does **not** disclose the proprietary training data recipe in detail. Treat "o1 generates test-time data and feeds it back to fine-tune" as a high-level course hypothesis, not a confirmed fact.

What did Google's Gemini technical report disclose about a self-improvement loop? ; The Gemini technical report (Gemini Team, 2024, arXiv 2312.11805) does not describe a closed-loop self-improvement pipeline. Treat the same framing for Gemini as a high-level course hypothesis.

What steps do reasoning models take on hard problems? ; Problem analysis, task decomposition, self-evaluation (feedback), self-correction, and alternative proposals (backtracking).

On which benchmarks does o1 outperform GPT-4o per OpenAI? ; Per OpenAI's o1 launch page: AIME, MATH, GPQA, Codeforces. OpenAI also reports GPT-4o competitive or superior on writing/editing tasks.

---

## W1 — Agents

How is an agent different from a chatbot / reasoning model? ; An agent is defined by autonomy and a control loop — it has a goal, plans, interacts with an environment / tools, gets feedback, corrects itself, and decides when to stop. Chatbots and reasoning models are not strictly "single-turn" (modern chat products are multi-turn); agents are distinguished by the loop, tool/environment interaction, state/memory, and termination behavior.

What building blocks do agentic workflows use? ; LLM calls, verifiers, critics/judges (LLM-as-judge), tool calls (search, terminal, code execution), and orchestration.

What are the common orchestration patterns? ; Prompt chaining, routing, parallelization, orchestrator (planning LLM), evaluator/judge, and verifiers.

Why is verification the bottleneck for agents? ; In verifiable domains (math, code) you can give automatic feedback; in open-ended domains feedback is scarce and human feedback becomes the bottleneck — the **generator-verifier gap**.

---

## W1 — Course Logistics

What is the grading breakdown for CS329A (Autumn 2025)? ; HW1 15% · HW2 15% · HW3 20% · Project Proposal 2.5% · Midterm presentation + Report 10% · Final project 35% · Poster 2.5%. Source: https://cs329a.stanford.edu/.

What makes a good vs. bad course project? ; Good: new benchmark/eval set, reliability study, hill-climbing a benchmark, questioning a paper's decision. Bad: a survey paper or a plain app with no hypothesis.

---

## Needs Review
<!-- Wrong answers from periodic quizzes go here -->