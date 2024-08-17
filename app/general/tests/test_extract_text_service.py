import os
import unittest

from general.service.extract_text import pdf_to_text


class TestExtractTextService(unittest.TestCase):
    def setUp(self):
        test_dir = os.getenv("TESTING_DIR", "/app/general/tests/files")
        self.file_name = os.path.join(test_dir, "Lorem.pdf")

    def test_text_extraction(self):
        with open(self.file_name, "rb") as file:
            text = pdf_to_text(file)
        self.assertIn("fermentum turpis.", text)
        self.assertNotIn("notintext.", text)
        self.assertGreater(len(text), 1470, "Too little text extracted")
        self.assertGreater(len(text.split()), 220, "Too few words (spaces) extracted")
