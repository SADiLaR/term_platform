import unittest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from general.models import DocumentFile, Institution, Language, Subject


class DocumentFileTest(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Test Subject")
        self.language = Language.objects.create(name="Test Language", iso_code="TL")
        self.institution = Institution.objects.create(name="Test Institution")

        self.title = "Some document"
        self.url = "https://example.com"
        self.uploaded_file = SimpleUploadedFile(
            "example.pdf", b"file_content", content_type="application/pdf"
        )
        self.license = "MIT"
        self.mime_type = "pdf"
        self.document_type = "Glossary"
        self.institution = self.institution

        self.document = DocumentFile.objects.create(
            title=self.title,
            url=self.url,
            uploaded_file=self.uploaded_file,
            license=self.license,
            mime_type=self.mime_type,
            document_type=self.document_type,
            Institution=self.institution,
        )
        self.document.subjects.add(self.subject)
        self.document.languages.add(self.language)

    def test_document_creation(self):
        self.assertEqual(DocumentFile.objects.count(), 1)
        self.assertEqual(DocumentFile.objects.get().title, self.title)

    def test_document_str_representation(self):  # Test __str__ method
        self.assertEqual(str(self.document), self.title)

    def test_document_available_by_default(self):  # Test default value
        self.assertTrue(self.document.available)


if __name__ == "__main__":
    unittest.main()
