from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import TodoForm
from .models import Todo


def todo_list(request):
    filter_by = request.GET.get("filter", "all")
    todos = Todo.objects.all()
    if filter_by == "active":
        todos = todos.filter(completed=False)
    elif filter_by == "done":
        todos = todos.filter(completed=True)
    else:
        filter_by = "all"

    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Todo added.")
            return redirect("todo_list")
    else:
        form = TodoForm()

    return render(request, "todos/todo_list.html", {
        "todos": todos,
        "form": form,
        "filter": filter_by,
        "remaining": Todo.objects.filter(completed=False).count(),
    })


def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, "Todo updated.")
            return redirect("todo_list")
    else:
        form = TodoForm(instance=todo)
    return render(request, "todos/todo_edit.html", {"form": form, "todo": todo})


@require_POST
def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save(update_fields=["completed", "updated_at"])
    return redirect(request.META.get("HTTP_REFERER") or "todo_list")

@login_required
@require_POST
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    messages.success(request, "Todo deleted.")
    return redirect("todo_list")

@login_required
@require_POST
def todo_clear_completed(request):
    count, _ = Todo.objects.filter(completed=True).delete()
    messages.success(request, f"Cleared {count} completed todo(s).")
    return redirect("todo_list")
