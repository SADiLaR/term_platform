from django.test import Client, TestCase


class TestViews(TestCase):
    def test_health(self):
        response = Client().get("/_health/")
        self.assertIn(b"OK", response.content)


class CustomTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_custom_404_page(self):
        response = self.client.get("/example/")

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
