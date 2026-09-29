from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Post


POSTS_PER_PAGE = 4


def post_list(request):
    """Display posts with simple server-side pagination."""
    posts = Post.objects.select_related('author').all()

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page', "1")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    """Display a single post."""
    post = get_object_or_404(
        Post.objects.select_related('author'),
        pk=pk,
    )

    context = {
        'post': post,
    }

    return render(request, 'blog/post_detail.html', context)
