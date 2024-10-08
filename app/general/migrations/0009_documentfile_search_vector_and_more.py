# Generated by Django 5.0.2 on 2024-06-14 10:33

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0008_documentfile_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentfile',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name='documentfile',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='general_doc_search__752b22_gin'),
        ),
    ]
