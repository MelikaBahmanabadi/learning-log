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

## Ch 3 — آنتی‌الگوهای طراحی منطقی

آنتی‌الگوی Jaywalking چیست؟ ; ذخیره چند مقدار در یک ستون (لیست کاما-جدا). مشکل: FK وجود ندارد، نمی‌توان index زد، query نیاز به FIND_IN_SET یا LIKE دارد. راه‌حل: همیشه از یک جدول join (جدول واسط) استفاده کن.

آنتی‌الگوی Naive Trees چیست و Closure Table چطور کار می‌کند؟ ; ذخیره سلسله‌مراتب با parent_id — پرس‌وجوی عمق نامحدود نیازمند recursive CTE است. Closure Table یک جدول مجزا همه جفت‌های ancestor-descendant را ذخیره می‌کند. پرس‌وجوی فرزندان یا اجداد با یک query ساده.

چهار روش مدل‌سازی داده‌های سلسله‌مراتبی در SQL کدامند؟ ; ۱) adjacency list (parent_id — ساده، محدود)، ۲) nested sets (nsleft/nsright — خواندن عالی، نوشتن سخت)، ۳) path enumeration (رشته مسیر — مناسب ancestry ساده)، ۴) closure table (انعطاف‌پذیر، توصیه شده).

چه موقع استفاده از parent_id (adjacency list) قابل قبول است؟ ; وقتی فقط parent بلافصل نیاز است (کارمند → مدیر) و هرگز به پیمایش کامل درخت نیاز نیست. فقط سلسله‌مراتب کوتاه.

مشکل auto-increment id برای همه جدول‌ها چیست؟ ; آنتی‌الگوی "ID Required". کلیدهای طبیعی وجود دارند و پایدارند — از آنها استفاده کن. surrogate key سربار index اضافه می‌کند، معنا را پنهان می‌کند. با کلید طبیعی شروع کن.

چه موقع surrogate key خوب است؟ ; وقتی کلید طبیعی پایدار وجود ندارد، پهن است (>۴ ستون)، یا در سیستم‌های توزیع‌شده (UUID/ULID). همچنین برای چارچوب‌هایی مثل Rails، Django.

مشکل "ما integrity داده را در app اعمال می‌کنیم" چیست؟ ; آنتی‌الگوی "Keyless Entry". کد app باگ دارد → داده کثیف. هر کلاینتی باید همان بررسی‌ها را دوباره پیاده کند. FK وجود ندارد، سطرهای یتیم. محدودیت‌های DB اتمیک و سازگار هستند.

آنتی‌الگوی EAV چیست؟ ; Entity-Attribute-Value — یک "اسکیما عمومی" با سطرهای (entity_id, attr_name, attr_value). مشکل: همه مقادیر VARCHAR (بدون type safety)، FK غیرممکن، SELECT نیازمند N تا JOIN. تقریباً همیشه غلط است.

جایگزین‌های بهتر برای EAV چیست؟ ; Single Table Inheritance (ستون‌های مشترک در یک جدول + ستون nullable برای subtypeها)، Class Table Inheritance (جدول مشترک + جدول‌های subtype)، یا JSONB برای ویژگی‌های واقعاً پویا.

آنتی‌الگوی Polymorphic Associations چیست؟ ; یک ستون FK که می‌تواند به هر جدولی اشاره کند: parent_type + parent_id. مشکل: referential integrity وجود ندارد، JOINها نیاز به UNION دارند. راه‌حل: یک جدول join مجزا برای هر نوع والد.

---

## Ch 3 — آنتی‌الگوهای طراحی فیزیکی

مشکل ذخیره پول به صورت FLOAT چیست؟ ; ممیز شناور نمی‌تواند اعداد اعشاری را دقیق نمایش دهد (0.1+0.2=0.30000000000000004). از DECIMAL(precision, scale) یا ذخیره به صورت سنت با BIGINT استفاده کن.

