import os
import unittest

from general.service.extract_text import GetTextFromPDF


class TestExtractTextService(unittest.TestCase):
    def setUp(self):
        test_dir = os.getenv("TESTING_DIR", "/app/general/tests/files")
        self.file_mock = test_dir + "/Lorem.pdf"

    def test_in_text(self):
        with open(self.file_mock, "rb") as file:
            pypdf = GetTextFromPDF(file)

            result = pypdf.to_text().strip()

            words = result.split()

            self.assertIn("turpis.", words)

    def test_not_in_text(self):
        with open(self.file_mock, "rb") as file:
            pypdf = GetTextFromPDF(file)

            result = pypdf.to_text().strip()

            words = result.split()

            self.assertNotIn("notintext.", words)
