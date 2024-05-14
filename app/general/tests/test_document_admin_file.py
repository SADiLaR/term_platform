import unittest

from django.core.files.uploadedfile import SimpleUploadedFile

from general.admin import DocumentFileForm
from general.models import Institution


class TestDocumentFileForm(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.form = None

    def setUp(self):
        pdf_file = b"%PDF-1.1 0 obj<</Pages 2 0 R>>endobj2 0 obj<</Kids[3 0 R]/Count 1>>endobj3 0 obj<</Parent 2 0 R>>endobjtrailer <</Root 1 0 R>>"

        self.file_mock = SimpleUploadedFile("test.pdf", pdf_file, content_type="application/pdf")

    def test_clean_without_url_and_file(self):
        tests_form = {
            "title": "Test",
            "license": "MIT",
            "document_type": "Glossary",
            "mime_type": "pdf",
            "institution": Institution.objects.create(name="Test Institution"),
            "url": "",
            "uploaded_file": "",
        }

        form = DocumentFileForm(tests_form)
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
            "institution": Institution.objects.create(name="Test Institution 2"),
            "url": "www.example.com",
            "uploaded_file": "",
        }

        form = DocumentFileForm(tests_form)
        self.assertTrue(form.is_valid())

    def test_clean_without_url(self):
        tests_form = {
            "title": "Test",
            "license": "CC0",
            "document_type": "Glossary",
            "mime_type": "pdf",
            "institution": Institution.objects.create(name="Test Institution 3"),
            "url": "",
            "uploaded_file": self.file_mock,
        }

        form = DocumentFileForm(tests_form, files={"uploaded_file": self.file_mock})
        self.assertTrue(form.is_valid())

    def test_clean_with_large_file(self):
        self.file_mock.size = 15728640

        tests_form = {
            "title": "Test",
            "license": "MIT",
            "document_type": "Glossary",
            "mime_type": "pdf",
            "institution": Institution.objects.create(name="Test Institution 4"),
            "url": "",
            "uploaded_file": self.file_mock,
        }

        form = DocumentFileForm(tests_form, files={"uploaded_file": self.file_mock})
        self.assertFalse(form.is_valid())
        self.assertIn("uploaded_file", form.errors)
        self.assertEqual(form.errors["uploaded_file"], ["File size must not exceed 10MB."])


if __name__ == "__main__":
    unittest.main()