آنتی‌الگوی Metadata Tribbles چیست؟ ; ساختن جدول‌های مجزا برای داده‌های مشابه در طول زمان: Bugs_2009, Bugs_2010. مشکل: پرس‌وجو بین سال‌ها = UNION ALL، اضافه کردن سال جدید = schema change. راه‌حل: یک جدول با ستون سال + پارتیشن‌بندی.

چرا ENUMها در production مشکل‌سازند؟ ; اضافه کردن مقدار نیاز به ALTER TABLE دارد (DDL → قفل جدول → downtime احتمالی). نمی‌توان FK زد. جدول‌های مختلف از هم فاصله می‌گیرند. lookup table را ترجیح بده — مقدار جدید = INSERT (DML)، نه ALTER TABLE.

چه موقع ENUM قابل قبول است؟ ; مجموعه‌های واقعاً ثابت (مخفف استاندارد ایالت‌ها، کدهای کشور ISO — اما حتی آن‌ها هم lookup table ضرر ندارد). اپ‌های کوچک داخلی که status هرگز تغییر نمی‌کند.

مشکل ذخیره چند tag در ستون‌های جدا (tag1, tag2, tag3) چیست؟ ; querying با WHERE tag1='x' OR tag2='x' OR tag3='x' دست و پاگیر است، اضافه tag چهارم = ALTER TABLE. راه‌حل: join table.

---

## Ch 3 — آنتی‌الگوهای Query و اپلیکیشن

آنتی‌الگوی Phantom Files چیست؟ ; ذخیره مسیر فایل در DB، خود فایل روی دیسک. مشکل: سطر DB و فایل ناهماهنگ می‌شوند، بکاپ دو فرایند مجزا نیاز دارد. راه‌حل: BLOB در DB (فایل‌های کوچک) یا object store با checksum.

چرا SELECT * در view و procedure بد است؟ ; ستون‌ها به ترتیب تعریف جدول برمی‌گردند، اضافه ستون خروجی view را تغییر می‌دهد (کد مصرف‌کننده خراب می‌شود)، covering index کار نمی‌کند. همیشه ستون‌ها را مشخص کن.

مشکل استفاده از -1 یا 'N/A' به جای NULL چیست؟ ; آنتی‌الگوی "Fear of the Unknown". مقادیر sentinel توابع aggregate را خراب می‌کنند (AVG شامل -1 می‌شود)، هر app باید قرارداد را بداند، برای FK غیرممکن است. از NULL استفاده کن.

آنتی‌الگوی Spaghetti Query چیست؟ ; یک query غول با ۱۲+ تا JOIN، subquery تو در تو با ۵ سطح عمق. راه‌حل: CTE، جدول موقت، view یا شکستن به مراحل app-level.

آنتی‌الگوی God Table چیست؟ ; جدولی با ۵۰+ ستون که هر فیچری از آن استفاده می‌کند. مشکل: سطرهای عریض، محدودیت اندازه ردیف/صفحه، lock contention. راه‌حل: vertical partitioning — جدول‌های مجزا بر اساس دامنه.

---

## Ch 3 — نکات مصاحبه

بدترین آنتی‌الگوی SQL کدام است؟ ; EAV یا Jaywalking — هر دو رایجند، نرمال‌سازی را می‌شکنند، queryability را نابود می‌کنند. EAV: همه مقادیر VARCHAR، بدون type safety. Jaywalking: بدون FK، بدون index.

چطور یک سیستم EAV را بازطراحی می‌کنی؟ ; ویژگی‌های مشترک → ستون، subtype-specific → class table inheritance، پویا → JSONB. مهاجرت مرحله‌ای: اسکیما جدید، همزمان به هر دو بنویس، backfill، EAV را حذف کن.

