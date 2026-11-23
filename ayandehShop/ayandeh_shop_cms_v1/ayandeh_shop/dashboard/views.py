from django.contrib import messages
from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST

from blog.models import BlogCategory, Comment, Post, Tag
from orders.models import Order
from products.models import Category, Product

from .forms import (
    BlogCategoryForm,
    CategoryForm,
    OrderStatusForm,
    PostForm,
    ProductForm,
    TagForm,
)


class CMSLoginView(LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = False

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy("dashboard:index")


class CMSLogoutView(LogoutView):
    next_page = reverse_lazy("dashboard:login")


def staff_required(view_func):
    """Require an active staff account; authenticated customers receive 403."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), reverse("dashboard:login"))
        if not request.user.is_active or not request.user.is_staff:
            raise PermissionDenied("دسترسی به پنل مدیریت مجاز نیست.")
        return view_func(request, *args, **kwargs)
    return _wrapped


def _paginate(request, queryset, per_page=15):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get("page"))


@staff_required
def index(request):
    today = timezone.localdate()
    orders = Order.objects.all()
    revenue = orders.exclude(status="cancelled").aggregate(value=Sum("total_price"))["value"] or 0
    context = {
        "products_count": Product.objects.count(),
        "active_products_count": Product.objects.filter(is_active=True, category__is_active=True).count(),
        "categories_count": Category.objects.count(),
        "active_categories_count": Category.objects.filter(is_active=True).count(),
        "orders_count": orders.count(),
        "today_orders_count": orders.filter(created_at__date=today).count(),
        "pending_orders_count": orders.filter(status="pending").count(),
        "revenue": revenue,
        "users_count": get_user_model().objects.filter(is_active=True).count(),
        "posts_count": Post.objects.count(),
        "draft_posts_count": Post.objects.filter(status=Post.Status.DRAFT).count(),
        "comments_pending_count": Comment.objects.filter(is_approved=False).count(),
        "low_stock_products": Product.objects.select_related("category").filter(
            is_active=True, category__is_active=True, stock__lte=5
        ).order_by("stock", "name")[:6],
        "recent_orders": orders.select_related("user").order_by("-created_at")[:7],
        "recent_posts": Post.objects.select_related("author").order_by("-updated_at")[:5],
    }
    return render(request, "dashboard/index.html", context)


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------
@staff_required
def product_list(request):
    queryset = Product.objects.select_related("category").all()
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    category_id = request.GET.get("category", "")
    if query:
        queryset = queryset.filter(Q(name__icontains=query) | Q(sku__icontains=query) | Q(slug__icontains=query))
    if status == "active":
        queryset = queryset.filter(is_active=True, category__is_active=True)
    elif status == "inactive":
        queryset = queryset.filter(Q(is_active=False) | Q(category__is_active=False))
    if category_id.isdigit():
        queryset = queryset.filter(category_id=int(category_id))
    page_obj = _paginate(request, queryset)
    return render(request, "dashboard/products.html", {
        "page_obj": page_obj,
        "query": query,
        "status": status,
        "selected_category": category_id,
        "categories": Category.objects.order_by("name"),
    })


@staff_required
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        product = form.save()
        messages.success(request, f"محصول «{product.name}» با موفقیت ایجاد شد.")
        return redirect("dashboard:products")
    return render(request, "dashboard/form.html", {
        "form": form, "page_title": "افزودن محصول جدید",
        "submit_label": "ذخیره محصول", "cancel_url": reverse("dashboard:products"),
    })


@staff_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"تغییرات محصول «{product.name}» ذخیره شد.")
        return redirect("dashboard:products")
    return render(request, "dashboard/form.html", {
        "form": form, "page_title": f"ویرایش محصول: {product.name}",
        "submit_label": "ذخیره تغییرات", "cancel_url": reverse("dashboard:products"),
    })


@staff_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        name = product.name
        product.delete()
        messages.success(request, f"محصول «{name}» حذف شد. سوابق سفارش‌های قبلی حفظ شده‌اند.")
        return redirect("dashboard:products")
    return render(request, "dashboard/confirm_delete.html", {
        "page_title": "حذف محصول", "object_name": product.name,
        "warning": "محصول از فروشگاه حذف می‌شود. نام و قیمت ثبت‌شده در سفارش‌های قبلی باقی می‌ماند.",
        "cancel_url": reverse("dashboard:products"),
    })


# ---------------------------------------------------------------------------
# Product categories
# ---------------------------------------------------------------------------
@staff_required
def category_list(request):
    queryset = Category.objects.annotate(product_count=Count("products")).order_by("name")
    query = request.GET.get("q", "").strip()
    if query:
        queryset = queryset.filter(name__icontains=query)
    return render(request, "dashboard/categories.html", {
        "page_obj": _paginate(request, queryset), "query": query,
    })


@staff_required
def category_create(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        category = form.save()
        messages.success(request, f"دسته‌بندی «{category.name}» ایجاد شد.")
        return redirect("dashboard:categories")
    return render(request, "dashboard/form.html", {
        "form": form, "page_title": "افزودن دسته‌بندی",
        "submit_label": "ذخیره دسته‌بندی", "cancel_url": reverse("dashboard:categories"),
    })


@staff_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"دسته‌بندی «{category.name}» به‌روزرسانی شد.")
        return redirect("dashboard:categories")
    return render(request, "dashboard/form.html", {
        "form": form, "page_title": f"ویرایش دسته‌بندی: {category.name}",
        "submit_label": "ذخیره تغییرات", "cancel_url": reverse("dashboard:categories"),
    })


@staff_required
@require_POST
def category_toggle(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.is_active = not category.is_active
    category.save(update_fields=["is_active"])
    if category.is_active:
        messages.success(request, f"دسته‌بندی «{category.name}» فعال شد؛ محصولات آن دوباره در فروشگاه نمایش داده می‌شوند، مشروط به فعال بودن خود محصول.")
    else:
        messages.warning(request, f"دسته‌بندی «{category.name}» غیرفعال شد؛ محصولات آن از فروشگاه عمومی پنهان شدند و حذف نشدند.")
    return redirect("dashboard:categories")


@staff_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    product_count = category.products.count()
    if request.method == "POST":
        name = category.name
        with transaction.atomic():
            category.delete()
        messages.success(request, f"دسته‌بندی «{name}» و {product_count} محصول وابسته حذف شدند. اطلاعات تاریخی سفارش‌ها حفظ شده است.")
        return redirect("dashboard:categories")
    return render(request, "dashboard/confirm_delete.html", {
        "page_title": "حذف دسته‌بندی",
        "object_name": category.name,
        "warning": f"با تأیید این عملیات، دسته‌بندی و تمام {product_count} محصول وابسته حذف می‌شوند. نام و قیمت اقلام سفارش‌های قبلی حفظ خواهد شد.",
        "cancel_url": reverse("dashboard:categories"),
    })


# ---------------------------------------------------------------------------
# Orders and customers
# ---------------------------------------------------------------------------
@staff_required
def order_list(request):
    queryset = Order.objects.select_related("user").all()
    status = request.GET.get("status", "")
    query = request.GET.get("q", "").strip()
    if status:
        queryset = queryset.filter(status=status)
    if query:
        search_filter = (
            Q(full_name__icontains=query) | Q(phone__icontains=query)
            | Q(user__username__icontains=query)
        )
        if query.isdigit():
            search_filter |= Q(pk=int(query))
        queryset = queryset.filter(search_filter)
    return render(request, "dashboard/orders.html", {
        "page_obj": _paginate(request, queryset), "status": status, "query": query,
        "status_choices": Order.STATUS_CHOICES,
    })


@staff_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related("user").prefetch_related("items__product"), pk=pk)
    form = OrderStatusForm(request.POST or None, instance=order)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"وضعیت سفارش #{order.pk} به‌روزرسانی شد.")
        return redirect("dashboard:order_detail", pk=order.pk)
    return render(request, "dashboard/order_detail.html", {"order": order, "form": form})


@staff_required
def user_list(request):
    User = get_user_model()
    queryset = User.objects.annotate(order_count=Count("orders")).order_by("-date_joined")
    query = request.GET.get("q", "").strip()
    if query:
        queryset = queryset.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query)
            | Q(last_name__icontains=query) | Q(email__icontains=query)
        )
    return render(request, "dashboard/users.html", {
        "page_obj": _paginate(request, queryset), "query": query,
    })


@staff_required
@require_POST
def user_toggle(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if user.is_staff or user.is_superuser:
        messages.error(request, "تغییر وضعیت حساب‌های مدیریتی از این بخش مجاز نیست.")
    else:
        user.is_active = not user.is_active
        user.save(update_fields=["is_active"])
        messages.success(request, f"حساب کاربری {user.username} {'فعال' if user.is_active else 'غیرفعال'} شد.")
    return redirect("dashboard:users")


# ---------------------------------------------------------------------------
# Blog content
# ---------------------------------------------------------------------------
@staff_required
def post_list(request):
    queryset = Post.objects.select_related("category", "author").all()
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    if query:
        queryset = queryset.filter(Q(title__icontains=query) | Q(slug__icontains=query))
    if status:
        queryset = queryset.filter(status=status)
    return render(request, "dashboard/posts.html", {
        "page_obj": _paginate(request, queryset), "query": query, "status": status,
        "post_statuses": Post.Status.choices,
    })


@staff_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        form.save_m2m()
        messages.success(request, f"مقاله «{post.title}» ذخیره شد.")
        return redirect("dashboard:posts")
    return render(request, "dashboard/form.html", {
        "form": form, "page_title": "افزودن مقاله جدید",
        "submit_label": "ذخیره مقاله", "cancel_url": reverse("dashboard:posts"),
    })


@staff_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"مقاله «{post.title}» به‌روزرسانی شد.")
        return redirect("dashboard:posts")
    return render(request, "dashboard/form.html", {
        "form": form, "page_title": f"ویرایش مقاله: {post.title}",
        "submit_label": "ذخیره تغییرات", "cancel_url": reverse("dashboard:posts"),
    })


@staff_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        title = post.title
        post.delete()
        messages.success(request, f"مقاله «{title}» حذف شد.")
        return redirect("dashboard:posts")
    return render(request, "dashboard/confirm_delete.html", {
        "page_title": "حذف مقاله", "object_name": post.title,
        "warning": "این عملیات مقاله را به‌صورت دائمی حذف می‌کند.",
        "cancel_url": reverse("dashboard:posts"),
    })


@staff_required
def blog_category_list(request):
    queryset = BlogCategory.objects.annotate(post_count=Count("posts")).order_by("name")
    query = request.GET.get("q", "").strip()
    if query:
        queryset = queryset.filter(name__icontains=query)
    return render(request, "dashboard/blog_categories.html", {
        "page_obj": _paginate(request, queryset), "query": query,
    })


@staff_required
def blog_category_create(request):
    form = BlogCategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save()
        messages.success(request, f"دسته‌بندی بلاگ «{obj.name}» ایجاد شد.")
        return redirect("dashboard:blog_categories")
    return render(request, "dashboard/form.html", {
        "form": form, "page_title": "افزودن دسته‌بندی بلاگ",
        "submit_label": "ذخیره دسته‌بندی", "cancel_url": reverse("dashboard:blog_categories"),
    })


@staff_required
def blog_category_update(request, pk):
    obj = get_object_or_404(BlogCategory, pk=pk)
    form = BlogCategoryForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"دسته‌بندی بلاگ «{obj.name}» به‌روزرسانی شد.")
        return redirect("dashboard:blog_categories")
    return render(request, "dashboard/form.html", {
        "form": form, "page_title": f"ویرایش دسته‌بندی بلاگ: {obj.name}",
        "submit_label": "ذخیره تغییرات", "cancel_url": reverse("dashboard:blog_categories"),
    })


@staff_required
@require_POST
def blog_category_toggle(request, pk):
    obj = get_object_or_404(BlogCategory, pk=pk)
    obj.is_active = not obj.is_active
    obj.save(update_fields=["is_active"])
    messages.success(request, f"دسته‌بندی بلاگ «{obj.name}» {'فعال' if obj.is_active else 'غیرفعال'} شد.")
    return redirect("dashboard:blog_categories")


@staff_required
def blog_category_delete(request, pk):
    obj = get_object_or_404(BlogCategory, pk=pk)
    count = obj.posts.count()
    if request.method == "POST":
        name = obj.name
        obj.delete()  # Related posts keep their content; category is set to NULL.
        messages.success(request, f"دسته‌بندی «{name}» حذف شد؛ {count} مقاله بدون دسته‌بندی باقی می‌مانند.")
        return redirect("dashboard:blog_categories")
    return render(request, "dashboard/confirm_delete.html", {
        "page_title": "حذف دسته‌بندی بلاگ", "object_name": obj.name,
        "warning": f"این دسته حذف می‌شود؛ {count} مقاله وابسته حذف نمی‌شوند و بدون دسته‌بندی باقی می‌مانند.",
        "cancel_url": reverse("dashboard:blog_categories"),
    })


@staff_required
def tag_list(request):
    queryset = Tag.objects.annotate(posts_count=Count("posts")).order_by("name")
    query = request.GET.get("q", "").strip()
    if query:
        queryset = queryset.filter(name__icontains=query)
    return render(request, "dashboard/tags.html", {
        "page_obj": _paginate(request, queryset), "query": query,
    })


@staff_required
def tag_create(request):
    form = TagForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        tag = form.save()
        messages.success(request, f"برچسب «{tag.name}» ایجاد شد.")
        return redirect("dashboard:tags")
    return render(request, "dashboard/form.html", {
        "form": form, "page_title": "افزودن برچسب بلاگ",
        "submit_label": "ذخیره برچسب", "cancel_url": reverse("dashboard:tags"),
    })


@staff_required
def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    form = TagForm(request.POST or None, instance=tag)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"برچسب «{tag.name}» به‌روزرسانی شد.")
        return redirect("dashboard:tags")
    return render(request, "dashboard/form.html", {
        "form": form, "page_title": f"ویرایش برچسب: {tag.name}",
        "submit_label": "ذخیره تغییرات", "cancel_url": reverse("dashboard:tags"),
    })


@staff_required
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    attached_posts = tag.posts.count()
    if request.method == "POST":
        name = tag.name
        tag.delete()  # Posts remain; only the many-to-many tag relation is removed.
        messages.success(request, f"برچسب «{name}» حذف شد؛ {attached_posts} مقاله حفظ شدند.")
        return redirect("dashboard:tags")
    return render(request, "dashboard/confirm_delete.html", {
        "page_title": "حذف برچسب", "object_name": tag.name,
        "warning": f"برچسب حذف می‌شود؛ مقالات وابسته حذف نمی‌شوند و فقط این برچسب از آن‌ها برداشته می‌شود. تعداد مقالات وابسته: {attached_posts}.",
        "cancel_url": reverse("dashboard:tags"),
    })


@staff_required
def comment_list(request):
    queryset = Comment.objects.select_related("post").all()
    state = request.GET.get("state", "pending")
    if state == "pending":
        queryset = queryset.filter(is_approved=False)
    elif state == "approved":
        queryset = queryset.filter(is_approved=True)
    return render(request, "dashboard/comments.html", {
        "page_obj": _paginate(request, queryset), "state": state,
    })


@staff_required
@require_POST
def comment_toggle(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.is_approved = not comment.is_approved
    comment.save(update_fields=["is_approved"])
    messages.success(request, f"دیدگاه {'تأیید' if comment.is_approved else 'از حالت تأیید خارج'} شد.")
    return redirect("dashboard:comments")


@staff_required
@require_POST
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    messages.success(request, "دیدگاه حذف شد.")
    return redirect("dashboard:comments")
