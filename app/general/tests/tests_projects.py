import unittest
from datetime import datetime

from django.test import TestCase

from general.models import Institution, Project, Subject


class TestProjects(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name="Test Institution")
        self.subject = Subject.objects.create(name="Test Subject")
        self.project = Project.objects.create(
            name="Test Project",
            url="http://test.com",
            logo="http://test.com/logo.png",
            start_date="2023-01-01",
            end_date="2023-12-31",
            Institution=self.institution,
        )
        self.project.subject.add(self.subject)

    def test_project_creation(self):
        self.assertTrue(isinstance(self.project, Project))
        self.assertEqual(self.project.__str__(), "Test Project")
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.url, "http://test.com")
        self.assertEqual(self.project.logo, "http://test.com/logo.png")
        self.assertEqual(self.project.start_date, "2023-01-01")
        self.assertEqual(self.project.end_date, "2023-12-31")
        self.assertEqual(self.project.Institution, self.institution)
        self.assertEqual(self.project.subject, self.project.subject)

    def test_project_name(self):
        self.assertEqual(self.project.name, "Test Project")

    def test_project_url(self):
        self.assertEqual(self.project.url, "http://test.com")

    def test_project_start_date(self):
        date_format = "%Y-%m-%d"
        end_date = datetime.strptime(self.project.start_date, date_format)
        self.assertEqual(end_date.strftime(date_format), "2023-01-01")

    def test_project_end_date(self):
        date_format = "%Y-%m-%d"
        end_date = datetime.strptime(self.project.end_date, date_format)
        self.assertEqual(end_date.strftime(date_format), "2023-12-31")

    def test_project_institution(self):
        self.assertEqual(self.project.Institution.name, "Test Institution")

    def test_project_subject(self):
        self.assertTrue(self.project.subject.filter(name="Test Subject").exists())

    def test_str(self):
        self.assertEqual(str(self.project), "Test Project")


if __name__ == "__main__":
    unittest.main()
