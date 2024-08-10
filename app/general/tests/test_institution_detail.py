from django.http import Http404
from django.test import TestCase
from django.urls import reverse

from general.models import DocumentFile, Institution, Project


class InstitutionDetailViewTests(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(
            name="Sample Institution",
            abbreviation="SI",
            url="https://example.com",
            email="info@example.com",
            logo="path/to/logo.png",
        )

    def test_institution_detail_view_with_valid_id(self):
        response = self.client.get(reverse("institution_detail", args=[self.institution.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="main-heading"')
        self.assertContains(response, self.institution.name)

    def test_institution_detail_view_with_invalid_id(self):
        invalid_id = self.institution.id + 1
        response = self.client.get(reverse("institution_detail", args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    def test_project_detail_view_num_queries(self):
        with self.assertNumQueries(1):
            response = self.client.get(reverse("project_detail", args=[self.institution.id]))
