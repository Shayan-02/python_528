from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Todo

User = get_user_model()


class AuthenticationTests(TestCase):
    def test_home_shows_login_and_signup_forms(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome back")
        self.assertContains(response, "Create an account")
        self.assertIn("signup_form", response.context)

    def test_todo_pages_require_login(self):
        response = self.client.get(reverse("todo_list"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"].split("?", 1)[0], reverse("home"))
        self.assertIn("next=", response["Location"])

    def test_register_creates_user_and_logs_them_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "StrongPass!234",
                "password2": "StrongPass!234",
            },
        )
        self.assertRedirects(response, reverse("todo_list"))
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_redirects_to_todo_list(self):
        user = User.objects.create_user(username="member", password="StrongPass!234")
        response = self.client.post(
            reverse("home"),
            {"username": "member", "password": "StrongPass!234"},
        )
        self.assertRedirects(response, reverse("todo_list"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_logout_redirects_to_home(self):
        user = User.objects.create_user(username="member", password="StrongPass!234")
        self.client.force_login(user)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)


class TodoViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="member", password="StrongPass!234")
        self.other_user = User.objects.create_user(username="other", password="StrongPass!234")
        self.client.force_login(self.user)

    def test_create_todo_assigns_current_user_as_owner(self):
        response = self.client.post(reverse("todo_list"), {"title": "Buy milk"})
        self.assertRedirects(response, reverse("todo_list"))
        todo = Todo.objects.get(title="Buy milk")
        self.assertEqual(todo.owner, self.user)

    def test_title_required(self):
        response = self.client.post(reverse("todo_list"), {"title": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Todo.objects.count(), 0)

    def test_user_sees_only_own_todos(self):
        own_todo = Todo.objects.create(title="Mine", owner=self.user)
        Todo.objects.create(title="Not mine", owner=self.other_user)
        response = self.client.get(reverse("todo_list"))
        self.assertContains(response, "Mine")
        self.assertNotContains(response, "Not mine")
        self.assertEqual(list(response.context["todos"]), [own_todo])

    def test_toggle(self):
        todo = Todo.objects.create(title="x", owner=self.user)
        response = self.client.post(reverse("todo_toggle", args=[todo.pk]))
        self.assertRedirects(response, reverse("todo_list"))
        todo.refresh_from_db()
        self.assertTrue(todo.completed)

    def test_edit(self):
        todo = Todo.objects.create(title="old", owner=self.user)
        response = self.client.post(reverse("todo_edit", args=[todo.pk]), {"title": "new"})
        self.assertRedirects(response, reverse("todo_list"))
        todo.refresh_from_db()
        self.assertEqual(todo.title, "new")

    def test_user_cannot_access_another_users_todo(self):
        todo = Todo.objects.create(title="private", owner=self.other_user)
        self.assertEqual(self.client.get(reverse("todo_edit", args=[todo.pk])).status_code, 404)
        self.assertEqual(self.client.post(reverse("todo_toggle", args=[todo.pk])).status_code, 404)
        self.assertEqual(self.client.post(reverse("todo_delete", args=[todo.pk])).status_code, 404)
        self.assertTrue(Todo.objects.filter(pk=todo.pk).exists())

    def test_delete_requires_post(self):
        todo = Todo.objects.create(title="x", owner=self.user)
        self.assertEqual(self.client.get(reverse("todo_delete", args=[todo.pk])).status_code, 405)
        response = self.client.post(reverse("todo_delete", args=[todo.pk]))
        self.assertRedirects(response, reverse("todo_list"))
        self.assertEqual(Todo.objects.count(), 0)

    def test_filters_and_clear_completed_only_affect_current_user(self):
        Todo.objects.create(title="a", completed=True, owner=self.user)
        Todo.objects.create(title="b", owner=self.user)
        other_completed = Todo.objects.create(title="other", completed=True, owner=self.other_user)

        response = self.client.get(reverse("todo_list"), {"filter": "active"})
        self.assertEqual(len(response.context["todos"]), 1)

        self.client.post(reverse("todo_clear_completed"))
        self.assertEqual(Todo.objects.filter(owner=self.user).count(), 1)
        self.assertTrue(Todo.objects.filter(pk=other_completed.pk).exists())
