# جزوه جامع توسعه و تست‌نویسی پروژه آینده‌شاپ با Django

------------------------------------------------------------------------

# بخش اول: توسعه عملی آینده‌شاپ

## ۱. ساختار کلی پروژه

ساختار پیشنهادی:

``` text
AyandehShop/
├── manage.py
├── config/
│   ├── settings.py
│   └── urls.py
├── products/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
├── cart/
│   └── tests/
├── orders/
│   └── tests/
├── blog/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── tests/
├── dashboard/
│   ├── views.py
│   ├── urls.py
│   └── tests/
├── users/
│   └── tests/
├── templates/
└── static/
```

این ساختار نمونه است؛ ممکن است در پروژه واقعی نام اپلیکیشن‌ها یا پوشه
تنظیمات متفاوت باشد.

## ۲. اجرای پروژه و اپلیکیشن‌ها

``` bash
python manage.py runserver
```

در `settings.py` اپلیکیشن‌های مورد استفاده باید در `INSTALLED_APPS` ثبت
شوند:

``` python
INSTALLED_APPS = [
    # Django apps
    "products",
    "blog",
    "dashboard",
]
```

## ۳. افزودن قابلیت به مدل محصول

مثلاً برای کنترل نمایش محصول و ویژه‌کردن آن:

**products/models.py**

``` python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    discount_percent = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    def get_discounted_price(self):
        discount = self.price * self.discount_percent / 100
        return self.price - discount

    def __str__(self):
        return self.name
```

پس از تغییر مدل:

``` bash
python manage.py makemigrations
python manage.py migrate
```

`BooleanField` برای مقادیر درست/نادرست است. `default=True` مقدار پیش‌فرض
را فعال تعیین می‌کند.

## ۴. فیلترکردن محصولات

**products/views.py**

``` python
from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.filter(is_active=True)

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    return render(
        request,
        "products/product_list.html",
        {"products": products},
    )
```

نمونه URL:

``` text
/products/?min_price=100000&max_price=500000
```

-   `filter()` رکوردها را فیلتر می‌کند.
-   `price__gte` یعنی قیمت بزرگ‌تر یا مساوی مقدار داده‌شده.
-   `price__lte` یعنی قیمت کوچک‌تر یا مساوی مقدار داده‌شده.
-   `request.GET` پارامترهای Query String را دریافت می‌کند.

در پروژه واقعی، ورودی‌های عددی باید اعتبارسنجی شوند و قیمت‌ها با نوع داده
مناسب پولی، معمولاً `DecimalField`، نگهداری شوند.

## ۵. جست‌وجوی محصولات با Q

``` python
from django.db.models import Q
from django.shortcuts import render
from .models import Product

def product_search(request):
    query = request.GET.get("q", "").strip()

    products = Product.objects.filter(
        is_active=True,
        category__is_active=True,
    )

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
        )

    return render(
        request,
        "products/search.html",
        {"products": products, "query": query},
    )
```

`Q` امکان ترکیب شرط‌ها را می‌دهد. علامت `|` معادل OR و `&` معادل AND است.
فیلد `description` و رابطه `category` باید در مدل واقعی وجود داشته
باشند.

## ۶. نمایش محصولات در Template

**products/product_list.html**

``` django
{% for product in products %}
    <article class="product-card">
        <h3>{{ product.name }}</h3>
        <p>قیمت: {{ product.price }}</p>
        <p>قیمت با تخفیف: {{ product.get_discounted_price }}</p>
    </article>
{% empty %}
    <p>محصولی برای نمایش وجود ندارد.</p>
{% endfor %}
```

------------------------------------------------------------------------

# بخش دوم: ساخت بلاگ

## ۷. ایجاد اپلیکیشن بلاگ

``` bash
python manage.py startapp blog
```

سپس `"blog"` را به `INSTALLED_APPS` اضافه کنید.

## ۸. طراحی مدل‌های بلاگ

**blog/models.py**

``` python
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "پیش‌نویس"),
        ("published", "منتشر شده"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="blog_posts",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="posts",
    )
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to="blog/")
    body = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

ارتباط‌ها: - هر مقاله یک دسته‌بندی دارد. - هر مقاله یک نویسنده دارد. - هر
مقاله می‌تواند چند برچسب داشته باشد. - هر برچسب می‌تواند به چند مقاله متصل
باشد.

`ForeignKey` رابطه چندبه‌یک و `ManyToManyField` رابطه چندبه‌چند ایجاد
می‌کند. استفاده از `PROTECT` باعث می‌شود حذف نویسنده یا دسته‌بندی دارای
مقاله وابسته به‌سادگی انجام نشود.

پس از تعریف مدل‌ها:

``` bash
python manage.py makemigrations blog
python manage.py migrate
```

## ۹. Viewهای بلاگ

**blog/views.py**

``` python
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = (
        Post.objects
        .filter(
            status="published",
            category__is_active=True,
        )
        .select_related("author", "category")
        .prefetch_related("tags")
    )

    return render(
        request,
        "blog/post_list.html",
        {"posts": posts},
    )


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related("author", "category"),
        slug=slug,
        status="published",
        category__is_active=True,
    )

    return render(
        request,
        "blog/post_detail.html",
        {"post": post},
    )
