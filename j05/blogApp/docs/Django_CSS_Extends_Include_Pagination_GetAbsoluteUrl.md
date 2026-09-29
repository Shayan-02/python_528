# جزوه جامع و پروژه‌محور Django — CSS، Static Files، extends، include، Pagination و get_absolute_url

> این جزوه ادامهٔ مسیر آموزش Django و معماری MVT است.
>
> پروژه نمونه: `blogApp_MVT_Django_Styled`
>
> نکته مهم: این جزوه به یک پروژه خاص محدود نیست. مفاهیم را مستقل و از پایه توضیح می‌دهد و در هر جا که لازم باشد، از پروژه Blog برای تبدیل شدن مفهوم به کد واقعی استفاده می‌کنیم.

---

## فهرست مطالب

1. هدف این فصل
2. نقشه راه مباحث
3. قبل از CSS دقیقاً چه چیزی باید بدانیم؟
4. HTML و CSS چه تفاوتی دارند؟
5. Inline، Internal و External CSS
6. چرا فایل CSS جداگانه بهتر است؟
7. CSS از صفر — Syntax
8. Selectorها
9. Property و Value
10. رنگ، متن و فونت
11. Box Model
12. `margin`، `padding` و `border`
13. اندازه‌ها در CSS
14. `display` و مفهوم چیدمان
15. Flexbox به زبان ساده
16. Grid به زبان ساده
17. Pseudo-classهای مهم
18. Cascade، Specificity و ترتیب قوانین
19. Responsive Design
20. Static Files در Django
21. ساختار استاندارد پوشه static
22. `{% load static %}` و `{% static %}`
23. اتصال CSS خارجی به Template
24. Template Inheritance چیست؟
25. `base.html`
26. `extends`
27. `block`
28. رابطه بین extends و block
29. `include` چیست؟
30. تفاوت `include` و `extends`
31. ارسال Context به include
32. ساخت Component ساده با include
33. چرا Partialها مهم هستند؟
34. URL Naming و `{% url %}`
35. `reverse()` در Django
36. `get_absolute_url()` چیست؟
37. ساخت get_absolute_url در Model
38. استفاده از get_absolute_url در View و Template
39. چرا get_absolute_url از URL هاردکد بهتر است؟
40. Pagination چیست؟
41. چرا Pagination مهم است؟
42. `Paginator` در Django
43. Page Object چیست؟
44. ساخت Pagination در View — مرحله‌به‌مرحله
45. `request.GET.get('page')`
46. `get_page()` و مدیریت مقدار نامعتبر
47. متغیرهای مهم Page Object
48. ساخت رابط Pagination در Template
49. تبدیل Pagination به Partial با include
50. ساخت پروژه از صفر تا نسخه نهایی
51. مرحله اول — HTML ساده
52. مرحله دوم — اضافه کردن CSS خارجی
53. مرحله سوم — ساخت base.html
54. مرحله چهارم — ساخت کارت پست با include
55. مرحله پنجم — اضافه کردن get_absolute_url
56. مرحله ششم — اضافه کردن Pagination
57. مرحله هفتم — تمیز کردن پروژه
58. تشریح کامل فایل‌های پروژه
59. اشتباهات رایج CSS
60. اشتباهات رایج Static Files
61. اشتباهات رایج extends و block
62. اشتباهات رایج include
63. اشتباهات رایج get_absolute_url
64. اشتباهات رایج Pagination
65. تمرین‌های پروژه‌ای
66. چک‌لیست تسلط کارآموز
67. Cheat Sheet نهایی

---

# 1. هدف این فصل

در فصل‌های قبلی یاد گرفتیم چگونه در Django:

```text
URL → View → Model/ORM → Context → Template → Response
```

را اجرا کنیم.

اما یک پروژه واقعی فقط به نمایش HTML محدود نمی‌شود. وقتی اولین صفحه ساخته شد، خیلی زود با چند سؤال مواجه می‌شویم:

- این صفحه را چطور زیبا کنیم؟
- CSS را کجا قرار دهیم؟
- اگر ۱۰ صفحه داشته باشیم، Header را باید در هر ۱۰ فایل تکرار کنیم؟
- اگر کارت پست در چند صفحه استفاده شود چه؟
- اگر ۱۰۰ پست داشته باشیم، همه را در یک صفحه نشان دهیم؟
- اگر مسیر جزئیات پست عوض شد، باید همه لینک‌ها را دستی تغییر دهیم؟

این فصل برای پاسخ به همین سؤال‌هاست.

در پایان باید بتوانید یک پروژه Django را از یک صفحه ساده HTML به یک ساختار مرتب و قابل توسعه تبدیل کنید.

---

# 2. نقشه راه مباحث

مسیر این فصل عمداً مرحله‌ای است:

```text
HTML
  ↓
CSS
  ↓
Static Files
  ↓
base.html
  ↓
extends + block
  ↓
include
  ↓
URL Naming
  ↓
get_absolute_url
  ↓
Paginator
  ↓
Pagination Partial
```

در نتیجه هر مفهوم روی مفهوم قبل ساخته می‌شود.

---

# 3. قبل از CSS دقیقاً چه چیزی باید بدانیم؟

فرض کنید View داده زیر را به Template می‌دهد:

```python
posts = Post.objects.all()
```

Template می‌تواند بنویسد:

```django
{% for post in posts %}
    <h2>{{ post.title }}</h2>
{% endfor %}
```

این کد اطلاعات را نمایش می‌دهد، اما هیچ طراحی خاصی ندارد.

Browser چیزی شبیه این می‌بیند:

```text
عنوان اول
متن اول

عنوان دوم
متن دوم

عنوان سوم
متن سوم
```

HTML می‌گوید:

> چه چیزی روی صفحه وجود دارد؟

CSS می‌گوید:

> آن چیز چگونه دیده شود؟

پس در ذهن داشته باشید:

```text
HTML = ساختار و محتوا
CSS  = ظاهر و چیدمان
```

---

# 4. HTML و CSS چه تفاوتی دارند؟

مثال:

```html
<h1>سلام Django</h1>
```

این HTML فقط یک Heading ایجاد می‌کند.

حالا CSS:

```css
h1 {
    font-size: 40px;
    margin-bottom: 20px;
}
```

HTML می‌گوید عنصر چیست و CSS مشخص می‌کند چگونه نمایش داده شود.

در پروژه Blog:

```text
post_list.html
        ↓
      HTML
        ↓
style.css
        ↓
      ظاهر
```

