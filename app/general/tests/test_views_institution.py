from django.test import Client, TestCase
from django.urls import reverse

from general.models import Institution, Project


class InstitutionsViewTestCase(TestCase):
    def setUp(self):
        Institution.objects.create(name="Institution Banana")
        Institution.objects.create(name="Institution Apple")

        inst1 = Institution.objects.get(name="Institution Banana")
        Project.objects.create(name="Test Project 1", institution=inst1)
        Project.objects.create(name="Test Project 2", institution=inst1)

        self.url = reverse("institutions")

    def test_institutions_view_correct_template_used(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "app/institutions.html")

    def test_institutions_view_correct_context_returned(self):
        response = self.client.get(self.url)

        self.assertIn("current_page", response.context)
        self.assertIn("institutions", response.context)
        self.assertEqual(response.context["current_page"], "institutions")

    def test_institutions_view_correct_projects_returned(self):
        response = self.client.get(self.url)

        institutions = response.context["institutions"]
        self.assertEqual(len(institutions), 2)
        self.assertTrue(all(hasattr(inst, "project_count") for inst in institutions))
        self.assertEqual(institutions[0].project_count, 0)
        self.assertEqual(institutions[1].project_count, 2)

    def test_institutions_view_queries(self):
        response = self.client.get(self.url)

        with self.assertNumQueries(1):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