```

`select_related` برای بهینه‌سازی ارتباط‌های ForeignKey و OneToOne و
`prefetch_related` برای ارتباط‌هایی مانند ManyToMany استفاده می‌شود.

## ۱۰. URLهای بلاگ

**blog/urls.py**

``` python
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
]
```

در URL اصلی پروژه:

``` python
from django.urls import path, include

urlpatterns = [
    path("blog/", include("blog.urls")),
]
```

نمونه آدرس‌ها:

``` text
/blog/
/blog/python-learning/
```

## ۱۱. قالب فهرست مقالات

**blog/templates/blog/post_list.html**

``` django
<h1>آخرین مقالات</h1>

{% for post in posts %}
    <article>
        <h2>
            <a href="{% url 'blog:post_detail' post.slug %}">
                {{ post.title }}
            </a>
        </h2>

        <p>نویسنده: {{ post.author.username }}</p>
        <p>دسته‌بندی: {{ post.category.name }}</p>
    </article>
{% empty %}
    <p>مقاله‌ای منتشر نشده است.</p>
{% endfor %}
```

## ۱۲. قالب جزئیات مقاله

**blog/templates/blog/post_detail.html**

``` django
<h1>{{ post.title }}</h1>
<p>نویسنده: {{ post.author.username }}</p>

{% if post.image %}
    <img src="{{ post.image.url }}" alt="{{ post.title }}">
{% endif %}

<div>
    {{ post.body|linebreaks }}
</div>
```

------------------------------------------------------------------------

# بخش سوم: فرم ایجاد و ویرایش مقاله

## ۱۳. ساخت ModelForm

**blog/forms.py**

``` python
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "slug",
            "category",
            "tags",
            "image",
            "body",
            "status",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 8,
                }
            ),
        }
```

## ۱۴. View ایجاد مقاله

``` python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PostForm

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect("blog:post_list")
    else:
        form = PostForm()

    return render(
        request,
        "blog/post_form.html",
        {"form": form},
    )
```

`commit=False` اجازه می‌دهد قبل از ذخیره، نویسنده را تعیین کنیم. پس از
ذخیره شیء اصلی، `save_m2m()` ارتباط‌های چندبه‌چند فرم را ذخیره می‌کند.

در پروژه واقعی باید مجوز ایجاد مقاله، اعتبارسنجی وضعیت انتشار و سیاست
نویسنده نیز بررسی شود.

## ۱۵. قالب فرم

**blog/templates/blog/post_form.html**

``` django
<h1>ایجاد مقاله جدید</h1>

<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}

    <button type="submit">ذخیره مقاله</button>
</form>
```

برای ارسال تصویر، `enctype="multipart/form-data"` ضروری است.

------------------------------------------------------------------------

# بخش چهارم: آپلود تصویر و فایل‌های Media

## ۱۶. تنظیمات Media

در `settings.py`:

``` python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

در `urls.py` اصلی، فقط برای محیط توسعه:

``` python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # سایر مسیرها
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
```

در محیط Production باید فایل‌های Media توسط وب‌سرور یا فضای ذخیره‌سازی
مناسب ارائه شوند. همچنین محدودیت حجم، نوع فایل و اعتبارسنجی محتوای فایل
باید در نظر گرفته شود.

------------------------------------------------------------------------

# بخش پنجم: ساخت CMS اختصاصی

## ۱۷. ایجاد اپلیکیشن داشبورد

``` bash
python manage.py startapp dashboard
```

اپلیکیشن را در `INSTALLED_APPS` ثبت کنید.

## ۱۸. محدودکردن دسترسی به داشبورد

**dashboard/views.py**

``` python
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@staff_member_required
def dashboard_home(request):
    return render(request, "dashboard/home.html")
```

این دکوراتور دسترسی را به کاربران Staff محدود می‌کند. برای مجوزهای دقیق‌تر
باید Permissionهای Django یا سیاست دسترسی اختصاصی پروژه به کار رود.

## ۱۹. نمایش آمار داشبورد

``` python
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from products.models import Product
from blog.models import Post

@staff_member_required
def dashboard_home(request):
    context = {
        "products_count": Product.objects.count(),
        "active_products": Product.objects.filter(
            is_active=True
        ).count(),
        "posts_count": Post.objects.count(),
        "published_posts": Post.objects.filter(
            status="published"
        ).count(),
    }

    return render(
        request,
        "dashboard/home.html",
        context,
    )
```

## ۲۰. قالب داشبورد

**dashboard/templates/dashboard/home.html**

``` django
<h1>داشبورد مدیریت آینده‌شاپ</h1>

<div class="dashboard-card">
    <h3>تعداد محصولات</h3>
    <p>{{ products_count }}</p>
</div>

<div class="dashboard-card">
    <h3>محصولات فعال</h3>
    <p>{{ active_products }}</p>
</div>

<div class="dashboard-card">
    <h3>تعداد مقالات</h3>
    <p>{{ posts_count }}</p>
</div>

<div class="dashboard-card">
    <h3>مقالات منتشرشده</h3>
    <p>{{ published_posts }}</p>
</div>
```

