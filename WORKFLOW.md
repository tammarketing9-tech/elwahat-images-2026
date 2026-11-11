# دورة رفع صور منتجات بساتين الواحات (elwahat.com)

تعليمات ثابتة لأي نموذج أو جلسة Claude تكمل المهمة.

## القواعد
- لا قص خلفية، ولا قالب، ولا إعادة توليد للصورة. تفتيح خفيف فقط.
- الاستيكر (النص والشعار والباركود) منطقة محمية: يجب أن يكون `sticker_max_change = 0`.
- الصورة الرئيسية = صورة الاستيكر، والصورة الفرعية = العبوات من الخلف.
- لا تُدخل كلمات مرور أبداً؛ المستخدم يسجّل الدخول بنفسه.
- لا تحذف وسائط من الموقع؛ الحذف للمستخدم.
- الرد على المستخدم بالعربية دائماً.

## الخطوات
1. **التفتيح:** `python3 tools/lite.py in.jpg products/<SKU>-1.jpg` (والصورة الثانية بـ `-2`).
   تأكد أن تقرير QA يعطي `sticker_max_change: 0` وأن `dates_V_after` أعلى قليلاً من `dates_V_before`. احذف ملف `.prot.png` قبل الرفع.
2. **GitHub:** `git add products/ && git commit -m "Add <SKU> images" && git push origin HEAD`.
3. **الموقع:** في المتصفح المدمج بتطبيق Claude، والمستخدم داخل `https://elwahat.com/wp-admin/`، نفّذ JavaScript:
   - ابحث بالـ SKU: `/wp-json/wc/v3/products?sku=<SKU>&status=any` (يرجع النسختين العربية والإنجليزية).
   - اسحب الصورة من `https://raw.githubusercontent.com/tammarketing9-tech/elwahat-images-2026/main/products/<file>` وارفعها `POST /wp-json/wp/v2/media` مع `alt_text` عربي: `<اسم المنتج> - بساتين الواحات`.
   - `PUT /wp-json/wc/v3/products/<id>` بـ `images:[{id:main},{id:gallery}]` للنسختين، و`status:'publish'` إن كان المنتج مسودة.
   - الترويسة: `{'X-WP-Nonce': wpApiSettings.nonce}`. شغّل العمل في الخلفية وتابعه عبر `window.job` (تجنباً لمهلة 45 ثانية).
4. **التحقق:** امسح الكاش عبر رابط `a[href*=purge_all]` في شريط الإدارة، ثم افتح صفحتي المنتج وتأكد من ظهور اسمي الملفين.
5. **التقرير للمستخدم:** رابط الصفحتين، وأن الصورة القديمة باقية في المكتبة ليحذفها بنفسه.
