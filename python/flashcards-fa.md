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

---

## فصل ۳: دیکشنری‌ها، مجموعه‌ها و ساختارهای نگاشت

Q: چطور یک دیکشنری با مقدار پیش‌فرض برای کلیدهای缺失 بسازیم؟
A: `d.get("key", "default")` — مقدار پیش‌فرض برمی‌گردونه بدون KeyError. برای پیش‌فرض خودکار: `collections.defaultdict(list)`.

Q: فرق `d.get(k)` و `d.setdefault(k, default)` چیه؟
A: `get` مقدار پیش‌فرض برمی‌گردونه ولی دیکشنری رو تغییر نمی‌ده. `setdefault` اگه کلید نباشه مقدار پیش‌فرض رو اضافه می‌کنه و برمی‌گردونه. `setdefault` همیشه آرگومان پیش‌فرض رو ارزیابی می‌کنه (lazy نیست).

Q: `defaultdict` چطور کار می‌کنه؟
A: یک تابع factory می‌گیره. وقتی کلید缺失 با `d[key]` صدا زده بشه، factory صدا زده می‌شه تا مقدار پیش‌فرض رو تولید کنه: `defaultdict(list)` لیست خالی، `defaultdict(int)` صفر.

Q: `collections.Counter` چیه؟
A: زیرکلاس dict برای شمارش اشیاء hashable. `c = Counter("abracadabra")` → تعداد هر کاراکتر. متدهای `most_common(n)`، جمع و تفریق (`+`, `-`, `&`, `|`) و `elements()`.

Q: چطور دو دیکشنری رو ادغام کنیم (Python 3.9+)؟
A: `merged = d1 | d2` (دیکشنری جدید). `d1 |= d2` (درجا). کلیدهای تکراری از دیکشنری سمت راست برنده می‌شوند.

Q: هوک `__missing__` چیه؟
A: متدی روی زیرکلاس dict که وقتی `d[key]` KeyError می‌ده صدا زده می‌شه. برای مدیریت کلیدهای缺失: `class AutoDict(dict): def __missing__(self, k): return 0`.

Q: `collections.OrderedDict` چه کاربردی داره وقتی خود dict مرتب هست؟
A: `move_to_end(key)` و مقایسه برابری حساس به ترتیب. در غیر این صورت dict معمولی (3.7+) کافیه.

Q: `collections.ChainMap` چیه؟
A: چند دیکشنری رو یکجا به صورت یک نمای واحد نشون می‌ده. جستجو به ترتیب دیکشنری‌ها انجام می‌شه. تغییرات فقط روی دیکشنری اول اعمال می‌شه. مناسب برای لایه‌بندی کانفیگ.

Q: چه نوع‌هایی در پایتون hashable هستند؟
A: انواع immutable: int, float, str, bytes, tuple (اگه همه عناصر hashable باشند)، frozenset. انواع mutable (list, set, dict) hashable نیستند. اشیاء کاربر به طور پیش‌فرض hashable هستند (بر اساس id).

Q: پیچیدگی زمانی `key in dict` vs `key in list`؟
A: `key in dict` — O(1) میانگین (hash table). `key in list` — O(n) (جستجوی خطی). برای بررسی عضویت مجموعه‌های بزرگ از set/dict استفاده کن.

Q: فرق `set` و `frozenset` چیه؟
A: `set` mutable است (add/remove/discard/update). `frozenset` immutable و hashable است — می‌تونه به عنوان کلید دیکشنری یا داخل set دیگه استفاده بشه.

Q: عملیات set: union vs intersection vs difference؟
A: `a | b` — union (همه عناصر). `a & b` — intersection (مشترک‌ها). `a - b` — difference (در a که در b نیست). `a ^ b` — symmetric diff (در یکی، نه هر دو).

Q: چطور بررسی کنیم a زیرمجموعه b هست؟
A: `a <= b` یا `a.issubset(b)`. برای زیرمجموعه strict: `a < b`.

Q: `MappingProxyType` چیه؟
A: یک dict رو به صورت فقط‌خواندنی می‌پیچه. `MappingProxyType({"key": "val"})` — از تغییر جلوگیری می‌کنه. مناسب برای نمایش دیکشنری‌های داخلی به عنوان API.