## ۲۱. نمونه عملیات حذف محصول در CMS

``` python
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from products.models import Product

@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect("dashboard:home")

    return render(
        request,
        "dashboard/product_confirm_delete.html",
        {"product": product},
    )
```

عملیات حذف با POST انجام شده است؛ بازکردن یک لینک GET نباید باعث حذف
اطلاعات شود. در پروژه واقعی، مجوز حذف محصول باید به‌صورت دقیق بررسی شود.

------------------------------------------------------------------------

# بخش ششم: مدیریت کاربران و سطح دسترسی

## ۲۲. استفاده از Group

``` python
from django.contrib.auth.models import Group

editors, created = Group.objects.get_or_create(
    name="Editors"
)
```

افزودن کاربر به گروه:

``` python
user.groups.add(editors)
```

## ۲۳. محدودکردن View به گروه ویرایشگران

``` python
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def is_editor(user):
    return (
        user.is_authenticated
        and user.groups.filter(name="Editors").exists()
    )

@user_passes_test(is_editor)
def manage_posts(request):
    return render(
        request,
        "dashboard/manage_posts.html",
    )
```

-   Authentication مشخص می‌کند کاربر چه کسی است.
-   Authorization مشخص می‌کند کاربر اجازه انجام چه کاری را دارد.

در سیستم واقعی بهتر است برای عملیات مختلف مانند مشاهده، ایجاد، ویرایش و
حذف، مجوزهای مجزا تعریف شود.

------------------------------------------------------------------------

# بخش هفتم: قالب پایه و رابط کاربری

## ۲۴. ساخت قالب مشترک

**templates/base.html**

``` django
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">

    <title>
        {% block title %}آینده‌شاپ{% endblock %}
    </title>

    {% load static %}

    <link
        rel="stylesheet"
        href="{% static 'css/style.css' %}"
    >
</head>
<body>
    <header>
        <h2>آینده‌شاپ</h2>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        تمامی حقوق محفوظ است.
    </footer>
</body>
</html>
```

استفاده در صفحه دیگر:

``` django
{% extends "base.html" %}

{% block title %}
فهرست مقالات
{% endblock %}

{% block content %}
<h1>مقالات آموزشی</h1>
{% endblock %}
```

با `extends` قالب مشترک استفاده می‌شود و با `block` بخش‌های قابل جایگزینی
تعریف می‌شوند.

------------------------------------------------------------------------

# بخش هشتم: تست و استقرار

## ۲۵. نمونه تست مدل

**products/tests/test_models.py**

``` python
from django.test import TestCase
from products.models import Product

class ProductTest(TestCase):
    def test_discount_calculation(self):
        product = Product(
            name="Laptop",
            price=1_000_000,
            discount_percent=20,
        )

        self.assertEqual(
            product.get_discounted_price(),
            800_000,
        )
```

## ۲۶. دستورات مهم استقرار

``` bash
python manage.py check --deploy
python manage.py collectstatic
```

در محیط واقعی باید `DEBUG=False`، `ALLOWED_HOSTS`، کلید محرمانه، HTTPS،
دیتابیس، فایل‌های Static و Media و تنظیمات امنیتی به‌درستی پیکربندی شوند.

------------------------------------------------------------------------

# بخش نهم: تست‌نویسی جامع آینده‌شاپ

## ۲۷. انواع تست

### Unit Test

آزمایش یک تابع یا متد به‌صورت مستقل؛ مانند محاسبه قیمت تخفیف‌خورده.

### Model Test

بررسی رفتار مدل‌ها، فیلدها، روابط و اعتبارسنجی.

### View Test

بررسی پاسخ صفحات، وضعیت HTTP، قالب و محتوای خروجی.

### Integration Test

بررسی همکاری چند بخش؛ مانند ایجاد سفارش و ثبت اقلام آن.

### Security Test

بررسی دسترسی‌ها، اعتبارسنجی ورودی و جلوگیری از دسترسی غیرمجاز.

### End-to-End Test

شبیه‌سازی فرایند کامل کاربر از مرورگر.

------------------------------------------------------------------------

# بخش دهم: ساختار پوشه تست‌ها

ساختار پیشنهادی:

``` text
products/
    tests/
        __init__.py
        test_models.py
        test_views.py
        test_forms.py
        test_services.py

cart/
    tests/
        __init__.py
        test_cart.py
        test_views.py

orders/
    tests/
        __init__.py
        test_models.py
        test_checkout.py
        test_views.py

blog/
    tests/
        __init__.py
        test_models.py
        test_views.py
        test_forms.py

dashboard/
    tests/
        __init__.py
        test_permissions.py
        test_views.py

users/
    tests/
        __init__.py
        test_authentication.py
        test_registration.py
```

برای شناسایی تست‌ها توسط Django، پوشه تست باید قابل import باشد؛ به همین
دلیل `__init__.py` قرار داده شده است.

------------------------------------------------------------------------

# بخش یازدهم: تست تخفیف و اعتبارسنجی