برای سیستم کامنت‌های رشته‌ای با nesting بی‌نهایت از چه مدلی استفاده می‌کنی؟ ; Closure Table. پرس‌وجوی اجداد و نوادگان در depth دلخواه با یک query. جایگزین: path enumeration برای ancestry-only.

ENUM یا lookup table؟ ; همیشه lookup table مگر اینکه مقادیر واقعاً تا ابد ثابت باشند. ENUM = DDL (ALTER TABLE، lock، downtime). Lookup table = DML (INSERT، بدون downtime، FK-پذیر).

---

## Ch 4 — مبانی Window Functions

تفاوت window function و GROUP BY چیست؟ ; Window function روی مجموعه‌ای از سطرهای مرتبط با سطر جاری محاسبه می‌کند بدون اینکه سطرها را ادغام کند — هر سطر هویت خود را حفظ می‌کند. GROUP BY سطرها را یک گروه می‌کند و یک خروجی به ازای هر گروه می‌دهد.

سه بخش syntax یک window function چیست؟ ; FUNCTION(...) OVER (PARTITION BY ... ORDER BY ... frame_clause). PARTITION BY گروه‌ها را مشخص می‌کند، ORDER BY ترتیب درون گروه را مشخص می‌کند، frame تعیین می‌کند کدام سطرهای گروه در محاسبه شرکت کنند.

تفاوت ROW_NUMBER، RANK و DENSE_RANK چیست؟ ; ROW_NUMBER اعداد یکتا و ترتیبی می‌دهد (تساوی ترتیب دلخواه دارد، gap ندارد). RANK به مقادیر مساوی یک rank می‌دهد ولی gap دارد (۱,۱,۳,۴). DENSE_RANK به مقادیر مساوی یک rank می‌دهد و gap ندارد (۱,۱,۲,۳).

---

## Ch 4 — LAG / LEAD

LAG و LEAD چه کاری انجام می‌دهند؟ ; LAG به سطر قبل از سطر جاری دسترسی می‌دهد و LEAD به سطر بعد از سطر جاری. برای مقایسه سری‌های زمانی (تغییر روز-به-روز) استفاده می‌شوند.

وقتی LAG/LEAD در لبه‌های پارتیشن قرار دارند چه اتفاقی می‌افتد؟ ; NULL برمی‌گردانند (سطر قبلی/بعدی وجود ندارد). از پارامتر پیش‌فرض استفاده کن: LAG(col, 1, 0) تا به جای NULL صفر برگرداند.

---

## Ch 4 — FIRST_VALUE / LAST_VALUE / NTH_VALUE

چرا LAST_VALUE اغلب جواب اشتباه می‌دهد؟ ; فریم پیش‌فرض RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW است — پس LAST_VALUE مقدار سطر جاری را برمی‌گرداند. راه‌حل: ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING را مشخص کن.

---

## Ch 4 — پنجره (Window Frame)

تفاوت ROWS، RANGE و GROUPS چیست؟ ; ROWS = سطرهای فیزیکی (سریع، قطعی). RANGE = مقادیر منطقی — سطرهایی با مقدار ORDER BY یکسان همتا محسوب می‌شوند (کندتر). GROUPS = گروه‌های سطرهای همتا (PostgreSQL 11+).

فریم پیش‌فرض با ORDER BY چیست؟ بدون ORDER BY؟ ; با ORDER BY: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW. بدون ORDER BY: کل پارتیشن.

---

## Ch 4 — CTE

تفاوت CTE و subquery چیست؟ ; CTE نام‌گذاری شده، قابل استفاده مجدد در query است و خوانایی را بهبود می‌دهد. Subquery درون‌خطی است، باید تکرار شود. CTE می‌تواند بازگشتی باشد (WITH RECURSIVE) — subquery نمی‌تواند.

