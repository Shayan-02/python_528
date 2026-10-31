from django.urls import path

from . import views

urlpatterns = [
    path("", views.todo_list, name="todo_list"),
    path("clear-completed/", views.todo_clear_completed, name="todo_clear_completed"),
    path("<int:pk>/edit/", views.todo_edit, name="todo_edit"),
    path("<int:pk>/toggle/", views.todo_toggle, name="todo_toggle"),
    path("<int:pk>/delete/", views.todo_delete, name="todo_delete"),
]
