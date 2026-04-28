import os
import unittest

from django.conf import settings

from general.service.extract_text import excel_to_text, pdf_to_text


class TestExtractTextService(unittest.TestCase):
    def setUp(self):
        test_dir = settings.TESTING_DIR
        self.file_name = os.path.join(test_dir, "Lorem.pdf")
        self.excel_file_name = os.path.join(test_dir, "example.xlsx")

    def test_text_extraction(self):
        with open(self.file_name, "rb") as file:
            text = pdf_to_text(file)
        self.assertIn("fermentum turpis.", text)
        self.assertNotIn("notintext.", text)
        self.assertGreater(len(text), 1470, "Too little text extracted")
        self.assertGreater(len(text.split()), 220, "Too few words (spaces) extracted")

    def test_excel_text_extraction(self):
        with open(self.excel_file_name, "rb") as file:
            text = excel_to_text(file)

        self.assertIn("cat", text)
        self.assertIn("ikati", text)
        self.assertIn("definition", text)
        self.assertIn("café", text)
        self.assertIn("ɪŋoma", text)
        self.assertIn("ā", text)
