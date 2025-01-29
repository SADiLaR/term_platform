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

    def test_language_switcher(self):
        with self.settings(USE_LANGUAGE_SWITCHER=False):
            response = self.client.get("/")
            self.assertIn("USE_LANGUAGE_SWITCHER", response.context, "Value not passed in context")
            self.assertNotIn(b'id="ui-language"', response.content, "Language switcher in page")
        with self.settings(USE_LANGUAGE_SWITCHER=True):
            response = self.client.get("/")
            self.assertIn("USE_LANGUAGE_SWITCHER", response.context, "Value not passed in context")
            self.assertIn(b'id="ui-language"', response.content, "Language switcher not in page")
