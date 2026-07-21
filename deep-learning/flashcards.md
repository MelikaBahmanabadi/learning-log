# Flashcards

<!-- Cards in Anki format: Question? ; Answer -->

---

## W1 — What is a Neural Network?

ReLU مخفف چیه و فرمولش چیه؟ ; Rectified Linear Unit — max(0, z). اگه ورودی منفی باشه صفر، وگرنه خودش.

چرا بدون non-linearity، stack کردن چند لایه بی‌فایده‌ست؟ ; چون W2(W1x) = (W2W1)x = W3x — ضرب ماتریس‌ها ادغام میشن و کل شبکه معادل یه لایه‌ی خطی میشه. خطی فقط hyperplane می‌کشه، نه توابع پیچیده.

یه hidden layer با n نورون که به m ورودی densely connected باشه، چند وزن داره؟ (بدون bias) ; m × n

Dense (fully connected) layer یعنی چی؟ ; هر نورون لایه‌ی قبل به تمام نورون‌های لایه‌ی بعد وصله — شبکه آزاده هر ترکیبی از ورودی‌ها رو یاد بگیره.

چرا hidden layer به این اسم خوانده میشه؟ ; چون مقادیرش در training data برچسب مستقیم ندارن — برعکس input و output که مشخص هستن.

---

## W1 — Supervised Learning with Neural Networks

کدوم معماری برای کدوم داده؟ ; Standard NN → tabular/structured | CNN → spatial patterns (image, signal) | RNN/LSTM → sequential/temporal (audio, time-series, text) | Hybrid → complex mixed (autonomous driving)

چهار learning paradigm اصلی کدومن؟ ; Supervised (labeled), Unsupervised (no label), Semi-supervised (few labeled + many unlabeled), Reinforcement (reward signal)

تفاوت Learning Paradigm با Task Type چیه؟ ; Paradigm = نوع داده‌ی آموزشی (supervised/unsupervised/...) | Task = نوع خروجی (classification/regression/clustering/...). رگرسیون یه task هست که درون supervised قرار می‌گیره، نه یه paradigm.

چرا RNN برای time-series سنسور صنعتی بهتر از Standard NN هست؟ ; چون وابستگی زمانی دارن — قدم t به قدم t-1 مرتبطه (Markov chain). Standard NN هر ورودی رو مستقل می‌بینه.

Structured vs Unstructured data فرق اصلیشون چیه؟ ; Structured = هر feature معنی مشخص داره (جدول، سنسور با timestamp) | Unstructured = معنی از الگوهای خام استخراج میشه (تصویر، صدا، متن آزاد)

---

## W1 — Why is Deep Learning Taking Off?

[Deep Learning][Neural Networks and Deep Learning][W1-04-Why-is-Deep-Learning-taking-off] سه عامل اصلی رشد Deep Learning چیست؟ ; 1) داده‌ی بیشتر و برچسب‌دار، 2) محاسبات سریع‌تر و سخت‌افزارهایی مانند GPU، 3) نوآوری الگوریتمی و معماری.

[Deep Learning][Neural Networks and Deep Learning][W1-04-Why-is-Deep-Learning-taking-off] m در notation این دوره چه معنایی دارد؟ ; تعداد training examples؛ در supervised learning معمولاً تعداد نمونه‌های labeled که هم x و هم y دارند.

[Deep Learning][Neural Networks and Deep Learning][W1-04-Why-is-Deep-Learning-taking-off] چرا Sigmoid در شبکه‌های عمیق می‌تواند باعث vanishing gradient شود؟ ; در نواحی اشباع، مشتق Sigmoid نزدیک صفر می‌شود؛ در backpropagation ضرب پی‌درپی این گرادیان‌های کوچک، گرادیان لایه‌های ابتدایی را تقریباً صفر می‌کند.

