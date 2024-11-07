from django.test import TestCase
from django.urls import reverse

from general.models import Document, Institution, Language, Subject


class DocumentDetailViewTest(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name="University of Cape Town")

        self.subject1 = Subject.objects.create(name="Anatomy")
        self.subject2 = Subject.objects.create(name="Biology")

        self.language1 = Language.objects.create(name="Afrikaans", iso_code="af")
        self.language2 = Language.objects.create(name="English", iso_code="en")

        self.document = Document.objects.create(
            title="Afrikaans_HL_P1_Feb-March_2011",
            description="This is a description of the document.",
            url="https://externaldocumentrepository.com/document1",
            uploaded_file="path/to/document.pdf",
            available=True,
            license="(c)",
            document_type="Glossary",
            institution=self.institution,
            mime_type="application/pdf",
            document_data="",
            search_vector=None,
        )
        self.document.subjects.add(self.subject1, self.subject2)
        self.document.languages.add(self.language1, self.language2)

    def test_document_detail_num_queries(self):
        url = reverse("document_detail", args=[self.document.id])
        with self.assertNumQueries(3):
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="main-heading"')
        self.assertContains(response, self.document.title)
        self.assertContains(response, self.institution.name)
        self.assertContains(response, self.subject1.name)
        self.assertContains(response, self.language1.name)
