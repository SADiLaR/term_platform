import os

from django.core.management.base import BaseCommand

from general.models import DocumentFile


class Command(BaseCommand):
    help = "Updating the Vector Search index on document_file."

    def handle(self, *args, **options):
        os.system("clear")
        print("Querying the Vector Search index and Updating.")

        all_document_files = DocumentFile.objects.all()

        for document_file in all_document_files:
            document_file.save()  # This line updates the vector search for the document file
            print(f"Updated {document_file.title}.")
            print()
