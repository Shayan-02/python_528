from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.shortcuts import get_object_or_404, redirect, render
from products.models import Product
from .forms import CommentForm
from .models import BlogCategory, Post, Tag


def _post_list_context(request, queryset, active_category=None, active_tag=None):
    query = request.GET.get("q", "").strip()
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)
            | Q(excerpt__icontains=query)
            | Q(content__icontains=query)
        )

    featured_post = None
    if not active_category and not active_tag and not query:
        featured_post = queryset.filter(is_featured=True).select_related("category", "author").first()
        if featured_post:
            queryset = queryset.exclude(pk=featured_post.pk)
        if request.GET.get("page", "1") != "1":
            featured_post = None

    queryset = queryset.select_related("category", "author").prefetch_related("tags")
    paginator = Paginator(queryset, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "blog/post_list.html",
        {
            "page_obj": page_obj,
            "featured_post": featured_post,
            "query": query,
            "categories": BlogCategory.objects.filter(is_active=True),
            "tags": Tag.objects.filter(posts__in=Post.objects.published()).distinct()[:20],
            "active_category": active_category,
            "active_tag": active_tag,
        },
    )


def post_list(request):
    return _post_list_context(request, Post.objects.published())


def category_posts(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug, is_active=True)
    return _post_list_context(request, Post.objects.published().filter(category=category), active_category=category)


def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    return _post_list_context(request, Post.objects.published().filter(tags=tag), active_tag=tag)


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.published().select_related("category", "author").prefetch_related("tags"),
        slug=slug,
    )

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if not post.allow_comments:
            messages.error(request, "ثبت دیدگاه برای این مقاله غیرفعال است.")
            return redirect(post.get_absolute_url())
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "دیدگاه شما ثبت شد و پس از بررسی نمایش داده می‌شود.")
            return redirect(f"{post.get_absolute_url()}#comments")

    if request.method == "GET":
        Post.objects.filter(pk=post.pk).update(views=F("views") + 1)
        post.views += 1

    approved_comments = post.comments.filter(is_approved=True)
    related_posts = Post.objects.published().filter(category=post.category).exclude(pk=post.pk)[:3]
    related_products = post.related_products.filter(
        is_active=True,
        category__is_active=True,
    ).select_related("category")[:4]

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "form": form,
            "comments": approved_comments,
            "related_posts": related_posts,
            "related_products": related_products,
        },
    )
