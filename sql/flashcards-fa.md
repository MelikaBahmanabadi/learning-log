# Flashcards — فارسی

<!-- Cards in Anki format: Question? ; Answer -->

---

## Ch 1 — ترتیب اجرای SQL

ترتیب منطقی اجرای یک query چیست؟ ; FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT. SELECT آخرین مرحله اجرا می‌شود!

چرا نمی‌توانی از alias تعریف‌شده در SELECT در WHERE استفاده کرد؟ ; چون WHERE قبل از SELECT ارزیابی می‌شود. آن alias هنوز وجود ندارد. باید عبارت را تکرار کنی یا از subquery/CTE استفاده کنی.

---

## Ch 1 — انواع JOIN

تفاوت INNER JOIN، LEFT JOIN و FULL JOIN چیست؟ ; INNER = فقط سطرهای مطابق | LEFT = تمام سطرهای چپ دست + مطابق‌ها | FULL = تمام سطرهای هر دو جدول. سطرهای بی‌مطابق NULL می‌گیرند.

CROSS JOIN چیست و چه وقت استفاده می‌شود؟ ; Cartesian product — هر سطر A با هر سطر B جفت می‌شود. مثال: 10 مشتری × 3 محصول = 30 سطر. برای تولید تمام ترکیب‌ها مانند برنامه‌ریزی.

SELF JOIN چیست؟ یک مثال بزن. ; جوین کردن جدول با خودش. مثال: پیدا کردن کارمند و مدیرش: SELECT e.name, m.name FROM employees e LEFT JOIN employees m ON e.manager_id = m.id.

---

## Ch 1 — الگوریتم‌های Join

Nested Loop Join چه وقت بهترین گزینه است؟ ; وقتی ورودی خارجی کوچک باشد و index روی جدول داخلی وجود داشته باشد. هر سطر خارجی از طریق index جستجو می‌شود. هزینه: O(N × log M).

Hash Join چطور کار می‌کند؟ ; 1) از جدول کوچکتر یک hash table روی کلید join می‌سازد، 2) هر سطر جدول بزرگتر را probe می‌کند. هزینه: O(N + M). بهترین گزینه برای دو جدول بزرگ بدون index کارآمد.

Merge Join چه وقت استفاده می‌شود؟ ; وقتی هر دو ورودی قبلاً مرتب باشند (مثلاً از index). هر دو جریان موازی پیمایش داده می‌شوند. هزینه: O(N + M) در صورت مرتب بودن.

---

## Ch 1 — Correlated Subquery در مقابل JOIN

Correlated Subquery چیست؟ ; یک subquery که به query خارجی ارجاع دارد — به ازای هر سطر یک بار اجرا می‌شود. معمولاً کند مگر اینکه index روی ستون فیلتر وجود داشته باشد.

تفاوت EXISTS و IN چیست؟ ; EXISTS با اولین مطابقت short-circuit می‌کند و NULL-safe است — برای NOT EXISTS حیاتی است. IN نتیجه subquery را مادی‌سازی می‌کند؛ با NULL در لیست، NOT IN هیچ سطری برنمی‌گرداند. برای ستون‌های nullable از NOT EXISTS استفاده کن.

چرا `NOT IN (1, 2, NULL)` هیچ‌وقت چیزی برنمی‌گرداند؟ ; معادل x!=1 AND x!=2 AND x!=NULL است. x!=NULL همیشه UNKNOWN است، پس AND کلی UNKNOWN می‌شود و سطر فیلتر می‌خورد. به جایش NOT EXISTS استفاده کن.

---

## Ch 1 — سمانتیک NULL

`NULL = NULL` چه مقداری برمی‌گرداند؟ ; UNKNOWN (نه TRUE نه FALSE). پس `WHERE col = NULL` هیچ سطری برنمی‌گرداند. باید از `WHERE col IS NULL` استفاده کنی.

تفاوت COUNT(col) و COUNT(*) چیست؟ ; COUNT(col) سطرهای NULL را نادیده می‌گیرد. COUNT(*) تمام سطرها از جمله NULLها را می‌شمارد.