در recursive CTE، base case و recursive step چه نقشی دارند؟ ; Base case (عبارت غیربازگشتی) نتیجه اولیه را می‌سازد. Recursive step به CTE برمی‌گردد و به آن JOIN می‌خورد. UNION ALL هر دو را ترکیب می‌کند. جلوگیری از چرخه: مسیر پیموده‌شده را در array ذخیره کن و با NOT x = ANY(path) بررسی کن.

---

## Ch 4 — PIVOT / UNPIVOT

چطور سطرها را به ستون تبدیل کنیم (PIVOT) در MySQL/PostgreSQL؟ ; CASE + GROUP BY: SUM(CASE WHEN quarter='Q1' THEN revenue END) AS q1. PostgreSQL از crosstab() هم پشتیبانی می‌کند.

---

## Ch 4 — LATERAL

LATERAL join چیست؟ ; زیرپرس‌وجو را به ازای هر سطر query بیرونی اجرا می‌کند — شبیه correlated subquery اما خواناتر. کاربرد: TOP-N به ازای هر گروه. PostgreSQL و MySQL 8.0.14+.

---

## Ch 4 — GROUPING SETS

تفاوت ROLLUP و CUBE چیست؟ ; ROLLUP زیرمجموع‌های سلسله‌مراتبی تولید می‌کند: GROUP BY ROLLUP (year, month) → (year,month), (year), (). CUBE تمام ترکیب‌ها را تولید می‌کند: GROUP BY CUBE (a, b) → (a,b), (a), (b), ().

تابع GROUPING() چطور کمک می‌کند؟ ; GROUPING(col) وقتی سطر زیرمجموعه است ۱ برمی‌گرداند. بین NULL واقعی و NULL حاصل از grouping تمایز قائل می‌شود.

---

## Ch 4 — Conditional Aggregation

چطور سطرها را بر اساس شرط بدون subquery بشماریم؟ ; FILTER clause: COUNT(*) FILTER (WHERE salary > 80000). در PostgreSQL، SQLite، DuckDB. در MySQL/SQL Server: SUM(CASE WHEN salary > 80000 THEN 1 ELSE 0 END).

---

## Ch 4 — الگوهای پیشرفته

چرا window function در WHERE کار نمی‌کند؟ ; Window functions بعد از WHERE اجرا می‌شوند (ترتیب منطقی SQL). در یک subquery/CTE محاسبه کن، بعد خارجی فیلتر کن.

چطور دومین حقوق بالاترین را به ازای هر بخش پیدا کنیم؟ ; DENSE_RANK() در subquery: SELECT * FROM (SELECT *, DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk FROM employees) ranked WHERE rnk = 2.

تفاوت WHERE و HAVING چیست؟ ; WHERE سطرها را قبل از GROUP BY فیلتر می‌کند. HAVING گروه‌ها را بعد از GROUP BY فیلتر می‌کند. توابع aggregate در WHERE کار نمی‌کنند چون هنوز وجود ندارند.

---

## Ch 4 — کارایی Query

آیا window functions می‌توانند از index استفاده کنند؟ ; ORDER BY در window می‌تواند از index استفاده کند. PARTITION BY از index روی ستون پارتیشن بهره می‌برد. یک index ترکیبی روی (partition, order) می‌تواند کل sort window را پوشش دهد.

تفاوت FILTER و CASE-based conditional aggregation چیست؟ ; FILTER خواناتر است و در PostgreSQL ممکن است استراتژی اجرای متفاوتی فعال کند. در عمل هر دو پلن مشابهی دارند — FILTER برای خوانایی، CASE برای سازگاری.


---

## Ch 5 — موتورهای ذخیره‌سازی و ساختار داده

storage engine چیست؟ ; لایه‌ای که سازمان‌دهی فیزیکی داده، ایندکس‌ها، تراکنش‌ها و بازیابی را روی دیسک مدیریت می‌کند. از لایه query/planner جدا است. Row-oriented برای OLTP، column-oriented برای OLAP.

