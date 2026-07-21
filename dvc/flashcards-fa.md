# فلش‌کارت‌ها (فارسی)

<!-- Cards in Anki format: Question? ; Answer -->
<!-- اصطلاحات فنی CLI مانند cache، remote، pointer، pipeline، hash به انگلیسی نگه داشته شده‌اند -->

---

## فصل ۱ — انگیزه‌ی data versioning

چرا data versioning در ML ضروری است؟ ; چون نتیجه‌ی مدل به code، data و hyperparameterها وابسته است. version کردن فقط code نمی‌تواند یک experiment ML را به‌درستی بازتولید یا ممیزی کند

چه سه مؤلفه‌ای با هم نتیجه‌ی مدل ML را تعیین می‌کنند؟ ; code (الگوریتم و معماری)، data (ورودی‌های آموزشی) و hyperparameterها (تنظیمات پیش از training)

چرا دو مدل که روی زیرمجموعه‌های مختلف یک dataset آموزش دیده‌اند ممکن است metric متفاوتی داشته باشند؟ ; چون تقسیم تصادفی توزیع‌های sample متفاوتی می‌سازد؛ اگر distribution shift واقعی اتفاق بیفتد تفاوت metric می‌تواند بسیار بزرگ باشد

تفاوت عملی اصلی بین ابزارهای code versioning و data versioning چیست؟ ; Git برای code کافی است چون codebaseها کوچک و text-based هستند؛ data versioning به نرم‌افزار مکمل کنار Git نیاز دارد تا dataset های بزرگ، باینری و پرتغییر را مدیریت کند

اولین پیاده‌سازی‌های عملی data versioning چه زمانی ظاهر شدند؟ ; حدود سال ۲۰۱۲

---

## فصل ۱ — مبانی Git و DVC

رابطه‌ی Git و DVC چیست؟ ; Git کد و DVC metadata سبک‌وزن مثل .dvc files، dvc.yaml و dvc.lock را version می‌کند؛ DVC artifactهای واقعی بزرگ (data و model) را از طریق cache و remote storage مدیریت می‌کند

بعد از `dvc add data.csv` چه چیزی در Git و چه چیزی در DVC مدیریت می‌شود؟ ; Git فایل data.csv.dvc (pointer) و .gitignore را track می‌کند؛ DVC bytes واقعی data.csv را cache می‌کند و می‌تواند آن را به DVC remote بفرستد

workflow صحیح اشتراک‌گذاری بعد از track کردن یک dataset جدید با DVC چیست؟ ; اجرای `dvc add data.csv`، `git add data.csv.dvc .gitignore`، `git commit`، `dvc push` و `git push`. هر دوی dvc push و git push لازم هستند

بعد از `git clone` یک پروژه‌ی DVC چه اتفاقی می‌افتد؟ ; code، DVC config، .dvc pointer files، dvc.yaml و dvc.lock دریافت می‌شوند — اما data یا model artifactهای واقعی DVC-tracked دریافت نمی‌شوند

یک همتیمی چطور بعد از `git clone` data های DVC-tracked را بازیابی می‌کند؟ ; با اجرای `dvc pull`. این دستور artifactها را از DVC remote به local cache دانلود می‌کند و آن‌ها را در workspace قابل استفاده می‌کند

تفاوت `git push` و `dvc push` چیست؟ ; `git push` کد و DVC metadata (pointerها) را به Git remote می‌فرستد؛ `dvc push` bytes واقعی data و model artifact را به DVC remote storage می‌فرستد

`dvc add` چه کاری می‌کند؟ ; نسخه‌ی فعلی یک data file یا folder را hash و cache می‌کند، .dvc pointer file آن را می‌سازد/به‌روز می‌کند و path فایل tracked را به .gitignore اضافه می‌کند

فایل `.dvc` مثل `data.csv.dvc` چیست؟ ; metadata قابل‌track در Git که یک artifact DVC-tracked را با content hash مشخص می‌کند؛ خود dataset نیست، فقط pointer به آن است

`dvc.yaml` چیست؟ ; تعریف pipeline DVC: stageهای نام‌دار، command، dependencyها (deps)، outputها (outs) و اختیاراً params، metrics و plots

`dvc.lock` چیست؟ ; hash دقیق dependencyها و outputهای pipeline را از آخرین اجرای موفق ثبت می‌کند تا DVC بتواند staleبودن stageها را تشخیص دهد

آیا `dvc.lock` فایل‌ها را read-only می‌کند؟ ; خیر. dvc.lock فقط state pipeline را ثبت و تغییر را از طریق مقایسه‌ی hash تشخیص می‌دهد؛ read-only شدن احتمالی جداگانه از cache link typeهایی مثل hardlink یا symlink می‌آید

چه چیزی یک stage پایپلاین DVC را stale می‌کند؟ ; تغییر هر dependency ثبت‌شده به‌گونه‌ای که hash فعلی با hash ثبت‌شده در dvc.lock متفاوت باشد

اگر `train.py` تغییر کند اما data آموزشی تغییر نکند، `dvc repro` چه stageهایی را اجرا می‌کند؟ ; stage مربوط به train (dependency تغییر کرده) و stageهای downstream وابسته به output تغییریافته؛ stageهای upstream بدون تغییر اجرا نمی‌شوند

تفاوت `dvc add` و `dvc repro` چیست؟ ; `dvc add` یک data file یا folder مستقل را track می‌کند؛ `dvc repro` DAG را بررسی می‌کند و فقط stageهای stale را به ترتیب dependency اجرا می‌کند

workflow معمول تغییر data که با `dvc add` track شده چیست؟ ; اگر لازم است با `dvc unprotect` از cache جدا کن، تغییر بده، دوباره `dvc add` اجرا کن، .dvc pointer به‌روزشده را با Git commit کن، سپس `dvc push` و `git push` بزن

چرا `dvc commit` نباید دستور پیش‌فرض برای data تغییریافته‌ی مستقل باشد؟ ; برای data که با `dvc add` track شده، اجرای دوباره‌ی `dvc add` روش درست است؛ برای pipeline، `dvc repro` dependencyها را اعتبارسنجی می‌کند. هر دو از `dvc commit` مطمئن‌ترند

کدام دو دستور با هم state کامل پروژه را نشان می‌دهند؟ ; `git status` تغییرات code و DVC metadata را نشان می‌دهد؛ `dvc data status` تغییرات data های DVC-tracked و وضعیت cache را نشان می‌دهد

---

## Needs Review

<!-- پاسخ‌های اشتباه از quiz های دوره‌ای اینجا می‌آیند -->

تفاوت `dvc.lock` و cache protection چیست؟ ; dvc.lock یک دفتر hash-based از ورودی‌ها و خروجی‌های pipeline است که برای تشخیص staleness استفاده می‌شود؛ cache protection ممکن است workspace files را هنگام استفاده از cache link typeهای مبتنی بر hardlink یا symlink read-only کند
