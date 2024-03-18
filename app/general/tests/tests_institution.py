import unittest

from django.test import TestCase

from general.models import Institution, Project


class TestInstitution(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Centre",
            url="http://example.com",
            start_date="2021-01-01",
            end_date="2021-01-01",
            institution=1,
            # add additional fields here as required by the ProjectsAdmin model
        )

        self.institution = Institution.objects.create(
            name="Test University",
            abbreviation="tu",
            url="http://www.testuni.com",
            email="info@testuni.dev",
            logo="testuni.png",
            project=self.project,
        )

    def test_institution_creation(self):
        self.assertIsInstance(self.institution, Institution)

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

    def test_project(self):
        self.assertEqual(self.institution.projects, self.project)


if __name__ == "__main__":
    unittest.main()
