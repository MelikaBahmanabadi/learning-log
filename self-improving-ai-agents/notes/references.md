# Sources & Reference Map

This file lists every external source referenced in the Self-Improving AI Agents notes, with stable links and the topics each one supports.

## Course

| Key | Source | Topics covered |
|---|---|---|
| `cs329a-syllabus` | [https://cs329a.stanford.edu/](https://cs329a.stanford.edu/) — CS329A Self-Improving AI Agents (Stanford, Autumn 2025) | Course code, title, term, instructors, lecture topics, schedule, grading, course logistics, paper readings list |
| `cs329a-staff` | [https://cs329a.stanford.edu/](https://cs329a.stanford.edu/) — Course Staff section | Instructor names, photos, course-assistant names |
| `achowdhery-site` | [https://www.achowdhery.com/](https://www.achowdhery.com/) — Aakanksha Chowdhery's personal site | Instructor full name, title (Adjunct Professor, Stanford), research areas, prior affiliations (Google PaLM/Gemini, Microsoft Research, Princeton), publications list |
| `azalia-site` | [http://azaliamirhoseini.com/](http://azaliamirhoseini.com/) — Azalia Mirhoseini's personal site | Instructor full name, title (Assistant Professor of CS, Stanford), lab (Scaling Intelligence), affiliations (Ricursive Intelligence, Google Brain, Anthropic, Google DeepMind), publications list |

## Lecture recordings

The course page does not embed a canonical video URL. Stanford Online hosts the course for credit, and a YouTube playlist circulates among students.

- **Stanford Online course listing:** https://online.stanford.edu/courses/cs329a-self-improving-ai-agents (WAF-protected; not fetched here)
- **Lecture 1 — "Course Overview"** was scheduled for Mon Sep 22, 2025 per `cs329a-syllabus`. Exact video URL and timestamp ranges were **not independently verified** for these notes; claim-by-claim timestamps in `W1-summary.md` should be re-confirmed against the recording before long-term study.

## Papers and external claims cited in the notes

| Key | Source | Used for |
|---|---|---|
| `kaplan2020scaling` | Kaplan et al., "Scaling Laws for Neural Language Models" (arXiv 2001.08361) | Empirical scaling-law curves on which the "compute / data / parameters" axes are based |
| `hoffmann2022chinchilla` | Hoffmann et al., "Training Compute-Optimal Large Language Models" (arXiv 2203.15556, "Chinchilla") | Compute-optimal frontier; used to contextualize the parameter-count table |
| `devlin2019bert` | Devlin et al., "BERT: Pre-training of Deep Bidirectional Transformers" (arXiv 1810.04805) | BERT 340M parameter count |
| `radford2019gpt2` | Radford et al., "Language Models are Unsupervised Multitask Learners" (OpenAI Tech Report 2019) | GPT-2 1.5B parameter count |
| `brown2020gpt3` | Brown et al., "Language Models are Few-Shot Learners" (arXiv 2005.14165) | GPT-3 175B parameter count; zero-shot vs few-shot framing |
| `chowdhery2022palm` | Chowdhery et al., "PaLM: Scaling Language Modeling with Pathways" (JMLR 2023, arXiv 2204.02311) | PaLM 540B parameter count; CoT emergence claim attributed to PaLM |
| `wei2022cot` | Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (arXiv 2201.11903) | Chain-of-thought prompting technique and the original "emergent" framing |
| `cobbe2021gsm8k` | Cobbe et al., "Training Verifiers to Solve Math Word Problems" (arXiv 2110.14168, GSM8K) | "First signs of life" attribution for CoT |
| `brown2024llm-monkeys` | Brown et al., "Large Language Monkeys: Scaling Inference Compute with Repeated Sampling" (arXiv 2407.21787) | The repeated-sampling / coverage result, log-linear law, SWE-bench Lite 15.9% → 56% example, "7B with many samples" comparison |
| `snell2024testtime` | Snell et al., "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters" (arXiv 2408.03314) | Test-time compute scaling beyond repeated sampling (e.g. revision, verifier-guided search) |
| `wang2023self-consistency` | Wang et al., "Self-Consistency Improves Chain of Thought Reasoning in Language Models" (ICLR 2023, arXiv 2203.11171) | Self-consistency as the sampling-with-verifier precursor |
| `lightman2023letsverify` | Lightman et al., "Let's Verify Step by Step" (arXiv 2305.20050) | Process reward models and verifier-conditioned reasoning training |
| `guo2025deepseekr1` | DeepSeek-AI, "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning" (arXiv 2501.12948) | Reasoning-model RL pipeline; supports the "DeepSeek trained itself with test-time-generated data" claim, scoped to the public R1 technical report |
| `openai-o1-system` | OpenAI, "Learning to Reason with LLMs" / o1 system card (openai.com/index/learning-to-reason-with-llms, 2024) | General o1 description; **does not** disclose the proprietary training data recipe in detail |
| `gemini-team-2024` | Gemini Team, "Gemini: A Family of Highly Capable Multimodal Models" (arXiv 2312.11805) | General Gemini description; no public pipeline recipe for test-time → training self-improvement |
| `ouyang2022instructgpt` | Ouyang et al., "Training Language Models to Follow Instructions with Human Feedback" (arXiv 2203.02155, InstructGPT) | Pre-training → SFT → RLHF pipeline as described in the original InstructGPT paper; cited as the source for the canonical training pipeline, not as a literal ChatGPT training spec |
| `schulman2023chatgpt` | Schulman (OpenAI) talk / OpenAI ChatGPT launch blog, Nov 2022 | General ChatGPT launch date |
| `sutton2019bitter` | Sutton, "The Bitter Lesson" (2019) | Often-cited framing for "scaling wins"; not directly cited in the notes but useful background |

## Estimates / unverified claims

| Item | Status |
|---|---|
| "GPT-4 has trillions of parameters" | **Unverified third-party estimate.** OpenAI has not disclosed GPT-4's parameter count. The number circulating in press (e.g. SemiAnalysis, 2023) is a leaked estimate, not an official figure. Notes flag this as an estimate. |
| "Scaling held until ~2023–2024 and saturated" | **Lecture claim** as paraphrased. "Saturation" depends on the chosen metric (test loss vs benchmark performance vs economic cost); no single source backs a universal cutoff year. |
| "7B model with many samples beat GPT-4o with one sample" | **Specific to a cited experiment.** Per `brown2024llm-monkeys`, the repeated-sampling paper shows that with sufficient samples, smaller models can reach coverage competitive with much larger single-sample baselines on SWE-bench Lite. The exact "7B beat GPT-4o" framing should be re-checked against the paper's tables before being repeated. |
| "ChatGPT reached 1M users in 5 days" | Widely reported at launch (Nov 2022). Treat as a contemporaneous press claim, not a Stanford-verified number. |
| "Reasoning models generate synthetic data at test time and feed it back into fine-tuning" | Bounded claim about DeepSeek-R1's public RL recipe (`guo2025deepseekr1`). For o1 and Gemini, no public technical report describes an analogous closed-loop training pipeline; treat as a high-level course hypothesis for those systems. |
| "o1 outperforms GPT-4o on math, data analysis, programming" | Bounded to the evaluations summarized on OpenAI's o1 launch page; not a universal claim across tasks. |

## Stable citation keys used in notes

`W1-summary.md` uses the keys above as inline reference markers (e.g. `[cs329a-syllabus]`, `[brown2024llm-monkeys]`). When a claim cannot be sourced to a primary source, it is labeled `Lecture claim` (with the lecture identifier) or `Interpretation / synthesis`.