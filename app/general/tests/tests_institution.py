import unittest

from django.test import TestCase

from general.models import Institution, Project


class TestInstitution(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(
            name="Test University",
            abbreviation="tu",
            url="http://www.testuni.com",
            email="info@testuni.dev",
            logo="testuni.png",
        )

    def test_institution_creation(self):
        self.assertTrue(isinstance(self.institution, Institution))
        self.assertEqual(self.institution.__str__(), "Test University")

    def test_institution_name(self):
        self.assertEqual(self.institution.name, "Test University")

    def test_institution_abbreviation(self):
        self.assertEqual(self.institution.abbreviation, "tu")

    def test_institution_url(self):
        self.assertEqual(self.institution.url, "http://www.testuni.com")

    def test_institution_email(self):
        self.assertEqual(self.institution.email, "info@testuni.dev")

    def test_institution_logo(self):
        self.assertEqual(self.institution.logo, "testuni.png")


if __name__ == "__main__":
    unittest.main()
