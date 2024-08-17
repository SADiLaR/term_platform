from django.test import TestCase
from django.urls import reverse

from general.models import Document, Institution, Language, Project


class LanguagesViewTest(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(
            name="Test Institution",
            abbreviation="TI",
            url="http://testinstitution.org",
            email="info@testinstitution.org",
        )

        self.language1 = Language.objects.create(name="English", iso_code="lang1")
        self.language2 = Language.objects.create(name="Spanish", iso_code="lang2")

        self.document1 = Document.objects.create(
            title="Document 1", institution=self.institution, document_type="report"
        )
        self.document1.languages.add(self.language1)

        self.document2 = Document.objects.create(
            title="Document 2", institution=self.institution, document_type="report"
        )
        self.document2.languages.add(self.language2)

        self.project1 = Project.objects.create(name="Project 1", institution=self.institution)
        self.project1.languages.add(self.language1)

        self.project2 = Project.objects.create(name="Project 2", institution=self.institution)
        self.project2.languages.add(self.language2)

    def test_view_basics(self):
        with self.assertNumQueries(3):
            response = self.client.get(reverse("languages"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="main-heading"')
