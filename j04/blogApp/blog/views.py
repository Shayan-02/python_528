from django.shortcuts import get_object_or_404, render
from .models import Post
def home(request):
    posts = Post.objects.select_related("author").all()
    return render(request, "blog/home.html", {"posts": posts})
def detail(request, pk):
    post = get_object_or_404(Post.objects.select_related("author"), pk=pk)
    return render(request, "blog/detail.html", {"post": post})
