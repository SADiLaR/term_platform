from datetime import date

from django.test import Client, TestCase
from django.urls import reverse

from app.views import get_date_range
from general.models import Institution, Language, Project, Subject


class ProjectViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.subject1 = Subject.objects.create(name="Subject 1")
        self.subject2 = Subject.objects.create(name="Subject 2")
        self.language1 = Language.objects.create(name="Language 1", iso_code="lang1")
        self.language2 = Language.objects.create(name="Language 2", iso_code="lang2")
        self.language3 = Language.objects.create(name="Language 3", iso_code="lang3")
        self.language4 = Language.objects.create(name="Language 4", iso_code="lang4")
        self.institution = Institution.objects.create(
            name="Institution", logo="institution_logo.png"
        )

        self.project1 = Project.objects.create(
            name="Project 1",
            start_date="2020-01-01",
            end_date="2021-01-01",
            institution=self.institution,
            logo="project_logo.png",
        )
        self.project1.subjects.add(self.subject1)
        self.project1.languages.add(self.language1)

        self.project2 = Project.objects.create(
            name="Project 2",
            end_date="2021-01-01",
            institution=self.institution,
            logo="project_logo.png",
        )
        self.project2.subjects.add(self.subject1)
        self.project2.languages.add(self.language1)
        self.project2.languages.add(self.language2)
        self.project2.languages.add(self.language3)
        self.project2.languages.add(self.language4)

        self.url = reverse("projects")

    def test_projects_view(self):
        response = self.client.get(reverse("projects"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("projects", response.context)
        self.assertEqual(len(response.context["projects"]), 2)
        self.assertEqual(response.context["projects"][0]["project"].name, "Project 1")
        self.assertEqual(response.context["projects"][1]["project"].name, "Project 2")

    def test_projects_view_with_filters(self):
        response = self.client.get(reverse("projects"), {"language": self.language3.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["projects"]), 1)
        self.assertEqual(response.context["projects"][0]["project"].name, "Project 2")

    def test_projects_view_multilingual(self):
        response = self.client.get(reverse("projects"))
        self.assertEqual(response.status_code, 200)
        projects = response.context["projects"]
        self.assertEqual(projects[1]["languages"], "Multilingual")

    def test_projects_view_queries(self):
        response = self.client.get(self.url)

        with self.assertNumQueries(6):
            response = self.client.get(self.url)


class GetDateRangeTests(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name="Institution")
        self.project = Project.objects.create(name="Project", institution=self.institution)

    def test_get_date_range_different_years(self):
        self.project.start_date = date(2020, 1, 1)
        self.project.end_date = date(2021, 1, 1)
        self.project.save()
        self.assertEqual(get_date_range(self.project), "2020 – 2021")

    def test_get_date_range_same_year(self):
        self.project.start_date = date(2020, 1, 1)
        self.project.end_date = date(2020, 12, 31)
        self.project.save()
        self.assertEqual(get_date_range(self.project), 2020)

    def test_get_date_range_only_start_date(self):
        self.project.start_date = date(2020, 1, 1)
        self.project.end_date = None
        self.project.save()
        self.assertEqual(get_date_range(self.project), "Since 2020")

    def test_get_date_range_only_end_date(self):
        self.project.start_date = None
        self.project.end_date = date(2020, 12, 31)
        self.project.save()
        self.assertEqual(get_date_range(self.project), "Until 2020")

    def test_get_date_range_no_dates(self):
        self.project.start_date = None
        self.project.end_date = None
        self.project.save()
        self.assertIsNone(get_date_range(self.project))
