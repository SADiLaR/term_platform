import django.contrib.postgres.search
import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0018_alter_document_uploaded_file_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="document",
            old_name="title",
            new_name="name",
        ),
        migrations.RenameField(
            model_name="historicaldocument",
            old_name="title",
            new_name="name",
        ),
        migrations.AlterField(
            model_name="document",
            name="name",
            field=models.CharField(max_length=200, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="historicaldocument",
            name="name",
            field=models.CharField(max_length=200, verbose_name="name"),
        ),
        migrations.RemoveField(
            model_name="document",
            name="search_vector",
        ),
        migrations.AddField(
            model_name="document",
            name="search_vector",
            field=models.GeneratedField(
                blank=True,
                db_persist=True,
                expression=django.contrib.postgres.search.CombinedSearchVector(
                    django.contrib.postgres.search.CombinedSearchVector(
                        django.contrib.postgres.search.SearchVector(
                            "name", config="english", weight="A"
                        ),
                        "||",
                        django.contrib.postgres.search.SearchVector(
                            "description", config="english", weight="B"
                        ),
                        django.contrib.postgres.search.SearchConfig("english"),
                    ),
                    "||",
                    django.contrib.postgres.search.SearchVector(
                        "document_data", config="english", weight="C"
                    ),
                    django.contrib.postgres.search.SearchConfig("english"),
                ),
                null=True,
                output_field=django.contrib.postgres.search.SearchVectorField(),
            ),
        ),
        migrations.AddIndex(
            model_name="document",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["search_vector"], name="general_doc_search__12340c_gin"
            ),
        ),
    ]
