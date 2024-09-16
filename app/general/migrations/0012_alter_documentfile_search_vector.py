import django.contrib.postgres.search
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('general', '0011_alter_documentfile_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentfile',
            name='search_vector',
        ),  # also deletes `search_vector_trigger` and general_doc_search__752b22_gin
        migrations.AddField(
            model_name='documentfile',
            name='search_vector',
            field=models.GeneratedField(db_persist=True, expression=django.contrib.postgres.search.CombinedSearchVector(
                django.contrib.postgres.search.CombinedSearchVector(
                    django.contrib.postgres.search.SearchVector('title', config='english', weight='A'), '||',
                    django.contrib.postgres.search.SearchVector('description', config='english', weight='B'),
                    django.contrib.postgres.search.SearchConfig('english')), '||',
                django.contrib.postgres.search.SearchVector('document_data', config='english', weight='C'),
                django.contrib.postgres.search.SearchConfig('english')), null=True,
                                        output_field=django.contrib.postgres.search.SearchVectorField()),
        ),
        migrations.AddIndex(
            model_name='documentfile',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'],
                                                           name='general_doc_search__752b22_gin'),
        ),
    ]
