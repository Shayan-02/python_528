from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("login/", views.CMSLoginView.as_view(), name="login"),
    path("logout/", views.CMSLogoutView.as_view(), name="logout"),
    path("", views.index, name="index"),

    path("products/", views.product_list, name="products"),
    path("products/add/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_update, name="product_update"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),

    path("categories/", views.category_list, name="categories"),
    path("categories/add/", views.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", views.category_update, name="category_update"),
    path("categories/<int:pk>/toggle/", views.category_toggle, name="category_toggle"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),

    path("orders/", views.order_list, name="orders"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    path("users/", views.user_list, name="users"),
    path("users/<int:pk>/toggle/", views.user_toggle, name="user_toggle"),

    path("posts/", views.post_list, name="posts"),
    path("posts/add/", views.post_create, name="post_create"),
    path("posts/<int:pk>/edit/", views.post_update, name="post_update"),
    path("posts/<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("blog-categories/", views.blog_category_list, name="blog_categories"),
    path("blog-categories/add/", views.blog_category_create, name="blog_category_create"),
    path("blog-categories/<int:pk>/edit/", views.blog_category_update, name="blog_category_update"),
    path("blog-categories/<int:pk>/toggle/", views.blog_category_toggle, name="blog_category_toggle"),
    path("blog-categories/<int:pk>/delete/", views.blog_category_delete, name="blog_category_delete"),
    path("tags/", views.tag_list, name="tags"),
    path("tags/add/", views.tag_create, name="tag_create"),
    path("tags/<int:pk>/edit/", views.tag_update, name="tag_update"),
    path("tags/<int:pk>/delete/", views.tag_delete, name="tag_delete"),
    path("comments/", views.comment_list, name="comments"),
    path("comments/<int:pk>/toggle/", views.comment_toggle, name="comment_toggle"),
    path("comments/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
]
