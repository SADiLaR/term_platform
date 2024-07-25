import unittest

from django.test import Client, TestCase
from django.urls import reverse

from general.models import DocumentFile, Institution, Language, Subject


class SearchViewTest(TestCase):
    def setUp(self):
        # Create institutions
        self.institution1 = Institution.objects.create(name="Institution 1")
        self.institution2 = Institution.objects.create(name="Institution 2")

        # Create languages
        self.language1 = Language.objects.create(name="English", iso_code="EN")
        self.language2 = Language.objects.create(name="Afrikaans", iso_code="AF")

        # Create subjects
        self.subject1 = Subject.objects.create(name="Science")
        self.subject2 = Subject.objects.create(name="Math")

        # Create DocumentFiles
        for i in range(10):
            doc = DocumentFile.objects.create(
                title=f"Document {i + 1}",
                institution=self.institution1 if i % 2 == 0 else self.institution2,
                document_type="report" if i % 2 == 0 else "article",
                document_data="Document {i + 1} content",
            )
            doc.subjects.add(self.subject1 if i % 2 == 0 else self.subject2)
            doc.languages.add(self.language1 if i % 2 == 0 else self.language2)

    def test_search_pagination(self):
        client = Client()
        response = client.get(reverse("search"), {"page": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["documents"]), 5)

        response = client.get(reverse("search"), {"page": "2"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["documents"]), 5)

        response = client.get(reverse("search"), {"page": "3"})
        self.assertEqual(response.status_code, 200)

    def test_search_filtering(self):
        client = Client()
        response = client.get(reverse("search"), {"search": "Document 1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["documents"][0]["heading"], "Document 1")

    def test_invalid_page_number(self):
        client = Client()
        response = client.get(reverse("search"), {"page": "invalid"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["documents"]), 5)

    def test_combined_filters(self):
        client = Client()
        response = client.get(
            reverse("search"),
            {
                "institution": self.institution1.id,
                "document_type": "report",
                "subjects": self.subject1.id,
                "languages": self.language1.id,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["documents"]), 5)


if __name__ == "__main__":
    unittest.main()