---

# 5. Inline، Internal و External CSS

سه روش رایج داریم.

## 5.1 Inline CSS

```html
<h1 style="color: blue;">Django</h1>
```

CSS مستقیم داخل همان عنصر قرار گرفته است.

برای مثال‌های خیلی کوچک ممکن است قابل استفاده باشد، اما برای پروژه مناسب نیست.

### مشکل

اگر ۲۰ عنوان مشابه داشته باشیم، باید Style را بارها تکرار کنیم.

---

## 5.2 Internal CSS

```html
<head>
    <style>
        h1 {
            color: blue;
        }
    </style>
</head>
```

CSS در همان فایل HTML قرار گرفته است.

از Inline بهتر است، اما اگر چند Template داشته باشیم باز هم تکرار رخ می‌دهد.

---

## 5.3 External CSS

یک فایل مستقل:

```text
style.css
```

و سپس:

```html
<link rel="stylesheet" href="style.css">
```

این همان روشی است که در پروژه استفاده می‌کنیم.

مزیت اصلی:

```text
HTML → محتوا
CSS  → ظاهر
```

و این تفکیک بسیار تمیزتر است.

---

# 6. چرا فایل CSS جداگانه بهتر است؟

فرض کنید پروژه ۱۵ صفحه دارد.

بدون فایل CSS مشترک:

```text
page1.html → CSS
page2.html → CSS
page3.html → CSS
...
```

اما با فایل مشترک:

```text
style.css
   ↑
   ├── page1.html
   ├── page2.html
   ├── page3.html
   └── ...
```

حالا اگر رنگ اصلی سایت را تغییر دهیم، یک فایل را ویرایش می‌کنیم.

این همان ایدهٔ کلی:

> **Don't Repeat Yourself**

است.

---

# 7. CSS از صفر — Syntax

ساختار معمول CSS:

```css
selector {
    property: value;
}
```

مثلاً:

```css
h1 {
    color: red;
    font-size: 32px;
}
```

اجزای آن:

```text
h1       → Selector
color    → Property
red      → Value
```

و هر Declaration با `;` تمام می‌شود.

---

# 8. Selectorها

Selector مشخص می‌کند کدام عناصر تحت تأثیر CSS قرار بگیرند.

## 8.1 انتخاب بر اساس Tag

```css
p {
    color: gray;
}
```

تمام `p`ها را هدف می‌گیرد.

---

## 8.2 انتخاب بر اساس Class

HTML:

```html
<article class="post-card">...</article>
```

CSS:

```css
.post-card {
    padding: 20px;
}
```

برای پروژه‌های واقعی، Class یکی از مهم‌ترین ابزارهاست.

---

## 8.3 انتخاب بر اساس ID

```html
<div id="header">...</div>
```

```css
#header {
    ...
}
```

برای Styling عمومی معمولاً Class انتخاب بهتری است.

---

## 8.4 ترکیب Selectorها

```css
.post-card h2 {
    font-size: 22px;
}
```

یعنی هر `h2` داخل `.post-card`.

---

# 9. Property و Value

مثلاً:

```css
color: red;
```

`color` یک Property و `red` مقدار آن است.

چند Property بسیار مهم:

```css
color
background
font-size
font-weight
margin
padding
border
width
height
line-height
text-align
display
```

برای یادگیری CSS لازم نیست همه Propertyها را یک‌باره حفظ کنید. مهم این است که منطق انتخاب Property مناسب را یاد بگیرید.

---

# 10. رنگ، متن و فونت

مثال:

```css
body {
    color: #1f2937;
    background: #f5f7fb;
    font-family: Tahoma, Arial, sans-serif;
}
```

## رنگ متن

```css
color: #1f2937;
```

## رنگ پس‌زمینه

```css
background: #f5f7fb;
```

## اندازه متن

```css
font-size: 18px;
```

## ضخامت

```css
font-weight: 700;
```

## فاصله خطوط

```css
line-height: 1.8;
```

در متن فارسی، `line-height` مناسب اهمیت زیادی دارد.

---

# 11. Box Model

یکی از مهم‌ترین مفاهیم CSS، Box Model است.

هر عنصر را ساده‌شده می‌توان این‌طور دید:

```text
┌────────────────────────────┐
│          Margin            │
│  ┌──────────────────────┐  │
│  │       Border         │  │
│  │  ┌────────────────┐  │  │
│  │  │    Padding     │  │  │
│  │  │  ┌──────────┐  │  │  │
│  │  │  │ Content  │  │  │  │
│  │  │  └──────────┘  │  │  │
│  │  └────────────────┘  │  │
│  └──────────────────────┘  │
└────────────────────────────┘
```

ترتیب:

```text
Content
Padding
Border
Margin
```

---

# 12. margin، padding و border

## Padding

فاصله داخلی است.

```css
.post-card {
    padding: 20px;
}
```

یعنی محتوا از لبه کارت ۲۰ پیکسل فاصله دارد.

## Margin

فاصله بیرونی است.

```css
.post-card {
    margin-bottom: 20px;
}
```

یعنی کارت با عنصر بعدی ۲۰ پیکسل فاصله دارد.

## Border

مرز عنصر است.

```css
.post-card {
    border: 1px solid #e5e7eb;
}
```

---

# 13. اندازه‌ها در CSS

### px

```css
font-size: 16px;
```

برای شروع آموزشی بسیار ساده است.

### درصد

```css
width: 80%;
```

نسبت به والد محاسبه می‌شود.

### rem

```css
font-size: 1.2rem;
```

برای طراحی‌های مقیاس‌پذیر مفید است.

### vw و vh

```css
width: 80vw;
```

نسبت به Viewport.

در این پروژه بیشتر از `px`, `%` و `min()` / `calc()` استفاده کرده‌ایم تا کد برای کارآموز قابل فهم بماند.

---

# 14. display و مفهوم چیدمان

Property مهم:

```css
display
```

مقادیر مهم:

```text
block
inline
inline-block
flex
grid
none
```

دو موردی که در پروژه زیاد می‌بینیم:

```css
display: flex;
display: grid;
```

---

# 15. Flexbox به زبان ساده

وقتی چند عنصر می‌خواهیم کنار هم قرار بگیرند، Flexbox بسیار کاربردی است.

HTML:

```html
<div class="header-inner">
    <div>Logo</div>
    <nav>Menu</nav>
</div>
```

CSS:

```css
.header-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
```

مفهوم:

