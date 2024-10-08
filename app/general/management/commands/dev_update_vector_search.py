from django.core.management.base import BaseCommand

from general.models import Document


class Command(BaseCommand):
    help = "Updating the Vector Search index on document_file."

    def handle(self, *args, **options):
        for document_file in Document.objects.all():
            document_file.save()  # This line updates the vector search for the document file
            print(f"Updated {document_file.title}.")