Q: خطر استفاده از شیء mutable به عنوان کلید دیکشنری؟
A: اگه شیء بعد از درج تغییر کنه، hash آن عوض می‌شه. دیکشنری دیگه نمی‌تونه پیدا کنه (KeyError)، و ورودی قدیمی به عنوان زباله باقی می‌مونه.

Q: چطور یک دیکشنری رو invert کنیم (جابجایی کلید و مقدار)؟
A: `{v: k for k, v in d.items()}`. اگه مقادیر یکتا نباشند، کلیدهای بعدی قبلی رو بازنویسی می‌کنند — برای جمع‌آوری از `defaultdict(list)` استفاده کن.

Q: چطور آیتم‌ها رو از یک لیست تاپل با دیکشنری group کنیم؟
A: `defaultdict(list)` — `groups[lang].append(name)`. گروه‌بندی افراد بر اساس زبان، فایل‌ها بر اساس پسوند و غیره.

Q: `Counter("abracadabra").most_common(3)` چی برمی‌گردونه؟
A: `[("a", 5), ("b", 2), ("r", 2)]` — ۳ عنصر پرتکرار با تعداد.

Q: فرق `set.discard` و `set.remove` چیه؟
A: `remove(x)` اگه x نباشه KeyError می‌ده. `discard(x)` اگه x نباشه هیچ کاری نمی‌کنه (خطا نمی‌ده).

Q: پایتون چطور برخورد hash collision در dict را مدیریت می‌کنه؟
A: Open addressing — اسلات‌های بعدی رو تا پیدا شدن اسلات خالی بررسی می‌کنه. وقتی load factor از حدود ۲/۳ بیشتر بشه، جدول بزرگتر می‌شه.

Q: فرق `UserDict` و زیرکلاس مستقیم `dict` چیه؟
A: `UserDict` با `self.data` کار می‌کنه — `update()` و `__init__()` از overrideهای شما عبور می‌کنن. زیرکلاس `dict` بعضی متدها رو bypass می‌کنه. `UserDict` امن‌تره.

Q: `collections.abc.Mapping` و `MutableMapping` چی هستند؟
A: ABC برای کلاس‌های dict-like. با پیاده‌سازی ۶ متد core، ۲۰+ متد رایگان می‌گیرید (keys, values, items, get, pop, update, clear).

Q: آیا `dict.keys()` و `dict.items()` از عملیات set پشتیبانی می‌کنن؟
A: بله — `KeysView` و `ItemsView` پروتکل `Set` را پیاده‌سازی می‌کنن. `d1.keys() & d2.keys()` → کلیدهای مشترک. `d1.items() ^ d2.items()` → آیتم‌های تغییرکرده. `d.values()` پشتیبانی نمی‌کنه.

Q: چطور کلید با min/max مقدار رو در دیکشنری پیدا کنیم؟
A: `min(prices, key=prices.get)` — از `dict.get` به عنوان تابع key استفاده می‌کنه. برای مرتب‌سازی: `sorted(prices, key=prices.get)`.

Q: چطور یک لیست رو بدون به‌هم‌ریختن ترتیب dedup کنیم؟
A: `list(dict.fromkeys(items))` — دیکشنری (3.7+) ترتیب درج رو حفظ می‌کنه. برای آیتم‌های غیر hashable از generator با set استفاده کن.

---

## فصل ۴: رشته‌ها، بایت‌ها و پردازش متن

Q: فرق `str`، `bytes` و `bytearray` چیه؟
A: `str` — کد پوینت‌های یونیکد، immutable. `bytes` — دنباله immutable از اعداد ۰ تا ۲۵۵. `bytearray` — بایت mutable. `b"AB"[0]` → `65` (int)؛ `"AB"[0]` → `"A"`.

Q: چطور بین `str` و `bytes` تبدیل انجام بدیم؟
A: `s.encode("utf-8")` → بایت (در مرز I/O). `b.decode("utf-8")` → رشته. هیچ‌وقت با `+` یا `==` ترکیبشون نکن — `TypeError`.