`NULL * 0` چند است؟ ; NULL. هر عملیات حسابی با NULL نتیجه NULL می‌دهد. حتی 0 * NULL هم NULL است.

---

## Ch 1 — UNION

تفاوت UNION و UNION ALL چیست؟ ; UNION نتیجه‌ها را ترکیب می‌کند و تکراری‌ها را حذف می‌کند (sort/hash لازم است). UNION ALL تکراری‌ها را نگه می‌دارد (سریعتر). مگر dedup واقعاً لازم باشد، UNION ALL استفاده کن.

---

## Ch 1 — SET در مقابل BAG

SQL روی Set یا Bag کار می‌کند؟ ; Bag (مالتی‌ست). جداول SQL می‌توانند سطرهای تکراری داشته باشند، اما روابط ریاضی نمی‌توانند. SELECT DISTINCT یک bag را به set تبدیل می‌کند.

---

## Ch 1 — نکات مصاحبه

چرا SELECT * در محیط production بد است؟ ; 1) داده‌ی اضافی (پهنای باند، حافظه)، 2) اگر schema تغییر کند app خراب می‌شود، 3) covering index کار نمی‌کند، 4) هدف query نامشخص است.

تفاوت DELETE، TRUNCATE و DROP چیست؟ ; DELETE = حذف سطرهای خاص (کند، triggerهای row-level فعال می‌شوند، همیشه rollbackپذیر). TRUNCATE = حذف سریع همه سطرها — triggerهای row-level فعال نمی‌شوند، اما PostgreSQL triggerهای statement-level TRUNCATE را فعال می‌کند. DROP = حذف جدول + schema.

---

## Ch 2 — اصول B-tree Index

B-tree index چیست و چه عملیاتی را پشتیبانی می‌کند؟ ; یک ساختار درختی متعادل که داده‌ها را مرتب نگه می‌دارد. جستجوی equality (O(log N))، range scan، ORDER BY و prefix matching (LIKE 'abc%') را پشتیبانی می‌کند. در بیشتر دیتابیس‌ها پیش‌فرض index است.

چرا B-tree index به `WHERE name LIKE '%Alice'` کمکی نمی‌کند؟ ; wildcard ابتدایی full scan اجباری است — index مرتب است و نمی‌توان به وسط پرید. wildcard در انتها مانند `LIKE 'Alice%'` می‌تواند index استفاده کند.

چرا `WHERE YEAR(created_at) = 2024` از index روی created_at استفاده نمی‌کند؟ ; تابع ستون ایندکس‌شده را می‌پیچد — optimizer نمی‌تواند این را به index مطابق کند. راه‌حل: `WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'` یا ساختن functional index.

---

## Ch 2 — Composite Index و Leftmost Prefix

Leftmost prefix rule در composite index چیست؟ ; یک composite index روی (a, b, c) برای query روی a، a+b یا a+b+c کار می‌کند — اما برای b، c یا b+c تنها خیر. index بر اساس a مرتب شده، پس حذف a مرتب را می‌شکند.

چرا ستون‌های equality باید قبل از ستون‌های range در composite index بیایند؟ ; equality روی ستون scan را محدود می‌کند. range سایر ستون‌ها را بلااستفاده می‌کند. مثال: index (status, created_at) برای `WHERE status='active' AND created_at > '2024-01-01'` کار می‌کند اما برعکس نه.

Covering index چیست؟ ; یک index که شامل تمام ستون‌های مورد نیاز query است، پس دیتابیس هرگز سطرهای جدول را لمس نمی‌کند. در MySQL به شکل "Using index" و در PostgreSQL به شکل "Index Only Scan" نشان داده می‌شود. I/O را به شدت کاهش می‌دهد.

---

## Ch 2 — انواع Index

