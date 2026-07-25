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
