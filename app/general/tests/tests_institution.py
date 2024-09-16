import unittest

from django.test import TestCase

from general.models import Institution


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
        self.assertEqual(str(self.institution), "Test University (tu)")

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

    def test_history_records_creation(self):
        self.assertEqual(self.institution.history.count(), 1)
        self.assertEqual(self.institution.history.first().name, "Test University")
        self.assertEqual(self.institution.history.first().abbreviation, "tu")
        self.assertEqual(self.institution.history.first().url, "http://www.testuni.com")
        self.assertEqual(self.institution.history.first().email, "info@testuni.dev")
        self.assertEqual(self.institution.history.first().logo, "testuni.png")


if __name__ == "__main__":
    unittest.main()
