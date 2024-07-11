import unittest

from django.test import TestCase

from general.filters import DocumentFileFilter
from general.models import DocumentFile, Institution, Language, Subject


class TestSearchFilter(TestCase):
    def setUp(self):
        self.institution1 = Institution.objects.create(name="Institution 1")
        self.institution2 = Institution.objects.create(name="Institution 2")

        # Create languages
        self.language1 = Language.objects.create(name="English", iso_code="EN")
        self.language2 = Language.objects.create(name="Afrikaans", iso_code="AF")

        # Create subjects
        self.subject1 = Subject.objects.create(name="Science")
        self.subject2 = Subject.objects.create(name="Math")

        # Create DocumentFiles
        self.doc1 = DocumentFile.objects.create(
            title="Document 1",
            document_data="Document 1 content",
            institution=self.institution1,
            document_type="glossary",
        )
        self.doc1.subjects.add(self.subject1)
        self.doc1.languages.add(self.language1)

        self.doc2 = DocumentFile.objects.create(
            title="Document 2",
            document_data="Document 2 content",
            institution=self.institution2,
            document_type="glossary",
        )
        self.doc2.subjects.add(self.subject2)
        self.doc2.languages.add(self.language2)

    def test_institution_filter(self):
        data = {"institution": [self.institution1.id]}
        filter = DocumentFileFilter(data=data)
        self.assertEqual(len(filter.qs), 1)
        self.assertIn(self.doc1, filter.qs)

    def test_document_type_filter(self):
        data = {"document_type": ["glossary"]}
        filter = DocumentFileFilter(data=data)
        self.assertEqual(len(filter.qs), 2)
        self.assertIn(self.doc1, filter.qs)
        self.assertIn(self.doc2, filter.qs)

    def test_subjects_filter(self):
        data = {"subjects": [self.subject1.id]}
        filter = DocumentFileFilter(data=data)
        self.assertEqual(len(filter.qs), 1)
        self.assertIn(self.doc1, filter.qs)

    def test_languages_filter(self):
        data = {"languages": [self.language1.id]}
        filter = DocumentFileFilter(data=data)
        self.assertEqual(len(filter.qs), 1)
        self.assertIn(self.doc1, filter.qs)

    def test_combined_filters(self):
        data = {
            "institution": [self.institution1.id],
            "document_type": ["glossary"],
            "subjects": [self.subject1.id],
            "languages": [self.language1.id],
        }
        filter = DocumentFileFilter(data=data)
        self.assertEqual(len(filter.qs), 1)
        self.assertIn(self.doc1, filter.qs)

    def test_search_filter(self):
        data = {"search": "Document"}
        filter = DocumentFileFilter(data=data)
        self.assertEqual(len(filter.qs), 2)
        self.assertIn(self.doc1, filter.qs)
        self.assertIn(self.doc2, filter.qs)

        data = {"search": "Document 1"}
        filter = DocumentFileFilter(data=data)
        self.assertEqual(len(filter.qs), 1)
        self.assertIn(self.doc1, filter.qs)


if __name__ == "__main__":
    unittest.main()
