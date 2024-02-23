import unittest

from django.db.utils import IntegrityError
from django.test import TestCase

from general.models import ContributingCentre, Subject

# from subject.models import Subject


class TestContributingCentre(TestCase):
    def setUp(self):
        self.subject1 = Subject.objects.create(name="Maths")
        self.subject2 = Subject.objects.create(name="Science")

        self.contrib_centre1 = ContributingCentre.objects.create(
            name="Centre1", url="http://example.com"
        )
        self.contrib_centre2 = ContributingCentre.objects.create(
            name="Centre2", url="http://test.com", logo="http://test.com/logo.png"
        )

        self.contrib_centre1.subjects.add(self.subject1, self.subject2)
        self.contrib_centre2.subjects.add(self.subject1)

    def test_centre_creation(self):
        self.assertEqual(ContributingCentre.objects.count(), 2)

    def test_centre_name_unique(self):
        with self.assertRaises(IntegrityError):
            ContributingCentre.objects.create(name="Centre1", url="http://example.com")

    def test_centre_url_field(self):
        self.assertEqual(self.contrib_centre1.url, "http://example.com")
        self.assertEqual(self.contrib_centre2.url, "http://test.com")

    def test_centre_name_str(self):
        self.assertEqual(str(self.contrib_centre1), "Centre1")
        self.assertEqual(str(self.contrib_centre2), "Centre2")

    def test_centre_logo_field(self):
        self.assertEqual(self.contrib_centre1.logo, "")
        self.assertEqual(self.contrib_centre2.logo, "http://test.com/logo.png")

    def test_centre_subject_field(self):
        self.assertEqual(list(self.contrib_centre1.subjects.all()), [self.subject1, self.subject2])
        self.assertEqual(list(self.contrib_centre2.subjects.all()), [self.subject1])


if __name__ == "__main__":
    unittest.main()
