# Generated by Django 5.0.2 on 2024-05-10 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0004_historicaldocumentfile_historicalinstitution_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='logo',
            field=models.ImageField(blank=True, upload_to='institutions/logos/'),
        ),
        migrations.AlterField(
            model_name='project',
            name='logo',
            field=models.ImageField(blank=True, upload_to='projects/logos/'),
        ),
    ]
