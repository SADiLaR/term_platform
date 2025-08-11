import os
import random
import unittest
from unittest.mock import MagicMock, patch

from django.conf import settings
from faker import Faker

from general.management.commands.import_documents import Command
from general.models import Document, Institution


class TestHandleFile(unittest.TestCase):
    def setUp(self):
        self.command = Command()
        self.command.save_data = MagicMock()
        self.test_file = os.path.join(settings.TESTING_DIR, "Lorem.pdf")
        self.name = "Test file"
        self.fake = Faker()

    def tearDown(self):
        try:
            document_file = Document.objects.get(title=self.name)
            path = document_file.uploaded_file.path
            if os.path.isfile(path):
                os.remove(path)
        except Document.DoesNotExist:
            pass

    def test_handle_file_pdf(self):
        self.command.handle_file(self.test_file, self.test_file)
        self.command.save_data.assert_called_once()

    def test_handle_file_non_pdf(self):
        with patch("magic.from_file") as from_file:
            from_file.return_value = None
            self.command.handle_file(self.test_file, self.test_file)
        self.command.save_data.assert_not_called()

    def test_save_data(self):
        command = Command()
        # Create some Institutions instances for testing
        for i in range(1, 21):
            institution_id = random.randint(1, 1000)  # noqa: S311 - this is only for testing
            Institution.objects.create(
                id=i,
                name=f"{institution_id}_{self.fake.company()}",
                abbreviation=f"{institution_id}_{self.fake.company_suffix()}",
                url=f"{institution_id}_{self.fake.url()}",
                email=f"{institution_id}_{self.fake.company_email()}",
                logo="",
            )

        command.save_data(self.test_file, self.name)
        document_file = Document.objects.get(title=self.name)
        self.assertEqual(document_file.title, self.name)
        self.assertIn("Lorem ipsum dolor", document_file.document_data)
