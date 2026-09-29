from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from blog.models import Post


POSTS = [
    ('Django چیست؟', 'Django یک فریم‌ورک وب پایتونی است که ساخت برنامه‌های وب را سریع‌تر و ساختاریافته‌تر می‌کند.'),
    ('معماری MVT در Django', 'در معماری MVT، Model با داده، View با پردازش درخواست و Template با نمایش اطلاعات سروکار دارد.'),
    ('URL در Django', 'URL مشخص می‌کند یک آدرس به کدام View متصل شود و نام‌گذاری URLها ساخت لینک‌های قابل نگهداری را ساده می‌کند.'),
    ('آشنایی با View', 'View یک تابع پایتون است که درخواست را دریافت می‌کند و معمولاً یک Response مناسب برمی‌گرداند.'),
    ('Template چیست؟', 'Template ترکیبی از HTML و Django Template Language است و هدف آن نمایش داده‌های آماده‌شده توسط View است.'),
    ('Context چیست؟', 'Context داده‌ای است که View به Template می‌دهد؛ معمولاً به شکل یک Dictionary از نام متغیرها و مقادیر.'),
    ('QuerySet در Django ORM', 'QuerySet مجموعه‌ای از نتایج Query است که با روش‌هایی مثل all، filter و order_by ساخته و زنجیره‌وار ترکیب می‌شود.'),
    ('Static Files چیست؟', 'فایل‌های CSS، JavaScript و تصاویر ثابت معمولاً در بخش Static قرار می‌گیرند و با {% static %} به Template وصل می‌شوند.'),
    ('CSS و ظاهر صفحه', 'CSS مسئول ظاهر، فاصله‌ها، رنگ‌ها، فونت‌ها، چیدمان و رفتار واکنش‌گرای صفحه است.'),
    ('Template Inheritance', 'با extends و block می‌توان یک base.html ساخت و بخش‌های مشترک سایت را فقط یک‌بار نگهداری کرد.'),
    ('include در Template', 'include برای جدا کردن بخش‌های تکرارشونده مثل کارت پست یا Pagination به فایل‌های کوچک و قابل استفاده مجدد مناسب است.'),
    ('get_absolute_url', 'get_absolute_url یک آدرس canonical برای یک شیء مدل برمی‌گرداند و به جای تکرار مسیر URL، از reverse استفاده می‌کند.'),
    ('Pagination چیست؟', 'Pagination داده‌های زیاد را به چند صفحه کوچک‌تر تقسیم می‌کند تا هم رابط کاربری خواناتر باشد و هم حجم داده هر صفحه کمتر شود.'),
    ('Paginator در Django', 'Paginator ابزار داخلی Django برای تقسیم یک مجموعه داده به Pageهای جداگانه است و اطلاعاتی مثل has_next و number فراهم می‌کند.'),
    ('ساخت یک صفحه جزئیات', 'صفحه جزئیات معمولاً با یک URL پارامتردار، get_object_or_404 و یک Template مستقل ساخته می‌شود.'),
]


class Command(BaseCommand):
    help = 'Create an educational user and sample blog posts.'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(username='teacher')
        if created:
            user.set_password('teacher123')
            user.first_name = 'کارآموز'
            user.last_name = 'Django'
            user.save()

        created_count = 0
        for title, body in POSTS:
            _, was_created = Post.objects.get_or_create(
                title=title,
                defaults={'body': body, 'author': user},
            )
            created_count += int(was_created)

        self.stdout.write(
            self.style.SUCCESS(
                f'کاربر teacher آماده است؛ {created_count} پست جدید ایجاد شد.'
            )
        )
