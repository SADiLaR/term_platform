import unittest

from django.test import TestCase

from general.models import Language


class TestLanguage(TestCase):
    def setUp(self):
        self.language = Language.objects.create(name="English", iso_code="EN")
        self.language2 = Language.objects.create(name="Afrikaans", iso_code="AF")

    def test_subject_creation(self):
        self.assertEqual(self.language.name, "English")
        self.assertEqual(self.language.iso_code, "EN")

        self.assertEqual(self.language2.name, "Afrikaans")
        self.assertEqual(self.language2.iso_code, "AF")

    def test_subject_name_uniqueness(self):
        with self.assertRaises(Exception):
            Language.objects.create(name="English")

    #
    def test_history_records_creation(self):
        self.assertEqual(self.language.history.count(), 1)
        self.assertEqual(self.language.history.first().name, "English")
        self.assertEqual(self.language.history.first().iso_code, "EN")


if __name__ == "__main__":
    unittest.main()