```text
display: flex
    ↓
فرزندان را در یک Flex Container قرار می‌دهد
```

### `justify-content`

برای توزیع در محور اصلی.

```css
justify-content: space-between;
```

### `align-items`

برای تراز محور دیگر.

```css
align-items: center;
```

### gap

```css
gap: 12px;
```

برای فاصله بین فرزندان.

---

# 16. Grid به زبان ساده

برای کارت‌های Blog بسیار مناسب است.

```css
.post-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 20px;
}
```

یعنی:

```text
┌───────────┐ ┌───────────┐
│   Post    │ │   Post    │
└───────────┘ └───────────┘

┌───────────┐ ┌───────────┐
│   Post    │ │   Post    │
└───────────┘ └───────────┘
```

و در موبایل:

```css
@media (max-width: 760px) {
    .post-grid {
        grid-template-columns: 1fr;
    }
}
```

پس:

```text
Desktop → دو ستون
Mobile  → یک ستون
```

---

# 17. Pseudo-classهای مهم

برای رفتارهایی مثل Hover:

```css
.post-card h2 a:hover {
    color: blue;
}
```

`:hover` یعنی وقتی نشانگر روی عنصر قرار می‌گیرد.

یکی از بهترین راه‌های شروع تعامل ظاهری بدون JavaScript همین است.

---

# 18. Cascade، Specificity و ترتیب قوانین

ممکن است چند قانون یک عنصر را هدف بگیرند.

مثلاً:

```css
h2 {
    color: black;
}

.post-card h2 {
    color: blue;
}
```

Selector دوم اختصاصی‌تر است.

کارآموز در مرحله اول بهتر است این اصل را به خاطر بسپارد:

```text
هرچه Selector اختصاصی‌تر باشد، معمولاً قدرت بیشتری دارد.
```

و بهتر است تا جای ممکن CSS را ساده و قابل پیش‌بینی نگه داریم و بی‌دلیل از `!important` استفاده نکنیم.

---

# 19. Responsive Design

صفحه باید روی موبایل هم قابل استفاده باشد.

Media Query:

```css
@media (max-width: 760px) {
    .post-grid {
        grid-template-columns: 1fr;
    }
}
```

مفهوم:

> اگر عرض صفحه حداکثر ۷۶۰ پیکسل بود، این قوانین را اعمال کن.

در پروژه ما همین تکنیک برای Header، Grid و جزئیات پست استفاده شده است.

---

# 20. Static Files در Django

حالا از CSS عمومی وارد Django می‌شویم.

Django بین چند نوع فایل تفاوت مفهومی قائل می‌شود. یکی از مهم‌ترین‌ها **Static Files** هستند.

نمونه:

```text
CSS
JavaScript
تصاویر ثابت
آیکون‌ها
```

برای CSS پروژه، مسیر زیر را ساخته‌ایم:

```text
blog/
└── static/
    └── blog/
        └── css/
            └── style.css
```

---

# 21. ساختار استاندارد پوشه static

در این پروژه چون `static` داخل خود App یعنی `blog` قرار دارد و `django.contrib.staticfiles` فعال است، لازم نیست برای همین پوشه در `STATICFILES_DIRS` دوباره مسیری تعریف کنیم.

تنظیم اصلی پروژه برای شروع توسعه این است:

```python
STATIC_URL = 'static/'
```

`STATICFILES_DIRS` معمولاً زمانی کاربرد پیدا می‌کند که بخواهیم علاوه بر Staticهای داخل Appها، پوشه‌های Static دیگری را هم معرفی کنیم.

ساختار App:

```text
blog/
├── static/
│   └── blog/
│       └── css/
│           └── style.css
│
├── templates/
│   └── blog/
│       └── base.html
│
├── models.py
├── views.py
└── urls.py
```

چرا دوباره `blog` داخل static آمده است؟

چون اگر چند App داشته باشیم:

```text
blog/static/blog/...
shop/static/shop/...
news/static/news/...
```

نام‌گذاری‌ها منظم‌تر می‌شوند.

---

# 22. `{% load static %}` و `{% static %}`

در Template:

```django
{% load static %}
```

یعنی Tagهای مربوط به Static را در این Template در دسترس قرار بده.

سپس:

```django
{% static 'blog/css/style.css' %}
```

آدرس مناسب فایل را ایجاد می‌کند.

---

# 23. اتصال CSS خارجی به Template

در `base.html` پروژه:

```django
{% load static %}
```

و داخل `<head>`:

```html
<link rel="stylesheet" href="{% static 'blog/css/style.css' %}">
```

پس Browser در نهایت یک URL برای فایل CSS دریافت می‌کند.

فرآیند را این‌طور ببینید:

```text
base.html
   ↓
static tag
   ↓
style.css
   ↓
Browser
   ↓
صفحه Style می‌گیرد
```

---

# 24. Template Inheritance چیست؟

فرض کنید سایت ۱۰ صفحه دارد و Header در همه یکی است.

روش بد:

```text
header در page1
header در page2
header در page3
...
```

روش بهتر:

```text
base.html
   ↓
-----------------
صفحه‌های مختلف
```

این مفهوم را **Template Inheritance** می‌نامیم.

---

# 25. base.html

قالب پایه معمولاً شامل بخش‌های مشترک سایت است:

```html
<!DOCTYPE html>
<html>
<head>
    ...
</head>
<body>
    <header>...</header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>...</footer>
</body>
</html>
```

در پروژه Blog ما Header، لینک CSS، Footer و ساختار کلی HTML را در `base.html` قرار داده‌ایم.

---

# 26. extends

Child Template می‌گوید:

```django
{% extends 'blog/base.html' %}
```

یعنی:

> من ساختار اصلی صفحه را از `base.html` می‌گیرم و فقط بخش‌های مشخص‌شده را پر می‌کنم.

مثلاً:

```django
{% extends 'blog/base.html' %}

{% block content %}
    <h1>آخرین نوشته‌ها</h1>
{% endblock %}
```

---

# 27. block

در Base:

```django
{% block title %}بلاگ{% endblock %}
```

و:

```django
{% block content %}{% endblock %}
```

در Child:

```django
{% block title %}فهرست پست‌ها{% endblock %}
```

و:

```django
{% block content %}
    ...
{% endblock %}
```

`block` را به‌عنوان یک **جای خالی قابل پر کردن** تصور کنید.

---

# 28. رابطه بین extends و block

این دو معمولاً با هم استفاده می‌شوند:

```text
base.html
  ├── block title
  └── block content
          ↑
          │
          └── child template
```