Q: وقتی `"é".encode("ascii")` چی می‌شه؟
A: `UnicodeEncodeError` — é در ASCII نیست. از `errors="replace"`، `"ignore"` یا `"backslashreplace"` استفاده کن. برای decode: `b.decode("utf-8", errors="replace")` کاراکتر � جایگزین می‌کنه.

Q: کد پوینت چیه و `ord()`/`chr()` چطور کار می‌کنن؟
A: کد پوینت = عدد صحیح شناسایی یک کاراکتر یونیکد. `ord("A")` → ۶۵، `chr(65)` → `"A"`. طول بایت کد پوینت به encoding بستگی داره — "é" در UTF-8 دو بایت، در UTF-16 دو بایت، در UTF-32 چهار بایت.

Q: فرق UTF-8 و UTF-16 چیه؟
A: UTF-8: ۱ تا ۴ بایت، سازگار با ASCII، استاندارد وب. UTF-16: ۲ تا ۴ بایت، نیاز به BOM برای تشخیص byte order، قدیمی. UTF-32: ثابت ۴ بایت، پرهزینه.

Q: چرا `"café" == "café"` برابر False هست و چطور حلش کنیم؟
A: متن یکسان ولی کد پوینت‌های متفاوت (é آماده vs e + اکسنت ترکیبی). راه‌حل: `unicodedata.normalize("NFC", s)` — به شکل ترکیبی نرمال می‌کنه. `NFD` تجزیه می‌کنه.

Q: کی به جای `lower()` از `casefold()` استفاده کنیم؟
A: برای مقایسه بدون حساسیت به حروف بزرگ/کوچک. `casefold()` ß آلمانی رو هم هندل می‌کنه: `"Straße".casefold() == "strasse".casefold()` → True ولی `lower()` → False.

Q: چطور اکسنت‌ها رو از متن حذف کنیم؟
A: `unicodedata.normalize("NFD", s)` و بعد فیلتر `unicodedata.combining(c)`: `"".join(c for c in NFD(s) if not combining(c))`.

Q: چطور رشته رو بر اساس whitespace یا جداکننده دقیق split کنیم؟
A: `s.split()` — روی هر run از whitespace، فشرده می‌کنه. `s.split(",")` — جداکننده دقیق. `s.split(",", maxsplit=1)` — محدود. `rsplit` — از راست.

Q: خطر `str.strip(chars)` چیه؟
A: هر کاراکتری از مجموعه رو حذف می‌کنه، نه یک رشته literal — `"http://".strip("/")` همه `/`های دو سر رو حذف می‌کنه. برای پسوند literal از `removesuffix()` (Python 3.9+) استفاده کن.

Q: فرق `re.match` و `re.search` چیه؟
A: `match` فقط ابتدای رشته؛ `search` همه‌جا جستجو می‌کنه. بیشتر مواقع از `search` (یا `fullmatch` برای کل رشته) استفاده کن.

Q: چطور گروه‌ها رو با regex بگیریم؟
A: `(...)` گروه می‌سازه. `re.findall(r"#(\d+)", text)` محتوای گروه رو برمی‌گردونه. `(?P<name>...)` گروه نام‌دار → `m.group("name")` / `m.groupdict()`. `(?:...)` غیرکپچرینگه.

Q: جایگزینی regex با backreference؟
A: `re.sub(r"(\w+) (\w+)", r"\2 \1", "hello world")` → "world hello". در رشته جایگزین از `\1`، `\2` استفاده کن.

Q: کی از `re.escape` استفاده کنیم؟
A: وقتی regex از ورودی کاربر/لیترال می‌سازیم: `re.escape("a.b*c")` → `a\.b\*c` — کاراکترهای خاص literal در نظر گرفته می‌شن.

Q: روش درست باز کردن فایل متنی با encoding؟
A: `open("data.txt", encoding="utf-8")` — همیشه `encoding=` رو صریح بده (به locale اعتماد نکن). باینری: `"rb"`/`"wb"`. برای داده آلوده: `errors="replace"`.

