# TODO:
#  - Provide better command-line parameters for control, e.g.
#    - import for given institution
#    - associate with specific language(s)/subject(s)
#  - make usable outside Docker

import os
import random

import magic
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from general.models import Document
from general.service.extract_text import GetTextError, pdf_to_text


class Command(BaseCommand):
    help = "Mass PDF uploader for testing purposes"

    def add_arguments(self, parser):
        parser.add_argument("directory", help="Directory with files to import")

    def handle(self, *args, **options):
        for root, dirs, files in os.walk(options["directory"]):
            for file in files:
                if not os.path.splitext(file)[1] == ".pdf":
                    continue
                file_path = os.path.join(root, file)
                self.handle_file(file_path, file)

    def handle_file(self, file_path, file_name):
        print(file_name)
        file_type = magic.from_file(file_path, mime=True)
        if file_type == "application/pdf":
            self.save_data(file_path, file_name)
        else:
            print("Only PDF files are allowed")

    def save_data(self, file_path, file_name):
        with open(file_path, "rb") as f:
            content_file = ContentFile(f.read(), name=file_name)

        try:
            instance = Document(
                title=file_name,
                document_data=pdf_to_text(file_path),
                uploaded_file=content_file,
                document_type="Glossary",
                institution_id=random.randint(1, 20),
            )
            instance.save()
        except GetTextError as e:
            print(f"Error: {e}")
