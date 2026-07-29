# Python Flashcards — FA

## فصل ۱: مبانی پایتون

Q: روش پایتونیک باز کردن فایل؟
A: `with open(path) as fh:` — مدیریت زمینه خودکار می‌بنده.

Q: EAFP vs LBYL؟
A: EAFP (مخفف Easier to Ask Forgiveness) — try/except، پایتونیک. LBYL — if.

Q: ساخت venv؟
A: `python -m venv .venv && source .venv/bin/activate`

Q: فایل تنظیمات مدرن پروژه؟
A: `pyproject.toml` (PEP 517/518/621).

Q: مقادیر falsy کدوم‌ان؟
A: `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `None`, `False`.

Q: جابجایی دو متغیر؟
A: `a, b = b, a`

Q: ایندکس + مقدار در حلقه؟
A: `for i, v in enumerate(seq):`

Q: پیمایش همزمان دو دنباله؟
A: `for a, b in zip(xs, ys):`

Q: عملگر walrus `:=` چیه؟
A: انتساب + استفاده در عبارت: `if (data := get_data()):`

Q: `sorted(items, key=lambda x: x[1])` چیکار می‌کنه؟
A: مرتب‌سازی آیتم‌ها بر اساس عنصر دوم.

Q: مشکل پارامتر پیش‌فرض mutable؟
A: `def f(lst=[])` — لیست بین فراخوانی‌ها مشترکه. از `def f(lst=None)` استفاده کن.

Q: پارامترهای positional-only؟
A: پارامترهای قبل از `/` — نمی‌تونن به صورت keyword داده بشن.

Q: پارامترهای keyword-only؟
A: پارامترهای بعد از `*` — باید به صورت keyword داده بشن.

Q: `if __name__ == "__main__"` برای چیه؟
A: اجرای کد فقط وقتی فایل مستقیم اجرا بشه، نه وقتی import بشه.

Q: نام‌گذاری توابع PEP 8؟
A: `snake_case`

Q: نام‌گذاری کلاس‌ها PEP 8؟
A: `PascalCase`

Q: قانون LEGB؟
A: Local → Enclosing → Global → Built-in — ترتیب جستجوی نام.

Q: `match/case` چیه؟ (Python 3.10+)
A: pattern matching ساختاری — `match command.split(): case ["quit"]: ...`

Q: خط‌به‌خط خوندن فایل با مصرف حافظه کم؟
A: `for line in file:` — هر بار یک خط.

Q: فرق `is` و `==`؟
A: `is` هویت (همون شیء)؛ `==` برابری مقدار.

Q: شکل list comprehension؟
A: `[x**2 for x in range(10) if x % 2 == 0]`

Q: مثال dict comprehension؟
A: `{x: x**2 for x in range(5)}`

Q: مثال set comprehension؟
A: `{x for x in range(20) if x % 2 == 0}`

Q: چطور لیست دوبعدی رو با comprehension صاف کنیم؟
A: `[x for row in matrix for x in row]`

Q: `else` در `for` حلقه چیه؟
A: اگه حلقه بدون `break` تموم بشه اجرا می‌شه.

Q: پیمایش key-value دیکشنری؟
A: `for k, v in dict.items():`

Q: f-string برای ۲ رقم اعشار؟
A: `f"{value:.2f}"`

Q: f-string برای صفر تا عرض ۴؟
A: `f"{value:04d}"`

Q: pathlib: چطور مسیرها رو join کنیم؟
A: `Path("folder") / "sub" / "file.txt"`

Q: کپی لیست؟
A: `new_list = old_list.copy()` یا `new_list = old_list[:]`

Q: عملگر تفاضل set؟
A: `a - b`

Q: عملگر ادغام دیکشنری (Python 3.9+)؟
A: `dict1 | dict2`

Q: دسترسی امن به کلید دیکشنری با مقدار پیش‌فرض؟
A: `dict.get("key", "default")`

---

## فصل ۲: دنباله‌ها، لیست‌ها، تاپل‌ها و Slicing

Q: فرق `list` و `tuple` چیه؟
A: لیست mutable، تاپل immutable. تاپل حافظه کمتری مصرف می‌کنه، می‌تونه کلید دیکشنری بشه، و یک record ثابت رو نمایش می‌ده. لیست برای append کارآمد over-allocation داره.

Q: Slicing با `[start:stop:step]` چطور کار می‌کنه؟
A: start = ایندکس شروع (شامل)، stop = ایندکس پایان (غیرشامل)، step = گام. step منفی جهت را برعکس می‌کنه. هر سه اختیاری‌اند.

Q: `seq[::-1]` چیکار می‌کنه؟
A: دنباله رو برعکس می‌کنه — step منفی با حذف start/stop کل دنباله رو برعکس می‌پیماید.

Q: چطور به یک slice مقدار نسبت بدیم؟
A: `list[2:5] = [100, 200]` — آیتم‌های ۲ تا ۵ را با مقادیر جدید جایگزین می‌کنه. طول لیست می‌تونه تغییر کنه. در step-slice طول باید دقیقاً برابر باشه.

Q: چطور با استفاده از slice در موقعیت i به لیست اضافه کنیم؟
A: `list[i:i] = [item]` — در ایندکس i بدون حذف چیزی درج می‌کنه.

Q: شیء slice چیه؟
A: `slice(start, stop, step)` — به طور ضمنی توسط `seq[1:5:2]` ساخته می‌شه. می‌شه نام‌گذاری و استفاده مجدد کرد: `s = slice(1, 5, 2); seq[s]`.

Q: پیچیدگی زمانی `list.append()` چقدره؟
A: O(1) amortized — لیست بیش از نیاز فضا تخصیص می‌ده، پس اکثر appendها نیاز به تخصیص مجدد ندارند.

Q: پیچیدگی زمانی `list.pop(0)` چقدره؟
A: O(n) — همه عناصر باقی‌مانده به چپ منتقل می‌شوند. از `collections.deque.popleft()` برای O(1) استفاده کن.

Q: `namedtuple` چیه؟
A: `namedtuple("Point", ["x", "y"])` یک زیرکلاس از tuple با فیلدهای نام‌دار می‌سازه. دسترسی با نام (`p.x`) یا ایندکس (`p[0]`). Immutable، hashable، کم‌مصرف.

Q: کی از `array.array` به جای `list` استفاده کنیم؟
A: برای داده‌های عددی همگن بزرگ — کم‌مصرف، type-safe، I/O باینری سریع. لیست برای داده‌های ناهمگن یا ترکیبی.

Q: `collections.deque` چه مزیتی نسبت به `list` داره؟
A: O(1) `append`/`popleft` در هر دو سمت. لیست O(n) `pop(0)` داره. deque ایده‌آل برای صف‌ها، sliding windowها، و بافر محدود (`maxlen`).

Q: `bisect.insort` چطور کار می‌کنه؟
A: محل درج رو با جستجوی دودویی پیدا می‌کنه (O(log n))، سپس درج می‌کنه (O(n) شیفت). لیست را مرتب نگه می‌دارد.

Q: فرق `bisect.bisect_left` و `bisect.bisect` چیه؟
A: `bisect_left` چپ‌ترین محل درج (قبل از مقادیر مساوی موجود) را برمی‌گردونه. `bisect` راست‌ترین (بعد از مقادیر مساوی) را.

Q: چطور یک deque محدود بسازیم که آیتم‌های قدیمی رو حذف کنه؟
A: `deque(maxlen=5)` — وقتی پر شد، append جدید آیتم سمت مخالف رو حذف می‌کنه.

Q: پروتکل sequence چیه؟
A: پیاده‌سازی `__len__` و `__getitem__` — به هر کلاسی امکان slicing، iteration، `in` و `reversed()` می‌ده.

Q: `struct.pack` برای چیه؟
A: بسته‌بندی مقادیر پایتون به بایت‌های باینری بر اساس یک فرمت: `struct.pack('>i4sh', 7, b'spam', 8)`.

Q: `memoryview` برای چیه؟
A: دسترسی zero-copy به بافر یک شیء — مشاهده و تغییر بایت‌ها بدون کپی کردن داده.

Q: نحو tuple packing و unpacking چطوریه؟
A: Packing: `t = 1, 2, 3` → تاپل `(1, 2, 3)`. Unpacking: `a, b, c = t` → متغیرهای جدا.

Q: مقایسه named tuples با تاپل معمولی برای سریالایز؟
A: Named tuples متد `._asdict()` برای تبدیل به دیکشنری دارند. همان حافظه تاپل معمولی.

Q: اگه به یک عنصر tuple مقدار بدیم چی می‌شه؟
A: `TypeError` — تاپل immutable است. اما اگر تاپل شامل یک شیء mutable باشه، اون شیء می‌تونه تغییر کنه.

Q: چطور یک لیست رو درجا برعکس کنیم  vs  کپی برعکس بسازیم؟
A: `list.reverse()` درجا برعکس می‌کنه (None برمی‌گردونه). `reversed(seq)` یک iterator برمی‌گردونه. `seq[::-1]` یک لیست برعکس جدید می‌سازه.

Q: `seq[::2]` چی برمی‌گردونه؟
A: هر عنصر دوم دنباله.

Q: چطور یک دنباله رو در یک نقطه تقسیم کنیم؟
A: `head, tail = seq[:i], seq[i:]`

Q: `Ellipsis` (`...`) در پایتون برای چیه؟
A: در کانتینرهای سفارشی و NumPy: `arr[..., 0]` یعنی "همه ابعاد قبلی، سپس ستون ۰".

Q: فرق دنباله‌های container و flat چیه؟
A: دنباله‌های container (list, tuple, deque) reference نگه می‌دارند = می‌تونند انواع مختلف داشته باشند. دنباله‌های flat (str, bytes, array) مقادیر را مستقیم ذخیره می‌کنند = کم‌مصرف، یک نوع.

Q: کی از `collections.deque` برای صف استفاده کنیم؟
A: صف FIFO — `deque` با O(1) `popleft`. لیست با O(n) `pop(0)`. برای صف thread-safe از `queue.Queue` استفاده کن.

Q: الگوی rolling window با zip چطوریه؟
A: `list(zip(*(seq[i:] for i in range(n))))` — تاپل‌هایی به طول n که روی دنباله می‌لغزند.
