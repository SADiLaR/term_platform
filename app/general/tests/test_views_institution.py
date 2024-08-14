from django.test import Client, TestCase
from django.urls import reverse

from general.models import DocumentFile, Institution, Project


class InstitutionsViewTestCase(TestCase):
    def setUp(self):
        inst1 = Institution.objects.create(
            name="Institution Banana",
            abbreviation="UniB",
            url="unibanana.co.za",
            email="unibanana@email.com",
            logo="/unibanana/logo",
        )
        Institution.objects.create(
            name="Institution Apple", abbreviation="UniA", url="uniapple.co.za"
        )

        Project.objects.create(name="Test Project 1", institution=inst1)
        Project.objects.create(name="Test Project 2", institution=inst1)
        DocumentFile.objects.create(title="Test document 1", institution=inst1)
        DocumentFile.objects.create(title="Test document 2", institution=inst1)

        self.url = reverse("institutions")

    def test_view_basics(self):
        with self.assertNumQueries(1):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="main-heading"')
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
        self.assertTrue(all("project_count" in inst for inst in institutions))
        self.assertEqual(institutions[0]["project_count"], 0)
        self.assertEqual(institutions[1]["project_count"], 2)
        self.assertEqual(institutions[0]["document_count"], 0)
        self.assertEqual(institutions[1]["document_count"], 2)

    def test_institution_ratings(self):
        response = self.client.get(self.url)

        institutions = response.context["institutions"]

        institution1 = next(inst for inst in institutions if inst["name"] == "Institution Apple")
        institution2 = next(inst for inst in institutions if inst["name"] == "Institution Banana")

        self.assertEqual(institution1["rating"], 60)
        self.assertEqual(institution2["rating"], 100)
