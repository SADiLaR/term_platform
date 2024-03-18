import unittest

from django.db.utils import IntegrityError
from django.test import TestCase

from general.models import Institution, Project


class TestProjects(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(
            name="Institution1",
            abbreviation="Inst1",
            url="http://institution1.com",
            email="institution1@example.com",
        )

        self.project1 = Project.objects.create(
            name="Centre1",
            url="http://example.com",
            start_date="2021-01-01",
            end_date="2021-01-01",
            institution=self.institution,
        )

        self.project2 = Project.objects.create(
            name="Centre2",
            url="http://test.com",
            logo="http://test.com/logo.png",
            start_date="2021-01-01",
            end_date="2021-01-01",
            institution=self.institution,
        )

    def test_project_creation(self):
        self.assertEqual(Project.objects.count(), 2)

    def test_project_name_unique(self):
        with self.assertRaises(IntegrityError):
            Project.objects.create(name="Centre1", url="http://example.com")

    def test_project_url_field(self):
        self.assertEqual(self.project1.url, "http://example.com")
        self.assertEqual(self.project2.url, "http://test.com")

    def test_project_name_str(self):
        self.assertEqual(str(self.project1), "Centre1")
        self.assertEqual(str(self.project2), "Centre2")

    def test_project_logo_field(self):
        self.assertEqual(self.project1.logo, "")
        self.assertEqual(self.project2.logo, "http://test.com/logo.png")

    def test_start_date(self):
        self.project1.start_date = "2021-01-01"
        self.project1.save()
        self.assertEqual(self.project1.start_date, "2021-01-01")

    def test_end_date(self):
        self.project1.end_date = "2021-01-01"
        self.project1.save()
        self.assertEqual(self.project1.end_date, "2021-01-01")


if __name__ == "__main__":
    unittest.main()
