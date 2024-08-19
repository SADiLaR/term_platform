# Generated by Django 5.0.8 on 2024-08-17 14:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0012_alter_documentfile_search_vector'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentFile',
            new_name='Document',
        ),
        migrations.RenameModel(
            old_name='HistoricalDocumentFile',
            new_name='HistoricalDocument',
        ),
        migrations.RenameIndex(
            model_name='document',
            new_name='general_doc_search__12340c_gin',
            old_name='general_doc_search__752b22_gin',
        ),
    ]
