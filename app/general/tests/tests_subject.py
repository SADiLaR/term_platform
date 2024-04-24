import unittest

from django.test import TestCase

from general.models import Subject


class TestSubject(TestCase):
    def setUp(self):
        self.subject1 = Subject.objects.create(name="Mathematics")
        self.subject2 = Subject.objects.create(name="Science")

    def test_subject_creation(self):
        self.assertEqual(str(self.subject1), "Mathematics")
        self.assertEqual(str(self.subject2), "Science")

    def test_subject_name_uniqueness(self):
        with self.assertRaises(Exception):
            Subject.objects.create(name="Mathematics")

    def test_history_records_creation(self):
        self.assertEqual(self.subject1.history.count(), 1)
        self.assertEqual(self.subject1.history.first().name, "Mathematics")


if __name__ == "__main__":
    unittest.main()