## ۲۸. تست حالت‌های مختلف تخفیف

``` python
from django.test import TestCase
from products.models import Product

class ProductDiscountTest(TestCase):

    def test_discount_calculation(self):
        product = Product(
            name="Laptop",
            price=1_000_000,
            discount_percent=20,
        )

        self.assertEqual(
            product.get_discounted_price(),
            800_000,
        )

    def test_without_discount(self):
        product = Product(
            name="Mouse",
            price=500_000,
            discount_percent=0,
        )

        self.assertEqual(
            product.get_discounted_price(),
            500_000,
        )

    def test_full_discount(self):
        product = Product(
            name="Keyboard",
            price=500_000,
            discount_percent=100,
        )

        self.assertEqual(
            product.get_discounted_price(),
            0,
        )
```

## ۲۹. اعتبارسنجی درصد تخفیف

در مدل:

``` python
from django.core.validators import MinValueValidator, MaxValueValidator

discount_percent = models.PositiveSmallIntegerField(
    default=0,
    validators=[
        MinValueValidator(0),
        MaxValueValidator(100),
    ],
)
```

تست:

``` python
from django.core.exceptions import ValidationError
from django.test import TestCase
from products.models import Product

class ProductValidationTest(TestCase):

    def test_discount_over_100_is_invalid(self):
        product = Product(
            name="Laptop",
            price=1_000_000,
            discount_percent=120,
        )

        with self.assertRaises(ValidationError):
            product.full_clean()
```

نکته: `save()` به‌طور خودکار `full_clean()` را اجرا نمی‌کند. اعتبارسنجی
باید در فرم‌ها و سرویس‌های ذخیره‌سازی نیز رعایت شود.

------------------------------------------------------------------------

# بخش دوازدهم: تست دسته‌بندی‌ها

## ۳۰. سناریوهای حیاتی دسته‌بندی

برای آینده‌شاپ این سه رفتار باید تضمین شوند:

1.  غیرفعال‌کردن دسته‌بندی، محصولات را حذف نکند.
2.  فعال‌سازی مجدد دسته‌بندی، محصولات را دوباره قابل نمایش کند.
3.  حذف دسته‌بندی، محصولات وابسته را طبق سیاست پروژه حذف کند.

مدل نمونه:

``` python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )
    is_active = models.BooleanField(default=True)
```

تست‌ها:

``` python
from django.test import TestCase
from products.models import Category, Product

class CategoryTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Programming",
            is_active=True,
        )

        self.product = Product.objects.create(
            name="Python Course",
            category=self.category,
            is_active=True,
        )

    def test_deactivate_does_not_delete_products(self):
        self.category.is_active = False
        self.category.save()

        self.assertTrue(
            Product.objects.filter(
                pk=self.product.pk
            ).exists()
        )

    def test_reactivate_restores_visibility(self):
        self.category.is_active = False
        self.category.save()

        self.category.is_active = True
        self.category.save()

        visible_products = Product.objects.filter(
            category__is_active=True,
            is_active=True,
        )

        self.assertTrue(
            visible_products.filter(
                pk=self.product.pk
            ).exists()
        )

    def test_delete_category_deletes_products(self):
        self.category.delete()

        self.assertFalse(
            Product.objects.filter(
                pk=self.product.pk
            ).exists()
        )
```

این تست‌ها فرض می‌کنند محصول فقط یک دسته‌بندی اصلی دارد و رفتار حذف آن با
`CASCADE` تعریف شده است.

------------------------------------------------------------------------

# بخش سیزدهم: تست View و جست‌وجوی محصولات

## ۳۱. تست صفحه محصولات

``` python
from django.test import TestCase
from django.urls import reverse
from products.models import Product, Category

class ProductListViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Python",
            is_active=True,
        )

        Product.objects.create(
            name="Python Course",
            category=self.category,
            is_active=True,
        )

        Product.objects.create(
            name="Hidden Course",
            category=self.category,
            is_active=False,
        )

    def test_product_page_returns_200(self):
        response = self.client.get(
            reverse("products:product_list")
        )

        self.assertEqual(response.status_code, 200)

    def test_active_product_is_visible(self):
        response = self.client.get(
            reverse("products:product_list")
        )

        self.assertContains(response, "Python Course")

    def test_inactive_product_is_hidden(self):
        response = self.client.get(
            reverse("products:product_list")
        )

        self.assertNotContains(response, "Hidden Course")
```

این نمونه فرض می‌کند URL با نام `products:product_list` تعریف شده و View
محصولات غیرفعال و محصولات دسته‌بندی غیرفعال را فیلتر می‌کند.

## ۳۲. تست جست‌وجو

``` python
from django.test import TestCase
from django.urls import reverse
from products.models import Product, Category

class ProductSearchTest(TestCase):

    def setUp(self):
        category = Category.objects.create(
            name="Technology",
            is_active=True,
        )

        Product.objects.create(
            name="Python Course",
            category=category,
            is_active=True,
        )

        Product.objects.create(
            name="Django Course",
            category=category,
            is_active=True,
        )

    def test_search_python(self):
        response = self.client.get(
            reverse("products:product_search"),
            {"q": "Python"},
        )

        self.assertContains(response, "Python Course")
        self.assertNotContains(response, "Django Course")
```

