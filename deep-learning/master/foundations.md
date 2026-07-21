# Foundations of Deep Learning

**Topics:** Neural network unit, activation functions, multi-layer networks, supervised learning paradigm, architecture selection, DL growth factors.

---

## 1. The Artificial Neuron

A single neuron computes a two-step mapping [@goodfellow2016, ch. 6]:

$$z = \mathbf{w}^\top \mathbf{x} + b, \qquad a = g(z)$$

where **w** are weights, $b$ is bias, and $g(\cdot)$ is a nonlinear activation function. Without $g$, any stack of layers collapses to a single affine transform:

$$\mathbf{z}_2 = W_2(W_1\mathbf{x} + b_1) + b_2 = \underbrace{W_2 W_1}_{A}\mathbf{x} + \underbrace{W_2 b_1 + b_2}_{c}$$

**Core insight:** Depth is only meaningful because nonlinear activations break this collapse. [@goodfellow2016, ch. 6]

---

## 2. Activation Functions

### ReLU (Rectified Linear Unit)

$$g(z) = \max(0, z), \qquad g'(z) = \begin{cases}1 & z > 0 \\ 0 & z \leq 0\end{cases}$$

**Why ReLU dominates hidden layers:** Its gradient is constant (= 1) in the active region, which prevents vanishing gradients during backpropagation through deep networks. It is also computationally cheap (one comparison) [@goodfellow2016, ch. 6].

**Pitfall — Dying ReLU:** If a neuron always receives $z < 0$, its gradient is permanently zero and it never updates. Caused by large negative bias initialization. Fix: Leaky ReLU ($g(z) = \max(0.01z, z)$) or He initialization.

### Sigmoid

$$g(z) = \frac{1}{1 + e^{-z}}, \qquad g'(z) = g(z)(1 - g(z))$$

In the saturation regions ($z \gg 0$ or $z \ll 0$), $g'(z) \approx 0$. Multiplied across $n$ layers in backpropagation, the gradient becomes $\approx 0.01^n \approx 0$ for $n > 4$. **Use sigmoid only for binary output units, not hidden layers in deep networks** [@goodfellow2016, ch. 6].

### Tanh

$$g(z) = \tanh(z), \qquad g'(z) = 1 - \tanh^2(z)$$

Centered at zero (unlike sigmoid), so it has better gradient flow than sigmoid in shallow networks. Still suffers vanishing gradients in deep networks.

### Comparison

| Activation | Gradient in active region | Saturates? | Recommended for |
|---|---|---|---|
| ReLU | 1 (constant) | No | Hidden layers (default) |
| Leaky ReLU | 1 or 0.01 | No | When dying ReLU is a concern |
| Tanh | $1 - \tanh^2(z) \leq 1$ | Yes (extremes) | Shallow hidden layers |
| Sigmoid | $g(z)(1-g(z)) \leq 0.25$ | Yes | Binary output layer only |

---

## 3. Architecture Selection by Data Type

The choice of architecture should follow the structure of the input data [@ng2017, W1] [@goodfellow2016, ch. 9-10]:

| Data Type | Architecture | Reason |
|---|---|---|
| Tabular / Structured | MLP (fully connected) | No spatial or sequential structure to exploit |
| Images / Spatial | CNN | Weight sharing + local connectivity captures spatial invariance |
| Sequences / Time-Series | RNN, LSTM, GRU | Recurrent connections model temporal dependencies |
| Long-range dependencies | Transformer | Self-attention accesses any position in constant steps |

### Practical Warning (Industrial Sensor / Time-Series Data)

RNN/LSTM is **not** the universal default for time-series. In practice:

- **TCN (Temporal Convolutional Network):** Often faster and more accurate than LSTM on fixed-length sequences; fully parallelizable; strong empirical baseline [@bai2018tcn].
- **Transformer:** Superior on long-range dependency problems but data-hungry and memory-intensive.
- **MLP on engineered features:** A surprisingly strong baseline for anomaly detection and classification when the feature set is well-designed.