[Deep Learning][Neural Networks and Deep Learning][W1-04-Why-is-Deep-Learning-taking-off] مشتق ReLU در چه ناحیه‌هایی صفر و یک است؟ ; برای z < 0 برابر 0 و برای z > 0 برابر 1 است؛ در z = 0 مشتق معمولاً در پیاده‌سازی با یک convention تعیین می‌شود.

[Deep Learning][Neural Networks and Deep Learning][W1-04-Why-is-Deep-Learning-taking-off] چرا سرعت محاسبات برای موفقیت Deep Learning مهم است؟ ; چرخه‌ی idea → code → experiment → result → iteration را کوتاه می‌کند، بنابراین می‌توان experiment و iteration بیشتری انجام داد و سریع‌تر به مدل مؤثر رسید.

---

## W2 — Basics of Neural Network Programming

[Deep Learning][Neural Networks and Deep Learning][W2-01-Binary-Classification]
چرا در پیاده‌سازی شبکه‌های عصبی از حلقه‌های for صریح (explicit) روی کل مجموعه آموزشی استفاده نمی‌کنیم؟ ; چون عملیات ماتریسی و برداری (vectorized) بسیار بهینه‌تر، تمیزتر و برای محاسبات سنگین شبکه عصبی سریع‌تر هستند.

[Deep Learning][Neural Networks and Deep Learning][W2-01-Binary-Classification]
یک تصویر RGB با ابعاد 64x64 چگونه به یک بردار ویژگی (feature vector) تبدیل می‌شود؟ ; با باز کردن (unrolling) تمام مقادیر پیکسلی هر سه کانال رنگی در یک بردار بلند به طول 12288 = 3 * 64 * 64.

[Deep Learning][Neural Networks and Deep Learning][W2-01-Binary-Classification]
در نمادگذاری این دوره، ماتریس X نشان‌دهنده چیست و چه ابعادی دارد؟ ; ماتریس ورودی‌ها که از چیدن ستونی نمونه‌های آموزشی ساخته شده و ابعاد آن (n_x, m) است.

[Deep Learning][Neural Networks and Deep Learning][W2-01-Binary-Classification]
در نمادگذاری این دوره، ماتریس Y نشان‌دهنده چیست و چه ابعادی دارد؟ ; ماتریس برچسب‌ها (labels) که از چیدن ستونی خروجی‌ها ساخته شده و ابعاد آن (1, m) است.

[Deep Learning][Neural Networks and Deep Learning][W2-02-Logistic-Regression] مقدار y-hat در رگرسیون لجستیک (Logistic Regression) نشان‌دهنده چیست؟ ; \(\hat{y} = P(y=1 \mid x)\)، یعنی احتمال اینکه با توجه به ویژگی‌های ورودی \(x\)، برچسب واقعی \(y\) برابر 1 باشد.

[Deep Learning][Neural Networks and Deep Learning][W2-02-Logistic-Regression] چرا در رگرسیون لجستیک به تابع فعال‌ساز سیگموئید (Sigmoid) نیاز داریم؟ ; چون تابع سیگموئید هر عدد حقیقی را به بازه \((0,1)\) می‌برد و خروجی را به یک احتمال (Probability) معتبر تبدیل می‌کند.

[Deep Learning][Neural Networks and Deep Learning][W2-02-Logistic-Regression] چرا یک خروجی خطی به فرم \(w^T x + b\) برای طبقه‌بندی دودویی (Binary Classification) مناسب نیست؟ ; چون مقادیر خروجی خطی می‌تواند منفی یا بزرگ‌تر از 1 شود که به عنوان احتمال (Probability) قابل تفسیر نیست.

[Deep Learning][Neural Networks and Deep Learning][W2-02-Logistic-Regression] تعبیر احتمالی اصلی رگرسیون لجستیک چیست؟ ; مدل سعی می‌کند احتمال شرطی \(P(y=1 \mid x)\) را تخمین بزند، یعنی شانس اینکه ورودی \(x\) متعلق به کلاس مثبت باشد.


## Needs Review
<!-- Wrong answers from periodic quizzes go here -->