تفاوت clustered و non-clustered index چیست؟ ; Clustered index ترتیب فیزیکی سطرهای داده را کنترل می‌کند — در MySQL/InnoDB و SQL Server فقط یکی به ازای هر جدول (معمولاً PK). PostgreSQL clustered index پایدار ندارد: CLUSTER یک‌بار مرتب می‌کند اما حفظ نمی‌کند. Non-clustered index یک ساختار جداگانه با pointer است — lookup نیازمند fetch اضافی از جدول است مگر covering index باشد.

Partial (filtered) index چه وقتی مناسب است؟ ; وقتی بیشتر queryها روی زیرمجموعه‌ای از سطرها هستند (مثلاً `WHERE status = 'active'`). index فقط سطرهای مطابق را ذخیره می‌کند — کوچکتر و سریعتر برای maintenance. PostgreSQL و SQL Server پشتیبانی می‌کنند.

---

## Ch 2 — خواندن EXPLAIN

ستون `type` در MySQL EXPLAIN چه می‌گوید؟ ; مسیر دسترسی، از بهترین تا بدترین: system > const > eq_ref > ref > range > index > ALL. ALL = full table scan (معمولاً بد برای جداول بزرگ با WHERE حساس).

"Using filesort" در MySQL EXPLAIN یعنی چی؟ ; دیتابیس باید یک مرحله sort اضافی انجام دهد چون ORDER BY از index نمی‌تواند استفاده کند. معمولاً علامت هشدار — indexی برای ORDER BY اضافه کن.

"Using temporary" در MySQL EXPLAIN یعنی چی؟ ; یک جدول موقت حین اجرای query ساخته شد — معمولاً برای GROUP BY، DISTINCT یا برخی الگوهای JOIN. روی دیتاست بزرگ گران می‌شود.

---

## Ch 2 — پلن اجرایی و Optimizer

Query optimizer چه تصمیماتی می‌گیرد؟ ; مسیر دسترسی (full scan در مقابل index)، ترتیب join، الگوریتم join، استراتژی aggregation و parallelism را تعیین می‌کند. مبتنی بر هزینه است — ارزان‌ترین پلن را جستجو می‌کند، نه لزوماً سریع‌ترین.

چرا query در dev سریع است اما در production کند؟ ; 1) آمار جدول فرق دارد — dev دارای 100 سطر (full scan مشکلی ندارد)، prod دارای 10M. 2) آمار کهنه — ANALYZE بزن. 3) توزیع داده فرق دارد. 4) index در prod وجود ندارد. 5) Parameter sniffing — پلن کش شده برای مقادیر دیگر بهینه نیست.

Parameter sniffing چیست؟ ; دیتابیس یک پلن بر اساس اولین مقادیر parameter کش می‌کند. اگر مقادیر بعدی توزیع خیلی متفاوتی داشته باشند، پلن کش شده بهینه نیست. راه‌حل: RECOMPILE hint، pg_hint_plan یا plan_cache_mode.

---

## Ch 2 — نگهداری Index

چه زمانی full table scan از index سریعتر است؟ ; وقتی optimizer تخمین می‌زند I/O ترتیبی (full scan) از index lookup + I/O تصادفی ارزان‌تر است. بستگی به اندازه جدول، نوع storage، buffer cache و توزیع داده دارد. EXPLAIN (ANALYZE, BUFFERS) را بررسی کن.

چرا `WHERE phone = 5551234` از index روی ستون VARCHAR استفاده نمی‌کند؟ ; type cast ضمنی — مقایسه VARCHAR با INT هر سطر را تبدیل می‌کند و index را غیرقابل استفاده می‌کند. راه‌حل: `WHERE phone = '5551234'`.

چطور indexهای بی‌استفاده را پیدا کنیم؟ ; MySQL: `SELECT * FROM sys.schema_unused_indexes`. PostgreSQL: `SELECT indexrelname, idx_scan FROM pg_stat_user_indexes WHERE idx_scan = 0`. برای سرعت بخشیدن به writeها حذفشان کن.

---

## Needs Review
<!-- جواب‌های اشتباه از آزمون‌های دوره‌ای اینجا بیایند -->