Q: چرا باید بایت‌ها رو در مرز I/O decode کنیم؟
A: به محض ورود بایت‌ها به برنامه (شبکه، فایل) decode کن و درست قبل از خروج encode کن. منطق برنامه باید در `str` بمونه.

Q: چطور چند whitespace رو به یکی تبدیل کنیم؟
A: `" ".join(s.split())` — `split()` هر run whitespace رو فشرده می‌کنه، `join` با تک‌فاصله بازسازی می‌کنه.

---

## فصل ۵: توابع، اسکوپ و Closure

Q: مشکل default آرگومان mutable چیه؟
A: default ها فقط یک بار در زمان تعریف تابع ساخته می‌شن — `def f(x, lst=[])` همون لیست رو بین همه فراخوانی‌ها مشترک می‌کنه. راه‌حل: `def f(x, lst=None): lst = [] if lst is None else lst`.

Q: `*args` و `**kwargs` چی جمع می‌کنن؟
A: `*args` → تاپل از آرگومان‌های اضافی positional. `**kwargs` → دیکت از آرگومان‌های keyword اضافی. برعکس: `f(*[1,2,3])` لیست رو به positional باز می‌کنه، `f(**{"a":1})` دیکت رو به keyword.

Q: چطور پارامترهای keyword-only یا positional-only بسازیم؟
A: `def f(a, b, *, c)` — `*` یعنی هرچی بعدشه فقط keyword. `def f(a, b, /)` — `/` یعنی هرچی قبلشه فقط positional (Python 3.8+).

Q: قانون LEGB چیه؟
A: ترتیب حل نام: Local → Enclosing → Global → Built-in. انتساب داخل تابع اسم رو local می‌کنه؛ خواندن به بیرون برمی‌گرده.

Q: `nonlocal` با `global` چه فرقی داره؟
A: `nonlocal` نامی از اسکوپ تابع بیرونی رو بازتعریف می‌کنه (برای تغییر متغیر گرفته‌شده در closure لازمه). `global` نام ماژولی رو تغییر می‌ده. وقتی ممکنه هیچ‌کدوم رو استفاده نکن — مقدار برگردون.

Q: closure چیه؟
A: یک تابع به همراه متغیرهای آزادی که از اسکوپ بیرونی می‌گیره و بعد از برگشتن تابع بیرونی زنده می‌مونن. `make_counter()` که `counter()` برمی‌گردونه و `count` خودش رو نگه می‌داره.

Q: gotcha اتصال دیرهنگام در حلقه چیه؟
A: lambda/closure متغیر رو می‌گیره نه مقدارش رو: `[lambda: i for i in range(3)]` همه ۲ برمی‌گردونن. راه‌حل: binding به عنوان default `lambda i=i: i`.

Q: چرا `x = 10` بعد از `print(x)` داخل تابع UnboundLocalError می‌ده؟
A: انتساب بعدی `x` رو برای کل تابع local می‌کنه — اسکوپ در زمان کامپایل تصمیم گرفته می‌شه. استفاده از `global x`.

Q: `functools.partial` چیه؟
A: بخشی از آرگومان‌ها رو ثابت می‌کنه: `partial(pow, 2)` → تابعی که فقط یک آرگومان (توان) می‌گیره و پایه ۲ رو همیشه استفاده می‌کنه.

Q: `map`/`filter` در پایتون ۳ چی برمی‌گردونن؟
A: iterator تنبل، نه لیست — برای پر کردن لیست `list(map(f, xs))` و `list(filter(pred, xs))`. برای مرتب‌سازی از `sorted(xs, key=fn)` استفاده کن.

Q: توابع درجه اول (first-class) در پایتون چیه؟
A: توابع object هستن: قابل انتساب (`g = f`)، قابل ارسال (`apply(f, x)`)، قابل برگردوندن (`make_adder(5)` یه closure می‌ده)، قابل ذخیره در لیست/دیکت.

Q: حد بازگشت چقدره و چرا مهمه؟
A: حدود ۱۰۰۰ (`sys.getrecursionlimit()`). بیشتر از اون `RecursionError` می‌ده. همیشه base case داشته باش؛ برای بازگشت عمیق از iteration استفاده کن.