چرا ستون‌محورها بهتر از ردیف‌محورها فشرده می‌شوند؟ ; هر ستون یک نوع داده با تکرار بالا ذخیره می‌کند — کدینگ run-length، dictionary و delta خوب جواب می‌دهند. ردیف نوع‌های مختلف و مقادیر متنوع دارد، پس فشرده‌سازی کم بهره می‌برد.

B+tree چیست و چرا اکثر دیتابیس‌ها استفاده می‌کنند؟ ; درخت متوازن چندمسیره که فقط برگ‌ها داده دارند، گره‌های داخلی فقط کلید، و برگ‌ها به‌صورت لیست مرتب به هم وصل‌اند. ارتفاع کم (۲-۴) و لیست برگ‌ها اسکن بازه‌ای را سریع می‌کند. InnoDB، PostgreSQL و SQLite از B+tree استفاده می‌کنند.

کلاستر ایندکس (primary key در InnoDB) چطور کار می‌کند؟ ; ردیف‌های جدول فیزیکی داخل B+tree مرتب‌شده با primary key ذخیره می‌شوند. ایندکس‌های ثانویه به مقدار PK اشاره می‌کنند، پس جستجوی ثانویه = ۲ پیمایش. ORDER BY روی PK تقریباً رایگان است.

چرا PK یکنواخت بهتر از UUID تصادفی در InnoDB است؟ ; کلید یکنواخت لبه راست اضافه می‌شود — بدون page split و fragmentation. UUID تصادفی وسط درخت می‌رود و page split و write amplification ایجاد می‌کند.

LSM tree چیست؟ ; Log-structured merge: نوشتن append-only در memtable حافظه، flush به صورت SSTable مرتب، و ادغام در پس‌زمینه با compaction. بهینه برای بارهای write-heavy (RocksDB، Cassandra، HBase). هزینه: read/space amplification بیشتر.

B-tree یا LSM — کدام برای write-heavy و کدام read-heavy؟ ; LSM برای write-heavy: نوشتن append-only بدون به‌روزرسانی تصادفی درجا. B-tree برای read-heavy و point lookup: read amplification کمتر و تأخیر قابل پیش‌بینی. بر اساس تعادل بار انتخاب کن.

write-ahead logging (WAL) چیست و چرا لازم است؟ ; هر تغییر قبل از به‌روزرسانی فایل داده، اول به یک log ترتیبی append می‌شود. این buffer شدن تنبل را امن می‌کند: در crash با replay کردن log تراکنش‌های commit شده بازیابی می‌شوند. بدون fsync هر page در هر commit، durability می‌دهد.

checkpoint چیست؟ ; نقطه‌ای که page های کثیف به فایل داده flush می‌شوند و WAL کوتاه می‌شود. بازیابی فقط از آخرین checkpoint replay می‌کند و زمان بازیابی را محدود می‌کند.

فرق latch و lock چیست؟ ; Latch: ساختار فیزیکی درون حافظه (page های buffer pool، گره‌های ایندکس)، چند میکروثانیه، یک عملیات، بدون scope تراکنش و بدون تشخیص deadlock. Lock: داده منطقی، تا پایان تراکنش، صف‌بندی شده، با تشخیص deadlock.

STEAL و NO-FORCE در بازیابی یعنی چه؟ ; STEAL = موتور ممکن است page کثیف تراکنش ناکامل را زودتر flush کند (نیاز به undo log). NO-FORCE = موتور همه page کثیف را در commit flush نمی‌کند (به WAL redo اتکا می‌کند). InnoDB و PostgreSQL STEAL + NO-FORCE هستند.

MVCC چطور اجازه می‌دهد خواننده‌ها نویسنده‌ها را بلاک نکنند؟ ; هر تراکنش یک snapshot سازگار با نگه‌داشتن چند نسخه ردیف می‌بیند. خواننده‌ها نسخه قدیمی می‌خوانند؛ نویسنده‌ها نسخه جدید می‌سازند؛ undo log / versioning پاکسازی را مدیریت می‌کند. بدون contention بین خواننده و نویسنده.