سناریوهای تکمیلی: - جست‌وجوی بدون نتیجه - عبارت خالی - حروف فارسی - عبارت
ناقص - محصولات غیرفعال - ترکیب جست‌وجو و فیلتر قیمت

------------------------------------------------------------------------

# بخش چهاردهم: تست سبد خرید

## ۳۳. سناریوهای تست سبد خرید

  سناریو                نتیجه مورد انتظار
  --------------------- ------------------------
  افزودن محصول          محصول وارد سبد شود
  افزودن محصول تکراری   تعداد افزایش یابد
  کاهش تعداد            تعداد کم شود
  حذف محصول             از سبد حذف شود
  تعداد صفر             حذف یا درخواست رد شود
  تعداد منفی            درخواست نامعتبر باشد
  موجودی ناکافی         خرید محدود شود
  محصول غیرفعال         امکان خرید نداشته باشد

نمونه تست Session:

``` python
from django.test import TestCase

class CartSessionTest(TestCase):

    def test_cart_session_creation(self):
        session = self.client.session

        session["cart"] = {
            "1": {
                "quantity": 2,
                "price": "500000",
            }
        }

        session.save()

        response = self.client.get("/cart/")

        self.assertEqual(response.status_code, 200)

    def test_cart_quantity(self):
        session = self.client.session

        session["cart"] = {
            "1": {
                "quantity": 3,
                "price": "500000",
            }
        }

        session.save()

        self.assertEqual(
            self.client.session["cart"]["1"]["quantity"],
            3,
        )
```

این نمونه فقط ساختار Session را بررسی می‌کند. تست کامل باید Viewهای واقعی
افزودن، حذف و تغییر تعداد را فراخوانی کند.

**قاعده امنیتی:** قیمت و موجودی نهایی باید در سمت سرور از دیتابیس خوانده
شوند؛ به داده قیمت ذخیره‌شده در مرورگر یا Session به‌عنوان منبع قطعی
اعتماد نکنید.

------------------------------------------------------------------------

# بخش پانزدهم: تست سفارش و پرداخت

## ۳۴. سناریوهای تست سفارش

1.  ثبت سفارش کاربر واردشده.
2.  جلوگیری از سفارش کاربر ناشناس، در صورت الزام ورود.
3.  محاسبه صحیح مبلغ سفارش.
4.  ثبت جزئیات سفارش.
5.  بررسی موجودی.
6.  جلوگیری از خرید بیش از موجودی.
7.  جلوگیری از پردازش چندباره Callback پرداخت.
8.  ثبت وضعیت پرداخت.
9.  جلوگیری از دست‌کاری مبلغ سفارش.
10. مدیریت بازگشت موجودی در لغو سفارش.

نمونه تست محاسبه:

``` python
from decimal import Decimal
from django.test import TestCase

class OrderCalculationTest(TestCase):

    def test_order_total(self):
        unit_price = Decimal("500000")
        quantity = 2

        total = unit_price * quantity

        self.assertEqual(
            total,
            Decimal("1000000"),
        )
```

این تست محاسبه ریاضی را بررسی می‌کند. تست واقعی باید متد یا سرویس محاسبه
سفارش پروژه را اجرا کند.

------------------------------------------------------------------------

# بخش شانزدهم: تست بلاگ

## ۳۵. تست‌های ضروری بلاگ

  تست                نتیجه مورد انتظار
  ------------------ --------------------------------
  ایجاد مقاله        ذخیره شود
  Slug تکراری        رد شود
  پیش‌نویس            عمومی نباشد
  مقاله منتشرشده     نمایش داده شود
  دسته‌بندی غیرفعال   مقاله وابسته نمایش داده نشود
  نویسنده            درست ذخیره شود
  برچسب‌ها            درست ذخیره شوند
  صفحه‌بندی           درست عمل کند
  جست‌وجو             نتایج مرتبط بدهد
  دیدگاه             طبق سیاست تأیید نمایش داده شود

## ۳۶. تست مقاله پیش‌نویس

``` python
from django.test import TestCase
from django.urls import reverse
from blog.models import Post

class BlogViewTest(TestCase):

    def test_draft_post_is_not_public(self):
        post = Post.objects.create(
            title="Django Tutorial",
            slug="django-tutorial",
            status="draft",
            body="Django Training",
        )

        response = self.client.get(
            reverse(
                "blog:post_detail",
                kwargs={"slug": post.slug},
            )
        )

        self.assertEqual(response.status_code, 404)
```

اگر مدل Post فیلدهای اجباری دیگری مانند نویسنده یا دسته‌بندی داشته باشد،
باید آن رکوردها نیز در تست ایجاد شوند.

------------------------------------------------------------------------

# بخش هفدهم: تست فرم مقاله

## ۳۷. تست ModelForm

``` python
from django.test import TestCase
from blog.forms import PostForm

class PostFormTest(TestCase):

    def test_title_field_exists(self):
        form = PostForm()

        self.assertIn("title", form.fields)
```

