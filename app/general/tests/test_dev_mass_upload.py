import os
import unittest
from unittest.mock import MagicMock

from faker import Faker

from general.management.commands.dev_pdf_mass_upload import Command
from general.models import DocumentFile, Institution


class TestHandleFile(unittest.TestCase):
    def setUp(self):
        self.command = Command()
        self.command.check_file_type = MagicMock()
        self.command.move_file = MagicMock()
        self.command.print_error = MagicMock()
        self.command.print_pdf_file = MagicMock()
        self.command.save_data = MagicMock()
        self.test_dir = os.getenv("TESTING_DIR", "/app/general/tests/files")
        self.test_file = self.test_dir + "Lorem.pdf"
        self.fake = Faker()

    def test_handle_file_pdf(self):
        self.command.check_file_type.return_value = self.test_dir
        self.command.handle_file(self.test_file, self.test_file)
        self.command.check_file_type.assert_called_once()
        self.command.move_file.assert_called_once()
        self.command.save_data.assert_called_once()
        self.command.print_pdf_file.assert_called_once()
        self.command.print_error.assert_not_called()

    def test_handle_file_non_pdf(self):
        self.command.check_file_type.return_value = None
        self.command.handle_file(self.test_file, self.test_file)
        self.command.check_file_type.assert_called_once()
        self.command.move_file.assert_called_once()
        self.command.save_data.assert_not_called()
        self.command.print_pdf_file.assert_called_once()
        self.command.print_error.assert_called_once()

    def test_check_file_type_pdf(self):
        self.assertNotEqual(self.command.check_file_type("application/pdf"), self.test_dir)

    def test_save_data(self):
        self.command = Command()
        # Create some Institutions instances for testing
        for _ in range(20):
            Institution.objects.create(
                name=self.fake.company(),
                abbreviation=self.fake.company_suffix(),
                url=self.fake.url(),
                email=self.fake.company_email(),
                logo="",
            )

        data = {
            "title": "Test file",
            "file": "Test file",
            "uploaded_file": self.test_file,
        }

        self.command.save_data(data)

        document_file = DocumentFile.objects.get(title="Test file")
        self.assertEqual(document_file.title, "Test file")