**Rule of thumb:** Always benchmark a simple baseline first, then add architectural complexity only when justified by performance gains.

---

## 4. Supervised Learning Paradigm

Given a dataset of pairs $\{(\mathbf{x}^{(i)}, y^{(i)})\}_{i=1}^{m}$, supervised learning finds a mapping $f: \mathbf{x} \mapsto y$ that minimizes a loss function [@goodfellow2016, ch. 5].

**Cost function (cross-entropy for binary classification):**
$$J(W, b) = -\frac{1}{m}\sum_{i=1}^{m}\left[y^{(i)}\log\hat{y}^{(i)} + (1-y^{(i)})\log(1-\hat{y}^{(i)})\right]$$

**Gradient descent update:**
$$W \leftarrow W - \alpha \frac{\partial J}{\partial W}, \qquad b \leftarrow b - \alpha \frac{\partial J}{\partial b}$$

### Notation Convention (Coursera standard)

| Symbol | Meaning |
|---|---|
| $m$ | Number of training examples |
| $n_x$ | Number of input features |
| $X \in \mathbb{R}^{n_x \times m}$ | Input matrix (each column = one example) |
| $Y \in \mathbb{R}^{1 \times m}$ | Output matrix |
| $[l]$ | Superscript for layer $l$ |
| $(i)$ | Superscript for example $i$ |

**Why $X$ is $(n_x, m)$ not $(m, n_x)$?** The convention $Z = WX + b$ works directly and vectorizes over all $m$ examples simultaneously without transposition.

---

## 5. Why Deep Learning Took Off

Three reinforcing factors created the DL revolution [@ng2017, W1] [@goodfellow2016, ch. 1]:

1. **Data scale:** Millions of labeled examples (ImageNet, Common Crawl). Small models plateau quickly; large deep networks keep improving with more data.
2. **Compute (GPU):** Thousands of parallel cores make large matrix multiplications feasible. Without GPU, one training run takes weeks.
3. **Algorithmic improvements:** Sigmoid → ReLU (stable gradients), batch normalization, better optimizers (Adam), residual connections. Each improvement shortens the experiment cycle.

**The experiment cycle is critical:** Faster training → more iterations → better models in less calendar time. This is why PyTorch adoption accelerated over TensorFlow 1.x.

---

## 6. Structured vs Unstructured Data

- **Structured:** Fixed schema with named features (sensor readings, transactions, tabular). Feature meaning is explicit.
- **Unstructured:** Raw signals — pixels, waveforms, tokens. The network must learn the representation from scratch.

Deep Learning's biggest historical wins were in unstructured data (ImageNet 2012, speech recognition, LLMs). However, gradient-boosted trees (XGBoost, LightGBM) remain competitive on structured tabular data and should not be dismissed.

---

## Common Pitfalls

| Pitfall | Root Cause | Fix |
|---|---|---|
| Stacking linear layers with no activation | Composition of linear maps is linear | Always add activation between layers |
| Sigmoid in deep hidden layers | Saturation → vanishing gradient | Use ReLU as default hidden activation |
| Dying ReLU | Negative bias initialization | Leaky ReLU or He init |
| Wrong matrix shape (X as `(m, n_x)`) | Shape confusion in manual impl | Enforce $(n_x, m)$ convention |
| Assuming LSTM ≥ TCN for time-series | LSTM is not universal | Always benchmark TCN and simple MLP first |

---

## References

- [@goodfellow2016]: Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press. Chapters 5, 6.
- [@ng2017]: Andrew Ng et al. "Neural Networks and Deep Learning". Coursera / deeplearning.ai, 2017. Week 1.
- [@bai2018tcn]: Bai, S., Kolter, J. Z., & Koltun, V. (2018). "An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling." arXiv:1803.01271.