بدون `block`، Child نمی‌داند کجا محتوای اختصاصی خود را قرار دهد.

بدون `extends` نیز چیزی برای ارث‌بری ندارد.

---

# 29. include چیست؟

`include` برای وارد کردن یک Template کوچک داخل Template دیگر است.

مثلاً:

```django
{% include 'blog/partials/post_card.html' %}
```

می‌توانید به `include` مانند یک قطعه HTML قابل استفاده مجدد فکر کنید.

---

# 30. تفاوت include و extends

این تفاوت بسیار مهم است.

## extends

برای **ساختار صفحه** است.

```text
base.html
    ↓
extends
page.html
```

## include

برای **قطعه قابل استفاده مجدد** است.

```text
post_list.html
    ↓
include
    ↓
post_card.html
```

به زبان ساده:

```text
extends = صفحه از چه Layoutی استفاده می‌کند؟
include = داخل صفحه چه قطعه تکرارشونده‌ای قرار می‌گیرد؟
```

---

# 31. ارسال Context به include

می‌توانیم Context مشخص ارسال کنیم:

```django
{% include 'blog/partials/post_card.html' with post=post %}
```

در فایل Included:

```django
{{ post.title }}
```

این یعنی:

```text
Template اصلی
      ↓
post = یک Post
      ↓
include
      ↓
post_card.html
```

---

# 32. ساخت Component ساده با include

فرض کنید کارت پست چنین چیزی است:

```html
<article class="post-card">
    <h2>{{ post.title }}</h2>
    <p>{{ post.body|truncatewords:24 }}</p>
</article>
```

به جای اینکه این HTML را چند بار تکرار کنیم، فایل:

```text
blog/templates/blog/partials/post_card.html
```

را می‌سازیم.

سپس:

```django
{% for post in page_obj %}
    {% include 'blog/partials/post_card.html' with post=post %}
{% endfor %}
```

حالا کارت یک Component ساده و قابل استفاده مجدد شده است.

---

# 33. چرا Partialها مهم هستند؟

وقتی پروژه بزرگ‌تر شود، Template اصلی نباید هزار خط HTML داشته باشد.

مثلاً:

```text
templates/blog/
├── base.html
├── post_list.html
├── post_detail.html
└── partials/
    ├── post_card.html
    └── pagination.html
```

این ساختار باعث می‌شود خواندن پروژه آسان‌تر شود.

---

# 34. URL Naming و `{% url %}`

قبلاً یاد گرفتیم برای URL نام تعریف کنیم:

```python
path('post/<int:pk>/', views.post_detail, name='post_detail')
```

و در App:

```python
app_name = 'blog'
```

در Template:

```django
{% url 'blog:post_detail' post.pk %}
```

به جای هاردکد کردن:

```html
<a href="/post/5/">...</a>
```

از Name استفاده می‌کنیم.

---

# 35. reverse() در Django

در Python می‌توانیم URL دارای Name را با `reverse()` تولید کنیم.

مثال:

```python
from django.urls import reverse

url = reverse('blog:post_detail', kwargs={'pk': 5})
```

خروجی مفهومی:

```text
/post/5/
```

پس:

```text
{% url ... %}
```

برای Template مناسب است و:

```python
reverse(...)
```

برای Python مناسب است.

---

# 36. get_absolute_url() چیست؟

یکی از الگوهای مفید در Model این است که مدل بداند URL اصلی نمایش خودش چیست.

مثلاً در `Post`:

```python
class Post(models.Model):
    ...

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.pk}
        )
```

یعنی اگر Post شماره 7 باشد:

```python
post.pk == 7
```

آنگاه:

```python
post.get_absolute_url()
```

آدرس صفحه جزئیات همان Post را تولید می‌کند.

---

# 37. ساخت get_absolute_url در Model

کد کامل پروژه:

```python
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.pk},
        )
```

سه قسمت اصلی را ببینید:

```python
from django.urls import reverse
```

سپس:

```python
def get_absolute_url(self):
```

و درون آن:

```python
return reverse(
    'blog:post_detail',
    kwargs={'pk': self.pk},
)
```

---

# 38. استفاده از get_absolute_url در View و Template

در Python:

```python
post.get_absolute_url()
```

اما در Django Template معمولاً پرانتز نمی‌نویسیم:

```django
{{ post.get_absolute_url }}
```

برای لینک:

```html
<a href="{{ post.get_absolute_url }}">
    مشاهده پست
</a>
```

در پروژه ما همین روش در `post_card.html` استفاده شده است:

```django
<a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
```

و:

```django
<a href="{{ post.get_absolute_url }}">مطالعه پست ←</a>
```

---

# 39. چرا get_absolute_url از URL هاردکد بهتر است؟

روش هاردکد:

```html
<a href="/post/{{ post.pk }}/">...
```

این کد ممکن است کار کند، اما مسیر URL را در Template تکرار می‌کنیم.

با `get_absolute_url`:

```html
<a href="{{ post.get_absolute_url }}">...</a>
```

Template دیگر لازم نیست ساختار URL را بداند.

مدل می‌گوید:

> URL اصلی من این است.

این مزیت زمانی واضح‌تر می‌شود که مسیر URL تغییر کند.

مثلاً:

```text
/post/5/
```

به:

```text
articles/5/
```

در حالت مناسب، Route و Model را هماهنگ می‌کنیم و مجبور نیستیم تمام Templateها را برای پیدا کردن `/post/` جستجو کنیم.

---

# 40. Pagination چیست؟

فرض کنید 1000 Post داریم.

اگر View همه را بگیرد:

```python
posts = Post.objects.all()
```

و همه را نمایش دهد، یک صفحه بسیار بزرگ خواهیم داشت.

Pagination یعنی:

```text
1000 پست
   ↓
هر صفحه 10 پست
   ↓
100 صفحه
```

مثلاً:

```text
صفحه 1 → پست 1 تا 10
صفحه 2 → پست 11 تا 20
صفحه 3 → پست 21 تا 30
```

---

# 41. چرا Pagination مهم است؟

Pagination دو جنبه دارد:

### رابط کاربری

کاربر لازم نیست بین صدها پست اسکرول کند.

### مدیریت داده

تعداد آیتم‌هایی که برای یک صفحه نمایش می‌دهیم کنترل می‌شود.

البته Pagination به تنهایی همه مسائل Performance را حل نمی‌کند، اما یک الگوی مهم برای صفحات فهرستی است.

---

