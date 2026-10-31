from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import SignUpForm, TodoForm
from .models import Todo


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["signup_form"] = SignUpForm()
        context["next_url"] = self.request.POST.get("next") or self.request.GET.get("next", "")
        return context


def register_view(request):
    if request.user.is_authenticated:
        return redirect("todo_list")

    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect("todo_list")
    else:
        form = SignUpForm()

    return render(
        request,
        "registration/login.html",
        {"signup_form": form, "next_url": next_url},
    )


@login_required
def todo_list(request):
    filter_by = request.GET.get("filter", "all")
    todos = Todo.objects.filter(owner=request.user)
    if filter_by == "active":
        todos = todos.filter(completed=False)
    elif filter_by == "done":
        todos = todos.filter(completed=True)
    else:
        filter_by = "all"

    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.owner = request.user
            todo.save()
            messages.success(request, "Todo added.")
            return redirect("todo_list")
    else:
        form = TodoForm()

    return render(request, "todos/todo_list.html", {
        "todos": todos,
        "form": form,
        "filter": filter_by,
        "remaining": Todo.objects.filter(owner=request.user, completed=False).count(),
    })


@login_required
def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk, owner=request.user)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, "Todo updated.")
            return redirect("todo_list")
    else:
        form = TodoForm(instance=todo)
    return render(request, "todos/todo_edit.html", {"form": form, "todo": todo})


@login_required
@require_POST
def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk, owner=request.user)
    todo.completed = not todo.completed
    todo.save(update_fields=["completed", "updated_at"])
    return redirect(request.META.get("HTTP_REFERER") or "todo_list")


@login_required
@require_POST
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, owner=request.user)
    todo.delete()
    messages.success(request, "Todo deleted.")
    return redirect("todo_list")


@login_required
@require_POST
def todo_clear_completed(request):
    count, _ = Todo.objects.filter(owner=request.user, completed=True).delete()
    messages.success(request, f"Cleared {count} completed todo(s).")
    return redirect("todo_list")
