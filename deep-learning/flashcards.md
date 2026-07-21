# Flashcards

<!-- Cards in Anki format: Question? ; Answer -->

---

## W1 — What is a Neural Network?

What does ReLU stand for and what is its formula? ; Rectified Linear Unit — max(0, z). Output is zero for negative input, otherwise the input itself.

Why is stacking multiple layers useless without non-linearity? ; Because W2(W1x) = (W2W1)x = W3x — the matrices collapse into one. The whole network becomes equivalent to a single linear layer, which can only draw hyperplanes, not complex functions.

How many weights does a hidden layer with n neurons densely connected to m inputs have? (no bias) ; m × n

What does a Dense (fully connected) layer mean? ; Every neuron from the previous layer connects to every neuron in the next — the network is free to learn any combination of inputs.

Why is a hidden layer called "hidden"? ; Because its values have no direct labels in the training data — unlike input and output which are explicitly known.

---

## W1 — Supervised Learning with Neural Networks

Which architecture for which data type? ; Standard NN → tabular/structured | CNN → spatial patterns (image, signal) | RNN/LSTM → sequential/temporal (audio, time-series, text) | Hybrid → complex mixed (autonomous driving)

What are the four main learning paradigms? ; Supervised (labeled), Unsupervised (no label), Semi-supervised (few labeled + many unlabeled), Reinforcement (reward signal)

What is the difference between a Learning Paradigm and a Task Type? ; Paradigm = type of training data (supervised/unsupervised/...) | Task = type of output (classification/regression/clustering/...). Regression is a task that falls inside supervised learning, not a paradigm itself.

Why is RNN better than Standard NN for industrial sensor time-series? ; Because of temporal dependencies — step t depends on step t-1 (Markov chain). Standard NN treats each input independently.

What is the core difference between Structured and Unstructured data? ; Structured = each feature has explicit meaning (table, sensor with timestamp) | Unstructured = meaning is extracted from raw patterns (image, audio, free text)

---

## W1 — Why is Deep Learning Taking Off?

What are the three main drivers of Deep Learning growth? ; 1) More labeled data, 2) Faster computation and hardware like GPUs, 3) Algorithmic and architectural innovations.

What does m represent in this course's notation? ; The number of training examples; in supervised learning, typically the count of labeled samples that have both x and y.

Why can Sigmoid cause vanishing gradient in deep networks? ; In saturation regions, the Sigmoid derivative approaches zero; repeated multiplication of these small gradients during backpropagation makes early-layer gradients nearly zero.

In which regions is the ReLU derivative zero vs one? ; Zero for z < 0 and one for z > 0; at z = 0, the derivative is set by convention in most implementations.

Why does computation speed matter for Deep Learning success? ; It shortens the idea → code → experiment → result → iteration cycle, allowing more experiments and faster convergence to effective models.

---

## W2 — Basics of Neural Network Programming

Why do we avoid explicit for-loops over the full training set in neural network implementations? ; Because vectorized matrix operations are far more efficient, cleaner, and faster for heavy neural network computations.

How is a 64x64 RGB image converted to a feature vector? ; By unrolling all pixel values from each of the three color channels into a single long vector of length 12288 = 3 × 64 × 64.

What does matrix X represent in this course's notation and what are its dimensions? ; The input matrix formed by stacking training samples as columns; dimensions are (n_x, m).

What does matrix Y represent in this course's notation and what are its dimensions? ; The label matrix formed by stacking outputs as columns; dimensions are (1, m).

What does y-hat represent in Logistic Regression? ; P(y=1|x) — the probability that given input features x, the true label y equals 1.

Why do we need the Sigmoid activation function in Logistic Regression? ; Because Sigmoid maps any real number to the interval (0,1), converting the output into a valid probability.

Why is a linear output of the form w^T x + b unsuitable for binary classification? ; Because linear outputs can be negative or greater than 1, which cannot be interpreted as a probability.

What is the core probabilistic interpretation of Logistic Regression? ; The model tries to estimate the conditional probability P(y=1|x) — the chance that input x belongs to the positive class.

---

## Needs Review
<!-- Wrong answers from periodic quizzes go here -->