# 42. Paginator در Django

Django ابزار آماده‌ای دارد:

```python
from django.core.paginator import Paginator
```

ساختار ساده:

```python
paginator = Paginator(posts, 10)
```

یعنی:

```text
posts → داده اصلی
10    → تعداد آیتم در هر صفحه
```

سپس یک صفحه می‌گیریم.

---

# 43. Page Object چیست؟

نتیجه `get_page()` یک شیء Page می‌دهد.

مثلاً:

```python
page_obj = paginator.get_page(2)
```

`page_obj` اطلاعاتی درباره صفحه فعلی دارد، از جمله:

```text
number
has_previous()
previous_page_number()
has_next()
next_page_number()
paginator
```

و خود `page_obj` قابل Iteration است:

```django
{% for post in page_obj %}
```

---

# 44. ساخت Pagination در View — مرحله‌به‌مرحله

View ساده اولیه:

```python
def post_list(request):
    posts = Post.objects.select_related('author').all()
    return render(
        request,
        'blog/post_list.html',
        {'posts': posts},
    )
```

حالا قدم‌به‌قدم تغییرش می‌دهیم.

## مرحله 1 — Import

```python
from django.core.paginator import Paginator
```

## مرحله 2 — QuerySet

```python
posts = Post.objects.select_related('author').all()
```

## مرحله 3 — ساخت Paginator

```python
paginator = Paginator(posts, 4)
```

یعنی هر صفحه ۴ پست.

## مرحله 4 — خواندن شماره صفحه

```python
page_number = request.GET.get('page')
```

مثلاً URL:

```text
/?page=3
```

مقدار:

```text
page_number = '3'
```

## مرحله 5 — گرفتن صفحه

```python
page_obj = paginator.get_page(page_number)
```

## مرحله 6 — Context

```python
context = {
    'page_obj': page_obj,
}
```

## مرحله 7 — Render

```python
return render(
    request,
    'blog/post_list.html',
    context,
)
```

---

# 45. `request.GET.get('page')`

URL:

```text
/?page=2
```

قسمت Query String این است:

```text
page=2
```

در Django:

```python
request.GET
```

یک QueryDict است.

و:

```python
request.GET.get('page')
```

مقدار `page` را می‌دهد.

پس:

```python
page_number = request.GET.get('page')
```

یعنی:

> شماره صفحه‌ای که کاربر از طریق URL درخواست کرده را بخوان.

---

# 46. `get_page()` و مدیریت مقدار نامعتبر

مزیت مهم:

```python
paginator.get_page(page_number)
```

این است که برای ورودی‌های نامعتبر رفتار ساده‌تری دارد.

مثلاً:

```text
/?page=abc
```

یا:

```text
/?page=99999
```

برای آموزش Pagination معمولاً `get_page()` گزینه‌ای ساده و مناسب است.

---

# 47. متغیرهای مهم Page Object

## شماره فعلی

```django
{{ page_obj.number }}
```

## تعداد صفحات

```django
{{ page_obj.paginator.num_pages }}
```

## آیا صفحه قبلی وجود دارد؟

```django
{% if page_obj.has_previous %}
```

## شماره صفحه قبلی

```django
{{ page_obj.previous_page_number }}
```

## آیا صفحه بعدی وجود دارد؟

```django
{% if page_obj.has_next %}
```

## شماره صفحه بعدی

```django
{{ page_obj.next_page_number }}
```

## محدوده شماره صفحات

```django
{% for number in page_obj.paginator.page_range %}
```

---

# 48. ساخت رابط Pagination در Template

یک Pagination ساده:

```django
{% if page_obj.has_previous %}
    <a href="?page={{ page_obj.previous_page_number }}">قبلی</a>
{% endif %}

<span>
    صفحه {{ page_obj.number }} از {{ page_obj.paginator.num_pages }}
</span>

{% if page_obj.has_next %}
    <a href="?page={{ page_obj.next_page_number }}">بعدی</a>
{% endif %}
```

حالا می‌توانیم شماره صفحات را هم نشان دهیم:

```django
{% for number in page_obj.paginator.page_range %}
    {% if number == page_obj.number %}
        <span>{{ number }}</span>
    {% else %}
        <a href="?page={{ number }}">{{ number }}</a>
    {% endif %}
{% endfor %}
```

---

# 49. تبدیل Pagination به Partial با include

بهتر است Pagination در فایل اصلی پخش نشود.

فایل:

```text
blog/templates/blog/partials/pagination.html
```

سپس در `post_list.html`:

```django
{% include 'blog/partials/pagination.html' with page_obj=page_obj %}
```

این یک مثال کامل برای کنار هم قرار گرفتن دو مفهوم است:

```text
Pagination
   +
include
   ↓
pagination.html
```

---

# 50. ساخت پروژه از صفر تا نسخه نهایی

حالا تمام مباحث را به‌صورت یک سناریوی واقعی اجرا می‌کنیم.

هدف نهایی:

```text
Blog
├── Header مشترک
├── CSS خارجی
├── کارت پست
├── صفحه جزئیات
└── Pagination
```

ساختار:

```text
blogApp_MVT_Django_Styled/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── blogapp1/
│   ├── settings.py
│   └── urls.py
│
└── blog/
    ├── models.py
    ├── views.py
    ├── urls.py
    │
    ├── templates/
    │   └── blog/
    │       ├── base.html
    │       ├── post_list.html
    │       ├── post_detail.html
    │       └── partials/
    │           ├── post_card.html
    │           └── pagination.html
    │
    └── static/
        └── blog/
            └── css/
                └── style.css
```

---

# 51. مرحله اول — HTML ساده

اگر قبل از CSS بخواهیم فقط HTML بسازیم، می‌توانیم داشته باشیم:

```django
{% for post in posts %}
    <article>
        <h2>{{ post.title }}</h2>
        <p>{{ post.body }}</p>
    </article>
{% endfor %}
```

این نسخه برای فهم MVT کافی است.

اما برای پروژه آموزشی ما ظاهر حرفه‌ای‌تری لازم است تا کارآموز تفاوت CSS را ببیند.

---

# 52. مرحله دوم — اضافه کردن CSS خارجی

ابتدا:

```text
blog/static/blog/css/style.css
```

را می‌سازیم.

سپس در Base:

```django
{% load static %}
```

و:

```html
<link rel="stylesheet" href="{% static 'blog/css/style.css' %}">
```

حالا تمام صفحات فرزند که `base.html` را Extend کنند، همین CSS را دریافت می‌کنند.

