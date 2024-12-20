# Generated by Django 5.0.8 on 2024-11-07 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0014_alter_document_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_data',
            field=models.TextField(blank=True, help_text="The searchable text extracted from the document where possible, but it can also be edited.", verbose_name='Searchable content'),
        ),
    ]
