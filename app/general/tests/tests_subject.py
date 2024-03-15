import unittest

from django.test import TestCase

from general.models import Project, Subject


class TestSubject(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Maths")
        self.subject2 = Subject.objects.create(name="Science")

    def test_subject_creation(self):
        self.assertEqual(self.subject.name, "Maths")
        self.assertEqual(self.subject.__str__(), "Maths")

    def test_subject_name_uniqueness(self):
        duplicate_subject = Subject(name="Maths")
        self.assertRaises(Exception, duplicate_subject.save)

    def test_contributing_centre_relationship(self):
        contributing_centre = Project(name="Test Centre")
        contributing_centre.save()
        self.subject.contributing_centre.add(contributing_centre)
        self.assertTrue(contributing_centre in self.subject.contributing_centre.all())

    def test_blank_contributing_centre(self):
        self.assertEqual(self.subject.contributing_centre.count(), 0)


if __name__ == "__main__":
    unittest.main()