hash index چیست و محدودیتش کدام است؟ ; کلید را به offset در یک log append-only نگاشت می‌کند (طراحی Bitcask). point lookup با O(1)، اما اسکن بازه‌ای ندارد و باید در حافظه باشد. مناسب بارهای key-value نقطه‌ای.

---

## Ch 6 — Consistent Hashing

Consistent Hashing چیست و چرا استفاده می‌شود؟ ; کلیدها و نودها را روی یک حلقه هش (hash ring) نگاشت می‌کند. هر کلید به اولین نود در جهت ساعت‌گرد اختصاص می‌یابد. اضافه/حذف نود فقط همسایه‌ها را تحت تأثیر قرار می‌دهد — جابجایی داده‌ها بهینه است. در Dynamo، Cassandra، Riak استفاده می‌شود.

حلقه هش (hash ring) چطور کار می‌کند؟ ; نودها و کلیدها با هش کردن روی دایره قرار می‌گیرند. یک کلید به اولین نود در جهت ساعت‌گرد داده می‌شود. نودهای مجازی (vnodes) توزیع یکنواخت و ریکانفیگ راحت را تضمین می‌کنند.

---

## Ch 6 — Partitioning Strategies

تفاوت پارتیشن‌بندی key-range و hash-based چیست؟ ; Key-range: بر اساس محدوده‌های مرتب کلید (مثلاً ۱-۱۰۰۰ → نود A). range scan می‌شود اما hotspot دارد. Hash: hash(key) % N پارتیشن را تعیین می‌کند. توزیع یکنواخت اما range scan ندارد.

چطور پارتیشن‌ها را هنگام اضافه کردن نود rebalance می‌کنید؟ ; Fixed partitions: بسیاری از پارتیشن‌ها از پیش ساخته شده، زیرمجموعه به نود جدید منتقل می‌شود. Dynamic splitting: پارتیشن‌ها وقتی بزرگ شدند تقسیم می‌شوند. Consistent hashing: فقط داده‌های همسایه‌ها جابجا می‌شوند.

Virtual node (vnode) چیست؟ ; یک نود فیزیکی چندین "توکن" (اسلات) روی حلقه هش擁有 می‌کند. توزیع داده یکنواختر، ریکانفیگ هنگام add/remove راحت‌تر. در Cassandra، Kafka استفاده می‌شود.

---

## Ch 6 — Replication Models

سه مدل replication چیستند؟ ; Single-leader: همه writes → leader → replicas (اسکیل خواندن، ساده). Multi-leader: write به هر leader → replicate به بقیه (چند منطقه‌ای، conflict احتمالی). Leaderless (Dynamo): write به W نود، read از R نود، W+R>N (بسیار available، eventual).

تفاوت replication synchronous و asynchronous چیست؟ ; Sync: تا ack از replica منتظر می‌ماند. پایداری قوی‌تر، latency بالا، اگر replica down باشد block می‌شود. Async: بلافاصله ack می‌دهد. Latency پایین اما replica lag → stale read، احتمال data loss.

---

## Ch 6 — Consensus (Raft)

انتخاب رهبر (leader election) در Raft چطور کار می‌کند؟ ; Followers یک election timeout تصادفی صبر می‌کنند. اگر heartbeat از leader نیاید، candidate می‌شوند، term را افزایش می‌دهند، درخواست vote می‌دهند. اگر اکثریت رأی بدهند → leader می‌شوند. Timeout‌های تصادفی split vote را پیشگیری می‌کند.

Election restriction در Raft چیست؟ ; یک candidate باید log دارد که حداقل به اندازه اکثریت up-to-date باشد (term و index آخرین entry) تا برنده شود. تضمین می‌کند leader جدید همه entryهای committed را دارد.

