# Web Scraping Flashcards — FA (فارسی)

فرمت: `Q | A | زیرموضوع | تایر | New/Known/Needs Review | آخرین تست`

---

## T0 · http-semantics

س: تفاوت اصلی GET و POST در لایه‌ی سیم (wire) چیست؟  
ج: GET بدنه ندارد؛ پارامترها در query string می‌روند. POST بدنه دارد (JSON، فرم، multipart). تغییر state سرور فقط با POST انتظار می‌رود.  
`زیرموضوع: http-semantics | T0 | New | —`

س: یک scraper دقیقاً چه چیزی دریافت می‌کند — صفحه‌ی رندرشده یا پاسخ خام؟  
ج: بایت‌های خام HTTP response — قبل از اینکه هیچ JavaScript اجرا شود. DOM رندرشده فقط در مرورگر وجود دارد.  
`زیرموضوع: http-semantics | T0 | New | —`

س: کد 429 چه معنایی دارد و scraper باید چه کار کند؟  
ج: Too Many Requests. باید هدر Retry-After را بخواند و دقیقاً آن چند ثانیه صبر کند. هرگز بلافاصله retry نکند.  
`زیرموضوع: http-semantics | T0 | New | —`

س: چرا هرگز نباید requests را بدون timeout در production استفاده کرد؟  
ج: سرور کند یا معلق، thread/coroutine را برای همیشه نگه می‌دارد و pool را خفه می‌کند. همیشه `timeout=(connect_s, read_s)` بدهید.  
`زیرموضوع: http-semantics | T0 | New | —`

س: Content negotiation چیست و چطور به scraping کمک می‌کند؟  
ج: سرور فرمت response را بر اساس هدر Accept انتخاب می‌کند. ارسال `Accept: application/json` ممکن است JSON به‌جای HTML برگرداند — parse ارزان‌تر.  
`زیرموضوع: http-semantics | T0 | New | —`

---

## T0 · redirects-cookies

س: cookie jar چیست و چرا scraper باید آن را نگه دارد؟  
ج: هویت session سمت سرور در cookie ذخیره می‌شود. بدون نگه داشتن cookie بین درخواست‌ها، هر request به‌عنوان بازدیدکننده‌ی جدید ناشناس تلقی می‌شود.  
`زیرموضوع: redirects-cookies | T0 | New | —`

س: تفاوت 301 و 302 برای یک crawler چیست؟  
ج: 301 دائمی است — client می‌تواند URL اصلی را برای همیشه کنار بگذارد. 302 موقتی است — دفعه‌ی بعد URL اصلی را دوباره چک کن.  
`زیرموضوع: redirects-cookies | T0 | New | —`

---

## T0 · encodings

س: encoding یک HTTP response را چطور به درستی تشخیص می‌دهید؟  
ج: اول هدر Content-Type را بررسی کن (`charset=utf-8`). بعد `<meta charset>` در HTML. هرگز بدون دلیل UTF-8 فرض نکن.  
`زیرموضوع: encodings | T0 | New | —`

---

## T0 · url-normalization

س: چرا قبل از deduplication در crawl frontier باید URL را normalize کنید؟  
ج: `http://example.com/page`، `http://example.com/page?` و `HTTP://EXAMPLE.COM/page` همه یک resource هستند. بدون normalization یک صفحه چندین بار crawl می‌شود.  
`زیرموضوع: url-normalization | T0 | New | —`

---

## T0 · robots-sitemaps

س: sitemap.xml چیست و چرا قبل از crawl باید آن را بررسی کرد؟  
ج: فایل XML با تمام URL‌های canonical سایت. استفاده از آن یعنی discovery crawling اصلاً لازم نیست — سریع‌تر، کامل‌تر، و از honeypot trap در امان.  
`زیرموضوع: robots-sitemaps | T0 | New | —`

---

## T1 · httpx-client

س: چرا برای scraping های I/O-bound باید از httpx.AsyncClient به‌جای requests.Session استفاده کرد؟  
ج: requests سنکرون است — یک read مسدود کل thread را می‌گیرد. httpx.AsyncClient با asyncio صدها درخواست همزمان را در یک thread اجرا می‌کند.  
`زیرموضوع: httpx-client | T1 | New | —`

س: connection pooling چیست و در مقیاس چقدر اهمیت دارد؟  
ج: استفاده‌ی مجدد از اتصال‌های TCP+TLS باز بین درخواست‌ها — از handshake مجدد (~100-300ms) جلوگیری می‌کند. httpx.AsyncClient وقتی به‌صورت context manager باز بماند به‌صورت پیش‌فرض pool می‌کند.  
`زیرموضوع: httpx-client | T1 | New | —`

---

## T1 · selectors

س: چه زمانی CSS selector بر XPath ارجحیت دارد؟  
ج: CSS برای هدف‌گیری class/id/attribute در HTML — syntax کوتاه‌تر، native مرورگر. XPath وقتی به text() matching، محور parent، یا predicates موقعیت node نیاز دارید.  
`زیرموضوع: selectors | T1 | New | —`

س: چرا nth-child و class names تولیدشده selector های شکننده‌ای هستند؟  
ج: به موقعیت DOM یا class های obfuscated وابسته‌اند که با هر deploy تغییر می‌کنند. از attribute های semantic استفاده کنید: data-testid، itemprop، aria-label.  
`زیرموضوع: selectors | T1 | New | —`

---

## T1 · extraction-contracts

س: extraction contract چیست و چرا اهمیت دارد؟  
ج: یک schema تایپ‌شده (مثلاً Pydantic model) که field های استخراج‌شده را validate می‌کند. بدون آن، field های خالی/null بی‌صدا عبور می‌کنند و storage downstream را خراب می‌کنند.  
`زیرموضوع: extraction-contracts | T1 | New | —`

---

## T1 · structured-data

س: JSON-LD چیست و چرا باید قبل از نوشتن selector آن را بررسی کنید؟  
ج: `<script type="application/ld+json">` داده‌ی ساختاریافته‌ی machine-readable (Schema.org) را embed می‌کند. Parse آن O(1) است و به تغییرات layout HTML ایمن است — همیشه اول Network tab را چک کنید.  
`زیرموضوع: structured-data | T1 | New | —`