برای تست اعتبار واقعی فرم، باید داده‌های معتبر و تمام ارتباط‌های اجباری
مانند Category را بسازیم و سپس `form.is_valid()` را بررسی کنیم.

------------------------------------------------------------------------

# بخش هجدهم: تست CMS و مجوزها

## ۳۸. تست دسترسی به داشبورد

``` python
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class DashboardPermissionTest(TestCase):

    def test_anonymous_user_is_redirected(self):
        response = self.client.get(
            reverse("dashboard:home")
        )

        self.assertEqual(response.status_code, 302)

    def test_staff_user_can_access_dashboard(self):
        User.objects.create_user(
            username="admin",
            password="StrongPass123!",
            is_staff=True,
        )

        self.client.login(
            username="admin",
            password="StrongPass123!",
        )

        response = self.client.get(
            reverse("dashboard:home")
        )

        self.assertEqual(response.status_code, 200)
```

## ۳۹. سناریوهای امنیتی CMS

-   کاربر ناشناس نتواند وارد CMS شود.
-   کاربر عادی نتواند وارد بخش مدیریت شود.
-   مدیر بتواند عملیات مجاز را انجام دهد.
-   کاربر فاقد مجوز نتواند محصول را حذف کند.
-   حذف اطلاعات فقط با POST انجام شود.
-   فرم ناقص اطلاعات نامعتبر ذخیره نکند.
-   URLهای مدیریتی مستقیماً نیز محافظت شوند.

مخفی‌کردن دکمه در HTML امنیت نیست؛ کنترل مجوز باید سمت سرور انجام شود.

------------------------------------------------------------------------

# بخش نوزدهم: تست آپلود تصاویر

## ۴۰. مواردی که باید بررسی شوند

-   پذیرش تصویر معتبر
-   رد فایل غیرتصویری
-   محدودیت حجم فایل
-   بررسی نوع و محتوای فایل
-   ذخیره در مسیر درست
-   مدیریت نام فایل
-   پاک‌سازی فایل‌های بلااستفاده طبق سیاست پروژه

نمونه ساخت فایل تصویری آزمایشی:

``` python
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

def create_test_image():
    image = Image.new("RGB", (100, 100), color="red")

    buffer = BytesIO()
    image.save(buffer, format="PNG")

    return SimpleUploadedFile(
        "test.png",
        buffer.getvalue(),
        content_type="image/png",
    )
```

این تابع فایل آزمایشی تولید می‌کند. برای تست کامل باید آن را از طریق فرم
یا View واقعی ارسال و ذخیره فایل را بررسی کنیم.

------------------------------------------------------------------------

# بخش بیستم: تست امنیت

## ۴۱. مهم‌ترین سناریوهای امنیتی

  موضوع             هدف تست
  ----------------- -----------------------------------
  SQL Injection     کنترل ورودی جست‌وجو
  XSS               جلوگیری از اجرای محتوای مخرب
  CSRF              رد POST فاقد توکن معتبر
  Authentication    کنترل ورود
  Authorization     کنترل مجوز عملیات
  IDOR              جلوگیری از دسترسی به سفارش دیگران
  File Upload       جلوگیری از فایل مخرب
  Price Tampering   جلوگیری از دست‌کاری قیمت
  Session           کنترل نشست کاربر
  Password          ذخیره امن رمز عبور

## ۴۲. جلوگیری از مشاهده سفارش دیگران

نمونه View:

``` python
from django.shortcuts import get_object_or_404, render
from orders.models import Order

def order_detail(request, pk):
    order = get_object_or_404(
        Order,
        pk=pk,
        user=request.user,
    )

    return render(
        request,
        "orders/detail.html",
        {"order": order},
    )
```

نمونه تست:

``` python
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from orders.models import Order

class OrderSecurityTest(TestCase):

    def test_user_cannot_view_other_users_order(self):
        user1 = User.objects.create_user(
            username="user1",
            password="Pass12345",
        )

        user2 = User.objects.create_user(
            username="user2",
            password="Pass12345",
        )

        order = Order.objects.create(user=user1)

        self.client.login(
            username="user2",
            password="Pass12345",
        )

        response = self.client.get(
            reverse(
                "orders:detail",
                kwargs={"pk": order.pk},
            )
        )

        self.assertEqual(response.status_code, 404)
```

این مثال فرض می‌کند مدل Order فقط به فیلد `user` نیاز دارد و URL
نام‌گذاری‌شده فوق در پروژه تعریف شده است. View باید برای کاربر ناشناس نیز
به‌درستی محافظت شود.

------------------------------------------------------------------------

# بخش بیست‌ویکم: تست یکپارچگی

## ۴۳. سناریوی خرید موفق

فرایند مورد انتظار:

1.  ورود کاربر
2.  انتخاب محصول
3.  افزودن به سبد خرید
4.  بررسی موجودی
5.  ایجاد سفارش
6.  محاسبه مبلغ
7.  تأیید پرداخت
8.  تغییر وضعیت سفارش
9.  به‌روزرسانی موجودی

