# پروژهٔ آموزشی وبلاگ با Django (MVT)

پروژه‌ای ساده برای آموزش Model، View، Template، Admin و ORM در Django. اپلیکیشن `blog` فهرست نوشته‌ها و صفحهٔ جزئیات هر نوشته را ارائه می‌کند.

## اجرا

Python 3.10 یا بالاتر لازم است.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

صفحهٔ وبلاگ: `http://127.0.0.1:8000/` و پنل مدیریت: `http://127.0.0.1:8000/admin/`.

ZIP شامل `db.sqlite3` آماده با داده‌های نمونه است. برای پایگاه دادهٔ تازه، فایل را حذف و `migrate` و `seed_data` را اجرا کنید.

## کاربران و نوشته‌های نمونه

دستور `seed_data` با ORM سه کاربر (`sara`، `ali`، `mina`) و شش نوشته ایجاد می‌کند. اجرای مجدد دستور دادهٔ تکراری نمی‌سازد. گذرواژهٔ محلی کاربران نمونه `django-demo-123` است. مدیر را جداگانه با `createsuperuser` بسازید.

## فایل‌های کلیدی

- `blog/models.py`: مدل Post و رابطه با User پیش‌فرض Django.
- `blog/migrations/`: تعریف ساخت جدول.
- `blog/admin.py`: جست‌وجو و فیلتر در پنل مدیریت.
- `blog/views.py`: اجرای QuerySetها با ORM و یافتن نوشتهٔ تکی.
- `blog/templates/blog/`: فهرست و جزئیات.
- `blog/management/commands/seed_data.py`: ساخت داده‌ها با ORM.

جریان درخواست: Browser → URL → View → Model/ORM → Template → HTML.

## تمرین Shell

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from blog.models import Post
User = get_user_model()
User.objects.count()
Post.objects.all()
Post.objects.select_related("author")
Post.objects.filter(title__contains="Django")
Post.objects.get(pk=1)
Post.objects.create(title="نوشته از Shell", content="تمرین ORM", author=User.objects.get(username="sara"))
```

## امنیت

تنظیمات برای یادگیری و اجرای محلی‌اند؛ `DEBUG=True`، کلید ساده و گذرواژهٔ مشترک نمونه را برای انتشار اینترنتی استفاده نکنید.
