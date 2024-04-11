from django.test import Client, TestCase


class TestViews(TestCase):
    def test_health(self):
        response = Client().get("/_health/")
        self.assertIn(b"OK", response.content)
