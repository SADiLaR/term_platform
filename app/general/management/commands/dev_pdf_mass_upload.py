import os
import random
import shutil

import magic
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from general.models import DocumentFile
from general.service.extract_text import GetTextError, GetTextFromPDF


class Command(BaseCommand):
    help = "Mass PDF uploader for testing purposes."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dir_main = "/pdf_uploads/"
        self.dir_completed = "/pdf_upload_completed/completed/"
        self.dir_error = "/pdf_upload_completed/error/"

    def handle(self, *args, **options):
        os.system("clear")
        print("Mass file uploader for testing purposes.")

        self.create_directory(self.dir_completed)
        self.create_directory(self.dir_error)

        for root, dirs, files in os.walk(self.dir_main):
            for file in files:
                file_path = os.path.join(root, file)

                # Check if the file is a PDF file and save the data
                self.handle_file(file_path, file)

    def handle_file(self, file_path, file):
        # Get the file type
        file_type = magic.from_file(file_path, mime=True)

        # Check if the file is a PDF file
        directory = self.check_file_type(file_type)
        self.print_pdf_file(file)

        # If file is a PDF file it saves the data and moves the file to the completed directory
        if directory:
            data = {
                "title": file.strip(),
                "file": file.strip(),
                "uploaded_file": file_path,
            }
            # Save the data to the database and uploads the file
            self.save_data(data)

            #  Move the file to the completed directory
            self.move_file(file_path, file, directory)

        # If the file is not a PDF file, print an error message and move the file to the error directory
        else:
            self.print_error()
            # Move the file to the error directory
            self.move_file(file_path, file, self.dir_error)

    def check_file_type(self, file_type):
        return self.dir_completed if file_type == "application/pdf" else None

    def move_file(self, file_path, file, directory):
        if not os.path.isfile(directory + file):
            shutil.move(file_path, directory)
        else:
            print(
                f"The file '{os.path.basename(directory + file)}' already exists in the destination directory."
            )

    def print_pdf_file(self, file):
        print("\n")
        print("\033[92m" + file + "\033[0m")

    def print_error(self):
        print("\n")
        print("\033[91m" + "Only PDF files are allowed" + "\033[0m")

    def save_data(self, data):
        # Generate a random number for the institution ID
        random_number = random.randint(1, 20)
        content_file = ContentFile(data["uploaded_file"], name=data["title"])

        try:
            document_data = GetTextFromPDF(data["uploaded_file"]).to_text()

            instance = DocumentFile(
                title=data["title"],
                document_data=document_data,  # Scraps the PDF file and extracts the text
                uploaded_file=content_file,
                document_type="Glossary",
                institution_id=random_number,
            )
            instance.save()

        except GetTextError as e:
            print(f"Error: {e}")
            return

    def create_directory(self, directory):
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as error:
            print(f"Directory '{directory}' can not be created. Error: {error}")