این نکته بسیار مهم است:

> CSS مشترک را لازم نیست در همه Templateها دوباره Link کنیم؛ یک بار در Base کافی است.

---

# 53. مرحله سوم — ساخت base.html

Base پروژه ما تقریباً این ساختار را دارد:

```html
{% load static %}
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}بلاگ ساده Django{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'blog/css/style.css' %}">
</head>
<body>
    <header class="site-header">
        ...
    </header>

    <main class="container main-content">
        {% block content %}{% endblock %}
    </main>

    <footer class="site-footer">
        ...
    </footer>
</body>
</html>
```

فرزندان فقط بخش‌های موردنیاز را پر می‌کنند.

---

# 54. مرحله چهارم — ساخت کارت پست با include

فایل:

```text
partials/post_card.html
```

کد:

```django
<article class="post-card">
    <div class="post-card-top">
        <span class="badge">Django</span>
        <span class="date">{{ post.created_at|date:'Y/m/d' }}</span>
    </div>

    <h2>
        <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
    </h2>

    <p>{{ post.body|truncatewords:24 }}</p>

    <div class="post-card-bottom">
        <span class="author">{{ post.author.username }}</span>
        <a class="read-more" href="{{ post.get_absolute_url }}">مطالعه پست ←</a>
    </div>
</article>
```

سپس در لیست:

```django
{% for post in page_obj %}
    {% include 'blog/partials/post_card.html' with post=post %}
{% endfor %}
```

اکنون `post_list.html` خواناتر شده است.

---

# 55. مرحله پنجم — اضافه کردن get_absolute_url

در Model:

```python
from django.urls import reverse
```

و:

```python
def get_absolute_url(self):
    return reverse(
        'blog:post_detail',
        kwargs={'pk': self.pk},
    )
```

اکنون Template:

```django
<a href="{{ post.get_absolute_url }}">
```

و دیگر ساختار URL را هاردکد نمی‌کند.

---

# 56. مرحله ششم — اضافه کردن Pagination

در View:

```python
from django.core.paginator import Paginator
```

سپس:

```python
posts = Post.objects.select_related('author').all()
paginator = Paginator(posts, 4)
page_number = request.GET.get('page')
page_obj = paginator.get_page(page_number)
```

Context:

```python
context = {
    'page_obj': page_obj,
}
```

در Template:

```django
{% for post in page_obj %}
```

و در پایان:

```django
{% include 'blog/partials/pagination.html' with page_obj=page_obj %}
```

---

# 57. مرحله هفتم — تمیز کردن پروژه

در پایان باید مسئولیت‌ها تقریباً این‌طور تقسیم شده باشند:

```text
Model
 └── داده + get_absolute_url

View
 └── Query + Pagination + Context

Template
 └── نمایش

base.html
 └── Layout مشترک

partials/
 └── قطعات تکرارشونده

style.css
 └── ظاهر
```

این همان چیزی است که می‌خواهیم کارآموز از این فصل یاد بگیرد.

---

# 58. تشریح کامل فایل‌های پروژه

## `models.py`

```python
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.pk},
        )
```

---

## `views.py`

```python
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Post


POSTS_PER_PAGE = 4


def post_list(request):
    posts = Post.objects.select_related('author').all()

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related('author'),
        pk=pk,
    )

    context = {
        'post': post,
    }

    return render(request, 'blog/post_detail.html', context)
```

نکته آموزشی مهم:

عدد `4` را مستقیماً در View پخش نکرده‌ایم. آن را در Constant گذاشته‌ایم:

```python
POSTS_PER_PAGE = 4
```

این کد هم خواناتر است و هم تغییر آن آسان‌تر.

---

## `post_list.html`

```django
{% extends 'blog/base.html' %}

{% block title %}فهرست پست‌ها | Django Blog{% endblock %}

{% block content %}
<section class="page-intro">
    <span class="eyebrow">Django + Template + CSS</span>
    <h1>آخرین نوشته‌ها</h1>
    <p>در این صفحه چند مفهوم مهم را با هم می‌بینیم.</p>
</section>

<section class="post-grid">
    {% for post in page_obj %}
        {% include 'blog/partials/post_card.html' with post=post %}
    {% empty %}
        <div class="empty-state">
            <h2>هنوز پستی نداریم</h2>
        </div>
    {% endfor %}
</section>

{% include 'blog/partials/pagination.html' with page_obj=page_obj %}
{% endblock %}
```

در یک فایل کوچک، چند مفهوم مهم با هم استفاده شده‌اند:

```text
extends
block
for
empty
include
```

---

## `post_detail.html`

```django
{% extends 'blog/base.html' %}

{% block title %}{{ post.title }} | Django Blog{% endblock %}

{% block content %}
<article class="post-detail">
    <div class="post-detail-head">
        <span class="badge">پست آموزشی</span>
        <h1>{{ post.title }}</h1>
        <div class="meta-row">
            <span>نویسنده: {{ post.author.username }}</span>
            <span>تاریخ: {{ post.created_at|date:'Y/m/d H:i' }}</span>
        </div>
    </div>

    <div class="post-body">
        {{ post.body|linebreaks }}
    </div>

    <div class="back-row">
        <a class="button button-light" href="{% url 'blog:post_list' %}">
            ← بازگشت به پست‌ها
        </a>
    </div>
</article>
{% endblock %}
```

---

## `post_card.html`

```django
<article class="post-card">
    <div class="post-card-top">
        <span class="badge">Django</span>
        <span class="date">{{ post.created_at|date:'Y/m/d' }}</span>
    </div>

    <h2>
        <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
    </h2>

    <p>{{ post.body|truncatewords:24 }}</p>

    <div class="post-card-bottom">
        <span class="author">{{ post.author.username }}</span>
        <a class="read-more" href="{{ post.get_absolute_url }}">مطالعه پست ←</a>
    </div>
</article>
```

---

## `pagination.html`

