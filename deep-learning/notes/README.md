# Deep Learning — Notes

This folder contains structured study notes generated during the course.

## Structure

- `W<n>-summary.md` — Weekly summaries (command: `weekly notes`)
- `<section-name>.md` — Per-section notes (command: `section notes`)
- `<topic-name>.md` — Full topic deep-dives (command: `final file`)

## Commands

| Command | When to use | Output |
|---|---|---|
| `section notes` | End of any section | Compact: summary + formulas + flashcards |
| `weekly notes` | End of each week | Unified: all sections of that week |
| `final file` | Topic mastered (test ≥80%) | Full deep-dive with resources |

---

## Week Summaries

### W1 — Neural Networks and Deep Learning (DONE)

**Course:** Neural Networks and Deep Learning | **Platform:** Coursera

| Section | Status | Key Concepts |
|---|---|---|
| W1-01 / What is a Neural Network? | ✅ DONE | Neuron, ReLU, dense/fully-connected layers, hidden layers, non-linearity |
| W1-02 / Supervised Learning with Neural Networks | ✅ DONE | NN vs CNN vs RNN, structured vs unstructured data, learning paradigms vs task types |
| W1-03 / Why is Deep Learning Taking Off? | ✅ DONE (no test) | Three growth drivers: data, compute (GPU), algorithms; sigmoid vanishing gradient; iteration cycle |

**Core Ideas:**
- A neural network is a stack of layers; without **non-linearity** (e.g., ReLU), all layers collapse to one linear transform.
- Architecture choice is data-type driven: **Standard NN** → tabular, **CNN** → spatial, **RNN/LSTM** → sequential.
- Deep Learning took off due to **more labeled data**, **faster hardware**, and **better algorithms** (e.g., switching sigmoid → ReLU to fix vanishing gradients).
- Notation convention: `m` = number of training examples, `X` has shape `(n_x, m)`, `Y` has shape `(1, m)`.

**Flashcard count (W1):** 15 cards across 3 sections.

**Next:** W2 — Basics of Neural Network Programming (Logistic Regression, vectorization, backprop)
