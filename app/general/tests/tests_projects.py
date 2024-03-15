import unittest

from django.db.utils import IntegrityError
from django.test import TestCase

from general.models import Project, Subject

# from subject.models import Subject


class TestProjects(TestCase):
    def setUp(self):
        self.subject1 = Subject.objects.create(name="Maths")
        self.subject2 = Subject.objects.create(name="Science")

        self.project1 = Project.objects.create(name="Centre1", url="http://example.com")
        self.project2 = Project.objects.create(
            name="Centre2", url="http://test.com", logo="http://test.com/logo.png"
        )

        # self.project1.subjects.add(self.subject1, self.subject2)
        # self.project2.subjects.add(self.subject1)

    def test_centre_creation(self):
        self.assertEqual(Project.objects.count(), 2)

    def test_centre_name_unique(self):
        with self.assertRaises(IntegrityError):
            Project.objects.create(name="Centre1", url="http://example.com")

    def test_centre_url_field(self):
        self.assertEqual(self.project1.url, "http://example.com")
        self.assertEqual(self.project2.url, "http://test.com")

    def test_centre_name_str(self):
        self.assertEqual(str(self.project1), "Centre1")
        self.assertEqual(str(self.project2), "Centre2")

    def test_centre_logo_field(self):
        self.assertEqual(self.project1.logo, "")
        self.assertEqual(self.project2.logo, "http://test.com/logo.png")

    def test_centre_subject_field(self):
        self.assertEqual(list(self.project1.subjects.all()), [self.subject1, self.subject2])
        self.assertEqual(list(self.project2.subjects.all()), [self.subject1])

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
