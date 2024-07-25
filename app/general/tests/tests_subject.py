from django.test import TestCase
from django.urls import reverse

from general.models import DocumentFile, Institution, Project, Subject


class TestSubjects(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(
            name="Test Institution",
            abbreviation="TI",
            url="http://testinstitution.org",
            email="info@testinstitution.org",
        )

        self.subject1 = Subject.objects.create(name="Mathematics")
        self.subject2 = Subject.objects.create(name="Science")

        self.document1 = DocumentFile.objects.create(
            title="Document 1", institution=self.institution, document_type="report"
        )
        self.document1.subjects.add(self.subject1)

        self.document2 = DocumentFile.objects.create(
            title="Document 2", institution=self.institution, document_type="report"
        )
        self.document2.subjects.add(self.subject2)

        self.project1 = Project.objects.create(name="Project 1", institution=self.institution)
        self.project1.subjects.add(self.subject1)

        self.project2 = Project.objects.create(name="Project 2", institution=self.institution)
        self.project2.subjects.add(self.subject2)

    def test_subject_creation(self):
        self.assertEqual(str(self.subject1), "Mathematics")
        self.assertEqual(str(self.subject2), "Science")

    def test_subject_name_uniqueness(self):
        with self.assertRaises(Exception):
            Subject.objects.create(name="Mathematics")

    def test_history_records_creation(self):
        self.assertEqual(self.subject1.history.count(), 1)
        self.assertEqual(self.subject1.history.first().name, "Mathematics")

    def test_subjects_view_num_queries(self):
        with self.assertNumQueries(3):
            response = self.client.get(reverse("subjects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/subjects.html")
        self.assertTrue("subject_data" in response.context)
        self.assertTrue("page_obj" in response.context)
