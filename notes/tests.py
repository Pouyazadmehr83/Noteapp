from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Note

User = get_user_model()


class NoteViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="pass123456")
        self.other = User.objects.create_user(username="other", password="pass123456")
        self.first_note = Note.objects.create(
            User=self.owner,
            title="Weekly update",
            content="Sprint demo checklist",
        )
        self.second_note = Note.objects.create(
            User=self.owner,
            title="Roadmap",
            content="Search and pagination backlog",
        )
        self.other_note = Note.objects.create(
            User=self.other,
            title="Private note",
            content="Should stay hidden",
        )

    def test_list_requires_login(self):
        response = self.client.get(reverse("notes:read"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.headers["Location"])

    def test_list_shows_only_user_notes(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("notes:read"))
        self.assertContains(response, "Weekly update")
        self.assertContains(response, "Roadmap")
        self.assertNotContains(response, "Private note")

    def test_search_filters_by_query(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("notes:read"), {"q": "roadmap"})
        self.assertContains(response, "Roadmap")
        self.assertNotContains(response, "Weekly update")

    def test_detail_404_for_other_user(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("notes:detail", args=[self.other_note.pk]))
        self.assertEqual(response.status_code, 404)

    def test_detail_404_for_missing_pk(self):
        self.client.force_login(self.owner)
        missing_pk = self.other_note.pk + 999
        response = self.client.get(reverse("notes:detail", args=[missing_pk]))
        self.assertEqual(response.status_code, 404)

    def test_create_assigns_current_user(self):
        self.client.force_login(self.owner)
        payload = {"title": "New idea", "content": "Ship onboarding"}
        response = self.client.post(reverse("notes:create"), payload, follow=True)
        self.assertContains(response, "New idea")
        self.assertTrue(Note.objects.filter(User=self.owner, title="New idea").exists())

    def test_update_validation_errors_rendered(self):
        self.client.force_login(self.owner)
        url = reverse("notes:update", args=[self.first_note.pk])
        response = self.client.post(url, {"title": "", "content": ""})
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("This field is required.", form.errors["title"])

    def test_delete_requires_post(self):
        self.client.force_login(self.owner)
        url = reverse("notes:delete", args=[self.first_note.pk])
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTrue(Note.objects.filter(pk=self.first_note.pk).exists())
        post_response = self.client.post(url)
        self.assertRedirects(post_response, reverse("notes:read"))
        self.assertFalse(Note.objects.filter(pk=self.first_note.pk).exists())