```django
{% if page_obj.paginator.num_pages > 1 %}
<nav class="pagination" aria-label="صفحه‌بندی">
    <div class="pagination-summary">
        صفحه {{ page_obj.number }} از {{ page_obj.paginator.num_pages }}
    </div>

    <div class="pagination-links">
        {% if page_obj.has_previous %}
            <a class="page-link" href="?page=1">اول</a>
            <a class="page-link" href="?page={{ page_obj.previous_page_number }}">قبلی</a>
        {% else %}
            <span class="page-link disabled">اول</span>
            <span class="page-link disabled">قبلی</span>
        {% endif %}

        {% for number in page_obj.paginator.page_range %}
            {% if number == page_obj.number %}
                <span class="page-link active">{{ number }}</span>
            {% else %}
                <a class="page-link" href="?page={{ number }}">{{ number }}</a>
            {% endif %}
        {% endfor %}

        {% if page_obj.has_next %}
            <a class="page-link" href="?page={{ page_obj.next_page_number }}">بعدی</a>
            <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">آخر</a>
        {% else %}
            <span class="page-link disabled">بعدی</span>
            <span class="page-link disabled">آخر</span>
        {% endif %}
    </div>
</nav>
{% endif %}
```

---

# 59. اشتباهات رایج CSS

## اشتباه 1 — نوشتن CSS روی Tag بدون نیاز

به جای اینکه همه `h2`های پروژه را کنترل کنیم، بهتر است برای اجزای خاص Class تعریف کنیم:

```css
.post-card h2 { ... }
```

نه اینکه فقط:

```css
h2 { ... }
```

وقتی پروژه بزرگ‌تر شد، Selector عمومی ممکن است ناخواسته روی بخش‌های دیگر اثر بگذارد.

---

## اشتباه 2 — استفاده بیش از حد از `!important`

این:

```css
color: red !important;
```

ممکن است در کوتاه‌مدت مشکل را پنهان کند، اما در بلندمدت Debug کردن CSS را سخت می‌کند.

---

## اشتباه 3 — قاطی کردن وظایف HTML و CSS

مثلاً:

```html
<h1 style="color:red; margin:20px;">...</h1>
```

در پروژه آموزشی ما ترجیح می‌دهیم:

```html
<h1 class="page-title">...</h1>
```

و:

```css
.page-title {
    color: red;
    margin: 20px;
}
```

---

# 60. اشتباهات رایج Static Files

## خطای رایج 1 — فراموش کردن load static

اگر بنویسیم:

```django
{% static 'blog/css/style.css' %}
```

ولی:

```django
{% load static %}
```

نداشته باشیم، Template نمی‌تواند Tag را بشناسد.

---

## خطای رایج 2 — مسیر اشتباه

ساختار:

```text
blog/static/blog/css/style.css
```

پس داخل Static Tag:

```django
{% static 'blog/css/style.css' %}
```

و نه:

```django
{% static 'css/style.css' %}
```

---

## خطای رایج 3 — Link کردن فایل محلی با مسیر اشتباه

در پروژه Django بهتر است مسیر Static را با Tag مربوط به Static بسازیم:

```django
<link rel="stylesheet" href="{% static 'blog/css/style.css' %}">
```

---

# 61. اشتباهات رایج extends و block

## اشتباه 1 — فراموش کردن extends

Child Template:

```django
{% block content %}
...
{% endblock %}
```

اما هیچ:

```django
{% extends 'blog/base.html' %}
```

وجود ندارد.

در این حالت ارث‌بری موردنظر شما انجام نمی‌شود.

---

## اشتباه 2 — نام Block متفاوت

Base:

```django
{% block content %}{% endblock %}
```

Child:

```django
{% block main %}
...
{% endblock %}
```

این دو نام یکسان نیستند.

---

# 62. اشتباهات رایج include

## اشتباه 1 — Template path اشتباه

```django
{% include 'blog/card.html' %}
```

در حالی که فایل واقعاً اینجاست:

```text
blog/templates/blog/partials/post_card.html
```

پس باید:

```django
{% include 'blog/partials/post_card.html' %}
```

باشد.

---

## اشتباه 2 — Context اشتباه

اگر Include انتظار دارد:

```django
{{ post.title }}
```

ولی شما متغیر دیگری ارسال کرده‌اید، داده مورد انتظار نمایش داده نمی‌شود.

روش واضح:

```django
{% include 'blog/partials/post_card.html' with post=post %}
```

---

# 63. اشتباهات رایج get_absolute_url

## خطای 1 — Import نکردن reverse

باید:

```python
from django.urls import reverse
```

داشته باشیم.

---

## خطای 2 — URL name اشتباه

Route:

```python
name='post_detail'
```

و:

```python
app_name = 'blog'
```

پس:

```python
reverse('blog:post_detail', kwargs={'pk': self.pk})
```

درست است.

---

## خطای 3 — گذاشتن پرانتز در Template

در Python:

```python
post.get_absolute_url()
```

در Template:

```django
{{ post.get_absolute_url }}
```

---

# 64. اشتباهات رایج Pagination

## اشتباه 1 — حلقه روی QuerySet به جای Page

اگر Pagination ساخته‌ایم:

```python
page_obj = paginator.get_page(page_number)
```

Template بهتر است:

```django
{% for post in page_obj %}
```

باشد.

---

## اشتباه 2 — ساختن Pagination بدون خواندن شماره صفحه

فقط:

```python
Paginator(posts, 4)
```

کافی نیست.

باید شماره صفحه درخواست‌شده را نیز بگیریم و Page را تولید کنیم:

```python
page_number = request.GET.get('page')
page_obj = paginator.get_page(page_number)
```

---

## اشتباه 3 — نبودن شرط has_next / has_previous

نباید همیشه لینک «بعدی» تولید کنیم.

باید:

```django
{% if page_obj.has_next %}
```

را بررسی کنیم.

---

# 65. تمرین‌های پروژه‌ای

## تمرین 1 — تغییر تعداد پست هر صفحه

در View:

```python
POSTS_PER_PAGE = 4
```

را به 3 تغییر دهید.

انتظار:

```text
صفحه 1 → 3 پست
صفحه 2 → 3 پست
...
```

---

## تمرین 2 — تغییر رنگ اصلی

در CSS متغیر:

```css
:root {
    --primary: #3157d5;
}
```

را تغییر دهید و اثر آن را روی Button، Badge و Pagination ببینید.

این تمرین برای فهم مفهوم CSS Variable مناسب است.

---

## تمرین 3 — اضافه کردن Category به Card

فرض کنید Model بعداً فیلدی به نام Category داشته باشد.

در `post_card.html` یک Badge جدید اضافه کنید.

---

## تمرین 4 — Pagination شماره‌ای را حذف کنید

فقط این‌ها را نگه دارید:

```text
قبلی | صفحه X از Y | بعدی
```

هدف تمرین این است که Template را بدون وابستگی به `page_range` ساده‌تر کنید.

---

## تمرین 5 — ساخت یک Partial جدید

یک فایل:

