from django.test import TestCase
from django.urls import reverse

from general.models import Document, Institution, Language, Subject


class DocumentViewTests(TestCase):
    def setUp(self):
        self.subject1 = Subject.objects.create(name="Subject 1")
        self.subject2 = Subject.objects.create(name="Subject 2")
        self.language1 = Language.objects.create(name="Language 1", iso_code="lang1")
        self.language2 = Language.objects.create(name="Language 2", iso_code="lang2")
        self.language3 = Language.objects.create(name="Language 3", iso_code="lang3")
        self.language4 = Language.objects.create(name="Language 4", iso_code="lang4")
        self.institution = Institution.objects.create(
            name="Institution", logo="institution_logo.png"
        )

        self.document5 = Document.objects.create(
            title="Document 5",
            institution=self.institution,
        )
        self.document5.subjects.add(self.subject1)
        self.document5.languages.add(self.language1)

        self.document6 = Document.objects.create(
            title="Document 6",
            institution=self.institution,
        )
        self.document6.subjects.add(self.subject1)
        self.document6.languages.add(self.language1)
        self.document6.languages.add(self.language2)
        self.document6.languages.add(self.language3)
        self.document6.languages.add(self.language4)

    def test_view_basics(self):
        with self.assertNumQueries(7):
            response = self.client.get(reverse("documents"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="main-heading"')
        self.assertIn("documents", response.context)

    def test_with_filters(self):
        response = self.client.get(reverse("documents"), {"language": self.language3.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["documents"]), 1)
        self.assertEqual(response.context["documents"][0]["document"].title, "Document 6")
