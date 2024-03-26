import unittest

from django.test import TestCase

from general.models import Subject


class TestSubject(TestCase):
    def setUp(self):
        # pass
        self.subject = Subject.objects.create(name="Maths")
        self.subject2 = Subject.objects.create(name="Science")

    def test_subject_creation(self):
        self.assertEqual(self.subject.name, "Maths")
        self.assertEqual(self.subject.__str__(), "Maths")

    def test_subject_name_uniqueness(self):
        duplicate_subject = Subject(name="Maths")
        self.assertRaises(Exception, duplicate_subject.save)


if __name__ == "__main__":
    unittest.main()
