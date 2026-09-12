from django.contrib import admin


"""
URL configuration for app project.
"""

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("books.urls")),
]
