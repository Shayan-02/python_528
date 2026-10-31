from django.test import TestCase
from django.urls import reverse

from .models import Todo


class TodoViewTests(TestCase):
    def test_create_todo(self):
        resp = self.client.post(reverse("todo_list"), {"title": "Buy milk"})
        self.assertRedirects(resp, reverse("todo_list"))
        self.assertEqual(Todo.objects.count(), 1)

    def test_title_required(self):
        resp = self.client.post(reverse("todo_list"), {"title": ""})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Todo.objects.count(), 0)

    def test_toggle(self):
        t = Todo.objects.create(title="x")
        self.client.post(reverse("todo_toggle", args=[t.pk]))
        t.refresh_from_db()
        self.assertTrue(t.completed)

    def test_edit(self):
        t = Todo.objects.create(title="old")
        self.client.post(reverse("todo_edit", args=[t.pk]), {"title": "new"})
        t.refresh_from_db()
        self.assertEqual(t.title, "new")

    def test_delete_requires_post(self):
        t = Todo.objects.create(title="x")
        self.assertEqual(self.client.get(reverse("todo_delete", args=[t.pk])).status_code, 405)
        self.client.post(reverse("todo_delete", args=[t.pk]))
        self.assertEqual(Todo.objects.count(), 0)

    def test_filters_and_clear_completed(self):
        Todo.objects.create(title="a", completed=True)
        Todo.objects.create(title="b")
        resp = self.client.get(reverse("todo_list"), {"filter": "active"})
        self.assertEqual(len(resp.context["todos"]), 1)
        self.client.post(reverse("todo_clear_completed"))
        self.assertEqual(Todo.objects.count(), 1)
