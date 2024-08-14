from django.test import TestCase
from django.urls import reverse

from general.models import Institution, Language, Project, Subject


class ProjectDetailViewTests(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name="Test University")

        self.project = Project.objects.create(
            name="Test Project",
            description="This is a test project",
            url="https://example.com",
            logo="path/to/logo.png",
            start_date="2020-01-01",
            end_date="2021-01-01",
            institution=self.institution,
        )
        self.subject1 = Subject.objects.create(name="Subject 1")
        self.subject2 = Subject.objects.create(name="Subject 2")

        self.project.subjects.add(self.subject1, self.subject2)

        self.language1 = Language.objects.create(name="Language 1", iso_code="lang1")
        self.language2 = Language.objects.create(name="Language 2", iso_code="lang2")

        self.project.languages.add(self.language1, self.language2)

    def test_project_detail_view(self):
        response = self.client.get(reverse("project_detail", args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="main-heading"')
        self.assertContains(response, self.project.name)
        self.assertContains(response, self.project.url)
        self.assertContains(response, self.institution.name)
        self.assertContains(response, self.subject1.name)
        self.assertContains(response, self.language1.name)

    def test_project_detail_view_context(self):
        response = self.client.get(reverse("project_detail", args=[self.project.id]))
        self.assertIn("project", response.context)
        self.assertIn("logo", response.context)
        self.assertIn("subjects", response.context)
        self.assertIn("languages", response.context)
        self.assertEqual(response.context["project"], self.project)
        self.assertEqual(list(response.context["subjects"]), [self.subject1, self.subject2])
        self.assertEqual(list(response.context["languages"]), [self.language1, self.language2])

    def test_project_detail_view_num_queries(self):
        with self.assertNumQueries(3):
            response = self.client.get(reverse("project_detail", args=[self.project.id]))

    def test_project_detail_view_invalid_id(self):
        invalid_project_id = self.project.id + 1
        response = self.client.get(reverse("project_detail", args=[invalid_project_id]))
        self.assertEqual(response.status_code, 404)