نمونه ساده تست ایجاد سفارش و اقلام آن:

``` python
from decimal import Decimal
from django.test import TestCase

class CheckoutIntegrationTest(TestCase):

    def test_order_contains_correct_item(self):
        product = Product.objects.create(
            name="Python Course",
            price=Decimal("500000"),
            stock=10,
            is_active=True,
        )

        order = Order.objects.create(
            user=self.user,
            total_price=Decimal("1000000"),
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=2,
            price=Decimal("500000"),
        )

        self.assertEqual(
            order.total_price,
            Decimal("1000000"),
        )

        self.assertEqual(order.items.count(), 1)
```

این نمونه ایجاد ارتباط سفارش و اقلام را بررسی می‌کند، نه پرداخت واقعی یا
کاهش موجودی. تست کامل باید سرویس Checkout پروژه را اجرا کند.

برای جلوگیری از خطاهای هم‌زمانی موجودی و پرداخت، استفاده از تراکنش
دیتابیس و در موارد مناسب `select_for_update()` ضروری است.

------------------------------------------------------------------------

# بخش بیست‌ودوم: تست سرتاسری با Playwright

## ۴۴. نصب Playwright

``` bash
pip install playwright
playwright install chromium
```

نمونه تست بازشدن صفحه اصلی:

``` python
from playwright.sync_api import sync_playwright

def test_homepage():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("http://127.0.0.1:8000/")

        assert page.title() != ""

        browser.close()
```

سناریوهای E2E: - بازشدن صفحه اصلی - جست‌وجوی محصول - مشاهده جزئیات - ورود
کاربر - افزودن به سبد - ثبت سفارش - ورود مدیر به CMS - ایجاد مقاله -
انتشار و مشاهده مقاله

برای اجرای این تست‌ها، سرور آزمایشی باید در دسترس باشد. در پروژه جدی بهتر
است Playwright با تنظیمات CI اجرا شود.

------------------------------------------------------------------------

# بخش بیست‌وسوم: تست کارایی

## ۴۵. شمارش Queryهای دیتابیس

``` python
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection

class ProductPerformanceTest(TestCase):

    def test_product_list_query_count(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200)

        print("Number of queries:", len(queries))
```

پس از اندازه‌گیری اولیه، می‌توان تعداد Queryهای مورد انتظار را با
`assertNumQueries()` کنترل کرد.

موارد دیگر: - زمان پاسخ صفحه اصلی - تعداد Query صفحه محصولات - تعداد
Query بلاگ - سرعت جست‌وجو - عملکرد صفحه‌بندی - حجم تصاویر - عملکرد CMS با
داده زیاد

------------------------------------------------------------------------

# بخش بیست‌وچهارم: اجرای تست‌ها

## ۴۶. دستورات Django Test

اجرای همه تست‌ها:

``` bash
python manage.py test
```

اجرای تست یک اپ:

``` bash
python manage.py test products
```

اجرای یک ماژول:

``` bash
python manage.py test products.tests.test_models
```

اجرای یک کلاس:

``` bash
python manage.py test products.tests.test_models.ProductTest
```

اجرای یک متد:

``` bash
python manage.py test products.tests.test_models.ProductTest.test_discount_calculation
```

نمایش جزئیات بیشتر:

``` bash
python manage.py test --verbosity=2
```

Django هنگام اجرای تست‌ها معمولاً یک دیتابیس آزمایشی جداگانه می‌سازد و پس
از پایان تست آن را پاک می‌کند.

------------------------------------------------------------------------

# بخش بیست‌وپنجم: Coverage

## ۴۷. نصب Coverage

``` bash
pip install coverage
```

اجرای تست‌ها:

``` bash
coverage run manage.py test
```

گزارش متنی:

``` bash
coverage report
```

گزارش HTML:

``` bash
coverage html
```

فایل گزارش:

``` text
htmlcov/index.html
```

Coverage درصد خطوط اجراشده را نشان می‌دهد. Coverage بالا به‌تنهایی کیفیت
تست را تضمین نمی‌کند؛ باید نتیجه مورد انتظار نیز با Assertion بررسی شود.

------------------------------------------------------------------------

# بخش بیست‌وششم: چک‌لیست جامع تست آینده‌شاپ

## محصولات

-   [ ] ایجاد محصول
-   [ ] ویرایش محصول
-   [ ] حذف محصول
-   [ ] قیمت و تخفیف
-   [ ] موجودی
-   [ ] فعال و غیرفعال‌کردن
-   [ ] تصویر محصول
-   [ ] جست‌وجو
-   [ ] فیلتر و مرتب‌سازی

## دسته‌بندی‌ها

-   [ ] ایجاد دسته‌بندی
-   [ ] ویرایش دسته‌بندی
-   [ ] غیرفعال‌سازی بدون حذف محصولات
-   [ ] فعال‌سازی مجدد و بازگشت محصولات
-   [ ] حذف دسته‌بندی و محصولات وابسته
-   [ ] عدم نمایش محصولات دسته‌بندی غیرفعال

## سبد خرید

