import os
import unittest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from general.admin import DocumentForm, DocumentFormWithFulltext
from general.models import Document, Institution


class TestDocumentForm(TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.form = None

    def setUp(self):
        test_dir = os.getenv("TESTING_DIR", "/app/general/tests/files")
        test_file = test_dir + "/Lorem.pdf"

        with open(test_file, "rb") as f:
            pdf_file = f.read()

        self.file_mock = SimpleUploadedFile("test.pdf", pdf_file, content_type="application/pdf")
        self.test_institution = Institution.objects.create(
            name="Test Institution for Document tests"
        )

    def tearDown(self):
        self.test_institution.delete()

    def test_clean_without_url_and_file(self):
        tests_form = {
            "title": "Test",
            "license": "MIT",
            "document_type": "Glossary",
            "mime_type": "pdf",
            "institution": self.test_institution,
            "url": "",
            "uploaded_file": "",
            "description": "Test description",
        }

        form = DocumentForm(tests_form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["url"], ["Either URL or uploaded file must be provided."])
        self.assertEqual(
            form.errors["uploaded_file"], ["Either URL or uploaded file must be provided."]
        )

    def test_clean_without_file(self):
        tests_form = {
            "title": "Test",
            "license": "(c)",
            "document_type": "Glossary",
            "mime_type": "pdf",
            "institution": self.test_institution,
            "url": "www.example.com",
            "uploaded_file": "",
            "document_data": "",
            "description": "",
        }

        form = DocumentForm(tests_form)
        self.assertTrue(form.is_valid())

    #
    def test_clean_without_url(self):
        tests_form = {
            "title": "Test",
            "license": "CC0",
            "document_type": "Glossary",
            "mime_type": "pdf",
            "institution": self.test_institution,
            "url": "",
            "uploaded_file": self.file_mock,
            "document_data": "",
            "description": "Test description",
        }

        form = DocumentForm(tests_form, files={"uploaded_file": self.file_mock})
        self.assertTrue(form.is_valid())

    def test_clean_with_large_file(self):
        self.file_mock.size = 15728640

        tests_form = {
            "title": "Test",
            "license": "MIT",
            "document_type": "Glossary",
            "mime_type": "pdf",
            "institution": self.test_institution,
            "url": "",
            "uploaded_file": self.file_mock,
            "description": "Test description",
        }

        form = DocumentForm(tests_form, files={"uploaded_file": self.file_mock})
        self.assertFalse(form.is_valid())
        self.assertIn("uploaded_file", form.errors)
        self.assertEqual(form.errors["uploaded_file"], ["File size must not exceed 10MB."])

    def test_edited_pdf_takes_priority_over_unedited_fulltext(self):
        tests_form = {
            "title": "Test",
            "license": "CC0",
            "document_type": "Glossary",
            "mime_type": "pdf",
            "institution": self.test_institution,
            "url": "",
            "uploaded_file": self.file_mock,
            "document_data": "",
            "description": "Test description",
        }

        # Test both kinds of forms - both can have edited PDFs and unedited fulltext
        for FormType in [DocumentForm, DocumentFormWithFulltext]:
            form = FormType(tests_form, files={"uploaded_file": self.file_mock})
            self.assertTrue(form.is_valid())
            self.assertNotEqual(form.cleaned_data["document_data"], "")

    def test_edited_fulltext_takes_priority_over_edited_pdf(self):
        custom_data = "testingstringthatisnotinsidelorem.pdf"
        tests_form = {
            "title": "Test",
            "license": "CC0",
            "document_type": "Glossary",
            "mime_type": "pdf",
            "institution": self.test_institution,
            "url": "",
            "uploaded_file": self.file_mock,
            "document_data": custom_data,
            "description": "Test description",
        }

        # We only test the DocumentFormWithFulltext because this is the only one that can have edited fulltext
        form = DocumentFormWithFulltext(tests_form, files={"uploaded_file": self.file_mock})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["document_data"], custom_data)

    def test_edited_fulltext_reflects_in_database_and_search(self):
        title = "Test document with edited fulltext"
        custom_data = "testingstringthatisnotinsidelorem.pdf"

        original_form = {
            "title": title,
            "license": "CC0",
            "document_type": "Glossary",
            "mime_type": "pdf",
            "institution": self.test_institution,
            "url": "",
            "uploaded_file": self.file_mock,
            "document_data": "",
            "description": "Test description",
        }

        # Upload the form with the PDF fulltext extracted
        form = DocumentForm(original_form, files={"uploaded_file": self.file_mock})
        self.assertTrue(form.is_valid())
        doc = form.save()
        orig_fulltext = doc.document_data
        self.assertNotEqual(orig_fulltext, custom_data)

        # Check we can search by PDF content
        response = self.client.get(reverse("search"), {"search": orig_fulltext})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"][0]["heading"], title)

        # Now, upload a copy with edited fulltext
        edit_form = {**original_form, "document_data": custom_data, "id": doc.id}
        form = DocumentFormWithFulltext(
            edit_form, files={"uploaded_file": self.file_mock}, instance=doc
        )
        self.assertTrue(form.is_valid())
        doc = form.save()
        self.assertEqual(doc.document_data, custom_data)

        # Check that: 1. we only have one document with this title, and 2. it has the correct fulltext
        self.assertEqual(Document.objects.get(title=title).document_data, custom_data)

        # Check we can search by the new content too
        response = self.client.get(reverse("search"), {"search": custom_data})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"][0]["heading"], title)

        # Check that we CANNOT search by the old content anymore
        response = self.client.get(reverse("search"), {"search": orig_fulltext})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 0)


if __name__ == "__main__":
    unittest.main()
