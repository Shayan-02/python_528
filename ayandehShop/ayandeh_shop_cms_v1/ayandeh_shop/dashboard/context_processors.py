from blog.models import Comment


def cms_sidebar_context(request):
    """Expose small staff-only sidebar counters without querying for customers."""
    if request.user.is_authenticated and request.user.is_staff:
        return {"pending_comments_count": Comment.objects.filter(is_approved=False).count()}
    return {"pending_comments_count": 0}
