# W1 — Neural Networks and Deep Learning

**Course:** Neural Networks and Deep Learning | **Platform:** Coursera  
**Week:** 1 | **Status:** ✅ DONE  
**Sections:** W1-01, W1-02, W1-03  

---

## فهرست مطالب

1. [شبکه عصبی چیست؟](#۱-شبکه-عصبی-چیست)
2. [یادگیری نظارت‌شده با شبکه‌های عصبی](#۲-یادگیری-نظارت‌شده-با-شبکه‌های-عصبی)
3. [چرا Deep Learning جهش کرد؟](#۳-چرا-deep-learning-جهش-کرد)
4. [خلاصه ریاضی](#۴-خلاصه-ریاضی)
5. [Pitfalls رایج](#۵-pitfalls-رایج)
6. [Flashcards — W1](#۶-flashcards--w1)

---

## ۱. شبکه عصبی چیست؟

### مدل یک نورون (Perceptron / Unit)

ساده‌ترین نورون یک تابع دو مرحله‌ای است:

```
z = w·x + b       (ترکیب خطی ورودی‌ها)
a = g(z)          (اعمال تابع فعال‌سازی)
```

- **x**: بردار ویژگی‌های ورودی
- **w**: وزن‌ها (اهمیت هر ویژگی)
- **b**: bias (آستانه جداسازی)
- **g(·)**: activation function (منبع غیرخطی بودن)

### چرا چند لایه Linear بی‌اثر است؟

اگر activation نداشته باشیم:

```
Layer 1: z₁ = W₁x + b₁
Layer 2: z₂ = W₂z₁ + b₂ = W₂(W₁x + b₱) + b₂ = (W₂W₁)x + (W₂b₁ + b₂)
```

نتیجه: `z₂ = Ax + c` — یعنی یک نگاشت linear با `A = W₂W₁`. هر تعداد لایه Linear بدون activation، به یک لایه واحد linear تقلیل پیدا می‌کند. **Activation غیرخطی تنها عاملی است که depth شبکه را معنادار می‌کند.**

### توابع Activation اصلی

| تابع | فرمول | مشتق | کاربرد اصلی |
|---|---|---|---|
| **Sigmoid** | `σ(z) = 1/(1+e⁻ᶻ)` | `σ(z)·(1−σ(z))` | خروجی binary classification |
| **Tanh** | `(eᶻ−e⁻ᶻ)/(eᶻ+e⁻ᶻ)` | `1 − tanh²(z)` | Hidden layers (بهتر از sigmoid) |
| **ReLU** | `max(0, z)` | `1 اگر z>0 وگرنه 0` | Hidden layers (پیش‌فرض) |
| **Leaky ReLU** | `max(0.01z, z)` | `1 یا 0.01` | وقتی dying ReLU مشکل‌ساز است |

#### چرا ReLU بهتر از Sigmoid است؟

- **Vanishing Gradient:** در sigmoid، برای z بزرگ یا کوچک، مشتق ≈ 0 می‌شود. در backprop، gradient ضرب در ضرب این مشتقات کوچک، در لایه‌های عمیق‌تر تقریباً صفر می‌شود. شبکه یاد نمی‌گیرد.
- **ReLU راه‌حل:** مشتق در ناحیه فعال همیشه 1 است. Gradient پیچیده‌ای به لایه‌های پایین‌تر منتقل می‌شود.
- **سرعت محاسبه:** `max(0,z)` بسیار سریع‌تر از `1/(1+e⁻ᶻ)` است.

> **Pitfall:** ReLU برای z<0 مشتق صفر دارد → اگر بیشتر نورون‌ها «خاموش» شوند (همیشه z<0)، به پدیده **Dying ReLU** می‌رسیم. راه‌حل: Leaky ReLU یا initialization درست.

### لایه Dense (Fully Connected)

در یک لایه با `nₗ` واحد:

```
Z[l] = W[l] · A[l-1] + b[l]    ← ابعاد: (nₗ × nₗ₋₁) · (nₗ₋₁ × m) = (nₗ × m)
A[l] = g(Z[l])                  ← element-wise activation
```

تمام نورون‌ها ورودی یکسانی می‌گیرند → «fully connected» یا «dense». شبکه‌های MLP فقط از این لایه‌ها ساخته می‌شوند.

---

## ۲. یادگیری نظارت‌شده با شبکه‌های عصبی

### Supervised Learning چیست؟

مدل روی جفت‌های `(x, y)` آموزش می‌بیند، هدف یادگیری `f: x → y` است. برخلاف unsupervised که فقط `x` داریم و دنبال ساختار پنهان هستیم.

### انتخاب معماری بر اساس نوع داده

| نوع داده | معماری مناسب | مثال صنعتی |
|---|---|---|
| **Tabular / Structured** | Standard NN / MLP | قیمت‌گذاری، fraud detection |
| **Image / Spatial** | CNN | بینایی ماشین، بازرسی صنعتی |
| **Sequential / Time-Series** | RNN, LSTM, GRU | پیش‌بینی، NLP، سری زمانی |
| **Text / Long-range deps** | Transformer | LLM، ترجمه، summarization |

> **هشدار مهم برای داده‌های sensor/time-series صنعتی (مرتبط با کار تو):**  
> RNN/LSTM **default بد** برای همه time-series نیست. در عمل:
> - **TCN (Temporal Convolutional Network):** اغلب سریع‌تر، parallelizable، در بسیاری datasets بهتر از LSTM
> - **Transformer:** برای long-range dependency عالی است اما hungry memory و data است
> - **MLP ساده روی features:** برای anomaly detection با feature engineering کافی اغلب baseline قوی‌ای می‌دهد
> 
> توصیه: همیشه baseline ساده را اول بزن، بعد پیچیده‌تر کن.

### Structured vs Unstructured Data

- **Structured:** columns مشخص، معنای هر feature معلوم است (sensor readings, transactions)
- **Unstructured:** pixels، waveforms، tokens — معنا از ساختار خام استخراج می‌شود

Deep Learning در **unstructured data** جهش بزرگ‌تری داشته، اما امروز در structured هم state-of-the-art است (XGBoost هنوز رقیب جدی است).

### Notation استاندارد

| نماد | معنا |
|---|---|
| `m` | تعداد examples در dataset |
| `nₓ` | تعداد features |
| `X` | ماتریس ورودی — shape: `(nₓ, m)` |
| `Y` | ماتریس خروجی — shape: `(1, m)` |
| `[l]` | لایه l ام |
| `(i)` | example i ام |

> **چرا X با shape `(nₓ, m)` و نه `(m, nₓ)`؟**  
> با این convention، هر ستون یک example است. ضرب ماتریسی `W·X` مستقیم کار می‌کند و vectorize کردن آسان‌تر است.

---

## ۳. چرا Deep Learning جهش کرد؟

### سه عامل اصلی

```
        Scale of Data
            ↑
            |     ← Deep Learning
            |   /
            |  /
            | /  ← Traditional ML
            |/____________
               Data Volume
```

1. **داده (Data):** Labeled data در مقیاس میلیونی (ImageNet, Common Crawl, ...). شبکه‌های کوچک با داده بیشتر بهتر نمی‌شوند؛ شبکه‌های بزرگ می‌شوند.

2. **قدرت محاسباتی (Compute):** GPU با هزاران هسته موازی → matrix multiplication در مقیاس بزرگ ممکن شد. بدون GPU، یک training run هفته‌ها طول می‌کشید.

3. **الگوریتم‌های بهتر (Algorithms):** 
   - جایگزینی Sigmoid با ReLU: gradient پایدارتر، training سریع‌تر
   - Batch Normalization، Dropout، Adam optimizer، بهتر شدن initialization
   - هر بهبود الگوریتمی → **چرخه آزمایش سریع‌تر** → ایده بیشتر در زمان کمتر

### چرخه آزمایش (Iteration Cycle)

```
Idea → Code → Experiment → Result → Idea → ...
```

سرعت این چرخه مستقیماً به موفقیت تیم‌های deep learning ربط دارد. این دلیل محبوبیت PyTorch (iteration سریع‌تر از TensorFlow 1.x) بود.

### Vanishing Gradient و Sigmoid

سیگموید در نواحی اشباع (z بسیار بزرگ یا کوچک):

```
d/dz σ(z) = σ(z) · (1 − σ(z)) ≈ 0
```

در backprop، gradient هر لایه در مشتق activation ضرب می‌شود. با n لایه و مشتق ≈ 0.01، gradient در لایه اول ≈ `0.01ⁿ` می‌شود — عملاً صفر. **این سیگموید را برای hidden layers عمیق غیرعملی می‌کند.**

---

## ۴. خلاصه ریاضی

### Forward Pass (یک لایه)

```
Z[l] = W[l] · A[l-1] + b[l]
A[l] = g[l](Z[l])
```

### Loss Function (Binary Classification)

```
L(ŷ, y) = −[y·log(ŷ) + (1−y)·log(1−ŷ)]
```

### Cost Function (روی m example)

```
J(W, b) = (1/m) · Σᵢ L(ŷ⁽ⁱ⁾, y⁽ⁱ⁾)
```

### Gradient Descent Update

```
W := W − α · ∂J/∂W
b := b − α · ∂J/∂b
```

- `α`: learning rate (hyperparameter)

---

## ۵. Pitfalls رایج

| Pitfall | توضیح | راه‌حل |
|---|---|---|
| **Stacking linear layers** | چند لایه بدون activation = یک لایه linear | همیشه activation اضافه کن |
| **Sigmoid در hidden layers** | Vanishing gradient در شبکه‌های عمیق | ReLU را default بگذار |
| **Dying ReLU** | اگر bias اشتباه init شود، نورون‌ها همیشه خاموش می‌مانند | Leaky ReLU یا He initialization |
| **RNN برای همه time-series** | LSTM همیشه بهتر از TCN یا Transformer نیست | Benchmark هر سه |
| **فراموش کردن notation** | X با shape (m, nₓ) → باگ‌های سخت در matrix mult | X باید shape (nₓ, m) باشد |

---

## ۶. Flashcards — W1

```
Q: یک نورون مصنوعی ساده چه دو مرحله‌ای دارد؟
A: z = w·x + b (ترکیب خطی) و a = g(z) (اعمال activation)

Q: چرا چند لایه linear بدون activation بی‌فایده است؟
A: ترکیب چند نگاشت linear یک نگاشت linear است؛ depth بدون activation قدرت نمایش اضافه نمی‌کند.

Q: چرا ReLU برای hidden layers بهتر از Sigmoid است؟
A: مشتق ReLU در ناحیه فعال = 1، gradient ثابت. Sigmoid در نواحی اشباع مشتق ≈ 0 دارد → vanishing gradient.

Q: برای داده‌های تصویری چه معماری مناسب است و چرا؟
A: CNN — چون کانولوشن weight sharing و spatial invariance دارد؛ MLP هر pixel را مستقل می‌بیند.

Q: سه عامل اصلی رشد Deep Learning چیست؟
A: داده بیشتر، قدرت محاسباتی (GPU)، و الگوریتم‌های بهتر (مثلاً ReLU جای Sigmoid).

Q: در notation استاندارد Coursera، shape ماتریس X چیست؟
A: (nₓ, m) — نه (m, nₓ). هر ستون یک training example است.

Q: Vanishing Gradient چیست و چه زمانی رخ می‌دهد؟
A: وقتی مشتق activation در نواحی اشباع ≈ 0 باشد و در backprop gradient به تقریباً صفر تبدیل شود. در Sigmoid/Tanh با شبکه‌های عمیق.

Q: تفاوت Supervised و Unsupervised Learning چیست؟
A: Supervised از جفت (x,y) یاد می‌گیرد؛ Unsupervised فقط x دارد و ساختار پنهان پیدا می‌کند.

Q: چرا X shape (nₓ, m) دارد نه (m, nₓ)؟
A: با این convention ضرب W·X مستقیم کار می‌کند و vectorization راحت‌تر است.

Q: Dying ReLU چیست؟
A: وقتی نورون‌های ReLU همیشه z<0 داشته باشند، مشتق همیشه 0 است و نورون هرگز یاد نمی‌گیرد.
```

---

## منابع

- Andrew Ng, "Neural Networks and Deep Learning", Coursera (deeplearning.ai), Week 1
- Goodfellow et al., *Deep Learning*, MIT Press, 2016 — Chapters 6 (MLP), 8 (Optimization)
- Mueller & Massaron, *Deep Learning for Dummies*, Wiley — Chapter 5 (Activation Functions)
- Howard & Gugger, *Deep Learning Cookbook* — Fully Connected Layer section