-   [ ] افزودن محصول
-   [ ] افزایش تعداد
-   [ ] کاهش تعداد
-   [ ] حذف محصول
-   [ ] محدودیت موجودی
-   [ ] محاسبه قیمت نهایی
-   [ ] جلوگیری از دست‌کاری قیمت

## سفارش و پرداخت

-   [ ] ثبت سفارش
-   [ ] محاسبه مبلغ
-   [ ] ثبت جزئیات
-   [ ] پرداخت موفق
-   [ ] پرداخت ناموفق
-   [ ] Callback تکراری
-   [ ] لغو سفارش
-   [ ] به‌روزرسانی موجودی

## بلاگ

-   [ ] ایجاد مقاله
-   [ ] ویرایش مقاله
-   [ ] حذف مقاله
-   [ ] انتشار مقاله
-   [ ] پیش‌نویس
-   [ ] دسته‌بندی
-   [ ] برچسب‌ها
-   [ ] تصویر
-   [ ] جست‌وجو و صفحه‌بندی
-   [ ] دیدگاه‌ها

## CMS و کاربران

-   [ ] ورود مدیر
-   [ ] محدودیت کاربر عادی
-   [ ] مدیریت محصولات
-   [ ] مدیریت مقالات
-   [ ] مدیریت سفارش‌ها
-   [ ] مدیریت کاربران
-   [ ] سطح دسترسی
-   [ ] اعتبارسنجی فرم‌ها

## امنیت و کارایی

-   [ ] CSRF
-   [ ] XSS
-   [ ] دسترسی به سفارش دیگران
-   [ ] آپلود فایل مخرب
-   [ ] SQL Injection
-   [ ] تعداد Queryها
-   [ ] سرعت صفحات
-   [ ] مدیریت Session

------------------------------------------------------------------------

# بخش بیست‌وهفتم: برنامه استاندارد اجرای تست

پیشنهاد می‌شود تست‌ها در سه مرحله اجرا شوند:

  مرحله         زمان اجرا            هدف
  ------------- -------------------- --------------------------
  تست توسعه     پس از هر قابلیت      کشف سریع خطا
  تست یکپارچه   پس از تکمیل هر بخش   بررسی هماهنگی اپ‌ها
  تست انتشار    پیش از انتشار نسخه   اطمینان از سلامت فروشگاه

## پیشنهاد ساختار نهایی تست

``` text
tests/
    unit/
    integration/
    security/
    e2e/
```

یا در ساختار اپلیکیشن‌محور، تست‌ها داخل پوشه `tests/` هر اپلیکیشن قرار
بگیرند. برای پروژه آینده‌شاپ می‌توان از ترکیب این دو روش استفاده کرد:
تست‌های مدل و View در اپ‌ها و سناریوهای سرتاسری در پوشه مرکزی.

------------------------------------------------------------------------

# بخش بیست‌وهشتم: استانداردهای پیشنهادی برای آینده‌شاپ

1.  هر قابلیت جدید باید همراه با تست نوشته شود.
2.  تست‌های قبلی پس از تغییر کد دوباره اجرا شوند.
3.  منطق محاسباتی مهم در سرویس‌های قابل تست متمرکز شود.
4.  تست پرداخت با درگاه آزمایشی و Mock انجام شود؛ پرداخت واقعی در تست
    خودکار اجرا نشود.
5.  تست‌های امنیتی برای تمام عملیات CMS نوشته شوند.
6.  برای عملیات مالی از `Decimal` و `DecimalField` استفاده شود.
7.  عملیات حساس سفارش در تراکنش دیتابیس اجرا شوند.
8.  تست‌ها در CI مانند GitHub Actions به‌صورت خودکار اجرا شوند.
9.  پیش از انتشار، گزارش Coverage و تست‌های شکست‌خورده بررسی شوند.
10. برای هر خطای کشف‌شده یک تست Regression نوشته شود تا خطا دوباره
    بازنگردد.

------------------------------------------------------------------------

# نتیجه‌گیری

در این جزوه دو مسیر مکمل را یاد گرفتیم:

**مسیر توسعه** - افزودن قابلیت‌های فروشگاه - مدل‌سازی و ORM - ساخت بلاگ -
فرم و آپلود فایل - CMS اختصاصی - احراز هویت و مجوزها - قالب‌ها و رابط
کاربری - استقرار

**مسیر تضمین کیفیت** - Unit Test - Model Test - View Test - Integration
Test - Security Test - E2E Test - Performance Test - Coverage و اجرای
خودکار

هدف این است که آینده‌شاپ فقط یک فروشگاه دارای امکانات متعدد نباشد؛ بلکه
پروژه‌ای قابل توسعه، قابل نگهداری، امن و قابل اطمینان باشد.

> **یادآوری اجرایی:** کدهای این جزوه الگوهای آموزشی‌اند. پیش از انتقال به
> پروژه واقعی، نام مدل‌ها، فیلدها، URLها، سیاست حذف داده‌ها و ساختار
> سرویس‌های موجود را بررسی کنید. تست‌های نمونه‌ای که به مدل‌های فرضی
> وابسته‌اند باید با Factory یا داده‌های واقعی پروژه تکمیل شوند.
