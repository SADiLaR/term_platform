from django.contrib.postgres.search import SearchVector
from django.db import migrations


def compute_search_vector(apps, schema_editor):
    Quote = apps.get_model("general", "DocumentFile")
    Quote.objects.update(search_vector=SearchVector("document_data", "title"))


class Migration(migrations.Migration):
    dependencies = [
        ("general", "0009_documentfile_search_vector_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER search_vector_trigger
            BEFORE INSERT OR UPDATE OF document_data, title, search_vector
            ON general_documentfile
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(
                search_vector, 'pg_catalog.english', document_data, title
            );
            UPDATE general_documentfile SET search_vector = NULL;
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS search_vector_trigger
            ON general_documentfile;
            """,
        ),
        migrations.RunPython(
            compute_search_vector, reverse_code=migrations.RunPython.noop
        ),
    ]