Log replication در Raft چگونه انجام می‌شود؟ ; Leader entry می‌گیرد → به log خود append می‌کند → AppendEntries RPC به followers می‌فرستد → entry وقتی اکثریت append کنند committed می‌شود → leader روی state machine apply می‌کند → به followers از طریق commit index می‌گوید apply کنند.

---

## Ch 6 — Distributed Transactions

Two-Phase Commit (2PC) چطور کار می‌کند؟ ; Phase 1: coordinator از participants می‌پرسد "can you commit?" → participants منابع را lock می‌کنند، prepare در log می‌نویسند، YES/NO جواب می‌دهند. Phase 2: اگر همه YES → COMMIT به همه؛ اگر هر کدام NO → ABORT به همه.

مشکل 2PC چیست؟ ; Blocking: اگر coordinator بعد از prepare fail کند، participants تا بی‌نهایت block می‌شوند. Coordinator SPOF است. Lockها طول کامل prepare/commit نگه داشته می‌شوند.

Saga pattern چیست؟ ; یک تراکنش توزیع‌شده را به دنباله‌ای از تراکنش‌های محلی می‌شکند، هر کدام با یک compensating action برای rollback. Orchestration: coordinator مرکزی. Choreography: event-driven، coordinator ندارد.

---

## Ch 6 — CAP & PACELC

تئورم CAP چه می‌گوید؟ ; در یک network partition (P)، باید بین Consistency (C) و Availability (A) انتخاب کنید. هر دو نمی‌توانید داشته باشید. فقط در طول partition صدق می‌کند — در حالت عادی هر دو ممکن است.

PACELC چیست؟ ; توسعه CAP: Else (partition نیست)، Latency در برابر Consistency. PC/EC: consistency را اولویت می‌دهد (Spanner، CockroachDB). PA/EL: latency/availability را اولویت می‌دهد (Cassandra، DynamoDB).

---

## Ch 6 — Vector Clocks

Vector Clock چیست؟ ; causality را بین نودها با اختصاص counter به هر نود ردیابی می‌کند. هر version یک vector دارد (مثلاً counter نود A، counter نود B). آپدیت‌های concurrent را تشخیص می‌دهد (وقتی هیچ vector دیگری را dominate نمی‌کند).

چطور با vector clock conflict تشخیص می‌دهید؟ ; اگر vector clock X در حداقل یک نود count بالاتری از Y داشته باشد و Y در حداقل یک نود count بالاتری داشته باشد → concurrent (conflict). اگر یکی همه را dominate کند → happens-before.

---

## Ch 6 — Quorum & Read Repair

شرط quorum در سیستم‌های Dynamo-style چیست؟ W+R > N consistency قوی را تضمین می‌کند. با N=3، W=2، R=2: ۲+۲=۴>۳. یک read به ۲ نود می‌رسد؛ حداقل ۱ آنها آخرین write را دیده است.

Read Repair چیست؟ ; در طول یک read، اگر replicas disagree کنند، reader جدیدترین version را برمی‌گرداند و به replicas قدیمی برمی‌گرداند (write-back). Repairها به صورت lazy در background انجام می‌شوند، نه synchronous.

---

## Ch 6 — Distributed Query Execution

Indexهای ثانویه در دیتابیس sharded چطور مدیریت می‌شوند؟ ; Local index: query به همه shards fan-out می‌شود (scatter-gather). Global index: index بر اساس term پارتیشن‌بندی می‌شود؛ یک shard جواب می‌دهد اما writes به چندین index partition می‌روند.

Broadcast join در برابر shuffle join کی استفاده می‌شود؟ ; Broadcast: یک جدول đủ کوچک است که در حافظه جا شود — به همه نودها فرستاده می‌شود. Shuffle: هر دو جدول بزرگند — با hash(key) redistribute می‌شوند. Shuffle = network I/O بالا، broadcast = network کم اما حافظه.