```text
partials/site_message.html
```

بسازید و یک پیام ساده از آن نمایش دهید.

سپس در `post_list.html` از:

```django
{% include ... %}
```

استفاده کنید.

---

## تمرین 6 — تغییر مسیر URL

مسیر:

```python
path('post/<int:pk>/', ...)
```

را به مثلاً:

```python
path('articles/<int:pk>/', ...)
```

تغییر دهید.

سپس بررسی کنید کدام لینک‌های پروژه به‌واسطه `get_absolute_url` نیازی به تغییر مستقیم ندارند.

این تمرین یکی از بهترین راه‌های فهم مزیت URL Abstraction است.

---

# 66. چک‌لیست تسلط کارآموز

کارآموز پس از این فصل باید بتواند بدون کمک توضیح دهد:

### CSS

- Selector چیست؟
- Class چیست؟
- `margin` و `padding` چه تفاوتی دارند؟
- Flexbox برای چه کاری مناسب است؟
- Grid برای چه کاری مناسب است؟
- Media Query چیست؟

### Django Static

- Static File چیست؟
- چرا CSS را در `static` قرار می‌دهیم؟
- `{% load static %}` چه کاری می‌کند؟
- `{% static '...' %}` چه کاربردی دارد؟

### Template Inheritance

- `base.html` چیست؟
- `extends` چه می‌کند؟
- `block` چه می‌کند؟

### include

- `include` چیست؟
- چه زمانی باید Partial بسازیم؟
- چطور Context به Include بدهیم؟

### URL

- URL Name چیست؟
- `{% url %}` چه تفاوتی با URL هاردکد دارد؟
- `reverse()` چیست؟
- `get_absolute_url()` چیست؟

### Pagination

- `Paginator` چیست؟
- `page_obj` چیست؟
- `has_next` و `has_previous` چه می‌گویند؟
- `request.GET.get('page')` چه چیزی می‌خواند؟

اگر کارآموز بتواند این موارد را با کد توضیح دهد، این فصل را واقعاً فهمیده است.

---

# 67. Cheat Sheet نهایی

## CSS خارجی

```html
{% load static %}
<link rel="stylesheet" href="{% static 'blog/css/style.css' %}">
```

## Base Template

```html
{% block content %}{% endblock %}
```

## Child Template

```django
{% extends 'blog/base.html' %}

{% block content %}
...
{% endblock %}
```

## Include

```django
{% include 'blog/partials/post_card.html' with post=post %}
```

## URL Name

```python
path('post/<int:pk>/', views.post_detail, name='post_detail')
```

## URL در Template

```django
{% url 'blog:post_detail' post.pk %}
```

## reverse

```python
reverse('blog:post_detail', kwargs={'pk': self.pk})
```

## get_absolute_url

```python
def get_absolute_url(self):
    return reverse(
        'blog:post_detail',
        kwargs={'pk': self.pk},
    )
```

## لینک با get_absolute_url

```django
<a href="{{ post.get_absolute_url }}">
    {{ post.title }}
</a>
```

## Paginator

```python
paginator = Paginator(posts, 4)
page_number = request.GET.get('page')
page_obj = paginator.get_page(page_number)
```

## نمایش Page

```django
{% for post in page_obj %}
    ...
{% endfor %}
```

## صفحه بعدی

```django
{% if page_obj.has_next %}
    {{ page_obj.next_page_number }}
{% endif %}
```

## صفحه قبلی

```django
{% if page_obj.has_previous %}
    {{ page_obj.previous_page_number }}
{% endif %}
```

---

# جمع‌بندی نهایی

در این فصل چند ابزار ظاهراً جدا را کنار هم قرار دادیم:

```text
CSS
 ↓
Static Files
 ↓
base.html
 ↓
extends / block
 ↓
include / partial
 ↓
URL Naming
 ↓
get_absolute_url
 ↓
Paginator
 ↓
Pagination Partial
```

اما از دید معماری، هنوز همان MVT را داریم:

```text
Browser
   ↓
URL
   ↓
View
   ↓
Model / ORM
   ↓
Context
   ↓
Template
   ↓
HTML + CSS
   ↓
Browser
```

تفاوت اصلی این است که اکنون Template ما سازمان‌یافته‌تر شده است.

`base.html` ساختار مشترک را نگه می‌دارد.

`extends` صفحات مختلف را روی Base می‌سازد.

`include` قسمت‌های تکرارشونده را جدا می‌کند.

`static` فایل CSS را مدیریت می‌کند.

`get_absolute_url` مسئول تولید URL استاندارد یک Object است.

`Paginator` لیست بزرگ را به Pageهای کوچک‌تر تقسیم می‌کند.

و در نهایت همه این‌ها در یک پروژه واقعی کنار هم کار می‌کنند.

> **هدف این فصل حفظ کردن چند Tag نیست؛ هدف این است که کارآموز بتواند یک Feature واقعی Django را تمیز، قابل فهم و قابل توسعه پیاده‌سازی کند.**

---

# پیوست A — ترتیب پیشنهادی تدریس در کلاس

برای اینکه کارآموز گیج نشود، این فصل را یک‌باره تدریس نکنید. ترتیب پیشنهادی:

```text
جلسه 1
CSS پایه
↓
Selector + Box Model + Flex + Grid

جلسه 2
Static Files
↓
style.css + {% static %}

جلسه 3
Template Inheritance
↓
base + extends + block

جلسه 4
include
↓
post_card + partial

جلسه 5
URL Naming + get_absolute_url

جلسه 6
Pagination
↓
Paginator + page_obj + pagination partial
```

این ترتیب باعث می‌شود هر بخش به بخش قبلی تکیه کند، نه اینکه چند Concept جدید هم‌زمان وارد ذهن کارآموز شود.

---

# پیوست B — نسخه ذهنی بسیار ساده

اگر کارآموز فقط یک تصویر ذهنی بخواهد:

```text
base.html
= اسکلت مشترک سایت

extends
= این صفحه از اسکلت Base استفاده می‌کند

block
= این قسمت را خود صفحه پر می‌کند

include
= این قطعه کوچک را داخل صفحه بیاور

static
= فایل CSS/JS/تصویر ثابت من را پیدا کن

get_absolute_url
= URL اصلی این Object را به من بده

Paginator
= این لیست را به چند صفحه تقسیم کن

page_obj
= همین صفحه‌ای که الان کاربر دارد می‌بیند
```

این هفت جمله برای مرور سریع فصل کافی هستند.
